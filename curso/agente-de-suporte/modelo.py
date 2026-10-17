# Chama a API de mensagens da Anthropic usando só a biblioteca padrão (sem pip install).
# Devolve as chamadas de ferramenta que o modelo propôs. Quem executa é quem chamou.
import json
import os
import re
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
    # Sem chave: devolve o que o modelo costuma propor (cancelar o pedido citado).
    print("[modo simulado: sem chave de API, a resposta do modelo é fixa]")
    numero = re.search(r"\b[A-Z]\d{3}\b", mensagem)
    if not numero:
        return []
    return [{"type": "tool_use", "name": "cancel_order",
             "input": {"order_id": numero.group()}}]
