# EXERCÍCIO (aula 6): no hook, só o 2 bloqueia. Então tudo que não for um sim explícito vira 2.
# Escreva decidir e rode: python test_hook.py
import json, os, subprocess, sys
from pathlib import Path

GATE = [sys.executable, os.environ.get("GATE_POLITICA", str(Path(__file__).with_name("gate.py")))]
PRAZO = float(os.environ.get("HOOK_PRAZO", "5"))  # segundos; menor que o timeout do harness


def decidir(evento, gate, prazo):
    """Roda o gate com o evento no stdin. Devolve (0, "") ou (2, mensagem).

    gate é a lista do comando, como em subprocess.run: [sys.executable, "gate.py"].
    O gate responde no stdout: {"permitido": true | false, "motivos": [...]}.

    Só o "permitido": true libera. Todo o resto sai com 2, com a mensagem para o agente:
    1. O gate nega: 2, com os motivos dele.
    2. O gate não responde: não existe, dá erro (saída diferente de 0) ou passa do prazo.
    3. A resposta é estranha: vazia, não é JSON, sem "permitido",
       ou "permitido" que não é true nem false.
    """
    raise NotImplementedError("escreva aqui")


if __name__ == "__main__":
    try:
        codigo, mensagem = decidir(json.load(sys.stdin), GATE, PRAZO)
    except Exception as e:  # um defeito no próprio hook também nega
        codigo, mensagem = 2, f"negado: o hook falhou ({e!r})"
    if mensagem:
        print(mensagem, file=sys.stderr)
    sys.exit(codigo)
