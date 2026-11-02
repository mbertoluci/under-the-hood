# O hook ingênuo (aula 6): pergunta à política e sai com 2 se ela negar. Se ela quebrar, ele quebra junto.
import json, os, subprocess, sys
from pathlib import Path

GATE = os.environ.get("GATE_POLITICA", str(Path(__file__).with_name("gate.py")))

r = subprocess.run([sys.executable, GATE], input=sys.stdin.read(), capture_output=True, text=True)
resposta = json.loads(r.stdout)
if not resposta["permitido"]:
    print("negado pela política: " + "; ".join(resposta["motivos"]), file=sys.stderr)
    sys.exit(2)
