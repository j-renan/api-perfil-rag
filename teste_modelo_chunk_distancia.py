
from domain.models import Chunk


# Teste 1: criar um chunk sem informar a distância
chunk_sem_distancia = Chunk(
    documento_id=7,
    chunk_id=1,
    texto="Teste de busca semântica."
)

assert chunk_sem_distancia.distancia is None


# Teste 2: criar um chunk informando a distância
chunk_com_distancia = Chunk(
    documento_id=7,
    chunk_id=2,
    texto="PostgreSQL utiliza pgvector.",
    distancia=0.15
)

assert chunk_com_distancia.distancia == 0.15


print("Chunk sem distância:", chunk_sem_distancia.distancia)
print("Chunk com distância:", chunk_com_distancia.distancia)
print("Todos os testes passaram!")
