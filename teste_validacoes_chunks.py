
from app import dividir_em_chunks


texto = """
Python é uma linguagem de programação muito utilizada.
Flask é um framework para desenvolvimento de APIs.
PostgreSQL é um sistema gerenciador de banco de dados.
Docker permite empacotar aplicações em containers.
"""

tamanho = 100
overlap = 20

chunks = dividir_em_chunks(
    texto=texto,
    tamanho=tamanho,
    overlap=overlap,
)

# 1. Verifica a quantidade e a numeração dos chunks.
assert len(chunks) > 0

for indice, chunk in enumerate(chunks, start=1):
    assert chunk["chunk_id"] == indice
    assert chunk["texto"].strip()

    # Nenhum chunk deve ultrapassar o tamanho configurado.
    assert len(chunk["texto"]) <= tamanho

print("Teste de tamanho e identificação aprovado!")


# 2. Verifica a sobreposição entre chunks consecutivos.
for indice in range(len(chunks) - 1):
    atual = chunks[indice]["texto"]
    proximo = chunks[indice + 1]["texto"]

    sobreposicao = max(
        (
            quantidade
            for quantidade in range(
                1,
                min(len(atual), len(proximo)) + 1,
            )
            if atual.endswith(proximo[:quantidade])
        ),
        default=0,
    )

    print(
        f"Chunks {indice + 1} e {indice + 2}: "
        f"overlap encontrado = {sobreposicao} caracteres"
    )

    assert sobreposicao > 0

print("Teste de overlap aprovado!")


# 3. Verifica os parâmetros inválidos.
casos_invalidos = [
    {
        "texto": "Texto de teste",
        "tamanho": 0,
        "overlap": 0,
    },
    {
        "texto": "Texto de teste",
        "tamanho": 100,
        "overlap": -1,
    },
    {
        "texto": "Texto de teste",
        "tamanho": 100,
        "overlap": 100,
    },
    {
        "texto": "",
        "tamanho": 100,
        "overlap": 20,
    },
]

for caso in casos_invalidos:
    try:
        dividir_em_chunks(**caso)
        raise AssertionError(
            f"Era esperada uma exceção para: {caso}"
        )
    except ValueError as erro:
        print(f"Validação aprovada: {erro}")

print("Todos os testes de validação passaram!")
