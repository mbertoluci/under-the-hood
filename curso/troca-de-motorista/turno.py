# Aula 15: o turno das 17:10. O Anderson não pode sair, e o agente cuida da troca da carga C-9281.
# É uma simulação: as chamadas do agente são um roteiro fixo neste arquivo, sem modelo e sem chave de API.
# Rode: python turno.py --ingenuo   (o agente tem a ferramenta aplicar_troca)
#       python turno.py             (com o seu aplicar, de preparar.py)
#       python turno.py --solucao   (com a solução)
import sys
from preparar import FERRAMENTAS_DO_AGENTE, aprovar, chamar

if "--solucao" in sys.argv:
    from solucao.preparar import aplicar
else:
    from preparar import aplicar


def novo():
    return {"seq": 0, "mudancas": {}, "cargas": {"C-9281": {"motorista": "Anderson", "trocas": 0}}}


def cabecalho(extra=()):
    print("simulação: chamadas fixas, sem modelo")
    print(f"ferramentas do agente: {', '.join(sorted(FERRAMENTAS_DO_AGENTE | set(extra)))}")


def linha(hora, quem, chamada, resultado):
    print(f"{hora} {quem:<9} {chamada:<28} {resultado}")


def fim(s, aprovada_por):
    carga = s["cargas"]["C-9281"]
    trocas = "1 troca" if carga["trocas"] == 1 else f"{carga['trocas']} trocas"
    print(f"carga C-9281 no fim: motorista {carga['motorista']}, {trocas}, aprovada por {aprovada_por}")


def ingenuo():
    """O agente tem as duas ferramentas. O prompt pede: só aplique depois da aprovação."""
    cabecalho({"aplicar_troca"})
    s = novo()
    mid = chamar(s, "preparar_troca", {"carga": "C-9281", "motorista": "Carlos"})
    linha("17:10", "agente", "preparar_troca(Carlos)", mid)
    s["cargas"]["C-9281"].update(motorista="Davi", trocas=1)  # aplicar_troca: muda a carga com o que veio na chamada
    s["mudancas"][mid]["estado"] = "aplicada"
    linha("17:11", "agente", f"aplicar_troca({mid}, Davi)", "aplicada")
    fim(s, "ninguém")


def turno(aplicar):
    cabecalho()
    s = novo()
    mid = chamar(s, "preparar_troca", {"carga": "C-9281", "motorista": "Carlos"})
    linha("17:10", "agente", "preparar_troca(Carlos)", mid)
    linha("17:11", "agente", f"aplicar_troca({mid}, Davi)", chamar(s, "aplicar_troca", {"id": mid, "motorista": "Davi"}))
    ok, motivo = aplicar(s, {"id": mid})
    linha("17:12", "servidor", f"aplicar({mid})", "aplicada" if ok else "recusada: " + motivo)
    aprovar(s, mid, "Joana")
    linha("17:20", "Joana", f"aprova {mid} no portal", "")
    for hora in ("17:20", "17:21"):  # o mesmo pedido chega duas vezes, e traz um motorista que ninguém aprovou
        ok, motivo = aplicar(s, {"id": mid, "motorista": "Davi"})
        linha(hora, "servidor", f"aplicar({mid}, Davi)", "aplicada: " + s["cargas"]["C-9281"]["motorista"] if ok else "recusada: " + motivo)
    fim(s, "Joana")


if __name__ == "__main__":
    ingenuo() if "--ingenuo" in sys.argv else turno(aplicar)
