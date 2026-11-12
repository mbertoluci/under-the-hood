# Rode: python test_limite.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_limite.py --solucao
import sys, unittest

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.limite import cabe, pedir
else:
    from limite import cabe, pedir

TROCA = {"classe": "troca", "chave": "C-9281"}
AVISO = {"classe": "aviso", "chave": "XPTO"}
DEZ = "2026-10-20 10:00"


def ja(acao, n, quando=DEZ, estado="feita"):
    return [dict(acao, quando=quando, estado=estado) for _ in range(n)]


class OTotal(unittest.TestCase):
    def test_abaixo_do_teto_cabe(self):
        self.assertTrue(cabe(TROCA, ja(TROCA, 1), DEZ))

    def test_no_teto_nao_cabe(self):
        self.assertFalse(cabe(TROCA, ja(TROCA, 2), DEZ))

    def test_outra_carga_nao_conta(self):
        self.assertTrue(cabe(TROCA, ja({"classe": "troca", "chave": "C-1111"}, 2), DEZ))

    def test_classe_sem_teto_nao_cabe(self):
        self.assertFalse(cabe({"classe": "descarte", "chave": "D-03"}, [], DEZ))


class AJanela(unittest.TestCase):
    def test_vinte_na_hora_nao_cabe(self):
        self.assertFalse(cabe(AVISO, ja(AVISO, 20), "2026-10-20 10:59"))

    def test_uma_hora_depois_cabe(self):
        self.assertTrue(cabe(AVISO, ja(AVISO, 20), "2026-10-20 11:00"))


class OQueEstaEmAndamento(unittest.TestCase):
    def test_pendente_conta(self):
        self.assertFalse(cabe(TROCA, ja(TROCA, 1) + ja(TROCA, 1, estado="pendente"), DEZ))

    def test_cancelada_nao_conta(self):
        self.assertTrue(cabe(TROCA, ja(TROCA, 1) + ja(TROCA, 1, estado="cancelada"), DEZ))

    def test_dois_pedidos_juntos(self):
        registro = ja(TROCA, 1)                      # uma troca feita, teto 2
        self.assertTrue(pedir(TROCA, registro, DEZ))
        self.assertFalse(pedir(TROCA, registro, DEZ))   # a segunda, no mesmo turno, não cabe


if __name__ == "__main__":
    unittest.main(verbosity=2)
