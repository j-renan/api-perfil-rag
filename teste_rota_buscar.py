
from app import app
from flask_jwt_extended import create_access_token


# Criar um cliente de testes
cliente = app.test_client()


# Gerar um token JWT para autenticação
with app.app_context():
    token = create_access_token(identity="1")


# Preparar o cabeçalho de autenticação
headers = {
    "Authorization": f"Bearer {token}"
}


# --------------------------------------------------
# TESTE 1: Requisição sem autenticação
# --------------------------------------------------

resposta = cliente.get(
    "/buscar?pergunta=O que é Flask?"
)

print("TESTE 1: Acesso sem JWT")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 401

print("Resultado: aprovado!\n")


# --------------------------------------------------
# TESTE 2: Busca autenticada
# --------------------------------------------------

resposta = cliente.get(
    "/buscar",
    query_string={"pergunta": "Quem cagou na sala de aula?"},
    headers=headers,
)

print("TESTE 2: Busca autenticada")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 200
assert "resultados" in resposta.json
assert len(resposta.json["resultados"]) > 0

print("Resultado: aprovado!\n")


# --------------------------------------------------
# TESTE 3: Pergunta vazia
# --------------------------------------------------

resposta = cliente.get(
    "/buscar",
    query_string={"pergunta": ""},
    headers=headers,
)

print("TESTE 3: Pergunta vazia")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 400

print("Resultado: aprovado!\n")


print("Todos os testes da rota /buscar passaram!")
