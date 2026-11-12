
from application.dtos.resposta_rag import RespostaRAG


resultado = RespostaRAG(
    pergunta="O que é Flask?",
    contexto="Flask é um microframework web para Python.",
    resposta="Flask é um framework leve utilizado para desenvolver aplicações web."
)

print("DTO importado com sucesso!")
print(resultado)
