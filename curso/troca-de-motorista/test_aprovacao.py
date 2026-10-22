# Rode: python test_aprovacao.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_aprovacao.py --solucao
import sys, unittest

if "--solucao" in sys.argv:
    sys.argv.remove("--solucao")
    from solucao.aprovacao import cartao, precisa_perguntar, vale
else:
    from aprovacao import cartao, precisa_perguntar, vale
from operacao import CARGA, resumo

B17 = {"id": "B-17", "acao": "change_driver", "carga": "C-9281", "motorista": "Carlos", "veiculo": "R-12", "versao": 1}


class PrecisavaPerguntar(unittest.TestCase):
    def test_aviso_por_template_a_regra_faz_sozinha(self):
        self.assertFalse(precisa_perguntar({"id": "P-01", "acao": "send_email", "carga": "C-9281"}))

    def test_troca_de_motorista_vai_para_a_pessoa(self):
        self.assertTrue(precisa_perguntar(B17))

    def test_acao_fora_do_catalogo_vai_para_a_pessoa(self):
        self.assertTrue(precisa_perguntar({"id": "P-50", "acao": "change_commitment", "carga": "C-9281"}))


class ElaVeOQueMuda(unittest.TestCase):
    def test_mostra_o_antes_e_o_depois(self):
        texto = cartao(B17, dict(CARGA))
        self.assertIn("motorista: Anderson -> Carlos", texto)
        self.assertIn("veiculo: V-07 -> R-12", texto)

    def test_nao_mostra_o_que_nao_muda(self):
        so_motorista = {**B17, "veiculo": "V-07", "versao": 2}
        texto = cartao(so_motorista, dict(CARGA))
        self.assertIn("motorista: Anderson -> Carlos", texto)
        self.assertNotIn("veiculo", texto)
        self.assertNotIn("versao", texto)


class ExecutaOQueElaViu(unittest.TestCase):
    def setUp(self):
        self.aprovada = {"plano": "B-17", "decisao": "aprovo", "resumo": resumo(cartao(B17, dict(CARGA)))}

    def test_o_plano_mudou_depois_da_aprovacao(self):
        diego = {**B17, "versao": 2, "motorista": "Diego"}
        self.assertFalse(vale(self.aprovada, diego, dict(CARGA)))

    def test_recusa_nao_vale(self):
        recusa = {**self.aprovada, "decisao": "recuso"}
        self.assertFalse(vale(recusa, B17, dict(CARGA)))

    def test_versao_nova_com_o_mesmo_cartao_continua_valendo(self):
        self.assertTrue(vale(self.aprovada, {**B17, "versao": 2}, dict(CARGA)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
