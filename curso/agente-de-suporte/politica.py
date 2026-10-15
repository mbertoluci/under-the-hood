# EXERCÍCIO: a regra que decide se um cancelamento pode acontecer.
# Ela roda fora do modelo. O modelo só propõe; esta função decide.
from pedidos import PEDIDOS


def pode_cancelar(cliente, pedido_id):
    """Devolve (True, "") se pode cancelar, ou (False, motivo) se não pode.

    Regras:
    1. o pedido existe;
    2. o pedido é do cliente logado;
    3. o pedido ainda não foi enviado.
    """
    raise NotImplementedError("escreva a regra aqui e rode: python test_politica.py")
