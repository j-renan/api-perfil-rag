from psycopg2.extensions import connection

from database import criar_conexao
from ports.connection_factory import ConnectionFactory


class PostgresConnectionFactory(ConnectionFactory):
    def criar_conexao(self) -> connection:
        conexao = criar_conexao()

        if conexao is None:
            raise RuntimeError(
                "Não foi possível conectar ao banco de dados."
            )

        return conexao