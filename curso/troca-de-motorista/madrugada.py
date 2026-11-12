# Aula 12: 3h10 da madrugada. O baú da C-9281 marca 14 °C, e o agente propõe descartar a carga (D-03).
# Descarte não tem volta: pede duas chaves. Quatro tentativas de liberar, e quantas chaves cada uma tem.
# Rode: python madrugada.py            (com o seu chaves, de duas_chaves.py)
#       python madrugada.py --solucao  (com a solução)
import sys
from duas_chaves import CHAVES, liberado

if "--solucao" in sys.argv:
    from solucao.duas_chaves import chaves
else:
    from duas_chaves import chaves

D03 = {"id": "D-03", "classe": "descarte", "resumo": "descartar C-9281, baú a 14 °C", "pedida_por": "agente"}
SIM = D03["resumo"]
TENTATIVAS = [
    ("agente + joana", [{"quem": "agente", "resumo": SIM}, {"quem": "joana", "resumo": SIM}]),
    ("joana + joana", [{"quem": "joana", "resumo": SIM}, {"quem": "joana", "resumo": SIM}]),
    ("joana + bruna (às 2h, baú a 9 °C)", [{"quem": "joana", "resumo": SIM}, {"quem": "bruna", "resumo": "descartar C-9281, baú a 9 °C"}]),
    ("joana + bruna", [{"quem": "joana", "resumo": SIM}, {"quem": "bruna", "resumo": SIM}]),
]


def main(chaves):
    print(f"{D03['id']}, descarte da C-9281: pede {CHAVES['descarte']} chaves, pedido pelo agente")
    for rotulo, aprovacoes in TENTATIVAS:
        validas = chaves(D03, aprovacoes)
        n = len(validas)
        libera = liberado(D03, aprovacoes, chaves=chaves)
        print(f"{rotulo:<36}{n} chave{'s' if n != 1 else ' '}  {'LIBERA' if libera else 'não libera'}")


if __name__ == "__main__":
    main(chaves)
