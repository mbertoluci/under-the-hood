# Rode: python test_evidencia.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_evidencia.py --solucao
import sys, unittest

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.evidencia import pode_subir
else:
    from evidencia import pode_subir


def dia(acertos, erros=0, por_operacao=1):
    """acertos e erros contam operações; cada operação tem por_operacao decisões (o erro fica na primeira)."""
    out = []
    for i in range(acertos + erros):
        for j in range(por_operacao):
            out.append({"operacao": f"OP-{i:05d}", "erro": i >= acertos and j == 0})
    return out


class QuantosBastam(unittest.TestCase):
    def test_dez_acertos_seguidos_nao_sobem(self):
        self.assertFalse(pode_subir(dia(10), 0.01))            # limite de 25,9%

    def test_298_ainda_nao(self):
        self.assertFalse(pode_subir(dia(298), 0.01))           # 1,0002%

    def test_299_sobe(self):
        self.assertTrue(pode_subir(dia(299), 0.01))            # 0,997%

    def test_um_erro_em_mil_ainda_sobe(self):
        self.assertTrue(pode_subir(dia(999, erros=1), 0.01))   # 0,47%

    def test_um_erro_em_150_nao_sobe(self):
        self.assertFalse(pode_subir(dia(149, erros=1), 0.01))  # 3,1%


class ODenominador(unittest.TestCase):
    def test_as_falhas_contam(self):
        self.assertFalse(pode_subir(dia(300, erros=3), 0.01))  # 300 acertos, mas 3 falhas: 2,6%

    def test_sem_decisoes_nao_sobe(self):
        self.assertFalse(pode_subir([], 0.01))


class OperacoesNaoLinhas(unittest.TestCase):
    def test_600_decisoes_de_150_operacoes(self):
        self.assertFalse(pode_subir(dia(150, por_operacao=4), 0.01))         # n = 150, não 600

    def test_o_erro_vale_para_a_operacao_inteira(self):
        self.assertFalse(pode_subir(dia(299, erros=1, por_operacao=2), 0.01))  # 1 erro em 300 operações: 1,6%


if __name__ == "__main__":
    unittest.main(verbosity=2)
