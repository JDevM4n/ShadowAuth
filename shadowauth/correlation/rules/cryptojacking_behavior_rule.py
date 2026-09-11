from shadowauth.correlation.correlation_rule import (
    CorrelationMatch,
    CorrelationRule,
)


class CryptojackingBehaviorRule(CorrelationRule):

    rule_id = "CORR-004"

    rule_name = "Cryptojacking Behavior"

    def __init__(
        self,
        attack_probability_threshold: float = 0.70,
    ):

        self.attack_probability_threshold = (
            attack_probability_threshold
        )

    def evaluate(
        self,
        context: dict,
    ) -> CorrelationMatch | None:

        features = (
            context.get("features")
            or {}
        )

        ml_score = (
            context.get("ml_score")
            or {}
        )

        prediction = ml_score.get(
            "prediction"
        )

        attack_probability = ml_score.get(
            "attack_probability"
        )

        if attack_probability is None:
            return None

        cpu_recon = int(
            features.get(
                "cpu_recon_count",
                0,
            )
            or 0
        )

        mining_indicators = int(
            features.get(
                "cryptomining_indicator_count",
                0,
            )
            or 0
        )

        download_commands = int(
            features.get(
                "download_command_count",
                0,
            )
            or 0
        )

        executable_permissions = int(
            features.get(
                "executable_permission_count",
                0,
            )
            or 0
        )

        ml_signal = (
            prediction == "attack"
            and attack_probability
            >= self.attack_probability_threshold
        )

        mining_signal = (
            mining_indicators > 0
        )

        supporting_signals = sum(
            [
                cpu_recon > 0,
                download_commands > 0,
                executable_permissions > 0,
            ]
        )

        if not (
            ml_signal
            and mining_signal
            and supporting_signals >= 2
        ):
            return None

        behavioral_score = 0.40

        if cpu_recon > 0:
            behavioral_score += 0.20

        if download_commands > 0:
            behavioral_score += 0.20

        if executable_permissions > 0:
            behavioral_score += 0.20

        score = min(
            1.0,
            (
                float(attack_probability) * 0.60
                + behavioral_score * 0.40
            ),
        )

        severity = (
            "high"
            if supporting_signals >= 3
            else "medium"
        )

        return CorrelationMatch(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            matched=True,
            severity=severity,
            score=score,
            threat_type="cryptojacking",
            description=(
                "Machine Learning and behavioral "
                "signals indicate cryptojacking activity."
            ),
            evidence={
                "session_id": context.get(
                    "session_id"
                ),
                "ml_prediction": prediction,
                "attack_probability": (
                    attack_probability
                ),
                "cpu_recon_count": cpu_recon,
                "cryptomining_indicator_count": (
                    mining_indicators
                ),
                "download_command_count": (
                    download_commands
                ),
                "executable_permission_count": (
                    executable_permissions
                ),
            },
        )
