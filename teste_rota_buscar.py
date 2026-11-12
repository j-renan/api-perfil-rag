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


# Pergunta utilizada nos testes
pergunta = "Qual banco de dados utiliza a extensão pgvector?"


# --------------------------------------------------
# FUNÇÃO AUXILIAR: Validar os resultados
# --------------------------------------------------

def validar_resultados(dados, similaridade_minima):
    assert "resultados" in dados

    for resultado in dados["resultados"]:
        assert "distancia" in resultado
        assert "similaridade" in resultado

        assert isinstance(resultado["distancia"], float)
        assert isinstance(resultado["similaridade"], float)

        assert resultado["distancia"] >= 0

        assert resultado["similaridade"] == round(
            1 - resultado["distancia"],
            6,
        )

        assert resultado["similaridade"] >= similaridade_minima


# --------------------------------------------------
# TESTE 1: Requisição sem autenticação
# --------------------------------------------------

resposta = cliente.get(
    "/buscar",
    query_string={"pergunta": pergunta},
)

print("TESTE 1: Acesso sem JWT")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 401

print("Resultado: aprovado!\n")


# --------------------------------------------------
# TESTE 2: Busca autenticada com threshold padrão
# --------------------------------------------------

resposta = cliente.get(
    "/buscar",
    query_string={"pergunta": pergunta},
    headers=headers,
)

print("TESTE 2: Busca autenticada com threshold padrão")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 200

dados = resposta.json

assert len(dados["resultados"]) > 0

validar_resultados(
    dados=dados,
    similaridade_minima=0.40,
)

print("Resultados encontrados com similaridade >= 0.40.")
print("Distância e similaridade validadas!")
print("Resultado: aprovado!\n")


# --------------------------------------------------
# TESTE 3: Busca com threshold personalizado (0.50)
# --------------------------------------------------

resposta = cliente.get(
    "/buscar",
    query_string={
        "pergunta": pergunta,
        "similaridade_minima": "0.50",
    },
    headers=headers,
)

print("TESTE 3: Busca com threshold personalizado (0.50)")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 200

dados = resposta.json

assert len(dados["resultados"]) > 0

validar_resultados(
    dados=dados,
    similaridade_minima=0.50,
)

print("Todos os resultados possuem similaridade >= 0.50.")
print("Resultado: aprovado!\n")


# --------------------------------------------------
# TESTE 4: Threshold com valor não numérico
# --------------------------------------------------

resposta = cliente.get(
    "/buscar",
    query_string={
        "pergunta": pergunta,
        "similaridade_minima": "abc",
    },
    headers=headers,
)

print("TESTE 4: Threshold não numérico")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 400
assert "erro" in resposta.json

print("Valor não numérico rejeitado corretamente.")
print("Resultado: aprovado!\n")


# --------------------------------------------------
# TESTE 5: Threshold fora do intervalo permitido
# --------------------------------------------------

resposta = cliente.get(
    "/buscar",
    query_string={
        "pergunta": pergunta,
        "similaridade_minima": "1.50",
    },
    headers=headers,
)

print("TESTE 5: Threshold fora do intervalo permitido")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 400
assert "erro" in resposta.json

print("Valor fora do intervalo rejeitado corretamente.")
print("Resultado: aprovado!\n")


# --------------------------------------------------
# TESTE 6: Pergunta vazia
# --------------------------------------------------

resposta = cliente.get(
    "/buscar",
    query_string={"pergunta": ""},
    headers=headers,
)

print("TESTE 6: Pergunta vazia")
print(f"Status HTTP: {resposta.status_code}")
print(f"Resposta: {resposta.json}")

assert resposta.status_code == 400

print("Resultado: aprovado!\n")


# --------------------------------------------------
# RESULTADO FINAL
# --------------------------------------------------

print("Todos os testes da rota /buscar passaram!")