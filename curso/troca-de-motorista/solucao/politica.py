# Uma solução do exercício da aula 5.
from politica import CONHECIDAS


def permitido(entrada):
    motivos = []
    # 1 e 2. Cada regra confirma o que libera. O que não conhece ou não recebeu não confirma.
    acao = entrada.get("acao")
    if acao not in CONHECIDAS:
        motivos.append(f"ação desconhecida: {acao}")
    carga = entrada.get("carga")
    if not isinstance(carga, dict):
        motivos.append("o campo carga não veio")
    elif carga.get("status") != "liberada":
        motivos.append(f"a carga não está liberada: {carga.get('status')}")
    nivel = entrada.get("nivel")
    if type(nivel) is not int or nivel not in (1, 2, 3):  # em Python, True == 1
        motivos.append(f"nível de autonomia inválido: {nivel!r}")
    return not motivos, motivos


def consultar(politica, entrada):
    # 3. O que quebra nega. Só o True da própria política libera.
    try:
        ok, motivos = politica(entrada)
    except Exception as e:
        return False, [f"a política falhou: {e!r}"]
    if ok is True:
        return True, []
    if ok is False and motivos:
        return False, list(motivos)
    return False, [f"resposta inesperada da política: {(ok, motivos)!r}"]
