from psycopg2.extensions import connection

from ports.documento_repository import DocumentoRepository


class PostgresDocumentoRepository(DocumentoRepository):

    def __init__(self, conexao: connection) -> None:
        self.conexao = conexao

    def salvar(self, nome: str) -> int:
        sql = """
            INSERT INTO documentos (nome)
            VALUES (%s)
            RETURNING id
        """

        with self.conexao.cursor() as cursor:
            cursor.execute(sql, (nome,))
            resultado = cursor.fetchone()

        return resultado[0]

    def existe(self, nome: str) -> bool:
        sql = """
            SELECT EXISTS (
                SELECT 1
                FROM documentos
                WHERE nome = %s
            )
        """

        with self.conexao.cursor() as cursor:
            cursor.execute(sql, (nome,))
            resultado = cursor.fetchone()

        return resultado[0]