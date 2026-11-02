# Rode: python test_hook.py   (sem chave de API e sem o Claude Code)
# Para testar a solução em vez do seu exercício: python test_hook.py --solucao
import os, sys, tempfile, unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SOLUCAO = "--solucao" in sys.argv
if SOLUCAO:
    sys.argv.remove("--solucao")
    from solucao.hook import decidir
else:
    from hook import decidir
import harness

EVENTO = {"tool_name": "Bash", "tool_input": {"command": "rm -rf dados/cargas"}}


def gate(codigo):
    """Um gate falso: um programa Python de uma linha."""
    return [sys.executable, "-c", codigo]


LIBERA = gate('print(\'{"permitido": true, "motivos": []}\')')
NEGA = gate('print(\'{"permitido": false, "motivos": ["comando fora da lista: rm"]}\')')


class OGateResponde(unittest.TestCase):
    def test_liberado_sai_0(self):
        self.assertEqual(decidir(EVENTO, LIBERA, 2), (0, ""))

    def test_negado_sai_2(self):
        self.assertEqual(decidir(EVENTO, NEGA, 2)[0], 2)

    def test_o_motivo_chega_ao_agente(self):
        self.assertIn("comando fora da lista: rm", decidir(EVENTO, NEGA, 2)[1])


class OGateNaoResponde(unittest.TestCase):
    def test_gate_que_da_erro_sai_2(self):
        self.assertEqual(decidir(EVENTO, gate("raise FileNotFoundError('comandos.json')"), 2)[0], 2)

    def test_gate_que_nao_existe_sai_2(self):
        self.assertEqual(decidir(EVENTO, ["./gate_que_nao_existe.sh"], 2)[0], 2)

    def test_gate_lento_sai_2(self):
        lento = gate('import time; time.sleep(3); print(\'{"permitido": true}\')')
        self.assertEqual(decidir(EVENTO, lento, .5)[0], 2)


class ARespostaEEstranha(unittest.TestCase):
    def test_saida_vazia_sai_2(self):
        self.assertEqual(decidir(EVENTO, gate("pass"), 2)[0], 2)

    def test_saida_que_nao_e_json_sai_2(self):
        self.assertEqual(decidir(EVENTO, gate("print('ok')"), 2)[0], 2)

    def test_sem_o_campo_permitido_sai_2(self):
        self.assertEqual(decidir(EVENTO, gate('print(\'{"motivos": []}\')'), 2)[0], 2)

    def test_permitido_como_texto_sai_2(self):
        self.assertEqual(decidir(EVENTO, gate('print(\'{"permitido": "true"}\')'), 2)[0], 2)


class PeloCaminhoReal(unittest.TestCase):
    def test_pelo_harness_a_politica_quebrada_bloqueia(self):
        # O hook inteiro, chamado como o Claude Code chama, com a política fora do lugar.
        with tempfile.TemporaryDirectory() as d:
            quebrado = Path(d) / "gate.py"
            quebrado.write_text("raise FileNotFoundError('comandos.json')\n")
            hook = AQUI / ("solucao/hook.py" if SOLUCAO else "hook.py")
            env = {**os.environ, "GATE_POLITICA": str(quebrado)}
            acao, registro = harness.chamar([sys.executable, str(hook)], EVENTO, timeout=10, env=env)
        self.assertEqual(acao, "bloqueia")
        self.assertIn("a política", registro)  # quem negou foi o decidir, não o defeito do hook


if __name__ == "__main__":
    unittest.main(verbosity=2)
