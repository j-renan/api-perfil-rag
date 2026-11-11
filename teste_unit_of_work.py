# from ports.unit_of_work import UnitOfWork
#
# print("UnitOfWork importado com sucesso!")

from infrastructure.repositories.documento_repository import (
    PostgresDocumentoRepository,
)

from infrastructure.repositories.postgres_chunk_repository import (
    PostgresChunkRepository,
)

print("Repositórios atualizados e importados com sucesso!")