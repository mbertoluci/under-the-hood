# EXERCÍCIO (aula 10): a ação desce um degrau quando o limite de cima, nas últimas decisões auditadas,
# passa do dobro do risco tolerado. Escreva deve_descer e rode: python test_descida.py
import math
from evidencia import limite


def janela(risco, por_semana=30):
    """Quantas auditadas a janela guarda: o menor n com zero erros abaixo de 2 x risco,
    em semanas inteiras de 30 auditadas. Para 1%, 149 vira 150. Vem pronta."""
    n = math.floor(math.log(0.05) / math.log(1 - 2 * risco)) + 1
    return math.ceil(n / por_semana) * por_semana


def deve_descer(decisoes, risco, incidente=False, tamanho=None):
    """Diz se a ação desce um degrau: True ou False.

    decisoes: todas as decisões da ação, da mais antiga à mais nova:
              {"auditada": True/False, "erro": True/False, ou None se ninguém auditou}.
    tamanho:  quantas auditadas a janela guarda; se não vier, janela(risco).
    1. Incidente grave reportado: desce na hora, sem conta.
    2. O denominador são as auditadas, nunca o total. Use só as últimas `tamanho` auditadas.
    3. Desce se limite(erros, auditadas) passar de 2 x risco. Zero erros nunca derruba:
       janela curta é falta de prova, não prova de erro.
    """
    raise NotImplementedError("escreva aqui")
