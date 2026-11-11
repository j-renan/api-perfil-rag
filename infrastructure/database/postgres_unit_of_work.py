from psycopg2.extensions import connection

from ports.connection_factory import ConnectionFactory
from ports.unit_of_work import UnitOfWork

from infrastructure.repositories.documento_repository import (
    PostgresDocumentoRepository,
)
from infrastructure.repositories.postgres_chunk_repository import (
    PostgresChunkRepository,
)


class PostgresUnitOfWork(UnitOfWork):

    def __init__(
        self,
        connection_factory: ConnectionFactory,
    ) -> None:
        self.connection_factory = connection_factory
        self.connection: connection | None = None

        self.documento_repository: PostgresDocumentoRepository | None = None
        self.chunk_repository: PostgresChunkRepository | None = None

    def __enter__(self) -> "PostgresUnitOfWork":
        self.connection = self.connection_factory.criar_conexao()

        self.documento_repository = PostgresDocumentoRepository(
            conexao=self.connection
        )

        self.chunk_repository = PostgresChunkRepository(
            conexao=self.connection
        )

        return self

    def __exit__(
        self,
        tipo_excecao,
        excecao,
        traceback,
    ) -> None:

        try:
            if tipo_excecao is None:
                self.commit()
            else:
                self.rollback()
        finally:
            if self.connection is not None:
                self.connection.close()

    def commit(self) -> None:
        if self.connection is not None:
            self.connection.commit()

    def rollback(self) -> None:
        if self.connection is not None:
            self.connection.rollback()