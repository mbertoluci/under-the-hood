# EXERCÍCIO: a regra que decide se um sinal que chegou autoriza a proposta.
# Ela roda fora do modelo. O modelo lê e propõe; esta função decide quem manda.
from operacao import CANAIS, PAPEIS


def autorizou(sinal, proposta):
    """Devolve (True, "") se o sinal autoriza a proposta, ou (False, motivo) se não autoriza.

    Responda três perguntas, nesta ordem. Se qualquer uma falhar, não autoriza:
    1. De onde veio? De um contato do cadastro (CANAIS) de quem é solicitante (PAPEIS).
    2. O que foi? O botão "autorizo". Texto livre não vale, nem do número certo.
    3. Para quê? Para esta proposta (o id da proposta que vem no botão).
    Campo faltando também não autoriza.
    """
    raise NotImplementedError("escreva a regra aqui e rode: python test_autoridade.py")
