# Rode: python test_ids.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_ids.py --solucao
import sys, unittest
from ids import nova_sessao, ler_carga, buscar_motorista

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.ids import pode_usar
else:
    from ids import pode_usar


def sessao_com_carga():
    s = nova_sessao()
    ler_carga(s, "C-9281")
    return s


class Grupo1_OQueOServidorEntregou(unittest.TestCase):
    def test_consultado_pode(self):
        s = sessao_com_carga()
        buscar_motorista(s, "Carlos")
        self.assertTrue(pode_usar(s, {"carga": "C-9281", "motorista": "MOT-0102"})[0])

    def test_todos_os_campos(self):
        so_carga = sessao_com_carga()  # a carga foi entregue; o motorista, não
        so_motorista = nova_sessao()   # o motorista foi entregue; a carga, não
        buscar_motorista(so_motorista, "Carlos")
        for s in (so_carga, so_motorista):
            self.assertFalse(pode_usar(s, {"carga": "C-9281", "motorista": "MOT-0102"})[0], sorted(s["entregues"]))

    def test_campo_que_nao_veio(self):
        s = sessao_com_carga()
        buscar_motorista(s, "Carlos")
        for campo, args in (("motorista", {"carga": "C-9281"}), ("carga", {"motorista": "MOT-0102"})):
            ok, motivo = pode_usar(s, args)
            self.assertFalse(ok, f"faltou {campo}")
            self.assertIn(campo, motivo)


class Grupo2_OsOutrosCaminhos(unittest.TestCase):
    def test_inventado_nao_pode(self):
        s = sessao_com_carga()
        self.assertFalse(pode_usar(s, {"carga": "C-9281", "motorista": "MOT-9999"})[0])

    def test_colado_de_um_email_nao_pode(self):
        s = sessao_com_carga()  # o MOT-0417 existe no cadastro, mas chegou por um e-mail
        ok, motivo = pode_usar(s, {"carga": "C-9281", "motorista": "MOT-0417"})
        self.assertFalse(ok)
        self.assertIn("MOT-0417", motivo)  # o motivo diz qual número

    def test_de_outra_sessao_nao_pode(self):
        outra = sessao_com_carga()
        buscar_motorista(outra, "Carlos")  # o servidor entregou, mas para outra sessão
        s = sessao_com_carga()
        self.assertFalse(pode_usar(s, {"carga": "C-9281", "motorista": "MOT-0102"})[0])


class Grupo3_DepoisDeConsultar(unittest.TestCase):
    def test_a_busca_entrega_o_numero(self):
        s = sessao_com_carga()
        self.assertEqual(buscar_motorista(s, "Carlos"), {"MOT-0102": "Carlos Lima"})
        self.assertTrue(pode_usar(s, {"carga": "C-9281", "motorista": "MOT-0102"})[0])

    def test_busca_vazia_nao_entrega(self):
        s = sessao_com_carga()
        self.assertEqual(buscar_motorista(s, "Zeca"), {})  # ninguém com esse nome
        self.assertFalse(pode_usar(s, {"carga": "C-9281", "motorista": "MOT-0102"})[0])

    def test_de_outra_empresa_continua_fora(self):
        s = sessao_com_carga()
        buscar_motorista(s, "Carlos")  # a busca não devolve o Carlos Souza, da LogSul
        self.assertFalse(pode_usar(s, {"carga": "C-9281", "motorista": "MOT-0417"})[0])


class Curto(unittest.TextTestResult):
    """Uma linha por teste, com o grupo na frente: "OsOutrosCaminhos: inventado_nao_pode ... ok"."""
    def getDescription(self, test):
        return f"{type(test).__name__.split('_', 1)[1]}: {test._testMethodName[5:]}"


def rodar(**opcoes):
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2, resultclass=Curto), **opcoes)


if __name__ == "__main__":
    rodar()
