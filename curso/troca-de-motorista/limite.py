# EXERCÍCIO (aula 14): o limite sobre o total.
# Cada aviso cabe na regra. Cem avisos na mesma hora, não. O teto vale sobre o total depois desta ação.
# Rode: python test_limite.py
from datetime import datetime

# O teto de cada classe, por chave (a carga ou o cliente). "janela" em minutos; None: desde sempre.
# Classe sem teto escrito não cabe.
TETOS = {
    "troca": {"teto": 2, "janela": None},   # 2 trocas de motorista por carga
    "aviso": {"teto": 20, "janela": 60},    # 20 avisos por cliente em 60 minutos
}


def minutos(antes, depois):
    """Pronta: quantos minutos de "2026-10-20 10:00" até "2026-10-20 10:45" (45)."""
    f = "%Y-%m-%d %H:%M"
    return (datetime.strptime(depois, f) - datetime.strptime(antes, f)).total_seconds() / 60


def cabe(acao, registro, agora, tetos=TETOS):
    """True se, contando esta ação, o total ainda fica dentro do teto.

    acao: {"classe": "aviso", "chave": "XPTO"}
    registro: [{"classe": "aviso", "chave": "XPTO", "quando": "2026-10-20 10:00", "estado": "feita"}]
              estado: "feita", "pendente" (já saiu e ainda não terminou) ou "cancelada"
    agora: "2026-10-20 10:05"
    Como contar:
    1. a classe tem teto em tetos. Sem teto, não cabe;
    2. conte no registro as da mesma classe e da mesma chave, feitas ou pendentes. Cancelada não conta;
    3. se o teto tem janela, só as dos últimos N minutos;
    4. cabe se essa conta, mais esta ação, não passa do teto.
    """
    raise NotImplementedError("escreva aqui")


def pedir(acao, registro, agora, cabe=cabe):
    """Pronta: confere e reserva num passo só. Se cabe, a ação entra no registro como pendente."""
    if not cabe(acao, registro, agora):
        return False
    registro.append({"classe": acao["classe"], "chave": acao["chave"], "quando": agora, "estado": "pendente"})
    return True
