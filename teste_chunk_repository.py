from database import criar_conexao
from domain.models import Chunk
# from infrastructure.repositories.postgres_chunk_repository import PostgresChunkRepository

from infrastructure.repositories.postgres_chunk_repository import (
    PostgresChunkRepository
)


conexao = criar_conexao()

if conexao is None:
    raise RuntimeError("Não foi possível conectar ao banco de dados.")


repository = PostgresChunkRepository(conexao)

embedding_teste = [0.1] * 384

chunks = repository.buscar_semelhantes(
    embedding=embedding_teste,
    limite=5
)

for chunk in chunks:
    print(
        f"id={chunk.id}, "
        f"documento_id={chunk.documento_id}, "
        f"chunk_id={chunk.chunk_id}, "
        f"texto={chunk.texto}, "
        f"tipo_embedding={type(chunk.embedding)}, "
        f"dimensao={len(chunk.embedding) if chunk.embedding else 0}"
    )

conexao.close()

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