from shadowauth.models.normalized_event import NormalizedEvent


class EventCollector:
    """
    Receives normalized events from any parser.

    The collector does not know whether the event comes from
    Cowrie, Falco, Zeek, or any other source. It only works
    with the common NormalizedEvent contract.
    """

    def collect(self, event: NormalizedEvent) -> None:
        """
        Receive a normalized event.
        """

        print("=" * 50)
        print("Event received")
        print("=" * 50)
        print(f"Source       : {event.source}")
        print(f"Event Type   : {event.event_type}")
        print(f"Session ID   : {event.session_id}")
        print(f"Timestamp    : {event.event_timestamp}")
        print("=" * 50)