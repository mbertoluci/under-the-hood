def barra(trava, caso):
    try:
        return trava(caso) is True
    except Exception:
        return False  # trava que quebra não segura nada


def pode_tirar(trava, travas, casos):
    if not casos or trava not in travas:
        return False, []
    resto = [t for t in travas if t is not trava]
    passam = [nome for nome, caso in casos.items()
              if not any(barra(t, caso) for t in resto)]
    return not passam, passam
