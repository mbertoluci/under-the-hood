# SOLUÇÃO (aula 3): uma aprovação é um registro no disco, não uma espera na memória.
from registro import TABELA  # noqa: F401  (a tabela é a mesma do exercício)


def pedir(db, pedido, avisar):
    # 1. Grava antes de avisar. Se cair depois de gravar, o pedido está lá para reenviar.
    db.execute("INSERT INTO pedidos (id, resumo, expira) VALUES (?, ?, ?)",
               (pedido["id"], pedido["resumo"], pedido["expira"]))
    db.commit()
    avisar(pedido)


def responder(db, pedido_id, quem, decisao, agora):
    # 2. A primeira resposta vence: a condição fica no próprio UPDATE.
    cur = db.execute("UPDATE pedidos SET estado = ?, quem = ?, hora = ? "
                     "WHERE id = ? AND estado = 'pendente' AND ? < expira",
                     (decisao, quem, agora, pedido_id, agora))
    db.commit()
    return cur.rowcount == 1


def situacao(db, pedido_id, agora):
    # 3. Silêncio não é consentimento: pendente fora do prazo é expirado.
    linha = db.execute("SELECT estado, expira FROM pedidos WHERE id = ?", (pedido_id,)).fetchone()
    if linha is None:
        return "desconhecido"
    estado, expira = linha
    if estado == "pendente" and agora >= expira:
        return "expirado"
    return estado
