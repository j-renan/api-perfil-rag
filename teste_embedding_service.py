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


textos = [
    "Python é uma linguagem de programação.",
    "Flask é um microframework web.",
    "Eu trabalho com desenvolvimento Full-Stack."
]


embeddings = embedding_service.gerar_embeddings(
    textos
)


print(f"Quantidade de embeddings: {len(embeddings)}")
print(f"Dimensão do primeiro embedding: {len(embeddings[0])}")
print(f"Dimensão do segundo embedding: {len(embeddings[1])}")
print(f"Dimensão do terceiro embedding: {len(embeddings[2])}")

print("\nPrimeiros valores do primeiro embedding:")
print(embeddings[0][:5])