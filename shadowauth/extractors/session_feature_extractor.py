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

            failed_login_count=self._count_failed_logins(events),

            download_command_count=self._count_download_commands(events),

            executable_permission_count=self._count_executable_permissions(events),

            ransomware_extension_count=self._count_ransomware_extensions(events),

            ransom_note_count=self._count_ransom_notes(events),

            cpu_recon_count=self._count_cpu_recon(events),

            cryptomining_indicator_count=self._count_cryptomining_indicators(events),

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

    def _behavior_commands(
        self,
        events: list[NormalizedEvent],
    ) -> list[str]:
        """
        Return Cowrie commands used for behavioral analysis.

        Ground-truth marker commands are intentionally excluded
        to prevent label leakage into machine-learning features.
        """

        commands = []

        for event in events:

            if event.event_type != "cowrie.command.input":
                continue

            command = str(
                event.data.get("input", "")
            ).strip()

            if not command:
                continue

            if "shadowauth_controlled_" in command.lower():
                continue

            commands.append(
                command.lower()
            )

        return commands

    def _count_failed_logins(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        return sum(
            1
            for event in events
            if event.event_type == "cowrie.login.failed"
        )

    def _count_download_commands(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        indicators = (
            "wget",
            "curl",
            "scp ",
            "tftp",
        )

        return sum(
            1
            for command in self._behavior_commands(events)
            if any(
                indicator in command
                for indicator in indicators
            )
        )

    def _count_executable_permissions(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        return sum(
            1
            for command in self._behavior_commands(events)
            if (
                "chmod +x" in command
                or "chmod 755" in command
                or "chmod 777" in command
            )
        )

    def _count_ransomware_extensions(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        indicators = (
            ".locked",
            ".encrypted",
            ".enc",
        )

        return sum(
            1
            for command in self._behavior_commands(events)
            if any(
                indicator in command
                for indicator in indicators
            )
        )

    def _count_ransom_notes(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        indicators = (
            "recover_files",
            "restore_files",
            "readme_restore",
            "ransom_note",
            "decrypt",
        )

        return sum(
            1
            for command in self._behavior_commands(events)
            if any(
                indicator in command
                for indicator in indicators
            )
        )

    def _count_cpu_recon(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        indicators = (
            "nproc",
            "/proc/cpuinfo",
            "lscpu",
            "free -m",
            "free -h",
        )

        return sum(
            1
            for command in self._behavior_commands(events)
            if any(
                indicator in command
                for indicator in indicators
            )
        )

    def _count_cryptomining_indicators(
        self,
        events: list[NormalizedEvent],
    ) -> int:

        indicators = (
            "xmrig",
            "stratum",
            "--wallet",
            "--pool",
            "test_wallet",
        )

        return sum(
            1
            for command in self._behavior_commands(events)
            if any(
                indicator in command
                for indicator in indicators
            )
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