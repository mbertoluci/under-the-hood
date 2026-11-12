from escalar import EQUIPE, ROTA, minutos, hora


def quem_decide(classe, inicio, agora, equipe=EQUIPE, rota=ROTA):
    t, ja = minutos(inicio), minutos(agora)
    for papel, prazo in rota.get(classe, []):
        fim = t + prazo
        pessoa = next((p for p in equipe if p["papel"] == papel and classe in p["autoriza"]
                       and minutos(p["plantao"][0]) <= t and fim <= minutos(p["plantao"][1])), None)
        if pessoa is None:
            continue
        if ja < fim:
            return pessoa["nome"], hora(fim)
        t = fim
    return "seguro", None
