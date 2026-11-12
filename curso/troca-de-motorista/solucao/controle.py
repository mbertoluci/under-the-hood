# Uma solução do exercício da aula 8.
from controle import CATALOGO


def controle(proposta, catalogo=CATALOGO):
    efeito = catalogo.get(proposta.get("acao"))
    if not isinstance(efeito, dict):
        return "pessoa"                      # fora do catálogo
    volta, onde = efeito.get("volta"), efeito.get("onde")
    if volta is True and onde == "agente":
        return "confinar"                    # 2. volta e fica na área do agente
    if volta is True and onde == "fora":
        return "juiz"                        # 3. volta, mas mexe fora
    return "pessoa"                          # 1. não volta, e tudo o que não é um sim claro
