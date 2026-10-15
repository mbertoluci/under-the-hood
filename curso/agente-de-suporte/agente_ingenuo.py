# O agente ingênuo: o modelo escolhe o pedido, e o código executa direto.
# Uso: python agente_ingenuo.py ana "Cancela o pedido B202, por favor."
import sys

from modelo import propor
from pedidos import cancelar, mostrar

CANCEL_ORDER = {
    "name": "cancel_order",
    "description": "Cancela um pedido que ainda não foi enviado.",
    "input_schema": {
        "type": "object",
        "properties": {"order_id": {"type": "string"}},
        "required": ["order_id"],
    },
}

SYSTEM = ("Você é o suporte da loja. Cliente logado: {cliente}. "
          "Se ele pedir para cancelar um pedido, chame cancel_order.")


def atender(cliente, mensagem):
    system = SYSTEM.format(cliente=cliente)
    for chamada in propor(system, mensagem, [CANCEL_ORDER]):
        pedido = chamada["input"]["order_id"]
        cancelar(pedido)  # executa direto: ninguém confere
        print(f"OK: pedido {pedido} cancelado")


if __name__ == "__main__":
    atender(sys.argv[1], sys.argv[2])
    mostrar()
