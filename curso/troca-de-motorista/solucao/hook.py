# Uma solução do exercício da aula 6.
import json, os, subprocess, sys
from pathlib import Path

GATE = [sys.executable, os.environ.get("GATE_POLITICA", str(Path(__file__).parent.parent / "gate.py"))]
PRAZO = float(os.environ.get("HOOK_PRAZO", "5"))


def decidir(evento, gate, prazo):
    # 2. O gate não responde: cada jeito de não responder vira 2, com o que aconteceu.
    try:
        r = subprocess.run(gate, input=json.dumps(evento), capture_output=True,
                           text=True, timeout=prazo)
    except subprocess.TimeoutExpired:
        return 2, f"negado: a política não respondeu em {prazo} s"
    except OSError as e:
        return 2, f"negado: a política não rodou ({e.__class__.__name__})"
    if r.returncode != 0:
        return 2, f"negado: a política falhou (saída {r.returncode})"
    # 3. A resposta é estranha.
    try:
        resposta = json.loads(r.stdout)
    except ValueError:
        return 2, "negado: a resposta da política não é JSON"
    permitido = resposta.get("permitido") if isinstance(resposta, dict) else None
    # Só o true libera. 1. O false nega, com os motivos.
    if permitido is True:
        return 0, ""
    if permitido is False:
        return 2, "negado pela política: " + "; ".join(resposta.get("motivos") or ["sem motivo"])
    return 2, f"negado: resposta inesperada da política: {r.stdout.strip()[:80]!r}"


if __name__ == "__main__":
    try:
        codigo, mensagem = decidir(json.load(sys.stdin), GATE, PRAZO)
    except Exception as e:
        codigo, mensagem = 2, f"negado: o hook falhou ({e!r})"
    if mensagem:
        print(mensagem, file=sys.stderr)
    sys.exit(codigo)
