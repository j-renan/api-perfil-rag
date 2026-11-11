from app import app
from flask_jwt_extended import create_access_token

# Gera um token JWT válido para o teste.
with app.app_context():
    token = create_access_token(identity="usuario-teste")

# Cria o cliente de testes.
cliente = app.test_client()

# Configura o cabeçalho de autenticação.
headers = {
    "Authorization": f"Bearer {token}"
}

# Executa a rota.
resposta = cliente.post(
    "/processar-documento",
    headers=headers
)

print("Status HTTP:", resposta.status_code)
print("Resposta:", resposta.get_json())

# Valida o comportamento esperado.
assert resposta.status_code == 400
assert "já está cadastrado" in resposta.get_json()["erro"]

print("Teste de documento duplicado aprovado!")