# Rode: python test_revalidar.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_revalidar.py --solucao
import sys, unittest

if "--solucao" in sys.argv:
    sys.argv.remove("--solucao")
    from solucao.revalidar import pode_executar
else:
    from revalidar import pode_executar
from operacao import resumo
from revalidar import conteudo

B17 = {"id": "B-17", "acao": "change_driver", "carga": "C-9281", "motorista": "Carlos", "veiculo": "R-12", "versao": 1}
# A linha gravada às 17:00, quando a Maria apertou "autorizo".
MARIA = {"plano": "B-17", "quem": "maria", "papel": "solicitante", "resumo": resumo(conteudo(B17)), "hora": "17:00"}


def mundo():
    return {"papeis": {"maria": "solicitante", "anderson": "motorista", "carlos": "motorista"},
            "cargas": {"C-9281": "aguardando motorista", "C-9300": "aguardando motorista"},
            "escalas": {"Carlos": None, "Diego": None}}


class OConteudoEOQueElaViu(unittest.TestCase):
    def test_tudo_igual_as_17_40_executa(self):
        self.assertEqual(pode_executar(MARIA, B17, mundo())[0], True)

    def test_o_plano_mudou_para_o_diego(self):
        self.assertEqual(pode_executar(MARIA, {**B17, "versao": 2, "motorista": "Diego"}, mundo())[0], False)

    def test_versao_nova_com_o_mesmo_conteudo_executa(self):
        self.assertEqual(pode_executar(MARIA, {**B17, "versao": 2}, mundo())[0], True)


class QuemAutorizouAindaPode(unittest.TestCase):
    def test_a_maria_perdeu_o_acesso_as_17_30(self):
        agora = mundo()
        del agora["papeis"]["maria"]
        ok, motivo = pode_executar(MARIA, B17, agora)
        self.assertFalse(ok)
        self.assertIn("maria", motivo)

    def test_a_maria_continua_no_cadastro_mas_so_para_consulta(self):
        agora = mundo()
        agora["papeis"]["maria"] = "consulta"
        self.assertEqual(pode_executar(MARIA, B17, agora)[0], False)


class OMundoAindaEOQueEra(unittest.TestCase):
    def test_o_carlos_foi_para_outra_carga_as_17_35(self):
        agora = mundo()
        agora["escalas"]["Carlos"] = "C-9300"
        self.assertEqual(pode_executar(MARIA, B17, agora)[0], False)

    def test_a_xpto_cancelou_a_carga(self):
        agora = mundo()
        agora["cargas"]["C-9281"] = "cancelada"
        self.assertEqual(pode_executar(MARIA, B17, agora)[0], False)

    def test_o_carlos_ja_reservado_para_esta_carga_executa(self):
        agora = mundo()
        agora["escalas"]["Carlos"] = "C-9281"
        self.assertEqual(pode_executar(MARIA, B17, agora)[0], True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
