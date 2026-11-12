# Solução da aula 10.
from descida import janela
from evidencia import limite


def deve_descer(decisoes, risco, incidente=False, tamanho=None):
    if incidente:
        return True
    auditadas = [d for d in decisoes if d["auditada"]][-(tamanho or janela(risco)):]
    erros = sum(1 for d in auditadas if d["erro"])
    return erros > 0 and limite(erros, len(auditadas)) > 2 * risco
