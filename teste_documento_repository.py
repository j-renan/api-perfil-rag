from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory
)

from infrastructure.repositories.documento_repository import (
    PostgresDocumentoRepository
)


connection_factory = PostgresConnectionFactory()

repository = PostgresDocumentoRepository(
    connection_factory=connection_factory
)


documento_id = repository.salvar(
    "documento-teste-6-9-2.txt"
)


print(
    f"Documento criado com ID: {documento_id}"
)