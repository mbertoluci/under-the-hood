# A tarde do hook (aula 6): o agente de código da equipe pede o mesmo comando às 16:50 e às 17:40.
# Às 17:00, uma refatoração tira o comandos.json do lugar. O harness segue o contrato do Claude Code (harness.py).
# Uso: python tarde_do_hook.py --ingenuo            (o hook que quebra junto com a política)
#      python tarde_do_hook.py [--solucao]          (o seu hook.py, ou o da solução)
#      python tarde_do_hook.py --lento [--ingenuo | --solucao]   (a política não some: fica lenta)
# Nada é apagado de verdade: o "executa" é só impresso.
import os, shutil, sys, tempfile
from pathlib import Path

import harness

AQUI = Path(__file__).resolve().parent
if "--ingenuo" in sys.argv:
    HOOK = AQUI / "hook_ingenuo.py"
elif "--solucao" in sys.argv:
    HOOK = AQUI / "solucao/hook.py"
else:
    HOOK = AQUI / "hook.py"
LENTO = "--lento" in sys.argv
TIMEOUT = 3  # o timeout do hook no harness, em segundos (no settings.json: "timeout": 3)
COMANDO = "rm -rf dados/cargas"
EVENTO = {"tool_name": "Bash", "tool_input": {"command": COMANDO}}

with tempfile.TemporaryDirectory() as d:
    # A política da equipe de risco, numa cópia: a refatoração das 17:00 mexe só nela.
    shutil.copy(AQUI / "gate.py", d); shutil.copy(AQUI / "comandos.json", d)
    env = {**os.environ, "GATE_POLITICA": str(Path(d) / "gate.py"), "HOOK_PRAZO": "2"}

    def pede(hora):
        print(f"{hora} o agente pede: {COMANDO}")
        acao, registro = harness.chamar([sys.executable, str(HOOK)], EVENTO, timeout=TIMEOUT, env=env)
        print(f"{hora} registro da sessão: {registro}")
        print(f"{hora} harness: {'EXECUTA ' + COMANDO if acao == 'executa' else 'bloqueado'}")

    pede("16:50")
    if LENTO:
        env["GATE_ATRASO"] = "5"
        print("17:00 a política fica lenta: 5 s por resposta")
    else:
        Path(d, "comandos.json").rename(Path(d, "comandos.antigo.json"))
        print("17:00 refatoração: comandos.json mudou de lugar")
    pede("17:40")
