
from domain.models import Chunk
from application.services.montador_contexto import MontadorContexto


def test_montar_contexto_com_dois_chunks():
    chunks = [
        Chunk(
            documento_id=7,
            chunk_id=1,
            texto="O PostgreSQL é um banco de dados relacional."
        ),
        Chunk(
            documento_id=7,
            chunk_id=2,
            texto="A extensão pgvector permite trabalhar com embeddings."
        )
    ]

    montador = MontadorContexto()

    contexto = montador.montar(chunks)

    assert "[Documento: 7 | Trecho: 1]" in contexto
    assert "[Documento: 7 | Trecho: 2]" in contexto

    assert "O PostgreSQL é um banco de dados relacional." in contexto
    assert "A extensão pgvector permite trabalhar com embeddings." in contexto


def test_montar_contexto_preserva_ordem():
    chunks = [
        Chunk(
            documento_id=7,
            chunk_id=2,
            texto="Segundo trecho."
        ),
        Chunk(
            documento_id=7,
            chunk_id=1,
            texto="Primeiro trecho."
        )
    ]

    montador = MontadorContexto()

    contexto = montador.montar(chunks)

    assert contexto.index("Segundo trecho.") < contexto.index("Primeiro trecho.")


def test_montar_contexto_sem_chunks():
    montador = MontadorContexto()

    contexto = montador.montar([])

    assert contexto == ""
