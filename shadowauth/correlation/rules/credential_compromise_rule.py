from shadowauth.correlation.correlation_rule import (
    CorrelationMatch,
    CorrelationRule,
)


class CredentialCompromiseRule(CorrelationRule):
    """
    Detects a behavioral pattern where repeated
    authentication failures are followed by a
    successful login and subsequent activity.
    """

    rule_id = "CORR-002"

    rule_name = "Credential Compromise Activity"

    def __init__(
        self,
        minimum_failed_logins: int = 2,
        minimum_commands: int = 3,
    ):

        self.minimum_failed_logins = (
            minimum_failed_logins
        )

        self.minimum_commands = (
            minimum_commands
        )

    def evaluate(
        self,
        context: dict,
    ) -> CorrelationMatch | None:

        events = (
            context.get("events")
            or []
        )

        features = (
            context.get("features")
            or {}
        )

        ml_score = (
            context.get("ml_score")
            or {}
        )

        failed_logins = sum(
            1
            for event in events
            if event.event_type
            == "cowrie.login.failed"
        )

        successful_logins = sum(
            1
            for event in events
            if event.event_type
            == "cowrie.login.success"
        )

        command_count = int(
            features.get(
                "command_count",
                0,
            )
            or 0
        )

        download_count = int(
            features.get(
                "download_count",
                0,
            )
            or 0
        )

        authentication_signal = (
            failed_logins
            >= self.minimum_failed_logins
            and successful_logins > 0
        )

        post_auth_activity = (
            command_count
            >= self.minimum_commands
            or download_count > 0
        )

        if not (
            authentication_signal
            and post_auth_activity
        ):
            return None

        severity = (
            "high"
            if download_count > 0
            else "medium"
        )

        score = (
            0.90
            if download_count > 0
            else 0.80
        )

        return CorrelationMatch(
            rule_id=self.rule_id,

            rule_name=self.rule_name,

            matched=True,

            severity=severity,

            score=score,

            threat_type="credential_compromise",

            description=(
                "Repeated authentication failures "
                "were followed by a successful login "
                "and subsequent session activity."
            ),

            evidence={
                "session_id": context.get(
                    "session_id"
                ),

                "failed_logins": failed_logins,

                "successful_logins": (
                    successful_logins
                ),

                "command_count": command_count,

                "download_count": download_count,

                "ml_prediction": ml_score.get(
                    "prediction"
                ),

                "attack_probability": (
                    ml_score.get(
                        "attack_probability"
                    )
                ),
            },
        )
