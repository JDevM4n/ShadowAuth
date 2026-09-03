from shadowauth.extractors.feature_extractor import FeatureExtractor
from shadowauth.features.feature_vector import FeatureVector
from shadowauth.models.normalized_event import NormalizedEvent


class SessionFeatureExtractor(FeatureExtractor):
    """
    Extracts behavioral features from a session composed of
    multiple NormalizedEvent objects.
    """

    SHELL_NAMES = {
        "bash",
        "sh",
        "zsh",
        "dash",
        "ksh",
        "fish",
    }

    SENSITIVE_PATHS = (
        "/etc/passwd",
        "/etc/shadow",
        "/etc/sudoers",
        "/root/",
        "/.ssh/",
        "id_rsa",
        "authorized_keys",
    )

    def extract(
        self,
        events: list[NormalizedEvent],
        label: str = "unlabeled",
    ) -> FeatureVector:

        if not events:
            raise ValueError("Event list cannot be empty.")

        events = sorted(
            events,
            key=lambda event: event.event_timestamp,
        )

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

            unique_command_count=self._count_unique_commands(events),

            login_attempts=self._count_login_attempts(events),

            successful_login=self._successful_login(events),

            download_count=self._count_downloads(events),

            # ---------- Network ----------

            source_ip=first_event.network.source_ip,

            destination_ip=first_event.network.destination_ip,

            source_port=first_event.network.source_port,

            destination_port=first_event.network.destination_port,

            protocol=first_event.network.protocol,

            # ---------- Host / Falco ----------

            process_count=self._count_processes(events),

            shell_spawned=self._shell_spawned(events),

            sensitive_file_access=self._sensitive_file_access(events),

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

            label=label,
        )

    def _count_commands(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        return sum(
            1
            for event in events
            if event.event_type == "cowrie.command.input"
        )

    def _count_unique_commands(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        commands = {
            str(event.data.get("input", "")).strip()
            for event in events
            if (
                event.event_type == "cowrie.command.input"
                and event.data.get("input")
            )
        }

        return len(commands)

    def _count_login_attempts(
        self,
        events: list[NormalizedEvent],
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
        events: list[NormalizedEvent],
    ) -> bool:

        return any(
            event.event_type == "cowrie.login.success"
            for event in events
        )

    def _count_downloads(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        return sum(
            1
            for event in events
            if event.event_type == "cowrie.session.file_download"
        )

    def _count_processes(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        process_ids = {
            event.host.pid
            for event in events
            if (
                event.source == "falco"
                and event.host.pid is not None
            )
        }

        return len(process_ids)

    def _shell_spawned(
        self,
        events: list[NormalizedEvent],
    ) -> bool:

        for event in events:

            if event.source != "falco":
                continue

            process_name = (
                event.host.process_name or ""
            ).lower()

            rule_name = (
                event.rule_name or event.event_type or ""
            ).lower()

            output = str(
                event.data.get("output", "")
            ).lower()

            if process_name in self.SHELL_NAMES:
                return True

            if "shell" in rule_name:
                return True

            if "shell" in output:
                return True

        return False

    def _sensitive_file_access(
        self,
        events: list[NormalizedEvent],
    ) -> bool:

        for event in events:

            if event.source != "falco":
                continue

            output_fields = event.data.get(
                "output_fields",
                {},
            )

            file_name = str(
                output_fields.get("fd.name", "")
            ).lower()

            output = str(
                event.data.get("output", "")
            ).lower()

            text = f"{file_name} {output}"

            if any(
                path.lower() in text
                for path in self.SENSITIVE_PATHS
            ):
                return True

        return False

    def _calculate_duration(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        timestamps = [
            event.event_timestamp
            for event in events
        ]

        return int(
            (
                max(timestamps)
                - min(timestamps)
            ).total_seconds()
        )