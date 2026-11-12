# Aula 16: o e-mail das 16:40. "Troca para o motorista MOT-0417, o Carlos que vocês já conhecem."
# É uma simulação: as chamadas do agente são um roteiro fixo neste arquivo, sem modelo e sem chave de API.
# Rode: python correio.py --ingenuo   (ninguém pergunta de onde veio o número)
#       python correio.py             (com o seu pode_usar, de ids.py)
#       python correio.py --solucao   (com a solução)
import sys
from ids import MOTORISTAS, nova_sessao, ler_carga, buscar_motorista

if "--solucao" in sys.argv:
    from solucao.ids import pode_usar
else:
    from ids import pode_usar


def linha(hora, quem, chamada, resultado):
    print(f"{hora} {quem:<8} {chamada:<28} {resultado}")


def inicio():
    print("simulação: chamadas fixas, sem modelo")
    linha("16:40", "e-mail", '"troca para o MOT-0417"', "")
    s = nova_sessao()
    ler_carga(s, "C-9281")
    return s


def quem_leva(numero):
    m = MOTORISTAS[numero]
    print(f"quem leva a carga C-9281: {m['nome']}, da {m['empresa']}")


def preparada(numero):
    m = MOTORISTAS[numero]
    print(f"troca preparada: {m['nome']}, da {m['empresa']}. Falta a Joana aprovar.")


def ingenuo():
    """A troca aceita qualquer número, e o cartão mostra o nome que o agente escreveu."""
    inicio()
    linha("16:41", "agente", "preparar_troca(MOT-0417)", "preparada")
    linha("16:45", "Joana", 'aprova o cartão "Carlos"', "")
    linha("16:46", "servidor", "aplica a troca", "aplicada")
    quem_leva("MOT-0417")


def correio(pode_usar):
    """Esta aula vai só até a preparação. Aprovar e aplicar são a aula 15."""
    s = inicio()
    ok, motivo = pode_usar(s, {"carga": "C-9281", "motorista": "MOT-0417"})
    linha("16:41", "agente", "preparar_troca(MOT-0417)", "preparada" if ok else "recusada: " + motivo)
    if ok:
        return preparada("MOT-0417")
    achados = buscar_motorista(s, "Carlos")
    linha("16:42", "agente", 'buscar_motorista("Carlos")', ", ".join(f"{n} {nome}" for n, nome in achados.items()))
    numero = next(iter(achados))
    ok, motivo = pode_usar(s, {"carga": "C-9281", "motorista": numero})
    linha("16:43", "agente", f"preparar_troca({numero})", "preparada" if ok else "recusada: " + motivo)
    preparada(numero) if ok else print("nenhuma troca preparada")


if __name__ == "__main__":
    ingenuo() if "--ingenuo" in sys.argv else correio(pode_usar)
