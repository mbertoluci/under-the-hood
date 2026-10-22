# O despacho ingênuo (aula 2): pergunta tudo, mostra só o id do plano e guarda a aprovação pelo id.
# Uso: python despacho_ingenuo.py              (responda s ou n a cada pedido)
#      yes s | python despacho_ingenuo.py      (a despachante cansada: s para tudo)
from dia import PEDIDOS, executar, perguntar, plano_atual

aprovados = set()
for p in PEDIDOS:
    if perguntar(f"{p['hora']} aprovar o plano {p['id']}?"):
        aprovados.add(p["id"])
print(f"\n{len(PEDIDOS)} perguntas no dia, {len(aprovados)} aprovadas")

print("\n17:40 hora do despacho das trocas")
for p in PEDIDOS:
    if p["acao"] == "change_driver" and p["id"] in aprovados:
        executar(plano_atual(p))  # o B-17 mudou para o Diego às 17:25, e o id continua aprovado
