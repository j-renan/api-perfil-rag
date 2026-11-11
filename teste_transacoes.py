from uuid import uuid4

from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory,
)
from infrastructure.database.postgres_unit_of_work import (
    PostgresUnitOfWork,
)


connection_factory = PostgresConnectionFactory()

# Nomes exclusivos para permitir executar o teste várias vezes.
sufixo = uuid4().hex

nome_commit = f"teste-commit-{sufixo}.md"
nome_rollback = f"teste-rollback-{sufixo}.md"


# ---------------------------------------------
# TESTE 1: COMMIT
# ---------------------------------------------

with PostgresUnitOfWork(connection_factory) as uow:

    documento_id = uow.documento_repository.salvar(nome_commit)

    print(f"Documento inserido: {documento_id}")

# Ao sair do bloco, o __exit__ executa commit().

with PostgresUnitOfWork(connection_factory) as uow:

    assert uow.documento_repository.existe(nome_commit) is True

print("COMMIT confirmado: documento encontrado no banco!")


# ---------------------------------------------
# TESTE 2: ROLLBACK
# ---------------------------------------------

try:
    with PostgresUnitOfWork(connection_factory) as uow:

        documento_id = uow.documento_repository.salvar(nome_rollback)

        print(f"Documento inserido: {documento_id}")

        # Simula uma falha durante o processamento.
        raise RuntimeError("Falha simulada durante o processamento.")

except RuntimeError as erro:
    print(f"Exceção capturada: {erro}")


with PostgresUnitOfWork(connection_factory) as uow:

    assert uow.documento_repository.existe(nome_rollback) is False

print("ROLLBACK confirmado: documento não encontrado no banco!")


# ---------------------------------------------
# LIMPEZA DOS REGISTROS DO TESTE
# ---------------------------------------------

with PostgresUnitOfWork(connection_factory) as uow:

    with uow.connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM documentos
            WHERE nome IN (%s, %s)
            """,
            (nome_commit, nome_rollback),
        )

print("Registros de teste removidos.")
print("\nTodos os testes de transação passaram!")