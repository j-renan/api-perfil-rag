
from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory
)
from infrastructure.repositories.postgres_chunk_repository import (
    PostgresChunkRepository
)
from infrastructure.embeddings.sentence_transformer_service import (
    SentenceTransformerEmbeddingService
)

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

connection_factory = PostgresConnectionFactory()

repository = PostgresChunkRepository(
    connection_factory=connection_factory
)

embedding_service = SentenceTransformerEmbeddingService(
    model_name=MODEL_NAME
)

pergunta = "Teste do ChunkRepository"

embedding = embedding_service.gerar_embedding(pergunta)

resultados = repository.buscar_semelhantes(
    embedding=embedding,
    limite=5
)

print(f"Pergunta: {pergunta}")
print(f"Quantidade de resultados: {len(resultados)}")

for resultado in resultados:
    print("-" * 50)
    print(f"ID: {resultado.id}")
    print(f"Documento: {resultado.documento_id}")
    print(f"Chunk: {resultado.chunk_id}")
    print(f"Texto: {resultado.texto}")


# chunk = Chunk(
#     documento_id=1,
#     chunk_id=100,
#     texto="Este é um chunk criado para testar o Repository.",
#     embedding=[0.1] * 384
# )
#
# chunk_salvo = repository.salvar(chunk)
#
# print(chunk_salvo)
#
# conexao.close()