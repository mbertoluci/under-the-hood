from ids import CAMPOS_COM_NUMERO


def pode_usar(sessao, args):
    for campo in CAMPOS_COM_NUMERO:
        numero = args.get(campo)
        if numero is None:
            return False, f"faltou o campo {campo}"
        if numero not in sessao["entregues"]:
            return False, f"{numero} não veio do servidor nesta sessão"
    return True, ""
