from app import app

print("Aplicação Flask importada com sucesso!")

print("Rotas registradas:")

for regra in app.url_map.iter_rules():
    print(regra)

# import os
#
# from app import DIRETORIO_DOCUMENTOS
#
# nome = "teste-rag-chunks.txt"
#
# caminho = os.path.join(
#     DIRETORIO_DOCUMENTOS,
#     nome,
# )
#
# if os.path.isfile(caminho):
#     print("Arquivo de teste encontrado!")
#     print("Tamanho:", os.path.getsize(caminho), "bytes")
# else:
#     print("Arquivo de teste não encontrado!")

# from groq import Groq
#
# print("SDK Groq importado com sucesso!")

# from ports.llm_service import LLMService
#
# print("Interface LLMService importada com sucesso!")


# from application.use_cases.responder_pergunta import ResponderPergunta
#
# print("Caso de uso ResponderPergunta importado com sucesso!")
