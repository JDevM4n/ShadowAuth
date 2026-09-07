from shadowauth.collectors.postgres_event_collector import (
    PostgresEventCollector,
)
from shadowauth.parsers.zeek_parser import (
    ZeekParser,
)


class FakeRepository:

    def __init__(self):
        self.saved_event = None

    def save_event(
        self,
        event,
    ):
        self.saved_event = event


def test_postgres_event_collector():

    repository = FakeRepository()

    collector = PostgresEventCollector(
        repository=repository
    )

    parser = ZeekParser()

    event = parser.parse(
        {
            "ts": 1788811200.0,
            "uid": "CCollector001",
            "id.orig_h": "192.168.2.50",
            "id.orig_p": 45000,
            "id.resp_h": "192.168.2.27",
            "id.resp_p": 2222,
            "proto": "tcp",
            "conn_state": "SF",
        }
    )

    collector.collect(
        event
    )

    assert (
        repository.saved_event
        is event
    )

    assert (
        repository.saved_event.source
        == "zeek"
    )

    assert (
        repository.saved_event.session_id
        is None
    )
