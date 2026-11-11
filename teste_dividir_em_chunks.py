
from app import dividir_em_chunks

texto = """
O Python é uma linguagem de programação de alto nível.
Sua sintaxe simples facilita o aprendizado e a manutenção
dos programas.

O Flask é um framework web desenvolvido em Python.
Ele permite construir aplicações web e APIs REST.
Sua arquitetura é simples e extensível.

O PostgreSQL é um sistema gerenciador de banco de dados
relacional. Ele oferece suporte a consultas SQL,
transações e integridade dos dados.
"""

chunks = dividir_em_chunks(
    texto=texto,
    tamanho=100,
    overlap=20,
)

print(f"Quantidade de chunks: {len(chunks)}")

for chunk in chunks:
    print("-" * 50)
    print(f"Chunk ID: {chunk['chunk_id']}")
    print(f"Caracteres: {len(chunk['texto'])}")
    print(f"Texto: {chunk['texto']}")
