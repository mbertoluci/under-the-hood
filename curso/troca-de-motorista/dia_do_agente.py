# Aula 8: as 300 chamadas de ferramenta do agente num dia da operação, e quem confere cada uma.
# Rode: python dia_do_agente.py --tudo       (a despachante aprova cada chamada)
#       python dia_do_agente.py              (com o seu controle, de controle.py)
#       python dia_do_agente.py --solucao    (com a solução)
# O dia é inventado. A proporção real medida pela Anthropic está no README.
import sys
from collections import Counter

DIA = ([("ler_carga", {})] * 160 + [("escrever_rascunho", {})] * 52 + [("consultar_rastreador", {})] * 40
       + [("reservar_veiculo", {})] * 25 + [("remarcar_doca", {})] * 15 + [("enviar_email_embarcador", {})] * 4
       + [("trocar_motorista", {})] * 2
       # numa das trocas, o agente escreve na proposta que ela volta e fica na área dele
       + [("trocar_motorista", {"volta": True, "onde": "agente"})]
       # uma ação que alguém acrescentou ao agente e ninguém pôs no catálogo
       + [("cancelar_coleta", {})])


def main():
    if "--tudo" in sys.argv:
        print(f"o dia do agente: {len(DIA)} chamadas")
        print(f"pergunta tudo: {len(DIA)} cartões para a despachante")
        return
    if "--solucao" in sys.argv:
        from solucao.controle import controle
    else:
        from controle import controle
    caixas = {"confinar": Counter(), "juiz": Counter(), "pessoa": Counter()}
    for acao, extra in DIA:
        caixas[controle({"acao": acao, "argumentos": {"carga": "C-9281"}, **extra})][acao] += 1
    print(f"o dia do agente: {len(DIA)} chamadas")
    for caixa, conta in caixas.items():
        detalhe = ", ".join(f"{a} {n}" for a, n in conta.most_common())
        print(f"{caixa:<9}{sum(conta.values()):>4}   {detalhe}")
    n = sum(caixas["pessoa"].values())
    print(f"a despachante vê {n} cartões de {len(DIA)} ({n / len(DIA):.1%})".replace(".", ","))


if __name__ == "__main__":
    main()
