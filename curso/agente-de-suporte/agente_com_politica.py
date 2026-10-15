# O mesmo agente, com a regra fora do modelo: o modelo propõe, o sistema decide.
# Uso: python agente_com_politica.py ana "Cancela o pedido B202, por favor."
# Para usar a solução em vez do seu exercício, acrescente --solucao no fim.
import sys

from agente_ingenuo import CANCEL_ORDER, SYSTEM
from modelo import propor
from pedidos import cancelar, mostrar

if "--solucao" in sys.argv:
    from solucao.politica import pode_cancelar
else:
    from politica import pode_cancelar


def atender(cliente, mensagem):
    system = SYSTEM.format(cliente=cliente)
    for chamada in propor(system, mensagem, [CANCEL_ORDER]):
        pedido = chamada["input"]["order_id"]
        ok, motivo = pode_cancelar(cliente, pedido)  # o sistema decide
        if ok:
            cancelar(pedido)
            print(f"OK: pedido {pedido} cancelado")
        else:
            print(f"RECUSADO: {motivo}")


if __name__ == "__main__":
    atender(sys.argv[1], sys.argv[2])
    mostrar()
