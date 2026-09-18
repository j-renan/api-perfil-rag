from sentence_transformers import SentenceTransformer
from sentence_transformers import util

modelo_embedding = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

textos = [
    "Flask é um framework Python.",
    "Flask permite criar APIs utilizando Python.",
    "O Brasil possui cinco regiões."
]

embeddings = modelo_embedding.encode(textos)


print("\nEmbedding:")
print(embeddings.shape)

# print("\nVetores:")
# for indice, embedding in enumerate(embeddings):
#     print(f"Texto {indice + 1}")
#     print(embedding)
#     print("-" * 50)

similaridade_1_2 = util.cos_sim(
    embeddings[0],
    embeddings[1]
)

similaridade_1_3 = util.cos_sim(
    embeddings[0],
    embeddings[2]
)

print("Similaridade entre texto 1 e texto 2:")
print(similaridade_1_2)

print()

print("Similaridade entre texto 1 e texto 3:")
print(similaridade_1_3)

pergunta = "Quais tecnologias podem ser usadas para criar APIs?"

embedding_pergunta = modelo_embedding.encode(
    pergunta
)

print(embedding_pergunta.shape)