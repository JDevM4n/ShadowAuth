from shadowauth.extractors.feature_extractor import FeatureExtractor
from shadowauth.features.feature_vector import FeatureVector
from shadowauth.models.normalized_event import NormalizedEvent


class SessionFeatureExtractor(FeatureExtractor):
    """
    Extracts behavioral features from a session composed of
    multiple NormalizedEvent objects.
    """

    def extract(
        self,
        events: list[NormalizedEvent],
        label: str = "attack",
    ) -> FeatureVector:

        if not events:
            raise ValueError("Event list cannot be empty.")

        first_event = events[0]

        severities = [
            event.severity
            for event in events
            if event.severity is not None
        ]

        return FeatureVector(

    # ---------- Session ----------

    session_id=first_event.session_id or "unknown",

    duration_seconds=self._calculate_duration(events),

    command_count=self._count_commands(events),

    unique_command_count=0,

    login_attempts=self._count_login_attempts(events),

    successful_login=self._successful_login(events),

    download_count=self._count_downloads(events),

    # ---------- Network ----------

    source_ip=first_event.network.source_ip,

    destination_ip=first_event.network.destination_ip,

    source_port=first_event.network.source_port,

    destination_port=first_event.network.destination_port,

    protocol=first_event.network.protocol,

    # ---------- Host ----------

    process_count=0,

    shell_spawned=False,

    sensitive_file_access=False,

    # ---------- Severity ----------

    max_severity=max(severities) if severities else 0,

    average_severity=(
        sum(severities) / len(severities)
        if severities else 0
    ),

    # ---------- Time ----------

    session_hour=first_event.event_timestamp.hour,

    weekend=first_event.event_timestamp.weekday() >= 5,

    # ---------- Machine Learning ----------

    label="attack",
)

    def _count_commands(
        self,
        events: list[NormalizedEvent]
    ) -> int:

        return sum(
            1
            for event in events
            if event.event_type == "cowrie.command.input"
        )

    def _count_login_attempts(
        self,
        events: list[NormalizedEvent]
    ) -> int:

        return sum(
            1
            for event in events
            if event.event_type in (
                "cowrie.login.failed",
                "cowrie.login.success",
            )
        )

    def _successful_login(
        self,
        events: list[NormalizedEvent]
    ) -> bool:

        return any(
            event.event_type == "cowrie.login.success"
            for event in events
        )

    def _count_downloads(
        self,
        events: list[NormalizedEvent]
    ) -> int:

        return sum(
            1
            for event in events
            if event.event_type == "cowrie.session.file_download"
        )

    def _calculate_duration(
        self,
        events: list[NormalizedEvent]
    ) -> int:

        first = events[0].event_timestamp
        last = events[-1].event_timestamp

        return int(
            (last - first).total_seconds()
        )
        