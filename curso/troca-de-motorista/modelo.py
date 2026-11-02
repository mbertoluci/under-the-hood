# Chama a API de mensagens da Anthropic usando só a biblioteca padrão (sem pip install).
# Devolve as chamadas de ferramenta que o modelo propôs. Quem executa é quem chamou.
import json
import os
import urllib.request

URL = "https://api.anthropic.com/v1/messages"
MODELO = os.environ.get("MODELO", "claude-haiku-5-5")
SIMULADO = not os.environ.get("ANTHROPIC_API_KEY")


def propor(system, mensagem, ferramentas):
    chave = os.environ.get("ANTHROPIC_API_KEY")
    if not chave:
        return simular(mensagem)
    corpo = {
        "model": MODELO,
        "max_tokens": 512,
        "system": system,
        "tools": ferramentas,
        "messages": [{"role": "user", "content": mensagem}],
    }
    cabecalhos = {
        "x-api-key": chave,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    req = urllib.request.Request(URL, data=json.dumps(corpo).encode(), headers=cabecalhos)
    with urllib.request.urlopen(req, timeout=60) as r:
        resposta = json.load(r)
    return [bloco for bloco in resposta["content"] if bloco["type"] == "tool_use"]


def simular(mensagem):
    # Sem chave: devolve uma proposta fixa de troca, para o resto do programa rodar igual.
    print("[modo simulado: sem chave de API, a resposta do modelo é fixa]")
    if "Carlos" not in mensagem:
        return []
    return [{"type": "tool_use", "name": "change_driver",
             "input": {"carga": "C-9281", "motorista": "Carlos", "veiculo": "R-12"}}]


def responder(system, mensagem, modelo, esforco=None):
    """Aula 7: uma pergunta e a resposta em texto, para o juiz. Precisa de chave."""
    corpo = {"model": modelo, "max_tokens": 2000, "system": system, "messages": [{"role": "user", "content": mensagem}]}
    if esforco:  # "low" pensa menos: o juiz rápido, que responde sem raciocinar
        corpo["output_config"] = {"effort": esforco}
    cabecalhos = {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"}
    req = urllib.request.Request(URL, data=json.dumps(corpo).encode(), headers=cabecalhos)
    with urllib.request.urlopen(req, timeout=120) as r:
        resposta = json.load(r)
    return " ".join(b["text"] for b in resposta["content"] if b["type"] == "text").strip()
