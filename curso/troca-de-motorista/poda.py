# EXERCÍCIO (aula 19): a trava que saiu.
# Antes de tirar uma trava porque outra "cuida disso", rode os casos perigosos sem ela.
# Rode: python test_poda.py


# Cada trava olha uma troca de motorista e diz se barra (True) ou deixa passar (False).
def origem(caso):
    """Aula 16: o número do motorista tem que ter vindo do servidor."""
    return caso["numero_veio_de"] != "servidor"


def teto(caso):
    """Aula 14: no máximo duas trocas por carga."""
    return caso["trocas_da_carga"] >= 2


def juiz(caso):
    """Aula 7: um juiz automático barra a troca suspeita. Aqui, um substituto fixo."""
    return caso["parece_suspeita"]


def aprovacao(caso):
    """Aulas 2 e 15: sem a aprovação da Joana, a troca não sai."""
    return not caso["joana_aprovou"]


TRAVAS = [origem, teto, juiz, aprovacao]

# Os casos perigosos que a equipe conhece. Todos têm que ser barrados.
def caso(numero_veio_de="servidor", trocas_da_carga=0,
         parece_suspeita=False, joana_aprovou=True):
    return {"numero_veio_de": numero_veio_de, "trocas_da_carga": trocas_da_carga,
            "parece_suspeita": parece_suspeita, "joana_aprovou": joana_aprovou}


CASOS = {
    "número colado de um e-mail": caso(numero_veio_de="e-mail"),
    "terceira troca da carga": caso(trocas_da_carga=2),
    "SMS dizendo que é a Maria": caso(parece_suspeita=True, joana_aprovou=False),
    "troca normal, que ninguém aprovou": caso(joana_aprovou=False),
}


def pode_tirar(trava, travas, casos):
    """Dá para tirar esta trava? Devolve (True, []) ou (False, [casos que passariam]).

    trava: a função que se quer tirar, como aprovacao
    travas: a pilha de hoje, como TRAVAS
    casos: {"nome do caso": {...}}, os casos perigosos conhecidos
    Como decidir:
    1. se não há caso nenhum, ou a trava nem está na pilha, não pode: (False, []).
       Sem caso, sem prova;
    2. monte a pilha sem a trava, e rode cada caso nela. O caso está seguro se alguma
       trava que ficou o barra. Trava que dá erro não conta como barrar;
    3. junte os nomes dos casos que nenhuma trava barrou.
       Lista vazia: (True, []). Senão: (False, lista).
    """
    raise NotImplementedError("escreva aqui")
