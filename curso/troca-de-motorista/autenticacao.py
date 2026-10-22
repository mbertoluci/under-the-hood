# O login do app: o servidor entrega um JWT assinado (HS256, só com a biblioteca padrão).
# Quando a Maria aperta o botão, o app manda esse token junto. O servidor confere a assinatura e a validade, e só
# então escreve no sinal quem apertou. A origem vem do token conferido, nunca do corpo da requisição.
import base64, hashlib, hmac, json, time

SEGREDO = b"segredo-do-servidor-so-para-o-exemplo"  # em produção: variável de ambiente ou cofre, nunca no código


def _b64(dados):
    return base64.urlsafe_b64encode(dados).rstrip(b"=").decode()


def _de_b64(texto):
    return base64.urlsafe_b64decode(texto + "=" * (-len(texto) % 4))


def emitir(usuario, validade=3600, agora=None):
    """O login: devolve um JWT com o usuário (sub) e a validade (exp), assinado com o SEGREDO."""
    agora = time.time() if agora is None else agora
    cabecalho = _b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    corpo = _b64(json.dumps({"sub": usuario, "exp": int(agora + validade)}).encode())
    assinatura = hmac.new(SEGREDO, f"{cabecalho}.{corpo}".encode(), hashlib.sha256).digest()
    return f"{cabecalho}.{corpo}.{_b64(assinatura)}"


def usuario_do_token(token, agora=None):
    """Confere a assinatura e a validade. Devolve o usuário (sub), ou None se o token não vale."""
    try:
        cabecalho, corpo, assinatura = token.split(".")
        if json.loads(_de_b64(cabecalho)).get("alg") != "HS256":
            return None  # nunca aceite o algoritmo que o próprio token escolhe (o golpe do "alg": "none")
        esperado = hmac.new(SEGREDO, f"{cabecalho}.{corpo}".encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(esperado, _de_b64(assinatura)):
            return None
        dados = json.loads(_de_b64(corpo))
    except (ValueError, AttributeError):
        return None
    agora = time.time() if agora is None else agora
    if not isinstance(dados.get("exp"), (int, float)) or dados["exp"] < agora:
        return None
    return dados.get("sub")


def sinal_do_botao(requisicao, agora=None):
    """Monta o sinal de um botão do app. Sem token válido, não existe sinal: o botão é descartado."""
    autorizacao = requisicao.get("headers", {}).get("Authorization", "")
    usuario = usuario_do_token(autorizacao.removeprefix("Bearer "), agora)
    if usuario is None:
        return None
    corpo = requisicao.get("corpo", {})
    return {"canal": "app", "origem": usuario, "botao": corpo.get("botao"), "proposta": corpo.get("proposta")}
