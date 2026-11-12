# EXERCÍCIO (aula 12): a regra das duas pessoas.
# Ação sem volta pede duas chaves: duas pessoas diferentes, com autoridade,
# aprovando o mesmo conteúdo.
# Rode: python test_duas_chaves.py

# Quantas chaves cada classe pede. Classe fora da tabela nunca libera.
CHAVES = {"troca": 1, "descarte": 2}

# O cadastro: quem é pessoa, quem é agente, e o que cada um pode autorizar.
# O agente executa troca e descarte, mas aprovar, nunca: ele não é pessoa.
CADASTRO = {
    "joana": {"tipo": "pessoa", "autoriza": ["troca", "descarte"]},
    "bruna": {"tipo": "pessoa", "autoriza": ["troca", "descarte"]},
    "lia": {"tipo": "pessoa", "autoriza": []},
    "agente": {"tipo": "agente", "autoriza": ["troca", "descarte"]},
}


def chaves(acao, aprovacoes, cadastro=CADASTRO):
    """As chaves válidas: o conjunto de nomes de quem aprovou de verdade.

    acao: {"id": "D-03", "classe": "descarte", "resumo": "...", "pedida_por": "agente"}
    aprovacoes: [{"quem": "joana", "resumo": "..."}, ...]
    Uma aprovação só vale se:
    1. quem aprovou é pessoa do cadastro e autoriza a classe. O agente nunca é chave;
    2. aprovou o mesmo resumo da ação (aula 2);
    3. não foi quem pediu a ação.
    A mesma pessoa duas vezes é uma chave só.
    """
    raise NotImplementedError("escreva aqui")


def liberado(acao, aprovacoes, cadastro=CADASTRO, chaves=chaves):
    """Pronta: libera quando as chaves válidas chegam ao que a classe pede."""
    precisa = CHAVES.get(acao["classe"])
    return precisa is not None and len(chaves(acao, aprovacoes, cadastro)) >= precisa
