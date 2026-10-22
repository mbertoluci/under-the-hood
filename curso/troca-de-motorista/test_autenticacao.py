# Rode: python test_autenticacao.py   (sem chave de API)
# O botão só vira sinal com um token válido, e a origem do sinal sai do token, nunca do corpo da requisição.
import json, unittest

from autenticacao import _b64, emitir, sinal_do_botao
from solucao.autoridade import autorizou
from operacao import PROPOSTA

AGORA = 1_790_000_000  # instante fixo, para o teste não depender do relógio
BOTAO = {"botao": "autorizo", "proposta": "B-17"}


def requisicao(token, corpo=BOTAO):
    return {"headers": {"Authorization": f"Bearer {token}"}, "corpo": corpo}


class Autenticacao(unittest.TestCase):
    def test_1_token_valido_da_maria(self):
        sinal = sinal_do_botao(requisicao(emitir("maria-xpto", agora=AGORA)), AGORA)
        self.assertEqual(sinal["origem"], "maria-xpto")
        self.assertTrue(autorizou(sinal, PROPOSTA)[0])

    def test_2_o_corpo_nao_diz_quem_apertou(self):
        corpo = {**BOTAO, "origem": "maria-xpto"}  # o app (ou alguém no meio) diz que é a Maria
        sinal = sinal_do_botao(requisicao(emitir("anderson-frota", agora=AGORA), corpo), AGORA)
        self.assertEqual(sinal["origem"], "anderson-frota")
        self.assertFalse(autorizou(sinal, PROPOSTA)[0])

    def test_3_token_editado_para_maria(self):
        cabecalho, _, assinatura = emitir("anderson-frota", agora=AGORA).split(".")
        corpo = _b64(json.dumps({"sub": "maria-xpto", "exp": AGORA + 3600}).encode())
        self.assertIsNone(sinal_do_botao(requisicao(f"{cabecalho}.{corpo}.{assinatura}"), AGORA))

    def test_4_token_vencido(self):
        token = emitir("maria-xpto", validade=3600, agora=AGORA - 7200)
        self.assertIsNone(sinal_do_botao(requisicao(token), AGORA))

    def test_5_sem_token(self):
        self.assertIsNone(sinal_do_botao({"corpo": {**BOTAO, "origem": "maria-xpto"}}, AGORA))

    def test_6_token_com_alg_none(self):
        cabecalho = _b64(json.dumps({"alg": "none", "typ": "JWT"}).encode())
        corpo = _b64(json.dumps({"sub": "maria-xpto", "exp": AGORA + 3600}).encode())
        self.assertIsNone(sinal_do_botao(requisicao(f"{cabecalho}.{corpo}."), AGORA))


if __name__ == "__main__":
    unittest.main()
