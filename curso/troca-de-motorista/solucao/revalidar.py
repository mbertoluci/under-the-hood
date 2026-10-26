# Uma solução do exercício da aula 4. Tente antes de abrir.
from operacao import resumo
from revalidar import conteudo


def pode_executar(autorizacao, plano, agora):
    # 1. O conteúdo é o que ela viu?
    if autorizacao.get("resumo") != resumo(conteudo(plano)):
        return False, "o plano mudou depois da autorização"
    # 2. Quem autorizou ainda pode? Pergunta ao cadastro de agora, não à linha gravada.
    quem = autorizacao.get("quem")
    if agora["papeis"].get(quem) != "solicitante":
        return False, f"{quem} não pode mais autorizar"
    # 3. O mundo ainda é o que era?
    if agora["cargas"].get(plano["carga"]) != "aguardando motorista":
        return False, f"a carga {plano['carga']} não está mais aguardando motorista"
    escala = agora["escalas"].get(plano["motorista"])
    if escala not in (None, plano["carga"]):
        return False, f"{plano['motorista']} já está na carga {escala}"
    return True, ""
