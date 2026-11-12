from preparar import CADASTRO, TETO_TROCAS


def aplicar(servidor, pedido, cadastro=CADASTRO):
    mudanca = servidor["mudancas"].get(pedido.get("id"))
    if mudanca is None or mudanca["estado"] != "preparada":
        return False, "mudança desconhecida ou já aplicada"
    quem = cadastro.get(mudanca["aprovada_por"])
    if not quem or quem["tipo"] != "pessoa" or "troca" not in quem["autoriza"]:
        return False, "sem aprovação de quem pode"
    carga = servidor["cargas"][mudanca["carga"]]
    if carga["trocas"] + 1 > TETO_TROCAS:
        return False, "passaria do teto de trocas"
    carga["motorista"] = mudanca["motorista"]
    carga["trocas"] += 1
    mudanca["estado"] = "aplicada"
    return True, ""
