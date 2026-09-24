from domain.models import Chunk
from application.use_cases.buscar_chunks_semelhantes import (
    BuscarChunksSemelhantes
)


class FakeEmbeddingService:

    def gerar_embedding(self, texto: str) -> list[float]:
        print(f"Gerando embedding para: {texto}")

        return [0.1] * 384


class FakeChunkRepository:

    def buscar_semelhantes(
        self,
        embedding: list[float],
        limite: int = 5
    ) -> list[Chunk]:

        print(f"Dimensão do embedding: {len(embedding)}")
        print(f"Limite solicitado: {limite}")

        return [
            Chunk(
                id=1,
                documento_id=1,
                chunk_id=1,
                texto="Python é uma linguagem de programação.",
                embedding=embedding
            )
        ]


embedding_service = FakeEmbeddingService()
repository = FakeChunkRepository()

use_case = BuscarChunksSemelhantes(
    repository=repository,
    embedding_service=embedding_service
)

resultados = use_case.executar(
    pergunta="Quais tecnologias eu conheço?",
    limite=5
)

for resultado in resultados:
    print(resultado)