from sentence_transformers import SentenceTransformer
from ports.embedding_service import EmbeddingService


class SentenceTransformerEmbeddingService(EmbeddingService):

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def _validar_texto(self, texto: str) -> None:
        if not texto.strip():
            raise ValueError("O texto não pode estar vazio.")

    def gerar_embedding(self, texto: str) -> list[float]:
        self._validar_texto(texto)
        embedding = self.model.encode(texto)
        return embedding.tolist()

    def gerar_embeddings(self, textos: list[str]) -> list[list[float]]:
        if not textos:
            return []

        for texto in textos:
            self._validar_texto(texto)

        embeddings = self.model.encode(textos)
        return embeddings.tolist()
