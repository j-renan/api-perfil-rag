from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory,
)
from infrastructure.database.postgres_unit_of_work import (
    PostgresUnitOfWork,
)

unit_of_work = PostgresUnitOfWork(
    connection_factory=PostgresConnectionFactory()
)

with unit_of_work as uow:
    existe = uow.documento_repository.existe("flask.txt")

if existe:
    print("O documento 'flask.txt' já está cadastrado.")
else:
    print("O documento 'flask.txt' ainda não está cadastrado.")