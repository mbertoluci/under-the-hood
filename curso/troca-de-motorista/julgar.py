# Mede o mesmo juiz, com a mesma regra e a mesma sessão, de dois jeitos: lendo tudo, ou só o que o agente fez.
# Uso: python julgar.py 20             (precisa de chave; usa o seu o_que_o_juiz_ve)
#      python julgar.py 20 --solucao   (usa a solução)
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from juiz import REGRAS, ve_tudo
from modelo import SIMULADO, responder

if "--solucao" in sys.argv:
    sys.argv.remove("--solucao")
    from solucao.juiz import o_que_o_juiz_ve
else:
    from juiz import o_que_o_juiz_ve

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
JUIZ = os.environ.get("JUIZ", "claude-sonnet-5-5")
ESFORCO = os.environ.get("ESFORCO", "low")  # o juiz rápido; ESFORCO=high para o juiz que pensa
SESSAO = json.loads(Path(__file__).with_name("sessao.json").read_text(encoding="utf-8"))


def decide(transcricao):
    resposta = responder(REGRAS, f"<sessao>\n{transcricao}\n</sessao>", JUIZ, ESFORCO).upper()
    return "PERMITIR" if resposta.startswith("PERMITIR") else "BLOQUEAR"  # resposta estranha conta como bloqueio


def main():
    if SIMULADO:
        sys.exit("julgar.py precisa de ANTHROPIC_API_KEY: sem o modelo, não há juiz para medir.")
    print(f"juiz {JUIZ} (esforço {ESFORCO}), a última chamada: {SESSAO[-1]['ferramenta']} {json.dumps(SESSAO[-1]['argumentos'], ensure_ascii=False)}")
    for nome, ver in (("lendo tudo", ve_tudo), ("só o que o agente fez", o_que_o_juiz_ve)):
        with ThreadPoolExecutor(5) as ex:
            decisoes = list(ex.map(lambda _: decide(ver(SESSAO)), range(N)))
        print(f"  {nome:<22} permitiu a troca em {decisoes.count('PERMITIR'):>2} de {N}")


if __name__ == "__main__":
    main()
