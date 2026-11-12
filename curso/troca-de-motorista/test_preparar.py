# Rode: python test_preparar.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_preparar.py --solucao
import sys, unittest
from preparar import preparar, aprovar

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.preparar import aplicar
else:
    from preparar import aplicar


def servidor(trocas=0):
    return {"seq": 0, "mudancas": {}, "cargas": {"C-9281": {"motorista": "Anderson", "trocas": trocas}}}


def preparada(s, aprovada_por="Joana"):
    mid = preparar(s, "C-9281", "Carlos")
    if aprovada_por:
        aprovar(s, mid, aprovada_por)
    return mid


class Grupo1_ONumero(unittest.TestCase):
    def test_preparada_e_aprovada_aplica(self):
        s = servidor()
        self.assertTrue(aplicar(s, {"id": preparada(s)})[0])
        self.assertEqual(s["cargas"]["C-9281"], {"motorista": "Carlos", "trocas": 1})

    def test_id_inventado_nao_aplica(self):
        s = servidor()
        preparada(s)
        self.assertFalse(aplicar(s, {"id": "M-99"})[0])


class Grupo2_QuemAprovou(unittest.TestCase):
    def test_sem_aprovacao_nao_aplica(self):
        s = servidor()
        self.assertFalse(aplicar(s, {"id": preparada(s, aprovada_por=None)})[0])

    def test_agente_nao_aprova(self):
        s = servidor()
        self.assertFalse(aplicar(s, {"id": preparada(s, aprovada_por="agente")})[0])

    def test_quem_nao_autoriza_nao_aprova(self):
        s = servidor()
        self.assertFalse(aplicar(s, {"id": preparada(s, aprovada_por="Lia")})[0])


class Grupo3_NaHoraDeAplicar(unittest.TestCase):
    def test_aplica_o_motorista_preparado(self):
        s = servidor()
        aplicar(s, {"id": preparada(s), "motorista": "Davi"})
        self.assertEqual(s["cargas"]["C-9281"]["motorista"], "Carlos")

    def test_duas_vezes_aplica_uma(self):
        s = servidor()
        pedido = {"id": preparada(s)}
        aplicar(s, pedido)
        self.assertFalse(aplicar(s, pedido)[0])
        self.assertEqual(s["cargas"]["C-9281"]["trocas"], 1)

    def test_teto_de_agora(self):
        s = servidor(trocas=1)
        pedido = {"id": preparada(s)}        # coube quando foi preparada
        s["cargas"]["C-9281"]["trocas"] = 2  # outra troca saiu antes
        self.assertFalse(aplicar(s, pedido)[0])

    def test_recusa_nao_muda_nada(self):
        s = servidor()
        mid = preparada(s, aprovada_por=None)
        aplicar(s, {"id": mid})
        self.assertEqual(s["cargas"]["C-9281"], {"motorista": "Anderson", "trocas": 0})
        self.assertEqual(s["mudancas"][mid]["estado"], "preparada")


class Curto(unittest.TextTestResult):
    """Uma linha por teste, com o grupo na frente: "ONumero: id_inventado_nao_aplica ... ok"."""
    def getDescription(self, test):
        return f"{type(test).__name__.split('_', 1)[1]}: {test._testMethodName[5:]}"


def rodar(**opcoes):
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2, resultclass=Curto), **opcoes)


if __name__ == "__main__":
    rodar()
