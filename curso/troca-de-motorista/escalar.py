# EXERCÍCIO (aula 11): o caminho até a pessoa certa.
# Quando uma ação precisa de uma pessoa (aula 8) ou desceu de nível (aula 10),
# a decisão anda por uma rota escrita.
# As horas são texto "HH:MM", do mesmo dia. Rode: python test_escalar.py

# A rota de cada classe de ação: quem decide, em ordem, e quantos minutos cada um tem.
ROTA = {
    "troca": [("despachante", 20), ("supervisora", 20), ("gerente", 30)],
}

# A equipe: papel, plantão e o que cada um pode autorizar. Vem do cadastro, nunca do cartão.
# A lia está em treino: ainda não autoriza nada.
EQUIPE = [
    {"nome": "paulo", "papel": "despachante", "plantao": ("06:00", "17:00"), "autoriza": ["troca"]},
    {"nome": "lia", "papel": "despachante", "plantao": ("12:00", "22:00"), "autoriza": []},
    {"nome": "joana", "papel": "despachante", "plantao": ("14:00", "22:00"), "autoriza": ["troca"]},
    {"nome": "bruna", "papel": "supervisora", "plantao": ("08:00", "20:00"), "autoriza": ["troca"]},
    {"nome": "renato", "papel": "gerente", "plantao": ("08:00", "18:00"), "autoriza": ["troca"]},
]


def minutos(hora):
    h, m = hora.split(":")
    return int(h) * 60 + int(m)


def hora(minutos):
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


def quem_decide(classe, inicio, agora, equipe=EQUIPE, rota=ROTA):
    """Para quem vai o cartão agora, e até quando. Devolve (nome, "HH:MM") ou ("seguro", None).

    1. Siga a rota da classe em ordem, a partir de inicio. Cada degrau tem o seu prazo.
    2. A pessoa do degrau é a primeira da equipe com aquele papel, que autoriza a classe
       e está de plantão do começo ao fim do prazo.
       Degrau sem ninguém assim passa direto, sem gastar tempo.
    3. Classe sem rota, ou rota que acabou: "seguro". Nada executa, a pendência fica
       registrada e a equipe é avisada. Nunca deixe o cartão com quem teve o prazo vencido.
    """
    raise NotImplementedError("escreva aqui")
