# A política dos comandos (aula 6), da equipe de risco: libera só o comando que está na lista.
# Recebe no stdin o evento do hook e responde no stdout: {"permitido": true | false, "motivos": [...]}.
import json, os, sys, time
from pathlib import Path

LIBERADOS = json.loads(Path(__file__).with_name("comandos.json").read_text())["liberados"]
time.sleep(float(os.environ.get("GATE_ATRASO", "0")))  # para simular a política lenta

evento = json.load(sys.stdin)
comando = evento["tool_input"]["command"]
programa = comando.split()[0] if comando.split() else ""
if programa in LIBERADOS:
    print(json.dumps({"permitido": True, "motivos": []}))
else:
    print(json.dumps({"permitido": False, "motivos": [f"comando fora da lista: {programa}"]}, ensure_ascii=False))
