from typing import Protocol

from domain.models import Chunk


class ChunkRepository(Protocol):

    def salvar(self, chunk: Chunk) -> Chunk:
        ...

    def buscar_semelhantes(
        self,
        embedding: list[float],
        limite: int = 5
    ) -> list[Chunk]:
        ...
