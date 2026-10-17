# Quando a pessoa pode parar de aprovar: quando o registro prova, não quando parece (aula 11).
# Uso: python autonomia.py           (lê aprovacoes.csv, do aprovacao.py)
#      python autonomia.py 95 5      (95 aprovados e 5 recusados, sem ler o arquivo)
import csv
import os
import sys
from math import comb

META = 0.01  # o agente só cancela sozinho se a taxa de recusa, no pior caso, ficar abaixo de 1%


def pior_caso(recusas, n):
    """Limite superior de 95% (Clopper-Pearson) da taxa de recusa: a maior taxa que o registro ainda não descarta."""
    if recusas >= n:
        return 1.0
    baixo, alto = recusas / n, 1.0
    for _ in range(60):  # busca binária: a taxa em que ver tão poucas recusas teria só 2,5% de chance
        p = (baixo + alto) / 2
        chance = sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(recusas + 1))
        if chance > 0.025:
            baixo = p
        else:
            alto = p
    return alto


if len(sys.argv) == 3:
    aprovados, recusados = int(sys.argv[1]), int(sys.argv[2])
elif not os.path.exists("aprovacoes.csv"):
    sys.exit("sem registro ainda: rode o aprovacao.py e decida alguns pedidos")
else:
    with open("aprovacoes.csv", newline="") as arquivo:
        decisoes = [linha[3] for linha in csv.reader(arquivo) if linha[1] == "cancelar"]
    aprovados, recusados = decisoes.count("aprovado"), decisoes.count("recusado")

n = aprovados + recusados
taxa = pior_caso(recusados, n)
print(f"cancelar: aprovados {aprovados}, recusados {recusados}")
print(f"a taxa de recusa pode chegar a {taxa * 100:.3g}% (meta: abaixo de {META:.0%})")
print("libera: o agente cancela sozinho, e a regra continua" if taxa < META else "continua com aprovação")
