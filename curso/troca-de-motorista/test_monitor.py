# Rode: python test_monitor.py   (sem chave de API)
# Para testar a solução em vez do seu exercício: python test_monitor.py --solucao
import sys, unittest

SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.monitor import proteger
else:
    from monitor import proteger


def bancada():
    """Três ferramentas que anotam quando executam, e um monitor que anota quando é chamado."""
    executou, conferiu = [], []
    ferramentas = {
        "ler_carga": lambda args: executou.append("ler_carga") or {"carga": args["carga"]},
        "preparar_troca": lambda args: executou.append("preparar_troca") or "M-1",
        "cancelar_coleta": lambda args: executou.append("cancelar_coleta") or "cancelada",  # entrou semana passada
    }

    def monitor(nome, args):
        conferiu.append(nome)
        return (False, "troca fora do escopo") if nome == "preparar_troca" and args.get("carga") == "C-1111" else (True, "")
    return ferramentas, monitor, executou, conferiu


class Grupo1_SempreChamado(unittest.TestCase):
    def test_a_chamada_passa_pelo_monitor(self):
        ferramentas, monitor, executou, conferiu = bancada()
        proteger(ferramentas, monitor)["preparar_troca"]({"carga": "C-9281"})
        self.assertEqual((conferiu, executou), (["preparar_troca"], ["preparar_troca"]))

    def test_leitura_tambem_passa(self):
        ferramentas, monitor, executou, conferiu = bancada()
        proteger(ferramentas, monitor)["ler_carga"]({"carga": "C-9281"})
        self.assertEqual(conferiu, ["ler_carga"])

    def test_ferramenta_nova_tambem_passa(self):
        ferramentas, monitor, executou, conferiu = bancada()
        proteger(ferramentas, monitor)["cancelar_coleta"]({"carga": "C-9281"})
        self.assertEqual(conferiu, ["cancelar_coleta"])


class Grupo2_AChamadaNaoPula(unittest.TestCase):
    def test_negado_nao_executa(self):
        ferramentas, monitor, executou, conferiu = bancada()
        resposta = proteger(ferramentas, monitor)["preparar_troca"]({"carga": "C-1111"})
        self.assertEqual((resposta, executou), ({"negado": "troca fora do escopo"}, []))

    def test_argumento_nao_desliga_o_monitor(self):
        ferramentas, monitor, executou, conferiu = bancada()
        resposta = proteger(ferramentas, monitor)["preparar_troca"]({"carga": "C-1111", "sem_monitor": True})
        self.assertEqual((resposta, executou), ({"negado": "troca fora do escopo"}, []))

    def test_mexer_no_original_nao_muda_o_protegido(self):
        ferramentas, monitor, executou, conferiu = bancada()
        protegidas = proteger(ferramentas, monitor)
        ferramentas["apagar_tudo"] = lambda args: executou.append("apagar_tudo")
        self.assertEqual(sorted(protegidas), ["cancelar_coleta", "ler_carga", "preparar_troca"])


class Grupo3_SoOSimLibera(unittest.TestCase):
    def test_permitido_executa_e_devolve(self):
        ferramentas, monitor, executou, conferiu = bancada()
        self.assertEqual(proteger(ferramentas, monitor)["ler_carga"]({"carga": "C-9281"}), {"carga": "C-9281"})

    def test_monitor_que_quebra_nega(self):
        ferramentas, monitor, executou, conferiu = bancada()

        def quebrado(nome, args):
            raise KeyError("escala")
        resposta = proteger(ferramentas, quebrado)["preparar_troca"]({"carga": "C-9281"})
        self.assertEqual((resposta, executou), ({"negado": "o monitor falhou"}, []))

    def test_resposta_estranha_nega(self):
        ferramentas, monitor, executou, conferiu = bancada()
        for estranha in ("sim", None, ("true", ""), (1, ""), [True, ""], {True: "sim", "motivo": ""}, (True,)):
            resposta = proteger(ferramentas, lambda nome, args: estranha)["preparar_troca"]({"carga": "C-9281"})
            self.assertEqual((resposta, executou), ({"negado": "o monitor falhou"}, []), repr(estranha))


class Curto(unittest.TextTestResult):
    """Uma linha por teste, com o grupo na frente: "SempreChamado: leitura_tambem_passa ... ok"."""
    def getDescription(self, test):
        return f"{type(test).__name__.split('_', 1)[1]}: {test._testMethodName[5:]}"


def rodar(**opcoes):
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2, resultclass=Curto), **opcoes)


if __name__ == "__main__":
    rodar()
