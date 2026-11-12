def combinar(acao, camadas):
    nega, exige = [], []
    for camada in camadas:
        nome = camada.__name__
        try:
            resposta = camada(acao)
            nega += [f"{nome}: {motivo}" for motivo in resposta["nega"]]
            exige += [f"{nome}: {pedido}" for pedido in resposta["exige"]]
        except Exception as erro:
            nega.append(f"{nome}: a camada falhou ({type(erro).__name__})")
    if not camadas:
        nega.append("nenhuma camada respondeu")
    resultado = "negado" if nega else "pendente" if exige else "executavel"
    return {"resultado": resultado, "nega": nega, "exige": exige}
