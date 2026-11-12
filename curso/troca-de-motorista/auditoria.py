# Aula 9: o que a auditoria rotulou de cada classe, e se ela pode subir um degrau.
# Rode: python auditoria.py            (com o seu pode_subir, de evidencia.py)
#       python auditoria.py --solucao  (com a solução)
# O histórico é inventado. O risco tolerado de cada classe é combinado com o negócio, não com o agente.
import sys
from evidencia import limite, minimo

if "--solucao" in sys.argv:
    from solucao.evidencia import pode_subir
else:
    from evidencia import pode_subir


def historico(operacoes, decisoes, erros=0):
    """decisoes repartidas entre as operações, uma atrás da outra; as primeiras operações com erro."""
    return [{"operacao": f"OP-{i % operacoes:05d}", "erro": i < erros} for i in range(decisoes)]


CLASSES = [
    # (classe, risco tolerado, decisões rotuladas por pessoas)
    ("consultar_rastreador", 0.01, historico(700, 800, erros=1)),
    ("reservar_veiculo", 0.01, historico(250, 1000)),
    ("trocar_motorista", 0.001, historico(100, 100)),
    ("remarcar_doca", 0.01, historico(10, 10)),
]


def pct(x):
    return f"{x:.2%}".replace(".", ",")


def main():
    print(f"{'ação':<22}{'decisões':>9}{'operações':>11}{'erros':>7}{'limite':>9}{'risco':>8}   resultado")
    for classe, risco, decisoes in CLASSES:
        ops = {d["operacao"] for d in decisoes}
        erros = len({d["operacao"] for d in decisoes if d["erro"]})
        fim = "sobe" if pode_subir(decisoes, risco) else f"fica (precisa de {minimo(risco):,})".replace(",", ".")
        print(f"{classe:<22}{len(decisoes):>9}{len(ops):>11}{erros:>7}{pct(limite(erros, len(ops))):>9}{pct(risco):>8}   {fim}")


if __name__ == "__main__":
    main()
