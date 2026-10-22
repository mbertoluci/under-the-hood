# Uma solução do exercício da aula 2. Tente antes de abrir.
from dia import ACOES, NIVEIS
from operacao import resumo


def precisa_perguntar(plano):
    # 1. Precisava perguntar? Só se a regra não faz sozinha. Fora do catálogo, pergunta.
    return NIVEIS.get(plano.get("acao")) != 2


def cartao(plano, carga):
    # 2. Ela vê o que muda? O antes e o depois, só do que muda.
    acao = ACOES.get(plano["acao"], plano["acao"])
    linhas = [f"{plano['id']}: {acao} na {carga['id']}, entrega {carga['entrega']}"]
    for campo in ("motorista", "veiculo"):
        if campo in plano and plano[campo] != carga[campo]:
            linhas.append(f"  {campo}: {carga[campo]} -> {plano[campo]}")
    return "\n".join(linhas)


def vale(aprovacao, plano, carga):
    # 3. O que executa é o que ela viu? O resumo do cartão de agora é o do aprovado?
    if aprovacao.get("decisao") != "aprovo":
        return False
    return aprovacao.get("resumo") == resumo(cartao(plano, carga))
