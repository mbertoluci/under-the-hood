# O agente com a regra e, antes do efeito, a aprovação de uma pessoa (aula 11).
# Uso: python aprovacao.py ana "Cancela o pedido A101, por favor." --solucao
# Cada decisão da pessoa vai para aprovacoes.csv, que o autonomia.py lê.
import csv
import sys
from datetime import datetime

from agente_ingenuo import CANCEL_ORDER, SYSTEM
from modelo import propor
from pedidos import cancelar, mostrar

if "--solucao" in sys.argv:
    from solucao.politica import pode_cancelar
else:
    from politica import pode_cancelar

REGISTRO = "aprovacoes.csv"


def perguntar(cliente, pedido):
    resposta = input(f"Aprovar o cancelamento do pedido {pedido} ({cliente})? [s/N] ")
    return resposta.strip().lower() == "s"  # Enter, ou qualquer outra coisa, é não


def registrar(acao, pedido, aprovado):
    with open(REGISTRO, "a", newline="") as arquivo:
        csv.writer(arquivo).writerow([datetime.now().isoformat(timespec="seconds"), acao, pedido,
                                      "aprovado" if aprovado else "recusado"])


def atender(cliente, mensagem):
    system = SYSTEM.format(cliente=cliente)
    for chamada in propor(system, mensagem, [CANCEL_ORDER]):
        pedido = chamada["input"]["order_id"]
        ok, motivo = pode_cancelar(cliente, pedido)  # a regra vem primeiro
        if not ok:
            print(f"RECUSADO: {motivo}")
            continue
        aprovado = perguntar(cliente, pedido)  # a pessoa decide o que a regra deixou passar
        registrar("cancelar", pedido, aprovado)
        if aprovado:
            cancelar(pedido)
            print(f"OK: pedido {pedido} cancelado")
        else:
            print(f"NÃO APROVADO: o pedido {pedido} fica como estava")


if __name__ == "__main__":
    atender(sys.argv[1], sys.argv[2])
    mostrar()
