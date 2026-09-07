from shadowauth.collectors.event_collector import EventCollector
from shadowauth.database.postgres_repository import PostgresRepository
from shadowauth.models.normalized_event import NormalizedEvent


class PostgresEventCollector(EventCollector):
    """
    Persists normalized ShadowAuth events
    into PostgreSQL.
    """

    def __init__(
        self,
        repository=None,
    ):
        self.repository = (
            repository
            or PostgresRepository()
        )

    def collect(
        self,
        event: NormalizedEvent,
    ) -> None:

        self.repository.save_event(
            event
        )
