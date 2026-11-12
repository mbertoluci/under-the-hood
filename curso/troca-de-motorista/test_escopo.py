# Rode: python test_escopo.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_escopo.py --solucao
import sys, unittest
from escopo import TAREFA

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.escopo import decidir
else:
    from escopo import decidir

AVISAR = {"acao": "avisar_cliente", "alvo": "C-9300"}
FORMULARIO = {"acao": "enviar_formulario", "alvo": "C-9300"}
OUTRA_CARGA = {"acao": "avisar_cliente", "alvo": "C-9301"}


class Grupo1_OQueEstaDentro(unittest.TestCase):
    def test_acao_e_alvo_da_lista_executa(self):
        self.assertEqual(decidir(TAREFA, AVISAR, []), "executa")

    def test_acao_fora_nega(self):
        self.assertEqual(decidir(TAREFA, FORMULARIO, []), "nega")

    def test_alvo_fora_nega(self):
        self.assertEqual(decidir(TAREFA, OUTRA_CARGA, []), "nega")


class Grupo2_AListaEDoQuePode(unittest.TestCase):
    def test_tarefa_so_com_proibicoes_nega(self):
        so_proibicoes = {"alvos": {"C-9281", "C-9300"}, "proibido": {"trocar_motorista", "descartar"}}
        self.assertEqual(decidir(so_proibicoes, AVISAR, []), "nega")

    def test_nome_parecido_nega(self):
        self.assertEqual(decidir(TAREFA, {"acao": "avisar_cliente_por_sms", "alvo": "C-9300"}, []), "nega")

    def test_chamada_sem_alvo_nega(self):
        self.assertEqual(decidir(TAREFA, {"acao": "avisar_cliente"}, []), "nega")


class Grupo3_AHoraDeParar(unittest.TestCase):
    def test_terceira_negacao_seguida_para(self):
        self.assertEqual(decidir(TAREFA, OUTRA_CARGA, ["executa", "nega", "nega"]), "para")

    def test_executa_no_meio_zera_a_conta(self):
        self.assertEqual(decidir(TAREFA, OUTRA_CARGA, ["nega", "nega", "executa", "nega"]), "nega")

    def test_depois_de_parar_continua_parada(self):
        self.assertEqual(decidir(TAREFA, AVISAR, ["nega", "nega", "para"]), "para")


class Curto(unittest.TextTestResult):
    """Uma linha por teste, com o grupo na frente: "AHoraDeParar: terceira_negacao_seguida_para ... ok"."""
    def getDescription(self, test):
        return f"{type(test).__name__.split('_', 1)[1]}: {test._testMethodName[5:]}"


def rodar(**opcoes):
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2, resultclass=Curto), **opcoes)


if __name__ == "__main__":
    rodar()
