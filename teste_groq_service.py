from dotenv import load_dotenv

from infrastructure.llm.groq_llm_service import GroqLLMService

load_dotenv()

servico = GroqLLMService()

print("Adaptador Groq inicializado com sucesso!")
print(f"Modelo configurado: {servico.model_name}")