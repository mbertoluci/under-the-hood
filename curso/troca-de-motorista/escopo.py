# EXERCÍCIO (aula 18): o escopo da tarefa.
# A tarefa diz o que está dentro: que ações, e em que alvos. Fora da lista, não.
# E o não repetido para a sessão.
# Rode: python test_escopo.py

# A tarefa da Joana: avisar os clientes das duas cargas atrasadas de hoje.
TAREFA = {
    "acoes": {"ler_carga", "avisar_cliente"},
    "alvos": {"C-9281", "C-9300"},
}
LIMITE = 3  # negações seguidas até a sessão parar


def decidir(tarefa, chamada, historico, limite=LIMITE):
    """O que fazer com esta chamada do agente? Devolve "executa", "nega" ou "para".

    tarefa: {"acoes": {"ler_carga", "avisar_cliente"}, "alvos": {"C-9281", "C-9300"}}
    chamada: {"acao": "avisar_cliente", "alvo": "C-9300"}
    historico: as decisões anteriores desta sessão, na ordem: ["executa", "nega", "nega"]
    Como decidir:
    1. se a sessão já parou (tem "para" no histórico), continua parada: "para";
    2. se a ação está em tarefa["acoes"] e o alvo está em tarefa["alvos"]: "executa".
       Tarefa sem uma das duas listas não tem nada dentro;
    3. senão, é uma negação. Conte as negações seguidas no fim do histórico, mais esta.
       Chegou em `limite`: "para". Não chegou: "nega".
    """
    raise NotImplementedError("escreva aqui")
