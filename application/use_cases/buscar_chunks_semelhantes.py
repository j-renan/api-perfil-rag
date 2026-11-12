
from domain.models import Chunk
from ports.embedding_service import EmbeddingService
from ports.unit_of_work import UnitOfWork
from application.services.montador_contexto import MontadorContexto


class BuscarChunksSemelhantes:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        embedding_service: EmbeddingService,
        montador_contexto: MontadorContexto,
    ) -> None:
        self.unit_of_work = unit_of_work
        self.embedding_service = embedding_service
        self.montador_contexto = montador_contexto

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

    def executar_com_contexto(
        self,
        pergunta: str,
        limite: int = 5,
        similaridade_minima: float = 0.40,
    ) -> str:

        chunks = self.executar(
            pergunta=pergunta,
            limite=limite,
            similaridade_minima=similaridade_minima,
        )

        return self.montador_contexto.montar(chunks)
