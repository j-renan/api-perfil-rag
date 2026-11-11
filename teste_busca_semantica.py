from database import criar_conexao

from application.use_cases.buscar_chunks_semelhantes import (
    BuscarChunksSemelhantes
)

from infrastructure.embeddings.sentence_transformer_service import (
    SentenceTransformerEmbeddingService
)

from infrastructure.repositories.postgres_chunk_repository import (
    PostgresChunkRepository
)


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


conexao = criar_conexao()

if conexao is None:
    raise RuntimeError(
        "Não foi possível conectar ao banco de dados."
    )


embedding_service = SentenceTransformerEmbeddingService(
    model_name=MODEL_NAME
)

repository = PostgresChunkRepository(
    conexao=conexao
)


use_case = BuscarChunksSemelhantes(
    repository=repository,
    embedding_service=embedding_service
)


pergunta = "Quais tecnologias eu conheço?"


resultados = use_case.executar(
    pergunta=pergunta,
    limite=5
)


print(f"\nPergunta: {pergunta}")
print(f"Quantidade de resultados: {len(resultados)}")
print("\nResultados:\n")


for resultado in resultados:
    print(
        f"ID: {resultado.id}\n"
        f"Documento: {resultado.documento_id}\n"
        f"Chunk: {resultado.chunk_id}\n"
        f"Texto: {resultado.texto}\n"
        f"{'-' * 60}"
    )


conexao.close()