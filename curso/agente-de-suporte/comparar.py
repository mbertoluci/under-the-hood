# Compara a triagem sem modelo (sem_modelo.py) com a do modelo, nas mesmas mensagens da Ana.
# Uso: python comparar.py 5   (5 rodadas do modelo por mensagem; sem chave de API, só a coluna sem modelo)
import os
import sys
import time

from agente_ingenuo import CANCEL_ORDER
from modelo import propor
from sem_modelo import propor_sem_modelo

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5

# Os pedidos entram no prompt só para o modelo entender a mensagem. Quem decide continua sendo a regra (aula 9).
SYSTEM = ("Você é o suporte da loja. Cliente logado: ana. Pedidos dela: A101 (fone sem fio), C303 (cadeira). "
          "Se ela pedir para cancelar um pedido, chame cancel_order. Se não pedir, não chame.")

CASOS = [  # (mensagem, o pedido que ela quer cancelar, ou None)
    ("Cancela o pedido A101, por favor.", "A101"),
    ("quero cancelar o a101", "A101"),
    ("Qual o prazo de entrega do A101?", None),
    ("Quero cancelar o fone que eu comprei.", "A101"),
    ("Não quero mais o fone sem fio, pode cancelar?", "A101"),
    ("Não cancela o A101, mudei de ideia.", None),
    ("Cancela o pedido A 101.", "A101"),
    ("Desisti da cadeira, cancela pra mim.", "C303"),
]


def pelo_modelo(mensagem):
    chamadas = propor(SYSTEM, mensagem, [CANCEL_ORDER])
    return chamadas[0]["input"]["order_id"] if chamadas else None


com_chave = bool(os.environ.get("ANTHROPIC_API_KEY"))
placar_regra = placar_modelo = 0
tempo_regra = tempo_modelo = 0.0
for mensagem, quer in CASOS:
    t0 = time.perf_counter()
    regra = propor_sem_modelo(mensagem)
    tempo_regra += time.perf_counter() - t0
    placar_regra += regra == quer
    linha = f"{mensagem:<47} {str(quer):<5} sem modelo: {'certo ' if regra == quer else 'errado'}"
    if com_chave:
        acertos = 0
        for _ in range(N):
            t0 = time.perf_counter()
            acertos += pelo_modelo(mensagem) == quer
            tempo_modelo += time.perf_counter() - t0
        placar_modelo += acertos
        linha += f"   modelo: {acertos} de {N}"
    print(linha)

print(f"\nsem modelo: {placar_regra} de {len(CASOS)} certas, {tempo_regra / len(CASOS) * 1000:.3f} ms por mensagem")
if com_chave:
    print(f"modelo:     {placar_modelo} de {len(CASOS) * N} certas, {tempo_modelo / (len(CASOS) * N):.2f} s por chamada")
else:
    print("modelo: precisa de chave de API (ANTHROPIC_API_KEY)")
