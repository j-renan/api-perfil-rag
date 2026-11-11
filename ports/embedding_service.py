from typing import Protocol


class EmbeddingService(Protocol):

    def gerar_embedding(self, texto: str) -> list[float]:
        ...

    def gerar_embeddings(self, textos: list[str]) -> list[list[float]]:
        ...

