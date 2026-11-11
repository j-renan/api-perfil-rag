from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory,
)

from infrastructure.database.postgres_unit_of_work import (
    PostgresUnitOfWork,
)


connection_factory = PostgresConnectionFactory()

with PostgresUnitOfWork(connection_factory) as uow:

    assert uow.connection is not None
    assert uow.documento_repository is not None
    assert uow.chunk_repository is not None

    assert (
        uow.documento_repository.conexao
        is uow.connection
    )

    assert (
        uow.chunk_repository.conexao
        is uow.connection
    )

    print("Conexão compartilhada pelos dois repositórios!")
    print("DocumentoRepository inicializado!")
    print("ChunkRepository inicializado!")

print("Unit of Work finalizado com sucesso!")