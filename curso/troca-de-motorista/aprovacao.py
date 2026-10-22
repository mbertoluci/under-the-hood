# EXERCÍCIO (aula 2): uma aprovação só vale pelo que a pessoa viu.
# Escreva as três funções e rode: python test_aprovacao.py
from dia import ACOES, NIVEIS
from operacao import resumo


def precisa_perguntar(plano):
    """1. Precisava perguntar?

    Devolve False se a regra pode executar sozinha (nível 2 no catálogo NIVEIS) e True se uma pessoa tem que aprovar.
    Ação fora do catálogo: pergunta.
    """
    raise NotImplementedError("escreva aqui")


def cartao(plano, carga):
    """2. Ela vê o que muda?

    Devolve o texto do cartão de aprovação: uma linha que diz o plano, a ação (ACOES) e a carga, e uma linha para cada
    campo que muda, no formato "  motorista: Anderson -> Carlos" ou "  veiculo: V-07 -> R-12".
    Só os campos motorista e veiculo, e só os que mudam. Versão e hora não entram: não mudam nada no mundo.
    """
    raise NotImplementedError("escreva aqui")


def vale(aprovacao, plano, carga):
    """3. O que executa é o que ela viu?

    A aprovação é um dicionário {"plano": id do plano, "decisao": "aprovo" ou "recuso",
    "resumo": resumo(texto do cartão que ela viu)}. O id do plano não basta: o plano muda e o id continua.
    Vale só se a decisão foi "aprovo" e o resumo do cartão de agora é igual ao resumo do cartão aprovado.
    """
    raise NotImplementedError("escreva aqui")
