from app import app
from flask_jwt_extended import create_access_token


# Cria o cliente de testes do Flask.
client = app.test_client()

# Gera um token JWT para autenticação.
with app.app_context():
    token = create_access_token(identity="usuario_teste")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}


# --------------------------------------------------
# TESTE 1: Acesso sem autenticação
# --------------------------------------------------

resposta = client.post(
    "/perguntar",
    json={"pergunta": "O que é Flask?"},
)

print("\nTESTE 1 - Sem autenticação")
print("Status HTTP:", resposta.status_code)


# --------------------------------------------------
# TESTE 2: JSON sem pergunta
# --------------------------------------------------

resposta = client.post(
    "/perguntar",
    headers=headers,
    json={},
)

print("\nTESTE 2 - Pergunta ausente")
print("Status HTTP:", resposta.status_code)
print("Resposta:", resposta.json)


# --------------------------------------------------
# TESTE 3: Pergunta vazia
# --------------------------------------------------

resposta = client.post(
    "/perguntar",
    headers=headers,
    json={"pergunta": "   "},
)

print("\nTESTE 3 - Pergunta vazia")
print("Status HTTP:", resposta.status_code)
print("Resposta:", resposta.json)


# --------------------------------------------------
# TESTE 4: JSON inválido
# --------------------------------------------------

resposta = client.post(
    "/perguntar",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    },
    data="conteudo invalido",
)

print("\nTESTE 4 - JSON inválido")
print("Status HTTP:", resposta.status_code)
print("Resposta:", resposta.json)


# --------------------------------------------------
# TESTE 5: Pergunta válida
# --------------------------------------------------

resposta = client.post(
    "/perguntar",
    headers=headers,
    json={
        "pergunta": "Quais tecnologias são utilizadas no projeto?"
    },
)

print("\nTESTE 5 - Pergunta válida")
print("Status HTTP:", resposta.status_code)
print("Resposta:", resposta.json)
