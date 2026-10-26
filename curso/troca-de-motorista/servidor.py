# O servidor de aprovações (aula 3). Lê um comando por linha e responde uma linha por comando.
# Uso: python servidor.py [--memoria] [--solucao]     (quem conversa com ele é o reinicio.py)
#   subir HH:MM | pedir HH:MM | responder HH:MM quem aprovo|recuso | despachar HH:MM
# --memoria: o jeito ingênuo, a espera num dicionário na memória do processo.
# sem --memoria: o registro no disco (aprovacoes.db), com o seu registro.py ou, com --solucao, o da solução.
import sqlite3, sys

from dia import CARGAS, PEDIDOS, executar
from operacao import resumo
from solucao.aprovacao import cartao

if "--solucao" in sys.argv:
    from solucao.registro import pedir, responder, situacao
else:
    from registro import pedir, responder, situacao
from registro import TABELA

B17 = PEDIDOS[-1]
CARTAO = cartao(B17, CARGAS[B17["carga"]])
PEDIDO = {"id": B17["id"], "resumo": resumo(CARTAO), "expira": "17:40"}


def avisar(pedido):
    pass  # aqui o cartão sairia para o celular da despachante e da supervisora


class Memoria:
    def __init__(self):
        self.esperando = {}  # id do pedido -> decisão; vive só enquanto o processo vive

    def subir(self, hora):
        return f"{hora} servidor no ar: memória vazia"

    def pedir(self, hora):
        self.esperando[PEDIDO["id"]] = None
        avisar(PEDIDO)
        return f"{hora} cartão enviado: {PEDIDO['id']}, esperando a resposta na memória"

    def responder(self, hora, quem, decisao):
        if PEDIDO["id"] not in self.esperando:
            return f"{hora} {quem}: {decisao} no {PEDIDO['id']}? pedido desconhecido, resposta ignorada"
        self.esperando[PEDIDO["id"]] = decisao
        return f"{hora} {quem}: {decisao} no {PEDIDO['id']}, guardado na memória"

    def despachar(self, hora):
        if self.esperando.get(PEDIDO["id"]) == "aprovo":
            executar(B17)
            return f"{hora} despacho: {PEDIDO['id']} executado"
        return f"{hora} despacho: nada aprovado na memória, nada a fazer"


class Disco:
    def __init__(self):
        self.db = sqlite3.connect("aprovacoes.db")
        self.db.execute(TABELA)

    def subir(self, hora):
        pendentes = [i for (i,) in self.db.execute("SELECT id FROM pedidos WHERE estado = 'pendente' AND ? < expira", (hora,))]
        for i in pendentes:
            avisar({"id": i})
        if not pendentes:
            return f"{hora} servidor no ar: nenhum pedido pendente no disco"
        return f"{hora} servidor no ar: {', '.join(pendentes)} pendente no disco, cartão reenviado"

    def pedir(self, hora):
        pedir(self.db, PEDIDO, avisar)
        return f"{hora} {PEDIDO['id']} gravado no disco, pendente até {PEDIDO['expira']}; cartão enviado"

    def responder(self, hora, quem, decisao):
        if responder(self.db, PEDIDO["id"], quem, decisao, hora):
            return f"{hora} {quem}: {decisao} no {PEDIDO['id']}, gravado"
        linha = self.db.execute("SELECT estado, quem, hora FROM pedidos WHERE id = ?", (PEDIDO["id"],)).fetchone()
        if linha and linha[0] != "pendente":
            return f"{hora} {quem}: {decisao} no {PEDIDO['id']}, não gravado: já está {linha[0]} ({linha[1]}, {linha[2]})"
        return f"{hora} {quem}: {decisao} no {PEDIDO['id']}, não gravado: {situacao(self.db, PEDIDO['id'], hora)}"

    def despachar(self, hora):
        estado = situacao(self.db, PEDIDO["id"], hora)
        if estado == "aprovo" and self.db.execute("SELECT resumo FROM pedidos WHERE id = ?", (PEDIDO["id"],)).fetchone()[0] == resumo(CARTAO):
            executar(B17)
            return f"{hora} despacho: {PEDIDO['id']} executado"
        if estado == "expirado":
            return f"{hora} despacho: {PEDIDO['id']} expirou sem resposta, não executa e avisa a supervisora"
        return f"{hora} despacho: {PEDIDO['id']} está {estado}, não executa"


servidor = Memoria() if "--memoria" in sys.argv else Disco()
for linha in sys.stdin:
    comando, hora, *resto = linha.split()
    print(getattr(servidor, comando)(hora, *resto), flush=True)
