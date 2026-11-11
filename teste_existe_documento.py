from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory,
)
from infrastructure.repositories.documento_repository import (
    PostgresDocumentoRepository,
)

fabrica_conexoes = PostgresConnectionFactory()

repositorio = PostgresDocumentoRepository(
    connection_factory=fabrica_conexoes
)

nome_existente = "documento-teste-6-9-2.txt"
nome_inexistente = "documento-que-nao-existe-teste-987654.md"

assert repositorio.existe(nome_existente) is True
print(f"Documento existente confirmado: {nome_existente}")

assert repositorio.existe(nome_inexistente) is False
print(f"Documento inexistente confirmado: {nome_inexistente}")

print("\nTodos os testes passaram!")