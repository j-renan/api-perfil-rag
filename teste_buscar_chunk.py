
from application.use_cases.buscar_chunks_semelhantes import (
    BuscarChunksSemelhantes,
)

from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory,
)

from infrastructure.database.postgres_unit_of_work import (
    PostgresUnitOfWork,
)

from infrastructure.embeddings.sentence_transformer_service import (
    SentenceTransformerEmbeddingService,
)


# Configuração do modelo de embeddings
MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


# Inicialização das dependências
connection_factory = PostgresConnectionFactory()

unit_of_work = PostgresUnitOfWork(
    connection_factory=connection_factory
)

embedding_service = SentenceTransformerEmbeddingService(
    model_name=MODEL_NAME
)


# Inicialização do caso de uso
buscar_chunks = BuscarChunksSemelhantes(
    unit_of_work=unit_of_work,
    embedding_service=embedding_service,
)


# Executar a busca semântica
pergunta = "O que é Flask?"

resultados = buscar_chunks.executar(
    pergunta=pergunta,
    limite=5,
)


# Exibir os resultados
print(f"Pergunta: {pergunta}")
print(f"Quantidade de resultados: {len(resultados)}")
print("-" * 50)

for resultado in resultados:
    print(f"ID: {resultado.id}")
    print(f"Documento: {resultado.documento_id}")
    print(f"Chunk: {resultado.chunk_id}")
    print(f"Texto: {resultado.texto}")
    print("-" * 50)


# Verificar o encerramento da conexão
conexao = unit_of_work.connection

assert conexao is not None
assert conexao.closed == 1

print("Conexão PostgreSQL encerrada corretamente!")
print("Teste de busca semântica concluído com sucesso!")
