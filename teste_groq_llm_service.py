
from infrastructure.llm.groq_llm_service import GroqLLMService


# Inicializa o serviço de comunicação com a Groq.
llm_service = GroqLLMService()

# Informações fictícias que simulam os trechos recuperados pelo RAG.
contexto = """
O projeto utiliza Python e Flask para desenvolver APIs REST.
O banco de dados utilizado é PostgreSQL com a extensão pgvector.
O modelo de embeddings utilizado é paraphrase-multilingual-MiniLM-L12-v2.
"""

# Pergunta que será enviada ao modelo.
pergunta = "Quais tecnologias são utilizadas neste projeto?"

# Envia a pergunta e o contexto para o modelo.
resposta = llm_service.gerar_resposta(
    pergunta=pergunta,
    contexto=contexto,
)

print("Pergunta:")
print(pergunta)

print("\nResposta gerada pela Groq:")
print(resposta)
