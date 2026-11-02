# O contrato do hook PreToolUse do Claude Code (aula 6), simulado para rodar sem o Claude Code.
# Conferido no Claude Code 2.1.312 em 29/10/2026: exit 0 libera; exit 2 bloqueia, e o stderr vai para o modelo;
# qualquer outra saída, o script que não existe e o timeout são erro não bloqueante, e a ação segue.
# Com on_failure="block" (Claude Code 2.1.295 ou mais novo), essas falhas bloqueiam.
import json, subprocess


def chamar(hook, evento, timeout=600, on_failure="continue", env=None):
    """Roda o hook com o evento no stdin. Devolve ("executa" | "bloqueia", o que fica no registro da sessão)."""
    try:
        r = subprocess.run(hook, input=json.dumps(evento), capture_output=True, text=True,
                           timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        falha = f"hook_cancelled: timeout de {timeout} s"
    except OSError:
        falha = "hook_non_blocking_error exitCode=127: o script não existe"
    else:
        if r.returncode == 0:
            return "executa", "hook_success exitCode=0"
        if r.returncode == 2:
            return "bloqueia", "exit 2: " + r.stderr.strip()
        ultima = (r.stderr.strip().splitlines() or [""])[-1]
        falha = f"hook_non_blocking_error exitCode={r.returncode}: {ultima}"
    return ("bloqueia" if on_failure == "block" else "executa"), falha
