# EXERCÍCIO (aula 4): na hora do efeito, pergunte de novo.
# Escreva pode_executar e rode: python test_revalidar.py
from operacao import resumo


def conteudo(plano):
    """O texto que a Maria viu no botão (pronto). A autorização guarda o resumo dele (aula 2)."""
    p = plano
    return f"{p['id']}: {p['carga']}, motorista {p['motorista']}, veiculo {p['veiculo']}"


def pode_executar(autorizacao, plano, agora):
    """Às 17:40, antes de trocar o motorista. Devolve (True, "") ou (False, motivo).

    autorizacao é a linha gravada quando a Maria apertou o botão:
        {"plano": "B-17", "quem": "maria", "papel": "solicitante",
         "resumo": "...", "hora": "17:00"}
    plano é o plano de agora. agora é o mundo de agora:
        {"papeis": {"maria": "solicitante", ...},            o cadastro da XPTO
         "cargas": {"C-9281": "aguardando motorista", ...},  a situação de cada carga
         "escalas": {"Carlos": None, ...}}                   em que carga está (None: livre)

    1. O conteúdo é o que ela viu? O resumo de conteudo(plano) é igual ao gravado.
    2. Quem autorizou ainda pode autorizar? O papel dessa pessoa no cadastro de agora é "solicitante".
    3. O mundo ainda é o que era? A carga ainda está "aguardando motorista", e o motorista está livre ou já está
       nesta mesma carga.
    """
    raise NotImplementedError("escreva aqui")
