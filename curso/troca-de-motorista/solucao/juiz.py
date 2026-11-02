# Uma solução do exercício da aula 7.
from juiz import chamada

ENTRA = {"usuario": lambda r: f"[usuario] {r['texto']}", "chamada": chamada}


def o_que_o_juiz_ve(sessao):
    # A lista do que entra, não do que sai: papel novo fica de fora até alguém pôr aqui.
    return "\n".join(ENTRA[r["papel"]](r) for r in sessao if r.get("papel") in ENTRA)
