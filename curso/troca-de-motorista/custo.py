# Aula 10: o preço da regra de descer. Um agente bom, que erra menos do que o negócio aceita,
# ainda desce às vezes. Quantas vezes? A conta é exata (binomial), não sorteio.
# Rode: python custo.py            (com o seu deve_descer, de descida.py)
#       python custo.py --solucao  (com a solução)
import math, sys
from descida import janela

if "--solucao" in sys.argv:
    from solucao.descida import deve_descer
else:
    from descida import deve_descer

RISCO = 0.01  # o rastreador: o negócio aceita 1%


def chance_de_descer(taxa_real, tamanho):
    """Soma a chance de cada número de erros na janela em que a regra manda descer."""
    total = 0.0
    for erros in range(tamanho + 1):
        janela_cheia = [{"auditada": True, "erro": i < erros} for i in range(tamanho)]
        if deve_descer(janela_cheia, RISCO, tamanho=tamanho):
            total += math.comb(tamanho, erros) * taxa_real ** erros * (1 - taxa_real) ** (tamanho - erros)
    return total


def pct(x, casas=0):
    return f"{x:.{casas}%}".replace(".", ",")


def main():
    curta, longa = janela(RISCO), 2 * janela(RISCO)
    print(f"risco aceito {pct(RISCO)}, desce acima de {pct(2 * RISCO)}")
    print(f"{'erro real':<12}{f'janela {curta}':>12}{f'janela {longa}':>12}")
    for taxa in (0.003, 0.005, 0.01, 0.02, 0.05):
        print(f"{pct(taxa, 1):<12}{pct(chance_de_descer(taxa, curta)):>12}{pct(chance_de_descer(taxa, longa)):>12}")


if __name__ == "__main__":
    main()
