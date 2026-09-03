import json

import shadowauth.database.postgres_repository as repository_module

from shadowauth.database.postgres_repository import PostgresRepository
from shadowauth.parsers.cowrie_parser import CowrieParser


class FakeCursor:

    def __init__(self):

        self.query = None
        self.params = None

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):

        return False

    def execute(
        self,
        query,
        params=None,
    ):

        self.query = query
        self.params = params


class FakeConnection:

    def __init__(self):

        self.cursor_instance = FakeCursor()
        self.committed = False

    def cursor(self):

        return self.cursor_instance

    def commit(self):

        self.committed = True


def test_postgres_repository_save_event(
    monkeypatch,
):

    fake_connection = FakeConnection()

    monkeypatch.setattr(
        repository_module.psycopg,
        "connect",
        lambda **kwargs: fake_connection,
    )

    monkeypatch.setenv(
        "POSTGRES_HOST",
        "localhost",
    )

    monkeypatch.setenv(
        "POSTGRES_PORT",
        "5432",
    )

    monkeypatch.setenv(
        "POSTGRES_DB",
        "shadowauth",
    )

    monkeypatch.setenv(
        "POSTGRES_USER",
        "shadowauth",
    )

    monkeypatch.setenv(
        "POSTGRES_PASSWORD",
        "shadowauth",
    )

    parser = CowrieParser()

    with open(
        "samples/raw/cowrie/controlled-session-01.jsonl",
        encoding="utf-8",
    ) as file:

        raw_event = json.loads(
            file.readline()
        )

    event = parser.parse(
        raw_event
    )

    repository = PostgresRepository()

    repository.save_event(
        event
    )

    query = (
        fake_connection
        .cursor_instance
        .query
    )

    assert (
        "INSERT INTO normalized_events"
        in query
    )

    assert (
        "ON CONFLICT (event_id) DO NOTHING"
        in query
    )

    assert (
        fake_connection.committed
        is True
    )