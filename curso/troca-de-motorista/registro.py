# EXERCÍCIO (aula 3): uma aprovação é um registro no disco, não uma espera na memória.
# Escreva as três funções e rode: python test_registro.py
# db é uma conexão sqlite3 (biblioteca padrão). As horas são texto "HH:MM", do mesmo dia: "17:12" < "17:40".

TABELA = """
CREATE TABLE IF NOT EXISTS pedidos (
    id      TEXT PRIMARY KEY,               -- o plano: B-17
    resumo  TEXT NOT NULL,                  -- o resumo do cartão que a pessoa vê (aula 2)
    expira  TEXT NOT NULL,                  -- até quando vale responder: "17:40"
    estado  TEXT NOT NULL DEFAULT 'pendente',  -- pendente, aprovo ou recuso
    quem    TEXT,                           -- quem respondeu
    hora    TEXT                            -- quando respondeu
)"""


def pedir(db, pedido, avisar):
    """1. Grava antes de avisar.

    pedido é {"id": "B-17", "resumo": "...", "expira": "17:40"}. Grave o pedido na tabela (estado pendente), confirme
    a gravação (commit) e só então chame avisar(pedido), que manda o cartão para o celular.
    Se avisar der erro, deixe o erro subir: o pedido continua gravado, e o servidor reenvia quando voltar.
    """
    raise NotImplementedError("escreva aqui")


def responder(db, pedido_id, quem, decisao, agora):
    """2. A primeira resposta vence.

    Grava a decisao ("aprovo" ou "recuso"), quem e a hora, só se o pedido existe, ainda está pendente e agora < expira.
    Devolve True se esta resposta foi gravada e False se não foi (pedido desconhecido, já respondido ou fora do prazo).
    Uma resposta gravada nunca muda.
    """
    raise NotImplementedError("escreva aqui")


def situacao(db, pedido_id, agora):
    """3. Silêncio não é consentimento.

    Devolve "aprovo", "recuso", "pendente", "expirado" (pendente com agora >= expira) ou "desconhecido".
    Só "aprovo" executa.
    """
    raise NotImplementedError("escreva aqui")
