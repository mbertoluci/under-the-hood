from functools import partial
import limite
from limite import TETOS, minutos


def cabe(acao, registro, agora, tetos=TETOS):
    regra = tetos.get(acao["classe"])
    if regra is None:
        return False
    total = sum(1 for r in registro
                if (r["classe"], r["chave"]) == (acao["classe"], acao["chave"])
                and r["estado"] in ("feita", "pendente")
                and (regra["janela"] is None or minutos(r["quando"], agora) < regra["janela"]))
    return total + 1 <= regra["teto"]


pedir = partial(limite.pedir, cabe=cabe)
