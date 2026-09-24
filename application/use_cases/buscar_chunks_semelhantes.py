from ports.chunk_repository import ChunkRepository
from ports.embedding_service import EmbeddingService
from domain.models import Chunk


class BuscarChunksSemelhantes:

    def __init__(
        self,
        repository: ChunkRepository,
        embedding_service: EmbeddingService
    ):
        self.repository = repository
        self.embedding_service = embedding_service

    def executar(self, pergunta: str, limite: int = 5) -> list[Chunk]:
        if not pergunta.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        if limite <= 0:
            raise ValueError("O limite deve ser maior que zero.")

        embedding = self.embedding_service.gerar_embedding(pergunta)

        return self.repository.buscar_semelhantes(
            embedding=embedding,
            limite=limite
        )