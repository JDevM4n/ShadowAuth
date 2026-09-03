import json

import shadowauth.database.postgres_repository as repository_module
from shadowauth.database.postgres_repository import PostgresRepository
from shadowauth.parsers.cowrie_parser import CowrieParser


class FakeCursor:

    def __init__(
        self,
        fetchone_results=None,
    ):

        self.executions = []

        self.fetchone_results = list(
            fetchone_results or []
        )

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

        self.executions.append(
            (
                query,
                params,
            )
        )

    def fetchone(self):

        if self.fetchone_results:

            return self.fetchone_results.pop(0)

        return None


class FakeConnection:

    def __init__(
        self,
        fetchone_results=None,
    ):

        self.cursor_instance = FakeCursor(
            fetchone_results=fetchone_results,
        )

        self.committed = False

    def cursor(self):

        return self.cursor_instance

    def commit(self):

        self.committed = True


def configure_database_environment(
    monkeypatch,
    fake_connection,
):

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


def load_sample_event():

    parser = CowrieParser()

    with open(
        "samples/raw/cowrie/controlled-session-01.jsonl",
        encoding="utf-8",
    ) as file:

        raw_event = json.loads(
            file.readline()
        )

    return parser.parse(
        raw_event
    )


def test_postgres_repository_save_event(
    monkeypatch,
):

    # Simulates PostgreSQL returning the event_id,
    # meaning the normalized event was really inserted.
    fake_connection = FakeConnection(
        fetchone_results=[
            ("inserted-event-id",),
        ]
    )

    configure_database_environment(
        monkeypatch,
        fake_connection,
    )

    event = load_sample_event()

    repository = PostgresRepository()

    repository.save_event(
        event
    )

    executions = (
        fake_connection
        .cursor_instance
        .executions
    )

    # First query:
    # normalized event insertion.
    assert len(executions) == 2

    event_query = executions[0][0]
    event_params = executions[0][1]

    assert (
        "INSERT INTO normalized_events"
        in event_query
    )

    assert (
        "ON CONFLICT (event_id) DO NOTHING"
        in event_query
    )

    assert (
        "RETURNING event_id"
        in event_query
    )

    assert (
        event_params[0]
        == event.event_id
    )

    # Second query:
    # session creation/update.
    session_query = executions[1][0]
    session_params = executions[1][1]

    assert (
        "INSERT INTO sessions"
        in session_query
    )

    assert (
        "ON CONFLICT (session_id)"
        in session_query
    )

    assert (
        "event_count ="
        in session_query
    )

    assert (
        session_params[0]
        == event.session_id
    )

    assert (
        fake_connection.committed
        is True
    )


def test_postgres_repository_duplicate_event_does_not_update_session(
    monkeypatch,
):

    # None simulates:
    #
    # ON CONFLICT (event_id) DO NOTHING
    #
    # PostgreSQL inserted no new event,
    # therefore RETURNING gives no row.
    fake_connection = FakeConnection(
        fetchone_results=[
            None,
        ]
    )

    configure_database_environment(
        monkeypatch,
        fake_connection,
    )

    event = load_sample_event()

    repository = PostgresRepository()

    repository.save_event(
        event
    )

    executions = (
        fake_connection
        .cursor_instance
        .executions
    )

    # Only normalized_events should be touched.
    assert len(executions) == 1

    assert (
        "INSERT INTO normalized_events"
        in executions[0][0]
    )

    assert (
        "INSERT INTO sessions"
        not in executions[0][0]
    )

    assert (
        fake_connection.committed
        is True
    )