# Rode: python test_controle.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_controle.py --solucao
import sys, unittest

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.controle import controle
else:
    from controle import controle
from controle import CATALOGO


def proposta(acao, **extra):
    return {"acao": acao, "argumentos": {"carga": "C-9281"}, **extra}


class AsTresCaixas(unittest.TestCase):
    def test_ler_a_carga_se_confina(self):
        self.assertEqual(controle(proposta("ler_carga")), "confinar")

    def test_o_rascunho_se_confina(self):
        self.assertEqual(controle(proposta("escrever_rascunho")), "confinar")

    def test_reservar_o_veiculo_vai_ao_juiz(self):
        self.assertEqual(controle(proposta("reservar_veiculo")), "juiz")

    def test_trocar_o_motorista_vai_a_pessoa(self):
        self.assertEqual(controle(proposta("trocar_motorista")), "pessoa")

    def test_o_email_ao_embarcador_vai_a_pessoa(self):
        self.assertEqual(controle(proposta("enviar_email_embarcador")), "pessoa")


class QuemDiz(unittest.TestCase):
    def test_a_proposta_dizer_que_volta_nao_conta(self):
        # O agente escreveu na proposta que a troca volta e fica na área dele.
        self.assertEqual(controle(proposta("trocar_motorista", volta=True, onde="agente")), "pessoa")


class NaDuvida(unittest.TestCase):
    def test_acao_fora_do_catalogo_vai_a_pessoa(self):
        self.assertEqual(controle(proposta("cancelar_coleta")), "pessoa")

    def test_campo_faltando_vai_a_pessoa(self):
        catalogo = {**CATALOGO, "remarcar_doca": {"onde": "fora"}}
        self.assertEqual(controle(proposta("remarcar_doca"), catalogo), "pessoa")

    def test_valor_estranho_vai_a_pessoa(self):
        catalogo = {**CATALOGO, "remarcar_doca": {"volta": True, "onde": "armazem"}}
        self.assertEqual(controle(proposta("remarcar_doca"), catalogo), "pessoa")


if __name__ == "__main__":
    unittest.main(verbosity=2)
