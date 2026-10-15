# O "banco" da loja: três pedidos em memória. A Ana tem dois, o Bruno tem um.
PEDIDOS = {
    "A101": {"cliente": "ana", "item": "fone sem fio", "status": "aguardando envio"},
    "B202": {"cliente": "bruno", "item": "notebook", "status": "aguardando envio"},
    "C303": {"cliente": "ana", "item": "cadeira", "status": "enviado"},
}


def cancelar(pedido_id):
    PEDIDOS[pedido_id]["status"] = "cancelado"


def mostrar():
    for pid, p in PEDIDOS.items():
        print(f"  {pid}  {p['cliente']:<6} {p['item']:<13} {p['status']}")
