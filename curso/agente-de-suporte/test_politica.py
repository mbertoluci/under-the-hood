# Rode: python test_politica.py   (sem chave de API: a regra não usa o modelo)
# Para testar a solução em vez do seu exercício: python test_politica.py --solucao
import sys, unittest

if "--solucao" in sys.argv:
    sys.argv.remove("--solucao")
    from solucao.politica import pode_cancelar
else:
    from politica import pode_cancelar


class Politica(unittest.TestCase):
    def test_cancela_o_proprio_pedido(self):
        self.assertTrue(pode_cancelar("ana", "A101")[0])

    def test_recusa_pedido_de_outra_pessoa(self):
        self.assertFalse(pode_cancelar("ana", "B202")[0])

    def test_recusa_pedido_ja_enviado(self):
        self.assertFalse(pode_cancelar("ana", "C303")[0])

    def test_recusa_pedido_que_nao_existe(self):
        self.assertFalse(pode_cancelar("ana", "Z999")[0])


if __name__ == "__main__":
    unittest.main()
