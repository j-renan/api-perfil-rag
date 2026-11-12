
from app import app
from flask_jwt_extended import create_access_token

with app.app_context():
    token = create_access_token(identity="usuario-teste")

cliente = app.test_client()

headers = {
    "Authorization": f"Bearer {token}"
}

pergunta = "Qual banco de dados utiliza a extensão pgvector?"

resposta = cliente.get(
    "/buscar",
    headers=headers,
    query_string={
        "pergunta": pergunta
    },
)

print("Status HTTP:", resposta.status_code)

dados = resposta.get_json()

print("Pergunta:", dados.get("pergunta"))

print("-" * 60)
print("Resultados encontrados:")

for resultado in dados.get("resultados", []):
    print("-" * 60)
    print("Documento ID:", resultado["documento_id"])
    print("Chunk ID:", resultado["chunk_id"])
    print("Texto:", resultado["texto"])

assert resposta.status_code == 200

assert any(
    resultado["documento_id"] == 7
    for resultado in dados["resultados"]
), "O documento de teste não foi recuperado!"

print("-" * 60)
print("Teste de recuperação semântica aprovado!")
