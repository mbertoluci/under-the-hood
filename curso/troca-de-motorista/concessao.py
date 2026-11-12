# EXERCÍCIO (aula 13): a aprovação permanente ("sempre permitir").
# Quem clica em "sempre permitir" aceita um risco: a concessão só vale dentro do que ela diz.
# Rode: python test_concessao.py

# Classes que aceitam concessão: só as que a própria ferramenta limita.
# Aviso com template fixo, sim. Troca e descarte, nunca: pedem aprovação a cada ação.
ACEITA_CONCESSAO = {"aviso"}

# O cadastro: quem é pessoa, quem é agente, e o que cada um pode autorizar.
CADASTRO = {
    "joana": {"tipo": "pessoa", "autoriza": ["aviso", "troca", "descarte"]},
    "bruna": {"tipo": "pessoa", "autoriza": ["aviso", "troca", "descarte"]},
    "lia": {"tipo": "pessoa", "autoriza": []},
    "agente": {"tipo": "agente", "autoriza": ["aviso", "troca", "descarte"]},
}


def cobre(concessao, acao, agora, cadastro=CADASTRO):
    """True se esta concessão libera esta ação agora, sem perguntar de novo.

    concessao: {"id": "C-1", "quem": "joana", "classe": "aviso", "ferramenta": "avisar_cliente",
                "argumentos": {"template": "atraso"}, "expira": "2026-10-17 18:00", "revogada": False}
    acao: {"classe": "aviso", "ferramenta": "avisar_cliente",
           "argumentos": {"template": "atraso", "cliente": "XPTO"}}
    agora: "2026-10-14 10:00" (texto nesse formato compara certo)
    A concessão só cobre se:
    1. a classe da ação aceita concessão, e é a mesma classe e a mesma ferramenta da concessão;
    2. cada argumento da concessão é igual ao da ação. Igual: um asterisco é texto, não curinga;
    3. quem concedeu é pessoa do cadastro e autoriza a classe. O agente nunca concede;
    4. não foi revogada, e agora é antes de expirar.
    """
    raise NotImplementedError("escreva aqui")


def por_concessao(acao, concessoes, agora, cadastro=CADASTRO, cobre=cobre):
    """Pronta: o id da concessão que libera a ação, ou None (a ação pede aprovação, como sempre)."""
    return next((c["id"] for c in concessoes if cobre(c, acao, agora, cadastro)), None)
