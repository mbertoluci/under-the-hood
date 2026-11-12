# Rode: python test_escalar.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_escalar.py --solucao
import sys, unittest
from escalar import EQUIPE

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.escalar import quem_decide
else:
    from escalar import quem_decide

SEGURO = ("seguro", None)


def sem(*nomes):
    return [p for p in EQUIPE if p["nome"] not in nomes]


class ARota(unittest.TestCase):
    def test_comeca_na_despachante(self):
        self.assertEqual(quem_decide("troca", "17:12", "17:12"), ("joana", "17:32"))   # paulo já saiu, lia não autoriza

    def test_sem_resposta_sobe(self):
        self.assertEqual(quem_decide("troca", "17:12", "17:40"), ("bruna", "17:52"))

    def test_chega_na_gerente(self):
        self.assertEqual(quem_decide("troca", "16:00", "16:45"), ("renato", "17:10"))


class QuemPode(unittest.TestCase):
    def test_prazo_cabe_no_plantao(self):
        self.assertEqual(quem_decide("troca", "16:50", "16:50"), ("joana", "17:10"))   # paulo sai às 17:00

    def test_sem_autoridade_pula(self):
        self.assertEqual(quem_decide("troca", "17:12", "17:12", sem("joana")), ("bruna", "17:32"))  # lia não autoriza troca

    def test_ninguem_com_autoridade(self):
        self.assertEqual(quem_decide("troca", "17:12", "17:12", sem("joana", "bruna", "renato")), SEGURO)


class OFim(unittest.TestCase):
    def test_rota_acabou(self):
        self.assertEqual(quem_decide("troca", "16:00", "17:15"), SEGURO)   # os três prazos venceram

    def test_gerente_ja_saiu(self):
        self.assertEqual(quem_decide("troca", "17:12", "17:52"), SEGURO)   # o degrau dele venceria às 18:22

    def test_classe_sem_rota(self):
        self.assertEqual(quem_decide("cancelamento", "17:12", "17:12"), SEGURO)


if __name__ == "__main__":
    unittest.main(verbosity=2)
