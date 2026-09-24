import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection

load_dotenv()


def criar_conexao() -> connection | None:
    try:
        if os.environ.get("DB_HOST") == "localhost":
            conn = psycopg2.connect(
                host=os.environ.get("DB_HOST"),
                database=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                sslmode="disable",
                channel_binding="disable"
            )
        else:
            conn = psycopg2.connect(
                host=os.environ.get("DB_HOST"),
                database=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                sslmode=os.environ.get("DB_SSLMODE"),
                channel_binding=os.environ.get("DB_CHANNEL_BINDING")
            )

        return conn

    except Exception as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None


def testar_conexao() -> str:
    conexao = None
    try:
        conexao = criar_conexao()
        return f"Status de conexão do banco de dados: {conexao}"
    except Exception as erro:
        return f"Erro ao testar conexão com o banco de dados: {erro}"
    finally:
        if conexao:
            conexao.close()