# EXERCÍCIO (aula 9): a ação só sobe quando o limite de cima do erro fica abaixo do risco tolerado.
# Escreva pode_subir e rode: python test_evidencia.py
import math


def limite(erros, n, confianca=0.95):
    """Limite de cima da taxa de erro (Clopper-Pearson): o maior erro real que explica o que viu.

    Com zero erros, é 1 - 0,05^(1/n), perto de 3/n (a regra de três). Vem pronta: você só usa.
    """
    if n <= 0:
        return 1.0
    if erros >= n:
        return 1.0

    def chance_de_ver_tao_pouco(p):  # P(X <= erros) numa binomial(n, p), em log para n grande
        return sum(math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
                            + k * math.log(p) + (n - k) * math.log1p(-p)) for k in range(erros + 1))

    baixo, alto = erros / n, 1.0
    for _ in range(100):
        meio = (baixo + alto) / 2
        if chance_de_ver_tao_pouco(meio) > 1 - confianca:
            baixo = meio
        else:
            alto = meio
    return alto


def minimo(risco, confianca=0.95):
    """Quantas operações seguidas sem erro fazem o limite ficar abaixo do risco."""
    return math.floor(math.log(1 - confianca) / math.log(1 - risco)) + 1


def pode_subir(decisoes, risco):
    """Diz se a ação pode subir um degrau: True ou False.

    decisoes: lista de {"operacao": "OP-...", "erro": True/False}, rotuladas por uma pessoa.
    1. Conte operações, não linhas: decisões da mesma operação erram juntas.
       A operação erra se uma decisão dela errou.
    2. Conte as falhas junto com os acertos.
    3. Sobe só se limite(erros, operacoes) ficar abaixo de risco. Sem decisões, não sobe.
    """
    raise NotImplementedError("escreva aqui")
