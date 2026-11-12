
from application.dtos.resposta_rag import RespostaRAG
from application.use_cases.buscar_chunks_semelhantes import (
    BuscarChunksSemelhantes,
)
from ports.llm_service import LLMService


class ResponderPergunta:
    def __init__(
        self,
        buscar_chunks: BuscarChunksSemelhantes,
        llm_service: LLMService,
    ) -> None:
        self.buscar_chunks = buscar_chunks
        self.llm_service = llm_service

    def executar(
        self,
        pergunta: str,
        limite: int = 5,
        similaridade_minima: float = 0.40,
    ) -> RespostaRAG:

        if not pergunta.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        contexto = self.buscar_chunks.executar_com_contexto(
            pergunta=pergunta,
            limite=limite,
            similaridade_minima=similaridade_minima,
        )

        if not contexto:
            return RespostaRAG(
                pergunta=pergunta,
                contexto="",
                resposta=(
                    "Não encontrei informações relevantes "
                    "nos documentos disponíveis para responder."
                ),
            )

        resposta = self.llm_service.gerar_resposta(
            pergunta=pergunta,
            contexto=contexto,
        )

        return RespostaRAG(
            pergunta=pergunta,
            contexto=contexto,
            resposta=resposta,
        )
