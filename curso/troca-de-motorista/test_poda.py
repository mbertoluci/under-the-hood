# Rode: python test_poda.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_poda.py --solucao
import sys, unittest
from poda import TRAVAS, CASOS, origem, teto, juiz, aprovacao

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.poda import pode_tirar
else:
    from poda import pode_tirar


def segunda_conferencia_de_origem(caso):
    """Uma cópia da trava de origem, posta por outra equipe."""
    return caso["numero_veio_de"] != "servidor"


def quebrada(caso):
    return caso["campo_que_nao_existe"]


class Grupo1_QuandoPodeTirar(unittest.TestCase):
    def test_copia_de_outra_trava_pode_sair(self):
        pilha = TRAVAS + [segunda_conferencia_de_origem]
        self.assertEqual(pode_tirar(segunda_conferencia_de_origem, pilha, CASOS), (True, []))

    def test_com_a_copia_na_pilha_a_original_pode_sair(self):
        pilha = TRAVAS + [segunda_conferencia_de_origem]
        self.assertEqual(pode_tirar(origem, pilha, CASOS), (True, []))

    def test_juiz_pode_sair_com_estes_casos(self):
        self.assertEqual(pode_tirar(juiz, TRAVAS, CASOS), (True, []))  # o SMS da Maria também para na aprovação


class Grupo2_AUnicaQueSegura(unittest.TestCase):
    def test_aprovacao_nao_pode_sair(self):
        self.assertEqual(pode_tirar(aprovacao, TRAVAS, CASOS), (False, ["troca normal, que ninguém aprovou"]))

    def test_origem_nao_pode_sair(self):
        self.assertEqual(pode_tirar(origem, TRAVAS, CASOS), (False, ["número colado de um e-mail"]))

    def test_teto_nao_pode_sair(self):
        self.assertEqual(pode_tirar(teto, TRAVAS, CASOS), (False, ["terceira troca da carga"]))


class Grupo3_OQueNaoEProva(unittest.TestCase):
    def test_sem_caso_nao_pode(self):
        self.assertEqual(pode_tirar(juiz, TRAVAS, {}), (False, []))

    def test_trava_que_nem_esta_na_pilha(self):
        self.assertEqual(pode_tirar(segunda_conferencia_de_origem, TRAVAS, CASOS), (False, []))

    def test_trava_quebrada_nao_segura(self):
        pilha = [origem, teto, quebrada, aprovacao]  # a quebrada dá erro em todo caso
        self.assertEqual(pode_tirar(aprovacao, pilha, CASOS)[0], False)


class Curto(unittest.TextTestResult):
    """Uma linha por teste, com o grupo na frente: "AUnicaQueSegura: teto_nao_pode_sair ... ok"."""
    def getDescription(self, test):
        return f"{type(test).__name__.split('_', 1)[1]}: {test._testMethodName[5:]}"


def rodar(**opcoes):
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2, resultclass=Curto), **opcoes)


if __name__ == "__main__":
    rodar()
