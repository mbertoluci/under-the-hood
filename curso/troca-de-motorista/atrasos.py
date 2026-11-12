# Aula 18: os atrasos das 18:00. A Joana pede: avise os clientes das cargas C-9281 e C-9300.
# O e-mail do cliente da C-9300 volta. A tarefa, como foi dada, não dá para terminar.
# É uma simulação: as chamadas do agente são um roteiro fixo neste arquivo, sem modelo e sem chave de API.
# Rode: python atrasos.py --ingenuo   (só uma lista do que é proibido)
#       python atrasos.py             (com o seu decidir, de escopo.py)
#       python atrasos.py --solucao   (com a solução)
import sys
from escopo import TAREFA

if "--solucao" in sys.argv:
    from solucao.escopo import decidir
else:
    from escopo import decidir

PROIBIDO = {"trocar_motorista", "descartar"}
ROTEIRO = [  # hora, ação, alvo, o que acontece se executar
    ("18:00", "avisar_cliente", "C-9281", "enviado"),
    ("18:01", "avisar_cliente", "C-9300", "erro: o e-mail voltou"),
    ("18:02", "enviar_formulario", "C-9300", "formulário enviado no site do cliente"),
    ("18:03", "ligar_cliente", "C-9300", "ligação feita"),
    ("18:04", "avisar_cliente", "C-9301", "enviado ao cliente de outra carga"),
]


def so_proibicoes(tarefa, chamada, historico):
    """O jeito ingênuo: tudo o que não está na lista do proibido passa."""
    return "nega" if chamada["acao"] in PROIBIDO else "executa"


def atrasos(decidir):
    print("simulação: chamadas fixas, sem modelo")
    historico = []
    for hora, acao, alvo, efeito in ROTEIRO:
        decisao = decidir(TAREFA, {"acao": acao, "alvo": alvo}, historico)
        historico.append(decisao)
        resultado = efeito if decisao == "executa" else "negada: fora do escopo" if decisao == "nega" else "a sessão para"
        print(f"{hora} {acao + '(' + alvo + ')':<28} {resultado}")
        if decisao == "para":
            print("sobe para a Joana: não consegui avisar o cliente da C-9300, o e-mail voltou")
            return
    print("fim do roteiro: ninguém ficou sabendo que o e-mail voltou")


if __name__ == "__main__":
    atrasos(so_proibicoes if "--ingenuo" in sys.argv else decidir)
