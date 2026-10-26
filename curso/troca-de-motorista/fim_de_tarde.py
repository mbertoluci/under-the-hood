# O fim de tarde (aula 4): a Maria autoriza às 17:00 e perde o acesso às 17:30. O despacho é às 17:40.
# Uso: python fim_de_tarde.py --ingenuo            (confia na autorização gravada)
#      python fim_de_tarde.py [--solucao]          (pergunta de novo, com o seu revalidar.py ou o da solução)
#      python fim_de_tarde.py --solucao --escala   (a Maria continua, mas o Carlos vai para outra carga às 17:35)
import sys, time

from autenticacao import emitir, sinal_do_botao, usuario_do_token
from operacao import PAPEIS, resumo
from revalidar import conteudo

if "--solucao" in sys.argv:
    from solucao.revalidar import pode_executar
elif "--ingenuo" not in sys.argv:
    from revalidar import pode_executar

DIA = time.mktime((2026, 10, 14, 0, 0, 0, 0, 0, -1))


def as_(hora):
    h, m = map(int, hora.split(":"))
    return DIA + h * 3600 + m * 60


B17 = {"id": "B-17", "acao": "change_driver", "carga": "C-9281", "motorista": "Carlos", "veiculo": "R-12", "versao": 1}
agora = {"papeis": dict(PAPEIS), "cargas": {"C-9281": "aguardando motorista", "C-9300": "aguardando motorista"},
         "escalas": {"Carlos": None}}

# 17:00: o login e o botão da aula 1, com um JWT de verdade.
token = emitir("maria", validade=3600, agora=as_("17:00"))
botao = {"headers": {"Authorization": f"Bearer {token}"}, "corpo": {"botao": "autorizo", "proposta": "B-17"}}
sinal = sinal_do_botao(botao, agora=as_("17:00"))
validade = time.strftime("%H:%M", time.localtime(as_("17:00") + 3600))
print(f'17:00 {sinal["origem"]} aperta "autorizo" no app, com um token que vale até {validade}')
autorizacao = {"plano": "B-17", "quem": sinal["origem"], "papel": agora["papeis"][sinal["origem"]],
               "resumo": resumo(conteudo(B17)), "hora": "17:00"}
print(f'17:00 autorização gravada: B-17, {autorizacao["quem"]} ({autorizacao["papel"]})')

if "--escala" in sys.argv:
    agora["escalas"]["Carlos"] = "C-9300"
    print("17:35 o Carlos é escalado para a carga C-9300")
else:
    del agora["papeis"]["maria"]
    print("17:30 a maria sai da XPTO, e o acesso dela é removido do cadastro")

vale = "sim" if usuario_do_token(token, as_("17:40")) else "não"
print(f"17:40 o token da maria ainda vale? {vale}")
if "--ingenuo" in sys.argv:
    # Confia no que foi gravado às 17:00: o conteúdo e o papel daquela hora.
    ok, motivo = autorizacao["papel"] == "solicitante" and autorizacao["resumo"] == resumo(conteudo(B17)), ""
else:
    ok, motivo = pode_executar(autorizacao, B17, agora)
if ok:
    print(f"17:40 despacho: executado: C-9281 motorista Carlos (R-12), autorizado por {autorizacao['quem']} às 17:00")
else:
    print(f"17:40 despacho: não executa: {motivo}")
    print("      volta para a despachante, com o motivo")
