# Rode: python test_politica.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_politica.py --solucao
import sys, unittest

if "--solucao" in sys.argv:
    sys.argv.remove("--solucao")
    from solucao.politica import consultar, permitido
else:
    from politica import consultar, permitido

# O que o despacho manda às 16:50, antes da versão nova.
CERTA = {"acao": "change_driver", "carga": {"id": "C-9281", "status": "liberada"}, "nivel": 1}


class ONaoConhecidoNega(unittest.TestCase):
    def test_tudo_certo_libera(self):
        self.assertEqual(permitido(CERTA), (True, []))

    def test_status_novo_retida_nega(self):
        self.assertFalse(permitido({**CERTA, "carga": {"id": "C-9281", "status": "retida"}})[0])

    def test_acao_que_ela_nao_conhece_nega(self):
        self.assertFalse(permitido({**CERTA, "acao": "change_commitment"})[0])

    def test_nivel_true_nega(self):
        # Em JSON, "nivel": true. Em Python, True == 1.
        self.assertFalse(permitido({**CERTA, "nivel": True})[0])


class OQueFaltaNega(unittest.TestCase):
    def test_entrada_vazia_nega(self):
        self.assertFalse(permitido({})[0])

    def test_sem_o_campo_carga_nega(self):
        # A versão nova do despacho manda "carga_atual" no lugar de "carga".
        entrada = {"acao": "change_driver", "nivel": 1,
                   "carga_atual": {"id": "C-9281", "status": "bloqueada"}}
        ok, motivos = permitido(entrada)
        self.assertFalse(ok)
        self.assertIn("carga", " ".join(motivos))

    def test_sem_o_nivel_nega(self):
        self.assertFalse(permitido({"acao": "change_driver", "carga": CERTA["carga"]})[0])


class OQueQuebraNega(unittest.TestCase):
    def test_politica_que_da_erro_nega(self):
        def quebra(entrada):
            return entrada["carga"]["status"] == "liberada", []  # KeyError sem o campo carga
        ok, motivos = consultar(quebra, {"acao": "change_driver", "nivel": 1})
        self.assertFalse(ok)
        self.assertTrue(motivos)

    def test_politica_que_responde_outra_coisa_nega(self):
        self.assertFalse(consultar(lambda entrada: None, CERTA)[0])

    def test_politica_que_libera_passa(self):
        self.assertEqual(consultar(lambda entrada: (True, []), CERTA), (True, []))

    def test_o_motivo_da_politica_chega_ao_despacho(self):
        self.assertEqual(consultar(lambda entrada: (False, ["a carga está retida"]), CERTA),
                         (False, ["a carga está retida"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
