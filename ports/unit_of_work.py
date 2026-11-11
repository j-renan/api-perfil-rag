from typing import Protocol

from ports.chunk_repository import ChunkRepository
from ports.documento_repository import DocumentoRepository


class UnitOfWork(Protocol):

    documento_repository: DocumentoRepository
    chunk_repository: ChunkRepository

    def __enter__(self) -> "UnitOfWork":
        ...

    def __exit__(
        self,
        tipo_excecao,
        excecao,
        traceback,
    ) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...