# Rode: python test_descida.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_descida.py --solucao
import sys, unittest

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.descida import deve_descer
else:
    from descida import deve_descer


def decisoes(auditadas, erros=0, outras=0):
    """outras: decisões que ninguém auditou (vêm antes); erros: as auditadas mais recentes."""
    out = [{"auditada": False, "erro": None} for _ in range(outras)]
    return out + [{"auditada": True, "erro": i >= auditadas - erros} for i in range(auditadas)]


class NaHora(unittest.TestCase):
    def test_incidente_desce_na_hora(self):
        self.assertTrue(deve_descer(decisoes(150), 0.01, incidente=True))

    def test_janela_cheia_sem_erro_fica(self):
        self.assertFalse(deve_descer(decisoes(150), 0.01))                  # 1,98%, abaixo de 2%

    def test_um_erro_na_janela_desce(self):
        self.assertTrue(deve_descer(decisoes(150, erros=1), 0.01))          # 3,12%, acima de 2%


class ODenominador(unittest.TestCase):
    def test_um_erro_em_150_auditadas_de_5000(self):
        self.assertTrue(deve_descer(decisoes(150, erros=1, outras=4850), 0.01))   # n = 150, não 5.000

    def test_dois_erros_em_30_auditadas_de_2000(self):
        self.assertTrue(deve_descer(decisoes(30, erros=2, outras=1970), 0.01))    # 2 em 30, não 2 em 2.000


class AJanela(unittest.TestCase):
    def test_zero_erros_em_30_fica(self):
        self.assertFalse(deve_descer(decisoes(30), 0.01))       # limite de 9,5%, mas nenhum erro visto

    def test_um_erro_em_30_desce(self):
        self.assertTrue(deve_descer(decisoes(30, erros=1), 0.01))

    def test_erro_antigo_sai_da_janela(self):
        antigo = [{"auditada": True, "erro": True}]
        self.assertFalse(deve_descer(antigo + decisoes(150), 0.01))         # as últimas 150 estão limpas

    def test_risco_de_meio_por_cento(self):
        self.assertTrue(deve_descer(decisoes(300, erros=1), 0.005))         # 1,57%, acima de 1%


if __name__ == "__main__":
    unittest.main(verbosity=2)
