# O dia do reinício (aula 3): o servidor cai de verdade (kill -9) um minuto depois de mandar o cartão.
# Uso: python reinicio.py --memoria              (a espera na memória)
#      python reinicio.py [--solucao]            (o registro no disco, com o seu registro.py ou o da solução)
#      python reinicio.py --solucao --silencio   (ninguém responde)
import os, subprocess, sys

opcoes = [a for a in sys.argv[1:] if a in ("--memoria", "--solucao")]
if os.path.exists("aprovacoes.db"):
    os.remove("aprovacoes.db")  # cada execução começa um dia limpo


def subir():
    proc = subprocess.Popen([sys.executable, "servidor.py", *opcoes], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    print(f"      [servidor no ar, pid {proc.pid}]")
    return proc


def mandar(proc, comando):
    try:
        proc.stdin.write(comando + "\n")
        proc.stdin.flush()
    except BrokenPipeError:
        sys.exit("      [o servidor parou: veja o erro acima]")
    while True:
        linha = proc.stdout.readline()
        if not linha:
            sys.exit("      [o servidor parou: veja o erro acima]")
        print(linha.rstrip())
        if not linha.startswith("  executado"):
            return


servidor = subir()
mandar(servidor, "subir 17:00")
mandar(servidor, "pedir 17:10")
print(f"17:11 deploy: kill -9 {servidor.pid}")
servidor.kill()  # SIGKILL: o processo não tem chance de salvar nada
servidor.wait()

servidor = subir()
mandar(servidor, "subir 17:11")
if "--silencio" not in sys.argv:
    mandar(servidor, "responder 17:12 supervisora recuso")
    mandar(servidor, "responder 17:13 despachante aprovo")
mandar(servidor, "despachar 17:40")
servidor.stdin.close()
servidor.wait()
