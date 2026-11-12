
from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory,
)

connection_factory = PostgresConnectionFactory()
conexao = connection_factory.criar_conexao()

try:
    sql = """
        SELECT
            c.id,
            c.chunk_id,
            c.texto,
            LENGTH(c.texto) AS quantidade_caracteres,
            vector_dims(c.embedding) AS dimensao_embedding
        FROM chunks c
        INNER JOIN documentos d
            ON d.id = c.documento_id
        WHERE d.nome = %s
        ORDER BY c.chunk_id
    """

    with conexao.cursor() as cursor:
        cursor.execute(
            sql,
            ("teste-rag-chunks.txt",)
        )

        resultados = cursor.fetchall()

    print("Documento: teste-rag-chunks.txt")
    print(f"Quantidade de chunks encontrados: {len(resultados)}")
    print("-" * 60)

    for registro in resultados:
        print(f"ID no banco: {registro[0]}")
        print(f"Chunk ID: {registro[1]}")
        print(f"Caracteres: {registro[3]}")
        print(f"Dimensão do embedding: {registro[4]}")
        print(f"Texto: {registro[2]}")
        print("-" * 60)

    # Validações
    assert len(resultados) == 6, (
        "A quantidade de chunks encontrada está incorreta."
    )

    assert all(
        registro[4] == 384
        for registro in resultados
    ), "Foi encontrado um embedding com dimensão incorreta."

    print("Todos os chunks foram persistidos corretamente!")
    print("Todos os embeddings possuem 384 dimensões!")

finally:
    conexao.close()
