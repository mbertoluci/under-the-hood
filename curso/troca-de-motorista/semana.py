# Aula 13: a semana da concessão. Na segunda, a Joana cansou de aprovar aviso de atraso e clicou em "sempre permitir".
# Cinco pedidos do agente na semana, e quais saem sem perguntar a ninguém.
# Rode: python semana.py            (com o seu cobre, de concessao.py)
#       python semana.py --solucao  (com a solução)
import sys
from concessao import por_concessao

if "--solucao" in sys.argv:
    from solucao.concessao import cobre
else:
    from concessao import cobre


def concessao(id, quem, classe, ferramenta, argumentos, revogada=False):
    return {"id": id, "quem": quem, "classe": classe, "ferramenta": ferramenta, "argumentos": argumentos,
            "expira": "2026-10-17 18:00", "revogada": revogada}


CONCESSOES = [
    concessao("C-1", "joana", "aviso", "avisar_cliente", {"template": "atraso"}),
    concessao("C-2", "bruna", "aviso", "avisar_cliente", {"template": "atraso*"}),   # ela quis dizer "os de atraso"
    concessao("C-3", "joana", "troca", "trocar_motorista", {}),                      # cansou de aprovar troca também
    concessao("C-4", "agente", "aviso", "avisar_cliente", {"template": "desconto"}),  # um e-mail pediu, e o agente ativou
]
PEDIDOS = [
    ("ter 14/10 10:00", "aviso de atraso, XPTO", "2026-10-14 10:00", "aviso", "avisar_cliente", {"template": "atraso", "cliente": "XPTO"}),
    ("ter 14/10 10:05", "aviso com reembolso", "2026-10-14 10:05", "aviso", "avisar_cliente", {"template": "atraso_com_reembolso", "cliente": "XPTO"}),
    ("qua 15/10 17:12", "troca B-17 (Carlos)", "2026-10-15 17:12", "troca", "trocar_motorista", {"carga": "C-9281", "motorista": "Carlos"}),
    ("qui 16/10 09:30", "aviso com desconto", "2026-10-16 09:30", "aviso", "avisar_cliente", {"template": "desconto", "cliente": "XPTO"}),
    ("sex 17/10 18:01", "aviso de atraso, XPTO", "2026-10-17 18:01", "aviso", "avisar_cliente", {"template": "atraso", "cliente": "XPTO"}),
]


def main(cobre):
    for c in CONCESSOES:
        escopo = ", ".join(f"{k}={v}" for k, v in c["argumentos"].items()) or "qualquer argumento"
        print(f"{c['id']}  {c['quem']:<7}{c['classe']:<7}{escopo}")
    for quando, rotulo, agora, classe, ferramenta, argumentos in PEDIDOS:
        acao = {"classe": classe, "ferramenta": ferramenta, "argumentos": argumentos}
        id = por_concessao(acao, CONCESSOES, agora, cobre=cobre)
        print(f"{quando}  {rotulo:<24}{'sai sem perguntar (' + id + ')' if id else 'pede aprovação'}")


if __name__ == "__main__":
    main(cobre)
