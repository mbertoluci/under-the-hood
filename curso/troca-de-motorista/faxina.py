# Aula 19: a faxina. A equipe olha a pilha de travas da troca e acha que a aprovação da Joana é redundante:
# "o juiz automático já barra troca suspeita". Antes de tirar, roda os casos perigosos sem ela.
# É uma simulação: os casos são fixos em poda.py, sem modelo e sem chave de API.
# Rode: python faxina.py --ingenuo   (tira a aprovação sem rodar nada)
#       python faxina.py             (com o seu pode_tirar, de poda.py)
#       python faxina.py --solucao   (com a solução)
import sys
from poda import TRAVAS, CASOS, aprovacao, juiz

if "--solucao" in sys.argv:
    from solucao.poda import pode_tirar
else:
    from poda import pode_tirar


def rodar_casos(travas):
    for nome, caso in CASOS.items():
        quem = [t.__name__ for t in travas if t(caso)]
        print(f"  {nome:<36} {'barrada por ' + ', '.join(quem) if quem else 'PASSA'}")


def ingenuo():
    print("simulação: casos fixos, sem modelo")
    print('faxina: "o juiz já barra troca suspeita, a aprovação é redundante"')
    sem = [t for t in TRAVAS if t is not aprovacao]
    print(f"travas depois da faxina: {', '.join(t.__name__ for t in sem)}")
    rodar_casos(sem)


def faxina(pode_tirar):
    print("simulação: casos fixos, sem modelo")
    print(f"travas: {', '.join(t.__name__ for t in TRAVAS)}")
    for trava in (aprovacao, juiz):
        pode, passam = pode_tirar(trava, TRAVAS, CASOS)
        print(f"tirar {trava.__name__ + '?':<11} {'pode: nenhum caso conhecido passa' if pode else 'não pode. Passaria: ' + '; '.join(passam)}")


if __name__ == "__main__":
    ingenuo() if "--ingenuo" in sys.argv else faxina(pode_tirar)
