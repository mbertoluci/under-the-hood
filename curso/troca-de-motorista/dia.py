# O dia da despachante (aula 2, dados fictícios): 41 pedidos do replanejador, das 8h às 17h10.
# A maioria é rotina: aviso por template e reserva provisória, que expira sozinha. Três são trocas de motorista.
from operacao import CARGA

CARGAS = {
    "C-9281": dict(CARGA),
    "C-9302": {"id": "C-9302", "item": "carga seca", "entrega": "até 14h", "motorista": "Bruno", "veiculo": "S-14"},
    "C-9310": {"id": "C-9310", "item": "carga refrigerada", "entrega": "até 16h", "motorista": "Paulo", "veiculo": "R-03"},
}

# O catálogo: o que a regra pode fazer sozinha com cada ação.
# 2 = a regra executa e registra (aviso por template, reserva que expira sozinha).
# 1 = uma pessoa aprova antes (muda quem leva a carga). Ação fora do catálogo não tem nível.
NIVEIS = {"send_email": 2, "hold_group": 2, "change_driver": 1}
ACOES = {"send_email": "aviso por template", "hold_group": "reserva provisória", "change_driver": "trocar motorista"}

TROCAS = {
    9: {"id": "P-09", "acao": "change_driver", "carga": "C-9302", "motorista": "Edson"},
    23: {"id": "P-23", "acao": "change_driver", "carga": "C-9310", "motorista": "Rita"},
    41: {"id": "B-17", "acao": "change_driver", "carga": "C-9281", "motorista": "Carlos", "veiculo": "R-12"},
}


def _pedidos():
    pedidos = []
    for n in range(1, 42):
        minutos = 8 * 60 + (n - 1) * 13  # de 8h00 a 16h40, um pedido a cada 13 minutos
        hora = "17:10" if n == 41 else f"{minutos // 60:02d}:{minutos % 60:02d}"
        if n in TROCAS:
            p = dict(TROCAS[n])
        else:
            acao = "hold_group" if n % 3 == 0 else "send_email"
            p = {"id": f"P-{n:02d}", "acao": acao, "carga": ("C-9281", "C-9302", "C-9310")[n % 3]}
        pedidos.append({**p, "hora": hora, "versao": 1})
    return pedidos


PEDIDOS = _pedidos()

# 17:25: o Carlos avisa que não pode. O replanejador atualiza o mesmo plano B-17 para o Diego, no mesmo veículo.
ATUALIZACAO = {**PEDIDOS[-1], "hora": "17:25", "versao": 2, "motorista": "Diego"}


def plano_atual(plano):
    """O plano como está na hora do despacho: o B-17 foi atualizado depois da aprovação."""
    return ATUALIZACAO if plano["id"] == ATUALIZACAO["id"] else plano


def executar(plano):
    carga = CARGAS[plano["carga"]]
    for campo in ("motorista", "veiculo"):
        if campo in plano:
            carga[campo] = plano[campo]
    print(f"  executado: {carga['id']}  motorista {carga['motorista']}, veículo {carga['veiculo']}")


def perguntar(texto):
    import sys
    resposta = input(f"{texto} [s/N] ").strip().lower()
    if not sys.stdin.isatty():
        print(resposta)  # quando a resposta vem de um pipe (yes s | ...), mostra o que foi respondido
    return resposta == "s"
