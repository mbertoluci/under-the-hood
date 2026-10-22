# O despacho com as três perguntas (aula 2).
# Uso: python despacho.py [--solucao]               (responda s ou n a cada cartão)
#      yes s | python despacho.py --solucao         (s para tudo, como no despacho ingênuo)
import sys

if "--solucao" in sys.argv:
    from solucao.aprovacao import cartao, precisa_perguntar, vale
else:
    from aprovacao import cartao, precisa_perguntar, vale
from dia import CARGAS, PEDIDOS, executar, perguntar, plano_atual
from operacao import resumo


def pedir(plano):
    texto = cartao(plano, CARGAS[plano["carga"]])
    print(f"\n{plano['hora']} {texto}")
    return {"plano": plano["id"], "decisao": "aprovo" if perguntar("aprova?") else "recuso", "resumo": resumo(texto)}


aprovacoes, sozinha = {}, 0
for p in PEDIDOS:
    if not precisa_perguntar(p):
        sozinha += 1  # a regra executa e registra
        continue
    aprovacoes[p["id"]] = pedir(p)
print(f"\n{sozinha} de {len(PEDIDOS)} a regra fez sozinha e registrou; {len(PEDIDOS) - sozinha} foram para a despachante")

print("\n17:40 hora do despacho das trocas")
for p in PEDIDOS:
    if p["id"] not in aprovacoes:
        continue
    agora = plano_atual(p)
    if not vale(aprovacoes[p["id"]], agora, CARGAS[agora["carga"]]):
        print(f"  {agora['id']}: o cartão mudou depois da aprovação, não executa e pergunta de novo")
        aprovacoes[p["id"]] = pedir(agora)
        if not vale(aprovacoes[p["id"]], agora, CARGAS[agora["carga"]]):
            continue
    executar(agora)
