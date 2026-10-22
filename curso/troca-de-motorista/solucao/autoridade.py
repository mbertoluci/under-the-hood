# Uma solução do exercício. Tente antes de abrir.
from operacao import CANAIS, PAPEIS


def autorizou(sinal, proposta):
    # 1. De onde veio? Do cadastro, de quem pode autorizar.
    pessoa = CANAIS.get((sinal.get("canal"), sinal.get("origem")))
    if pessoa is None:
        return False, "contato fora do cadastro"
    if PAPEIS.get(pessoa) != "solicitante":
        return False, f"{pessoa} não pode autorizar troca"
    # 2. O que foi? O botão de autorizar, não um texto.
    if sinal.get("botao") != "autorizo":
        return False, "não é o botão de autorizar"
    # 3. Para quê? Para esta proposta, não para outra.
    if sinal.get("proposta") != proposta["id"]:
        return False, "o botão é de outra proposta"
    return True, ""
