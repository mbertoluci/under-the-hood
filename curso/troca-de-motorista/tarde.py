# Aula 17: a tarde da delegação. Às 17:30 a Joana delega os atrasos a um subagente com o perfil "rápido".
# É uma simulação: as ações do subagente são um roteiro fixo neste arquivo, sem modelo e sem chave de API.
# Rode: python tarde.py --ingenuo   (a última camada vence)
#       python tarde.py             (com o seu combinar, de camadas.py)
#       python tarde.py --solucao   (com a solução)
import sys
from camadas import piso, manual, equipe, perfil_rapido

if "--solucao" in sys.argv:
    from solucao.camadas import combinar
else:
    from camadas import combinar

PILHA = [piso, manual, equipe, perfil_rapido]


def ultima_vence(acao, camadas):
    """O combinador ingênuo: a negação da última camada vence, "dispensa" tira exigência, e erro só vai ao log."""
    nega, exige = [], []
    for camada in camadas:
        try:
            resposta = camada(acao)
        except Exception:
            print(f"log: a camada {camada.__name__} falhou, seguindo")
            continue
        nega = [f"{camada.__name__}: {motivo}" for motivo in resposta["nega"]]
        exige = [e for e in exige + [f"{camada.__name__}: {p}" for p in resposta["exige"]]
                 if e.split(": ", 1)[1] not in resposta.get("dispensa", [])]
    return {"resultado": "negado" if nega else "pendente" if exige else "executavel", "nega": nega, "exige": exige}


def linha(hora, texto, r):
    detalhe = "; ".join(r["nega"] or r["exige"])
    print(f"{hora} {texto:<38} {r['resultado']}{': ' + detalhe if detalhe else ''}")


def tarde(combinar):
    print("simulação: ações fixas, sem modelo")
    print(f"camadas: {', '.join(c.__name__ for c in PILHA)}")
    troca = {"tipo": "troca", "motorista": "Carlos", "escala": {"Carlos": "livre"}}
    linha("17:30", "subagente: troca para o Carlos", combinar(troca, PILHA))
    sem_escala = {"tipo": "troca", "motorista": "Davi"}  # 17:45: a escala saiu do ar
    linha("17:45", "subagente: troca para o Davi", combinar(sem_escala, PILHA))


if __name__ == "__main__":
    tarde(ultima_vence if "--ingenuo" in sys.argv else combinar)
