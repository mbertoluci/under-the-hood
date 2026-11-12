# Aula 20: o fecho da playlist. Seis chamadas do agente passam por um conferente só,
# montado com as peças das aulas 16 (origem do número), 17 (camadas) e 18 (escopo).
# É uma simulação: as chamadas do agente são um roteiro fixo neste arquivo, sem modelo e sem chave de API.
# Rode: python fecho.py --ingenuo   (só as ferramentas "perigosas" passam pelo conferente)
#       python fecho.py             (com o seu proteger, de monitor.py)
#       python fecho.py --solucao   (com a solução)
import sys
from ids import nova_sessao, ler_carga, buscar_motorista
from camadas import piso, manual
from solucao.ids import pode_usar      # aula 16
from solucao.camadas import combinar   # aula 17
from solucao.escopo import decidir     # aula 18

if "--solucao" in sys.argv:
    from solucao.monitor import proteger
else:
    from monitor import proteger

TAREFA = {"acoes": {"ler_carga", "buscar_motorista", "preparar_troca"}, "alvos": {"C-9281"}}
ROTEIRO = [
    ("ler_carga", {"carga": "C-9281"}),
    ("preparar_troca", {"carga": "C-9281", "motorista": "MOT-0417"}),  # o número veio de um e-mail
    ("cancelar_coleta", {"carga": "C-9281"}),                           # ferramenta que entrou semana passada
    ("buscar_motorista", {"carga": "C-9281", "nome": "Carlos"}),
    ("preparar_troca", {"carga": "C-9281", "motorista": "MOT-0102"}),
    ("aplicar_troca", {"id": "M-1"}),                                   # aplicar não é ferramenta do agente
]


def so_as_perigosas(ferramentas, monitor):
    """O jeito ingênuo: o conferente só embrulha a lista das perigosas."""
    perigosas = {"preparar_troca"}
    def embrulhar(nome, ferramenta):
        def chamada(args):
            permitido, motivo = monitor(nome, args)
            return ferramenta(args) if permitido else {"negado": motivo}
        return chamada
    return {nome: embrulhar(nome, f) if nome in perigosas else f for nome, f in ferramentas.items()}


def fecho(proteger):
    sessao, historico, conferidas, falta = nova_sessao(), [], [], []

    ferramentas = {
        "ler_carga": lambda args: "carga lida" if ler_carga(sessao, args["carga"]) else "carga desconhecida",
        "buscar_motorista": lambda args: ", ".join(f"{n} {nome}" for n, nome in buscar_motorista(sessao, args["nome"]).items()),
        "preparar_troca": lambda args: "aula 17, camadas: preparada. Falta: " + "; ".join(falta),
        "cancelar_coleta": lambda args: "coleta cancelada",
    }

    def monitor(nome, args):
        """O conferente: escopo (aula 18), origem do número (aula 16) e camadas de política (aula 17)."""
        conferidas.append(nome)
        decisao = decidir(TAREFA, {"acao": nome, "alvo": args.get("carga")}, historico)
        historico.append(decisao)
        if decisao != "executa":
            return False, "aula 18, escopo: fora da tarefa"
        if nome == "preparar_troca":
            ok, motivo = pode_usar(sessao, args)
            if not ok:
                return False, "aula 16, origem: " + motivo
            camadas = combinar({"tipo": "troca"}, [piso, manual])
            if camadas["resultado"] == "negado":
                return False, "aula 17, camadas: " + "; ".join(camadas["nega"])
            falta[:] = camadas["exige"]  # o que ainda falta para aplicar
        return True, ""

    protegidas = proteger(ferramentas, monitor)
    print("simulação: chamadas fixas, sem modelo")
    for nome, args in ROTEIRO:
        chamada = f"{nome}({args.get('motorista') or args.get('nome') or args.get('carga') or args.get('id')})"
        if nome not in protegidas:
            print(f"{chamada:<26} aula 15: não existe para o agente")
            continue
        antes = len(conferidas)
        resposta = protegidas[nome](args)
        texto = "negado: " + resposta["negado"] if isinstance(resposta, dict) else resposta
        print(f"{chamada:<26} {texto}{'' if len(conferidas) > antes else '   <- SEM CONFERENTE'}")
    print(f"chamadas que passaram pelo conferente: {len(conferidas)} de {sum(1 for n, _ in ROTEIRO if n in protegidas)}")


if __name__ == "__main__":
    fecho(so_as_perigosas if "--ingenuo" in sys.argv else proteger)
