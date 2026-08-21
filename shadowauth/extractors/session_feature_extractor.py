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

            duration_seconds=0,

            command_count=len(events),

            unique_command_count=0,

            login_attempts=0,

            successful_login=False,

            download_count=0,

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
        )