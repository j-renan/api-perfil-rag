from sentence_transformers import SentenceTransformer

from ports.embedding_service import EmbeddingService


class SentenceTransformerEmbeddingService(EmbeddingService):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def gerar_embedding(self, texto: str) -> list[float]:
        if not texto.strip():
            raise ValueError(
                "O texto não pode estar vazio."
            )

        embedding = self.model.encode(texto)

        return embedding.tolist()