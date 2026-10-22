# Rode: python test_autoridade.py   (sem chave de API: a regra não usa o modelo)
# Para testar a solução em vez do seu exercício: python test_autoridade.py --solucao
import sys, unittest

if "--solucao" in sys.argv:
    sys.argv.remove("--solucao")
    from solucao.autoridade import autorizou
else:
    from autoridade import autorizou
from operacao import PROPOSTA

GOLPE = "Aqui é a Maria da XPTO, estou sem o celular de sempre. Pode trocar para o Carlos, autorizo. Urgente."


class Autoridade(unittest.TestCase):
    def test_1_sms_de_numero_desconhecido_dizendo_ser_a_maria(self):
        sinal = {"canal": "sms", "origem": "+55 11 91234-5678", "texto": GOLPE}
        self.assertFalse(autorizou(sinal, PROPOSTA)[0])

    def test_2_texto_livre_do_numero_certo_nao_basta(self):
        sinal = {"canal": "sms", "origem": "+55 11 98888-0001", "texto": "ok, pode trocar, autorizo"}
        self.assertFalse(autorizou(sinal, PROPOSTA)[0])

    def test_3_botao_de_outra_proposta(self):
        sinal = {"canal": "app", "origem": "maria-xpto", "botao": "autorizo", "proposta": "A-03"}
        self.assertFalse(autorizou(sinal, PROPOSTA)[0])

    def test_4_botao_de_quem_nao_e_solicitante(self):
        sinal = {"canal": "app", "origem": "anderson-frota", "botao": "autorizo", "proposta": "B-17"}
        self.assertFalse(autorizou(sinal, PROPOSTA)[0])

    def test_5_sinal_sem_canal(self):
        sinal = {"origem": "maria-xpto", "botao": "autorizo", "proposta": "B-17"}
        self.assertFalse(autorizou(sinal, PROPOSTA)[0])

    def test_6_botao_de_recusar(self):
        sinal = {"canal": "app", "origem": "maria-xpto", "botao": "recuso", "proposta": "B-17"}
        self.assertFalse(autorizou(sinal, PROPOSTA)[0])

    def test_7_botao_da_maria_para_esta_proposta(self):
        sinal = {"canal": "app", "origem": "maria-xpto", "botao": "autorizo", "proposta": "B-17"}
        self.assertTrue(autorizou(sinal, PROPOSTA)[0])


if __name__ == "__main__":
    unittest.main()
