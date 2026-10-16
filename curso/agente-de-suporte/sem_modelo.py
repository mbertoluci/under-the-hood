# A mesma triagem, sem modelo: procura a palavra "cancel" e um número de pedido no formato A101.
# Uso: python sem_modelo.py "Cancela o pedido A101, por favor."
import re
import sys

NUMERO = re.compile(r"\b([A-Z]\d{3})\b", re.IGNORECASE)


def propor_sem_modelo(mensagem):
    if "cancel" not in mensagem.lower():
        return None
    achado = NUMERO.search(mensagem)
    return achado.group(1).upper() if achado else None


if __name__ == "__main__":
    print(propor_sem_modelo(sys.argv[1]))
