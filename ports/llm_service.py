
from typing import Protocol


class LLMService(Protocol):

    def gerar_resposta(
        self,
        pergunta: str,
        contexto: str,
    ) -> str:
        """
        Gera uma resposta utilizando a pergunta e o contexto fornecidos.
        """
        ...
