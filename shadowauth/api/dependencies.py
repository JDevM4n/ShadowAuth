from collections.abc import Generator

from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


def get_repository() -> Generator[
    PostgresRepository,
    None,
    None,
]:
    repository = PostgresRepository()

    try:
        yield repository
    finally:
        repository.connection.close()
