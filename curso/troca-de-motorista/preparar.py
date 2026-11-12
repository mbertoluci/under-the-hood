# EXERCÍCIO (aula 15): o agente prepara, outro aplica.
# A ferramenta do agente só prepara a mudança. Aplicar é outra função, fora da lista dele.
# Rode: python test_preparar.py

# O que o agente pode chamar. aplicar não está aqui, de propósito.
FERRAMENTAS_DO_AGENTE = {"ler_carga", "preparar_troca"}

CADASTRO = {
    "Joana": {"tipo": "pessoa", "autoriza": {"troca"}},
    "Lia": {"tipo": "pessoa", "autoriza": set()},        # em treino
    "agente": {"tipo": "agente", "autoriza": {"troca"}},  # executa, mas não é pessoa
}
TETO_TROCAS = 2  # trocas de motorista por carga


def preparar(servidor, carga, motorista):
    """Pronta: a ferramenta do agente. Grava a mudança e devolve o id. Não troca nada."""
    servidor["seq"] += 1
    mid = f"M-{servidor['seq']}"
    servidor["mudancas"][mid] = {"carga": carga, "motorista": motorista,
                                 "estado": "preparada", "aprovada_por": None}
    return mid


def chamar(servidor, ferramenta, args, ferramentas=FERRAMENTAS_DO_AGENTE):
    """Pronta: toda chamada do agente passa aqui. Fora da lista, não existe para ele."""
    if ferramenta not in ferramentas:
        return f"ferramenta desconhecida: {ferramenta}"
    if ferramenta == "preparar_troca":
        return preparar(servidor, args["carga"], args["motorista"])  # só estes dois campos
    return dict(servidor["cargas"][args["carga"]])


def aprovar(servidor, mid, pessoa):
    """Pronta: o botão do portal. Quem chama é o portal, com a pessoa que está logada."""
    mudanca = servidor["mudancas"].get(mid)
    if mudanca and mudanca["estado"] == "preparada":
        mudanca["aprovada_por"] = pessoa


def aplicar(servidor, pedido, cadastro=CADASTRO):
    """Aplica uma mudança preparada. Devolve (True, "") ou (False, motivo).

    servidor: {"seq": 1,
               "mudancas": {"M-1": {"carga": "C-9281", "motorista": "Carlos",
                                    "estado": "preparada", "aprovada_por": "Joana"}},
               "cargas": {"C-9281": {"motorista": "Anderson", "trocas": 1}}}
    pedido: {"id": "M-1"}  quem pede para aplicar. Outros campos: não confie neles.
    Condições:
    1. o id existe em servidor["mudancas"], e a mudança está "preparada";
    2. aprovada_por é uma pessoa do cadastro que autoriza troca;
    3. a carga, agora, ainda cabe no teto de trocas;
    4. aí sim: ponha na carga o motorista da mudança (não o do pedido), some a troca
       e marque a mudança como "aplicada".
    """
    raise NotImplementedError("escreva aqui")
