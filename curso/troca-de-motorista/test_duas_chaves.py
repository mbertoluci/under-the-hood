# Rode: python test_duas_chaves.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_duas_chaves.py --solucao
import sys, unittest

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.duas_chaves import liberado
else:
    from duas_chaves import liberado

TROCA = {"id": "B-17", "classe": "troca", "resumo": "Carlos, R-12, 14/10 8h00", "pedida_por": "agente"}
DESCARTE = {"id": "D-03", "classe": "descarte", "resumo": "descartar C-9281, baú a 14 °C", "pedida_por": "agente"}


def ok(quem, acao=DESCARTE):
    return {"quem": quem, "resumo": acao["resumo"]}


class UmaChave(unittest.TestCase):
    def test_troca_com_joana(self):
        self.assertTrue(liberado(TROCA, [ok("joana", TROCA)]))

    def test_troca_sem_aprovacao(self):
        self.assertFalse(liberado(TROCA, []))

    def test_quem_nao_autoriza(self):
        self.assertFalse(liberado(TROCA, [ok("lia", TROCA)]))           # lia está em treino


class DuasChaves(unittest.TestCase):
    def test_descarte_com_uma(self):
        self.assertFalse(liberado(DESCARTE, [ok("joana")]))

    def test_descarte_com_duas(self):
        self.assertTrue(liberado(DESCARTE, [ok("joana"), ok("bruna")]))

    def test_mesma_pessoa_duas_vezes(self):
        self.assertFalse(liberado(DESCARTE, [ok("joana"), ok("joana")]))   # uma pessoa, uma chave


class QuemNaoConta(unittest.TestCase):
    def test_agente_nao_e_chave(self):
        self.assertFalse(liberado(DESCARTE, [ok("agente"), ok("joana")]))

    def test_quem_pediu_nao_aprova(self):
        pedido_da_joana = dict(DESCARTE, pedida_por="joana")
        self.assertFalse(liberado(pedido_da_joana, [ok("joana", pedido_da_joana), ok("bruna", pedido_da_joana)]))

    def test_outro_resumo_nao_conta(self):
        antigo = {"quem": "bruna", "resumo": "descartar C-9281, baú a 9 °C"}
        self.assertFalse(liberado(DESCARTE, [ok("joana"), antigo]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
