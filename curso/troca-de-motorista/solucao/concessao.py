from functools import partial
import concessao
from concessao import ACEITA_CONCESSAO, CADASTRO


def cobre(c, acao, agora, cadastro=CADASTRO):
    quem = cadastro.get(c["quem"], {})
    return (acao["classe"] in ACEITA_CONCESSAO
            and c["classe"] == acao["classe"] and c["ferramenta"] == acao["ferramenta"]
            and all(acao["argumentos"].get(k) == v for k, v in c["argumentos"].items())
            and quem.get("tipo") == "pessoa" and acao["classe"] in quem.get("autoriza", [])
            and not c["revogada"] and agora < c["expira"])


por_concessao = partial(concessao.por_concessao, cobre=cobre)
