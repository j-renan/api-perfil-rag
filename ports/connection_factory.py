from typing import Protocol
from psycopg2.extensions import connection


class ConnectionFactory(Protocol):
    def criar_conexao(self) -> connection:
        ...