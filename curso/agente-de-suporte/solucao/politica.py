# Uma solução do exercício. Tente antes de abrir.
from pedidos import PEDIDOS


def pode_cancelar(cliente, pedido_id):
    pedido = PEDIDOS.get(pedido_id)
    if pedido is None:
        return False, "pedido não existe"
    if pedido["cliente"] != cliente:
        return False, "o pedido não é seu"
    if pedido["status"] != "aguardando envio":
        return False, f"pedido já está {pedido['status']}"
    return True, ""
