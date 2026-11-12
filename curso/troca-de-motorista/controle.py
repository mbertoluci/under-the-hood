# EXERCÍCIO (aula 8): o controle vem do que acontece se der errado, e quem diz é o catálogo.
# Escreva controle e rode: python test_controle.py
import json
from pathlib import Path

# O que cada ação faz quando dá errado, escrito por quem cuida da operação, não pelo agente.
CATALOGO = json.loads((Path(__file__).resolve().parent / "efeitos.json").read_text(encoding="utf-8"))


def controle(proposta, catalogo=CATALOGO):
    """Diz quem confere a ação antes de ela rodar: "confinar", "juiz" ou "pessoa".

    Olhe o que o CATÁLOGO diz da ação proposta["acao"], nesta ordem:
    1. Não dá para desfazer ("volta" é false): "pessoa".
    2. Volta e fica na área do agente ("onde" é "agente"): "confinar". Ninguém confere.
    3. Volta, mas mexe fora da área do agente ("onde" é "fora"): "juiz".
    O que a proposta diz sobre ela mesma não conta.
    Fora do catálogo, campo faltando ou valor diferente desses: "pessoa".
    """
    raise NotImplementedError("escreva aqui")
