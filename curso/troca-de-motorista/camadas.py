# EXERCÍCIO (aula 17): camadas que só apertam.
# Cada camada de política diz o que nega e o que exige. Juntar camadas só mantém ou aperta.
# Rode: python test_camadas.py


def piso(acao):
    """Pronta: o piso da plataforma. Vale para todo cliente."""
    bloqueada = acao.get("carga_bloqueada")
    return {"nega": ["carga bloqueada"] if bloqueada else [], "exige": []}


def manual(acao):
    """Pronta: o manual do cliente XPTO. Troca de motorista exige a aprovação da Joana."""
    troca = acao["tipo"] == "troca"
    return {"nega": [], "exige": ["aprovação da Joana"] if troca else []}


def equipe(acao):
    """Pronta: a regra da equipe de despacho. Lê a escala; se a escala não veio, dá erro."""
    livre = acao["escala"][acao["motorista"]] == "livre"
    return {"nega": [] if livre else ["motorista ocupado"], "exige": []}


def perfil_rapido(acao):
    """Pronta: o perfil "rápido" do subagente. Não nega, não exige, e tenta dispensar."""
    return {"nega": [], "exige": [], "dispensa": ["aprovação da Joana"]}


def combinar(acao, camadas):
    """Junta a resposta de todas as camadas, numa decisão só.

    acao: {"tipo": "troca", "motorista": "Carlos", "escala": {"Carlos": "livre"}}
    camadas: lista de funções, como [piso, manual, equipe]
    Devolve {"resultado": "negado" | "pendente" | "executavel",
             "nega": ["piso: carga bloqueada"], "exige": ["manual: aprovação da Joana"]}.
    Como juntar:
    1. chame cada camada, e ponha o nome dela na frente de cada item que ela devolver:
       "piso: carga bloqueada", "manual: aprovação da Joana" (o nome é camada.__name__);
    2. se a camada der erro, ou a resposta não tiver "nega" e "exige", isso é uma negação:
       "equipe: a camada falhou (KeyError)";
    3. as negações se somam, e as exigências se somam. Ninguém tira o que outra pôs;
    4. sem camada nenhuma, a negação é "nenhuma camada respondeu";
    5. tem negação: "negado". Só exigência: "pendente". Nenhuma das duas: "executavel".
    """
    raise NotImplementedError("escreva aqui")
