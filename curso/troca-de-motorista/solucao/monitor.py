def proteger(ferramentas, monitor):
    def embrulhar(nome, ferramenta):
        def chamada(args):
            try:
                resposta = monitor(nome, args)
            except Exception:
                resposta = None
            if isinstance(resposta, tuple) and len(resposta) == 2:
                if resposta[0] is True:
                    return ferramenta(args)
                if resposta[0] is False:
                    return {"negado": resposta[1]}
            return {"negado": "o monitor falhou"}
        return chamada
    return {nome: embrulhar(nome, ferramenta) for nome, ferramenta in ferramentas.items()}
