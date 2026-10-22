# A operação do case da transportadora (dados fictícios): uma carga refrigerada, o motorista que não pode
# e o plano B. E o cadastro de canais: cada canal verificado (com código, no cadastro) aponta para uma pessoa.
CARGA = {"id": "C-9281", "item": "carga refrigerada", "entrega": "até 11h", "motorista": "Anderson", "veiculo": "V-07"}

# A proposta B do replanejador: troca o motorista para cumprir a entrega.
PROPOSTA = {"id": "B-17", "acao": "change_driver", "carga": "C-9281", "motorista": "Carlos", "veiculo": "R-12"}

# Quem é quem. Só a solicitante pode autorizar troca de motorista (manual da XPTO).
PAPEIS = {"maria": "solicitante", "anderson": "motorista", "carlos": "motorista"}

# Canais verificados: (canal, origem) -> pessoa.
CANAIS = {
    ("sms", "+55 11 98888-0001"): "maria",
    ("app", "maria-xpto"): "maria",
    ("sms", "+55 11 97777-0002"): "anderson",
    ("app", "anderson-frota"): "anderson",
}


def trocar_motorista(proposta):
    CARGA["motorista"] = proposta["motorista"]
    CARGA["veiculo"] = proposta["veiculo"]


def mostrar():
    print(f"  {CARGA['id']}  {CARGA['item']}  entrega {CARGA['entrega']}  motorista: {CARGA['motorista']} ({CARGA['veiculo']})")
