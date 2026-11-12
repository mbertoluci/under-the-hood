from functools import partial
import duas_chaves
from duas_chaves import CADASTRO


def chaves(acao, aprovacoes, cadastro=CADASTRO):
    return {a["quem"] for a in aprovacoes
            if cadastro.get(a["quem"], {}).get("tipo") == "pessoa"
            and acao["classe"] in cadastro[a["quem"]]["autoriza"]
            and a["resumo"] == acao["resumo"]
            and a["quem"] != acao["pedida_por"]}


liberado = partial(duas_chaves.liberado, chaves=chaves)
