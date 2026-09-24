from typing import Protocol


class EmbeddingService(Protocol):

    def gerar_embedding(self, texto: str) -> list[float]:
        ...