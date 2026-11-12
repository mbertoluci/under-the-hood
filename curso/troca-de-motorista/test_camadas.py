# Rode: python test_camadas.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_camadas.py --solucao
import itertools, sys, unittest
from camadas import piso, manual, equipe, perfil_rapido

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.camadas import combinar
else:
    from camadas import combinar

TROCA = {"tipo": "troca", "motorista": "Carlos", "escala": {"Carlos": "livre"}}
AVISO = {"tipo": "aviso", "motorista": "Carlos", "escala": {"Carlos": "livre"}}
FOLGA = {"negado": 0, "pendente": 1, "executavel": 2}  # quanto maior, mais frouxo


def exige_supervisora(acao):
    return {"nega": [], "exige": ["aprovação da Bruna"]}


class Grupo1_AsRespostasSeSomam(unittest.TestCase):
    def test_ninguem_nega_nem_exige(self):
        self.assertEqual(combinar(AVISO, [piso, manual, equipe])["resultado"], "executavel")

    def test_uma_camada_nega(self):
        r = combinar(dict(TROCA, carga_bloqueada=True), [piso, manual, equipe])
        self.assertEqual(r["resultado"], "negado")
        self.assertEqual(r["nega"], ["piso: carga bloqueada"])

    def test_exigencias_se_somam(self):
        r = combinar(TROCA, [manual, exige_supervisora])
        self.assertEqual(r["resultado"], "pendente")
        self.assertEqual(sorted(r["exige"]), ["exige_supervisora: aprovação da Bruna", "manual: aprovação da Joana"])


class Grupo2_NenhumaAfrouxa(unittest.TestCase):
    def test_ninguem_dispensa(self):
        r = combinar(TROCA, [piso, manual, equipe, perfil_rapido])
        self.assertEqual(r["resultado"], "pendente")
        self.assertIn("manual: aprovação da Joana", r["exige"])

    def test_qualquer_ordem_da_o_mesmo(self):
        resultados = {combinar(TROCA, list(ordem))["resultado"]
                      for ordem in itertools.permutations([piso, manual, equipe, perfil_rapido])}
        self.assertEqual(resultados, {"pendente"})

    def test_camada_a_mais_nunca_afrouxa(self):
        todas = [piso, manual, equipe, perfil_rapido, exige_supervisora]
        for acao in (TROCA, AVISO, dict(TROCA, carga_bloqueada=True)):
            for n in range(1, len(todas)):
                for pilha in itertools.combinations(todas, n):
                    antes = combinar(acao, list(pilha))
                    for nova in todas:
                        depois = combinar(acao, list(pilha) + [nova])
                        quem = f"{nova.__name__} afrouxou {[c.__name__ for c in pilha]}"
                        self.assertLessEqual(FOLGA[depois["resultado"]], FOLGA[antes["resultado"]], quem)
                        self.assertLessEqual(set(antes["nega"]), set(depois["nega"]), quem)    # nada do que estava
                        self.assertLessEqual(set(antes["exige"]), set(depois["exige"]), quem)  # negado ou exigido some


class Grupo3_CamadaQueQuebra(unittest.TestCase):
    def test_erro_e_negacao(self):
        sem_escala = {"tipo": "troca", "motorista": "Carlos"}  # a equipe lê a escala, e a escala não veio
        r = combinar(sem_escala, [piso, manual, equipe])
        self.assertEqual(r["resultado"], "negado")
        self.assertTrue(any(motivo.startswith("equipe: ") for motivo in r["nega"]))

    def test_resposta_pela_metade_e_negacao(self):
        def so_nega(acao):
            return {"nega": []}  # esqueceu o "exige"
        self.assertEqual(combinar(AVISO, [piso, so_nega])["resultado"], "negado")

    def test_sem_camada_nega(self):
        self.assertEqual(combinar(AVISO, [])["resultado"], "negado")


class Curto(unittest.TextTestResult):
    """Uma linha por teste, com o grupo na frente: "NenhumaAfrouxa: ninguem_dispensa ... ok"."""
    def getDescription(self, test):
        return f"{type(test).__name__.split('_', 1)[1]}: {test._testMethodName[5:]}"


def rodar(**opcoes):
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2, resultclass=Curto), **opcoes)


if __name__ == "__main__":
    rodar()
