
from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory,
)

from infrastructure.repositories.postgres_chunk_repository import (
    PostgresChunkRepository,
)

from infrastructure.embeddings.sentence_transformer_service import (
    SentenceTransformerEmbeddingService,
)


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

pergunta = "Qual banco de dados utiliza a extensão pgvector?"

connection_factory = PostgresConnectionFactory()

embedding_service = SentenceTransformerEmbeddingService(
    model_name=MODEL_NAME
)

conexao = connection_factory.criar_conexao()

try:
    repository = PostgresChunkRepository(conexao)

    embedding = embedding_service.gerar_embedding(pergunta)

    resultados = repository.buscar_semelhantes(
        embedding=embedding,
        limite=5,
    )

    print(f"Pergunta: {pergunta}")
    print("-" * 60)

    for resultado in resultados:
        print(f"Documento ID: {resultado.documento_id}")
        print(f"Chunk ID: {resultado.chunk_id}")
        print(f"Distância: {resultado.distancia:.6f}")
        print(f"Texto: {resultado.texto[:200]}")
        print("-" * 60)

    assert resultados, "Nenhum resultado foi encontrado."

    assert all(
        resultado.distancia is not None
        for resultado in resultados
    ), "Algum resultado não possui distância."

    distancias = [
        resultado.distancia
        for resultado in resultados
    ]

    assert distancias == sorted(distancias), (
        "Os resultados não estão ordenados por distância."
    )

    print("Todos os testes passaram!")

finally:
    conexao.close()
