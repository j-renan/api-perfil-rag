import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print("Chave Groq carregada com sucesso!")
else:
    print("Chave Groq não encontrada!")