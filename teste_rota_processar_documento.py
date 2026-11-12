
from app import app
from flask_jwt_extended import create_access_token

with app.app_context():
    token = create_access_token(identity="usuario-teste")

cliente = app.test_client()

headers = {
    "Authorization": f"Bearer {token}"
}

resposta = cliente.post(
"/processar-documento",
    headers=headers,
    json={
        "nome_arquivo": "teste-rag-chunks.txt"
    },
)

print("Status HTTP:", resposta.status_code)
print("Resposta:", resposta.get_json())

assert resposta.status_code == 201

dados = resposta.get_json()

assert dados["documento_id"] is not None
assert dados["quantidade_chunks"] > 1

print("Teste de processamento de documento aprovado!")
