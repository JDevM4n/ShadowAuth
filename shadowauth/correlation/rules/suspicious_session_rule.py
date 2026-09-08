from shadowauth.correlation.correlation_rule import (
    CorrelationMatch,
    CorrelationRule,
)


class SuspiciousSessionRule(CorrelationRule):
    """
    Correlates an ML attack prediction with
    suspicious behavioral activity in a session.
    """

    rule_id = "CORR-001"

    rule_name = "Suspicious Session Activity"

    def __init__(
        self,
        attack_probability_threshold: float = 0.80,
        minimum_commands: int = 3,
    ):

        self.attack_probability_threshold = (
            attack_probability_threshold
        )

        self.minimum_commands = (
            minimum_commands
        )

    def evaluate(
        self,
        context: dict,
    ) -> CorrelationMatch | None:

        ml_score = (
            context.get("ml_score")
            or {}
        )

        features = (
            context.get("features")
            or {}
        )

        prediction = ml_score.get(
            "prediction"
        )

        attack_probability = ml_score.get(
            "attack_probability"
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

        if attack_probability is None:
            return None

        ml_signal = (
            prediction == "attack"
            and attack_probability
            >= self.attack_probability_threshold
        )

        behavioral_signal = (
            command_count
            >= self.minimum_commands
            or download_count > 0
        )

        if not (
            ml_signal
            and behavioral_signal
        ):
            return None

        severity = (
            "high"
            if attack_probability >= 0.90
            else "medium"
        )

        score = min(
            1.0,
            float(
                attack_probability
            ),
        )

        return CorrelationMatch(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            matched=True,
            severity=severity,
            score=score,
            threat_type="suspicious_activity",
            description=(
                "Machine Learning classified the "
                "session as attack while behavioral "
                "activity was also detected."
            ),
            evidence={
                "session_id": context.get(
                    "session_id"
                ),
                "ml_prediction": prediction,
                "attack_probability": (
                    attack_probability
                ),
                "command_count": command_count,
                "download_count": download_count,
            },
        )
