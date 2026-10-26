# Rode: python test_registro.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_registro.py --solucao
import os, sqlite3, sys, tempfile, unittest

if "--solucao" in sys.argv:
    sys.argv.remove("--solucao")
    from solucao.registro import pedir, responder, situacao
else:
    from registro import pedir, responder, situacao
from registro import TABELA

B17 = {"id": "B-17", "resumo": "22409ed4e509dd64", "expira": "17:40"}


class Base(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = os.path.join(self.pasta.name, "aprovacoes.db")
        self.db = self.abrir()

    def abrir(self):
        db = sqlite3.connect(self.arquivo)
        db.execute(TABELA)
        return db

    def tearDown(self):
        self.db.close()
        self.pasta.cleanup()


class GravaAntesDeAvisar(Base):
    def test_quando_o_cartao_sai_o_pedido_ja_esta_no_disco(self):
        vistos = []

        def avisar(pedido):  # outro processo olhando o arquivo na hora do aviso
            outro = sqlite3.connect(self.arquivo)
            vistos.append(outro.execute("SELECT estado FROM pedidos WHERE id = ?", (pedido["id"],)).fetchone())
            outro.close()

        pedir(self.db, B17, avisar)
        self.assertEqual(vistos, [("pendente",)])

    def test_o_aviso_falhou_e_o_pedido_continua_gravado(self):
        def avisar(pedido):
            raise ConnectionError("sem sinal")

        with self.assertRaises(ConnectionError):
            pedir(self.db, B17, avisar)
        self.assertEqual(situacao(self.db, "B-17", "17:11"), "pendente")

    def test_o_pedido_sobrevive_ao_reinicio(self):
        pedir(self.db, B17, lambda p: None)
        self.db.close()  # o servidor caiu
        self.db = self.abrir()  # e voltou
        self.assertEqual(situacao(self.db, "B-17", "17:12"), "pendente")


class PrimeiraRespostaVence(Base):
    def setUp(self):
        super().setUp()
        pedir(self.db, B17, lambda p: None)

    def test_a_primeira_resposta_vale(self):
        self.assertTrue(responder(self.db, "B-17", "supervisora", "recuso", "17:12"))
        self.assertEqual(situacao(self.db, "B-17", "17:13"), "recuso")

    def test_a_segunda_resposta_nao_muda_nada(self):
        responder(self.db, "B-17", "supervisora", "recuso", "17:12")
        self.assertFalse(responder(self.db, "B-17", "despachante", "aprovo", "17:13"))
        self.assertEqual(situacao(self.db, "B-17", "17:40"), "recuso")

    def test_pedido_desconhecido_nao_aceita_resposta(self):
        self.assertFalse(responder(self.db, "B-99", "despachante", "aprovo", "17:12"))
        self.assertEqual(situacao(self.db, "B-99", "17:12"), "desconhecido")


class SilencioNaoEConsentimento(Base):
    def setUp(self):
        super().setUp()
        pedir(self.db, B17, lambda p: None)

    def test_antes_do_prazo_continua_pendente(self):
        self.assertEqual(situacao(self.db, "B-17", "17:39"), "pendente")

    def test_ninguem_respondeu_ate_o_prazo(self):
        self.assertEqual(situacao(self.db, "B-17", "17:40"), "expirado")

    def test_resposta_depois_do_prazo_nao_vale(self):
        self.assertFalse(responder(self.db, "B-17", "despachante", "aprovo", "17:41"))
        self.assertEqual(situacao(self.db, "B-17", "17:41"), "expirado")


if __name__ == "__main__":
    unittest.main(verbosity=2)
