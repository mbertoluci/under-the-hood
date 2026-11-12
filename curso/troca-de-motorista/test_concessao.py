# Rode: python test_concessao.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_concessao.py --solucao
import sys, unittest

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.concessao import por_concessao
else:
    from concessao import por_concessao

C1 = {"id": "C-1", "quem": "joana", "classe": "aviso", "ferramenta": "avisar_cliente",
      "argumentos": {"template": "atraso"}, "expira": "2026-10-17 18:00", "revogada": False}
AVISO = {"classe": "aviso", "ferramenta": "avisar_cliente", "argumentos": {"template": "atraso", "cliente": "XPTO"}}
TROCA = {"classe": "troca", "ferramenta": "trocar_motorista", "argumentos": {"carga": "C-9281", "motorista": "Carlos"}}
TERCA = "2026-10-14 10:00"


def com(**mudancas):
    return dict(C1, **mudancas)


class OEscopo(unittest.TestCase):
    def test_dentro_do_escopo(self):
        self.assertEqual(por_concessao(AVISO, [C1], TERCA), "C-1")

    def test_outro_template(self):
        desconto = dict(AVISO, argumentos={"template": "desconto", "cliente": "XPTO"})
        self.assertIsNone(por_concessao(desconto, [C1], TERCA))

    def test_asterisco_e_texto(self):
        reembolso = dict(AVISO, argumentos={"template": "atraso_com_reembolso", "cliente": "XPTO"})
        self.assertIsNone(por_concessao(reembolso, [com(argumentos={"template": "atraso*"})], TERCA))


class OPrazo(unittest.TestCase):
    def test_um_minuto_antes(self):
        self.assertEqual(por_concessao(AVISO, [C1], "2026-10-17 17:59"), "C-1")

    def test_expirada(self):
        self.assertIsNone(por_concessao(AVISO, [C1], "2026-10-17 18:00"))

    def test_revogada(self):
        self.assertIsNone(por_concessao(AVISO, [com(revogada=True)], TERCA))


class QuemEOQue(unittest.TestCase):
    def test_troca_nunca_por_concessao(self):
        sempre_troca = com(classe="troca", ferramenta="trocar_motorista", argumentos={})
        self.assertIsNone(por_concessao(TROCA, [sempre_troca], TERCA))

    def test_agente_nao_concede(self):
        self.assertIsNone(por_concessao(AVISO, [com(quem="agente")], TERCA))

    def test_quem_nao_autoriza(self):
        self.assertIsNone(por_concessao(AVISO, [com(quem="lia")], TERCA))   # lia está em treino


if __name__ == "__main__":
    unittest.main(verbosity=2)
