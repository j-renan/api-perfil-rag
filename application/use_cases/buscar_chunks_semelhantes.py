
from domain.models import Chunk
from ports.embedding_service import EmbeddingService
from ports.unit_of_work import UnitOfWork


class BuscarChunksSemelhantes:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        embedding_service: EmbeddingService,
    ) -> None:
        self.unit_of_work = unit_of_work
        self.embedding_service = embedding_service

    def executar(
            self,
            pergunta: str,
            limite: int = 5,
            similaridade_minima: float = 0.40,
    ) -> list[Chunk]:

        if not pergunta.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        if limite <= 0:
            raise ValueError("O limite deve ser maior que zero.")

        if not -1 <= similaridade_minima <= 1:
            raise ValueError(
                "A similaridade mínima deve estar entre -1 e 1."
            )

        embedding = self.embedding_service.gerar_embedding(pergunta)

        with self.unit_of_work as uow:
            resultados = uow.chunk_repository.buscar_semelhantes(
                embedding=embedding,
                limite=limite,
            )

            resultados_filtrados = [
                chunk
                for chunk in resultados
                if (
                        chunk.distancia is not None
                        and (1 - chunk.distancia) >= similaridade_minima
                )
            ]

            return resultados_filtrados

