# EXERCÍCIO (aula 5): na dúvida, a política nega.
# Escreva permitido e consultar e rode: python test_politica.py

# As ações que esta política sabe avaliar. Qualquer outra é desconhecida.
CONHECIDAS = {"change_driver"}


def permitido(entrada):
    """A política, antes de trocar o motorista. Devolve (True, []) ou (False, motivos).

    entrada é o que o despacho manda:
        {"acao": "change_driver",
         "carga": {"id": "C-9281", "status": "liberada"},
         "nivel": 1}                                       nível de autonomia da ação: 1, 2 ou 3

    Libera só o que ela consegue confirmar. Todo o resto nega, com o motivo:
    1. O que ela não conhece: ação fora de CONHECIDAS, status que não é "liberada",
       nível que não é o inteiro 1, 2 ou 3.
    2. O que falta: entrada sem acao, sem carga, sem status ou sem nivel.
    """
    raise NotImplementedError("escreva aqui")


def consultar(politica, entrada):
    """O despacho chama a política por aqui. Devolve (True, []) ou (False, motivos).

    3. O que quebra: se a política dá erro ou devolve outra coisa que não (True, ...) ou
       (False, motivos), nega, com o motivo. Só o True da própria política libera.
    """
    raise NotImplementedError("escreva aqui")
