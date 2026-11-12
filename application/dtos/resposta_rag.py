
from dataclasses import dataclass


@dataclass
class RespostaRAG:
    pergunta: str
    contexto: str
    resposta: str
