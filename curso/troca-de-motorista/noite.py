# Aula 11: a noite da B-17. A troca de motorista precisa de uma pessoa (nível 1), e o pedido sai às 17:12.
# Minuto a minuto, até 18:30: com quem está o cartão?
# Rode: python noite.py            (com o seu quem_decide, de escalar.py)
#       python noite.py --solucao  (com a solução)
import sys
from escalar import EQUIPE, minutos, hora

if "--solucao" in sys.argv:
    from solucao.escalar import quem_decide
else:
    from escalar import quem_decide

PAPEL = {p["nome"]: p for p in EQUIPE}


def noite(quem_decide, inicio="17:12", fim="18:30"):
    print(f"B-17, troca de motorista, pedido às {inicio}")
    antes = None
    for m in range(minutos(inicio), minutos(fim) + 1):
        agora = quem_decide("troca", inicio, hora(m))
        if agora == antes and (m < minutos(fim) or agora[0] == "seguro"):
            continue
        nome, ate = agora
        if nome == "seguro":
            linha = "estado seguro: nada executa, pendência registrada, equipe avisada"
        else:
            p = PAPEL[nome]
            linha = f"{nome} ({p['papel']}) até {ate}"
            if minutos(ate) > minutos(p["plantao"][1]):
                linha += f"   sai às {p['plantao'][1]}"
            if agora == antes:
                linha += ", ainda esperando"
        if agora != antes or m == minutos(fim):
            print(f"{hora(m)}  {linha}")
        antes = agora


if __name__ == "__main__":
    noite(quem_decide)
