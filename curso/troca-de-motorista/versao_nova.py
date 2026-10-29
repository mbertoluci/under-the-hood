# A versão nova (aula 5): às 17:00 o despacho passa a mandar "carga_atual" no lugar de "carga".
# Uso: python versao_nova.py --ingenua            (a política lista o que proíbe)
#      python versao_nova.py [--solucao]          (lista o que libera, com o seu politica.py ou o da solução)
#      python versao_nova.py --quebra [--solucao] (duas regras de outras equipes; uma dá erro com o campo novo)
import json, sys

if "--solucao" in sys.argv:
    from solucao.politica import consultar, permitido
elif "--ingenua" not in sys.argv:
    from politica import consultar, permitido

PROIBIDAS = {"cancel_cargo", "delete_cargo"}


def ingenua(entrada):
    # A política que lista o que proíbe. O que não está na lista passa.
    motivos = []
    if entrada.get("acao") in PROIBIDAS:
        motivos.append("ação proibida")
    if entrada.get("carga", {}).get("status") == "bloqueada":
        motivos.append("a carga está bloqueada")
    if entrada.get("nivel") == 0:
        motivos.append("nível 0: só observa")
    return not motivos, motivos


def regra_da_qualidade(entrada):
    status = entrada["carga"]["status"]  # escrita para a versão antiga
    return (True, []) if status == "liberada" else (False, [f"a carga está {status}"])


def regra_do_nivel(entrada):
    return (True, []) if entrada.get("nivel") in (1, 2, 3) else (False, ["nível de autonomia inválido"])


def despacho_ingenuo(regras, entrada):
    # Junta as negações de todas as regras. A que dá erro vai para o log, e o despacho segue com as outras.
    negacoes = []
    for regra in regras:
        try:
            ok, motivos = regra(entrada)
            if not ok:
                negacoes += motivos
        except Exception as e:
            print(f"17:40 log: a {regra.__name__} falhou ({e!r}); seguindo com as outras")
    return not negacoes, negacoes


def despacho(regras, entrada):
    negacoes = []
    for regra in regras:
        ok, motivos = consultar(regra, entrada)
        if not ok:
            negacoes += motivos
    return not negacoes, negacoes


antes = {"acao": "change_driver", "carga": {"id": "C-9281", "status": "liberada"}, "nivel": 1}
if "--quebra" in sys.argv:
    regras = [regra_da_qualidade, regra_do_nivel]
    decidir = despacho if "--solucao" in sys.argv else despacho_ingenuo
elif "--ingenua" in sys.argv:
    regras, decidir = [ingenua], despacho_ingenuo
else:
    regras, decidir = [permitido], despacho

ok, _ = decidir(regras, antes)
print(f"16:50 despacho pergunta: C-9281 liberada; política: {'permitido' if ok else 'negado'}")
print('17:00 sai a versão nova do despacho: o campo "carga" agora se chama "carga_atual"')
print("17:20 a qualidade bloqueia a C-9281: o baú refrigerado marcou 9 °C")
entrada = {"acao": "change_driver", "carga_atual": {"id": "C-9281", "status": "bloqueada"}, "nivel": 1}
print("17:40 despacho manda:", json.dumps(entrada, ensure_ascii=False))
ok, motivos = decidir(regras, entrada)
if ok:
    print("17:40 política: permitido (nenhuma regra negou)")
    print("17:40 despacho: executado: C-9281 motorista Carlos (R-12), numa carga bloqueada")
else:
    print("17:40 política: negado:", "; ".join(motivos))
    print("17:40 despacho: não executa; volta para a despachante, com o motivo")
