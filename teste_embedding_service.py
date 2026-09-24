from infrastructure.embeddings.sentence_transformer_service import (
    SentenceTransformerEmbeddingService
)


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


embedding_service = SentenceTransformerEmbeddingService(
    model_name=MODEL_NAME
)


texto = "Quais tecnologias eu conheço?"


embedding = embedding_service.gerar_embedding(texto)


print(f"Tipo: {type(embedding)}")
print(f"Dimensão: {len(embedding)}")
print(f"Primeiros valores: {embedding[:5]}")