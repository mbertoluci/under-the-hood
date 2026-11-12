from escopo import LIMITE


def decidir(tarefa, chamada, historico, limite=LIMITE):
    if "para" in historico:
        return "para"
    dentro = (chamada.get("acao") in tarefa.get("acoes", ())
              and chamada.get("alvo") in tarefa.get("alvos", ()))
    if dentro:
        return "executa"
    seguidas = 1  # esta negação
    for decisao in reversed(historico):
        if decisao != "nega":
            break
        seguidas += 1
    return "para" if seguidas >= limite else "nega"
