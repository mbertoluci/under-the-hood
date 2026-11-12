# EXERCÍCIO (aula 16): o número vem do servidor.
# O agente não cria nem copia número. Numa escrita, só usa o que o servidor entregou na sessão.
# Rode: python test_ids.py

# O cadastro que só o servidor lê. O MOT-0417 existe, mas é de outra empresa.
MOTORISTAS = {
    "MOT-0102": {"nome": "Carlos Lima", "empresa": "TransNorte"},
    "MOT-0417": {"nome": "Carlos Souza", "empresa": "LogSul"},
}
CARGAS = {"C-9281": {"empresa": "TransNorte", "motorista": "MOT-0031"}}

CAMPOS_COM_NUMERO = ("carga", "motorista")  # os campos de uma troca que levam número


def nova_sessao(empresa="TransNorte"):
    """Pronta: a sessão guarda a empresa e os números que o servidor entregou a ela."""
    return {"empresa": empresa, "entregues": set()}


def ler_carga(sessao, numero):
    """Pronta: consulta do servidor. Só carga da empresa da sessão. Anota o número."""
    carga = CARGAS.get(numero)
    if carga is None or carga["empresa"] != sessao["empresa"]:
        return None
    sessao["entregues"].add(numero)
    return dict(carga)


def buscar_motorista(sessao, nome):
    """Pronta: consulta do servidor. Só motoristas da empresa. Anota cada número."""
    achados = {numero: m["nome"] for numero, m in MOTORISTAS.items()
               if nome.lower() in m["nome"].lower() and m["empresa"] == sessao["empresa"]}
    sessao["entregues"].update(achados)
    return achados


def pode_usar(sessao, args):
    """Os números vieram do servidor, nesta sessão? Devolve (True, "") ou (False, motivo).

    sessao: {"empresa": "TransNorte", "entregues": {"C-9281", "MOT-0102"}}
    args: {"carga": "C-9281", "motorista": "MOT-0102"}  o que o agente passou para a troca
    Para cada campo de CAMPOS_COM_NUMERO:
    1. se o campo não veio em args, recuse, e diga qual campo faltou;
    2. se o número não está em sessao["entregues"], recuse, e ponha o número no motivo.
    Não pergunte ao cadastro. Existir no banco não diz de onde o número veio.
    """
    raise NotImplementedError("escreva aqui")
