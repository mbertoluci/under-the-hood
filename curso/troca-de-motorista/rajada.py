# Aula 14: a rajada. Segunda, 20/10: o agente entra num laço e repete o aviso de atraso da XPTO 25 vezes.
# E, no mesmo turno, propõe duas trocas de motorista para a carga C-9281, que já teve uma.
# Rode: python rajada.py            (com o seu cabe, de limite.py)
#       python rajada.py --solucao  (com a solução)
import sys
from limite import TETOS, pedir

if "--solucao" in sys.argv:
    from solucao.limite import cabe
else:
    from limite import cabe


def main(cabe):
    registro = [{"classe": "troca", "chave": "C-9281", "quando": "2026-10-20 08:00", "estado": "feita"}]
    aviso = {"classe": "aviso", "chave": "XPTO"}
    saem = sum(pedir(aviso, registro, f"2026-10-20 10:{i // 2:02}", cabe) for i in range(25))
    print(f"aviso de atraso, XPTO   teto {TETOS['aviso']['teto']} por hora")
    print(f"10:00 a 10:12  25 pedidos do agente   saem {saem}, recusados {25 - saem}")
    depois = pedir(aviso, registro, "2026-10-20 11:00", cabe)
    print(f"11:00          mais 1 pedido          {'sai' if depois else 'recusado'}")
    print(f"troca de motorista, C-9281   teto {TETOS['troca']['teto']} por carga, 1 já feita")
    for motorista in ("Carlos", "Davi"):
        ok = pedir({"classe": "troca", "chave": "C-9281"}, registro, "2026-10-20 17:12", cabe)
        print(f"17:12          troca para {motorista:<12}{'sai' if ok else 'recusada: passa do teto'}")
    trocas = sum(1 for r in registro if r["classe"] == "troca")
    print(f"trocas da C-9281 no fim: {trocas} (teto {TETOS['troca']['teto']})")


if __name__ == "__main__":
    main(cabe)
