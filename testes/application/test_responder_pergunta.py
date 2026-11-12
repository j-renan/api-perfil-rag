
from unittest.mock import Mock

import pytest

from application.dtos.resposta_rag import RespostaRAG
from application.use_cases.responder_pergunta import ResponderPergunta


@pytest.fixture
def buscar_chunks_mock():
    return Mock()


@pytest.fixture
def llm_service_mock():
    return Mock()


@pytest.fixture
def responder_pergunta(
    buscar_chunks_mock,
    llm_service_mock,
):
    return ResponderPergunta(
        buscar_chunks=buscar_chunks_mock,
        llm_service=llm_service_mock,
    )


def test_deve_gerar_resposta_com_contexto(
    responder_pergunta,
    buscar_chunks_mock,
    llm_service_mock,
):
    pergunta = "Quais tecnologias são utilizadas?"

    contexto = "O projeto utiliza Python, Flask e PostgreSQL."

    buscar_chunks_mock.executar_com_contexto.return_value = contexto

    llm_service_mock.gerar_resposta.return_value = (
        "O projeto utiliza Python, Flask e PostgreSQL."
    )

    resultado = responder_pergunta.executar(pergunta)

    assert isinstance(resultado, RespostaRAG)
    assert resultado.pergunta == pergunta
    assert resultado.contexto == contexto
    assert resultado.resposta == (
        "O projeto utiliza Python, Flask e PostgreSQL."
    )

    buscar_chunks_mock.executar_com_contexto.assert_called_once()
    llm_service_mock.gerar_resposta.assert_called_once_with(
        pergunta=pergunta,
        contexto=contexto,
    )


def test_nao_deve_chamar_llm_sem_contexto(
    responder_pergunta,
    buscar_chunks_mock,
    llm_service_mock,
):
    buscar_chunks_mock.executar_com_contexto.return_value = ""

    resultado = responder_pergunta.executar(
        pergunta="Qual é a tecnologia utilizada?"
    )

    assert resultado.contexto == ""
    assert "Não encontrei informações relevantes" in resultado.resposta

    llm_service_mock.gerar_resposta.assert_not_called()


def test_deve_rejeitar_pergunta_vazia(responder_pergunta):
    with pytest.raises(ValueError, match="A pergunta não pode estar vazia."):
        responder_pergunta.executar("   ")
