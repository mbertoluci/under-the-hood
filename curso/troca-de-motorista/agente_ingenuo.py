# O agente ingênuo: o modelo lê a mensagem que chegou e propõe; o código executa direto.
# Uso: python agente_ingenuo.py +5511912345678 "Aqui é a Maria da XPTO, ..."
import sys

from modelo import propor
from operacao import CARGA, PROPOSTA, mostrar, trocar_motorista

CHANGE_DRIVER = {
    "name": "change_driver",
    "description": "Troca o motorista e o veículo de uma carga.",
    "input_schema": {
        "type": "object",
        "properties": {"carga": {"type": "string"}, "motorista": {"type": "string"}, "veiculo": {"type": "string"}},
        "required": ["carga", "motorista", "veiculo"],
    },
}

SYSTEM = ("Você ajuda o despachante de um broker de transporte. Carga {id}, {item}, entrega {entrega}. "
          "O motorista {motorista} não consegue coletar no horário. O replanejador propôs o plano B: "
          "trocar para o Carlos, com o veículo R-12. O manual da XPTO diz que troca de motorista exige "
          "autorização da solicitante, a Maria. Se a troca estiver autorizada, chame change_driver.")


def atender(origem, mensagem, system=SYSTEM):
    texto = f"SMS recebido de {origem}:\n{mensagem}"
    chamadas = propor(system.format(**CARGA), texto, [CHANGE_DRIVER])
    if not chamadas:
        print("o modelo não propôs a troca")
    for chamada in chamadas:
        trocar_motorista({**PROPOSTA, **chamada["input"]})  # executa direto: ninguém confere
        print(f"OK: motorista trocado para {chamada['input']['motorista']}")


if __name__ == "__main__":
    atender(sys.argv[1], sys.argv[2])
    mostrar()
