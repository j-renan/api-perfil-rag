from psycopg2.extensions import connection

from domain.models import Chunk
from ports.chunk_repository import ChunkRepository


class PostgresChunkRepository(ChunkRepository):

    def __init__(self, conexao: connection):
        self.conexao = conexao

    def _formatar_embedding(self, embedding: list[float]) -> str:
        return "[" + ",".join(str(valor) for valor in embedding) + "]"

    def _converter_embedding(self, embedding: str) -> list[float]:
        valores = embedding.strip("[]").split(",")
        return [float(valor) for valor in valores]

    def salvar(self, chunk: Chunk) -> Chunk:
        if chunk.embedding is None:
            raise ValueError("O chunk precisa possuir um embedding.")

        sql = """INSERT INTO chunks (documento_id, chunk_id, texto, embedding)
            VALUES (%s, %s, %s, %s) RETURNING id"""

        embedding = self._formatar_embedding(chunk.embedding)

        with self.conexao.cursor() as cursor:
            cursor.execute(sql, (
                    chunk.documento_id,
                    chunk.chunk_id,
                    chunk.texto,
                    embedding
                )
            )
            resultado = cursor.fetchone()
        self.conexao.commit()
        chunk.id = resultado[0]
        return chunk

    def buscar_semelhantes(
            self,
            embedding: list[float],
            limite: int = 5
    ) -> list[Chunk]:

        if not embedding:
            raise ValueError(
                "O embedding não pode estar vazio."
            )

        if limite <= 0:
            raise ValueError(
                "O limite deve ser maior que zero."
            )

        sql = """
            SELECT
                id,
                documento_id,
                chunk_id,
                texto,
                embedding
            FROM chunks
            ORDER BY embedding <=> %s
            LIMIT %s
        """

        embedding_formatado = self._formatar_embedding(embedding)

        with self.conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    embedding_formatado,
                    limite
                )
            )

            resultados = cursor.fetchall()

        return [
            Chunk(
                id=registro[0],
                documento_id=registro[1],
                chunk_id=registro[2],
                texto=registro[3],
                embedding=self._converter_embedding(registro[4])
            )
            for registro in resultados
        ]