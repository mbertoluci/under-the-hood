from evidencia import limite


def pode_subir(decisoes, risco):
    operacoes = {}
    for d in decisoes:
        operacoes[d["operacao"]] = operacoes.get(d["operacao"], False) or d["erro"]
    n = len(operacoes)                      # operações, não linhas
    erros = sum(operacoes.values())         # as falhas contam
    return n > 0 and limite(erros, n) < risco
