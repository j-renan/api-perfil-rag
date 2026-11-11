from domain.models import Chunk, Documento

from application.dtos.chunk_entrada import ChunkEntrada

from ports.embedding_service import EmbeddingService
from ports.unit_of_work import UnitOfWork


class ProcessarDocumento:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        embedding_service: EmbeddingService,
    ) -> None:
        self.unit_of_work = unit_of_work
        self.embedding_service = embedding_service

    def executar(
        self,
        documento: Documento,
        chunks: list[ChunkEntrada],
    ) -> int:

        # 1. Validar o nome do documento.
        if not documento.nome.strip():
            raise ValueError(
                "O nome do documento não pode estar vazio."
            )

        # 2. Validar a quantidade de chunks.
        if not chunks:
            raise ValueError(
                "O documento precisa possuir pelo menos um chunk."
            )

        # 3. Extrair os textos dos chunks.
        textos = [
            chunk["texto"]
            for chunk in chunks
        ]

        # 4. Validar os textos.
        if any(not texto.strip() for texto in textos):
            raise ValueError(
                "Os chunks não podem possuir textos vazios."
            )

        # 5. Iniciar a unidade de trabalho.
        with self.unit_of_work as uow:

            # 6. Verificar se o documento já existe.
            if uow.documento_repository.existe(documento.nome):
                raise ValueError(
                    f"O documento '{documento.nome}' já está cadastrado."
                )

            # 7. Gerar os embeddings.
            embeddings = self.embedding_service.gerar_embeddings(
                textos
            )

            if len(embeddings) != len(chunks):
                raise ValueError(
                    "A quantidade de embeddings gerados "
                    "não corresponde à quantidade de chunks."
                )

            # 8. Salvar o documento.
            documento_id = uow.documento_repository.salvar(
                documento.nome
            )

            # 9. Salvar todos os chunks.
            for dados_chunk, embedding in zip(chunks, embeddings):

                chunk = Chunk(
                    documento_id=documento_id,
                    chunk_id=dados_chunk["chunk_id"],
                    texto=dados_chunk["texto"],
                    embedding=embedding,
                )

                uow.chunk_repository.salvar(chunk)

            # 10. Retornar o ID do documento.
            return documento_id