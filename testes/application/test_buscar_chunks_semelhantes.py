
from unittest.mock import Mock

import pytest

from domain.models import Chunk
from application.use_cases.buscar_chunks_semelhantes import (
    BuscarChunksSemelhantes,
)


@pytest.fixture
def dependencias():
    chunk_1 = Chunk(
        documento_id=7,
        chunk_id=1,
        texto="O PostgreSQL é um banco relacional.",
        distancia=0.20,
    )

    chunk_2 = Chunk(
        documento_id=7,
        chunk_id=2,
        texto="A extensão pgvector trabalha com embeddings.",
        distancia=0.30,
    )

    embedding_service = Mock()
    embedding_service.gerar_embedding.return_value = [0.1, 0.2, 0.3]

    chunk_repository = Mock()
    chunk_repository.buscar_semelhantes.return_value = [
        chunk_1,
        chunk_2,
    ]

    unit_of_work = Mock()
    unit_of_work.__enter__ = Mock(return_value=unit_of_work)
    unit_of_work.__exit__ = Mock(return_value=None)
    unit_of_work.chunk_repository = chunk_repository

    montador_contexto = Mock()
    montador_contexto.montar.return_value = (
        "[Documento: 7 | Trecho: 1]\n"
        "O PostgreSQL é um banco relacional.\n\n"
        "[Documento: 7 | Trecho: 2]\n"
        "A extensão pgvector trabalha com embeddings."
    )

    use_case = BuscarChunksSemelhantes(
        unit_of_work=unit_of_work,
        embedding_service=embedding_service,
        montador_contexto=montador_contexto,
    )

    return {
        "use_case": use_case,
        "unit_of_work": unit_of_work,
        "embedding_service": embedding_service,
        "chunk_repository": chunk_repository,
        "montador_contexto": montador_contexto,
        "chunk_1": chunk_1,
        "chunk_2": chunk_2,
    }


def test_executar_retorna_chunks_filtrados(dependencias):
    resultados = dependencias["use_case"].executar(
        pergunta="O que é pgvector?"
    )

    assert len(resultados) == 2
    assert resultados[0] == dependencias["chunk_1"]
    assert resultados[1] == dependencias["chunk_2"]


def test_executar_com_contexto_retorna_string(dependencias):
    contexto = dependencias["use_case"].executar_com_contexto(
        pergunta="O que é pgvector?"
    )

    assert isinstance(contexto, str)
    assert "PostgreSQL" in contexto
    assert "pgvector" in contexto


def test_executar_com_contexto_chama_montador(dependencias):
    dependencias["use_case"].executar_com_contexto(
        pergunta="O que é pgvector?"
    )

    dependencias["montador_contexto"].montar.assert_called_once_with(
        [
            dependencias["chunk_1"],
            dependencias["chunk_2"],
        ]
    )


def test_executar_rejeita_pergunta_vazia(dependencias):
    with pytest.raises(ValueError, match="pergunta não pode estar vazia"):
        dependencias["use_case"].executar(pergunta=" ")


def test_executar_rejeita_similaridade_invalida(dependencias):
    with pytest.raises(ValueError, match="similaridade mínima"):
        dependencias["use_case"].executar(
            pergunta="Teste",
            similaridade_minima=1.5,
        )
