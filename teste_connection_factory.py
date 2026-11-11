from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory
)


factory = PostgresConnectionFactory()

conexao = factory.criar_conexao()

print(f"Tipo da conexão: {type(conexao)}")
print(f"Conexão aberta: {not conexao.closed}")

conexao.close()

print(f"Conexão fechada: {conexao.closed}")