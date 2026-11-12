# EXERCÍCIO (aula 20): o conferente único.
# Toda chamada do agente passa por um conferente só: sempre chamado, que a chamada não pula,
# e pequeno o bastante para testar inteiro.
# Rode: python test_monitor.py


def proteger(ferramentas, monitor):
    """Embrulha as ferramentas: toda chamada passa pelo monitor antes de executar.

    ferramentas: {"ler_carga": funcao, "preparar_troca": funcao}   cada funcao recebe args
    monitor: funcao(nome, args) que devolve (True, "") ou (False, motivo)
    Devolve um dicionário novo, com os mesmos nomes. Cada entrada recebe args e:
    1. chama monitor(nome, args). Se ele negar, devolve {"negado": motivo} e não executa;
    2. se o monitor der erro, ou devolver outra coisa que não a tupla (True, ...) ou
       (False, ...), também nega: {"negado": "o monitor falhou"}. Lista não vale;
    3. só com (True, ...) executa a ferramenta, com os mesmos args, e devolve o resultado.
    Embrulhe todas as ferramentas, não só as perigosas. E o dicionário novo não muda
    se alguém mexer no original depois.
    """
    raise NotImplementedError("escreva aqui")
