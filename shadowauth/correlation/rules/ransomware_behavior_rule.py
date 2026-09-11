from shadowauth.correlation.correlation_rule import (
    CorrelationMatch,
    CorrelationRule,
)


class RansomwareBehaviorRule(CorrelationRule):

    rule_id = "CORR-003"

    rule_name = "Early Ransomware Behavior"

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

        ransomware_extensions = int(
            features.get(
                "ransomware_extension_count",
                0,
            )
            or 0
        )

        ransom_notes = int(
            features.get(
                "ransom_note_count",
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

        ransomware_signal = (
            ransomware_extensions > 0
            or ransom_notes > 0
        )

        staging_signal = (
            download_commands > 0
            or executable_permissions > 0
        )

        if not (
            ml_signal
            and ransomware_signal
            and staging_signal
        ):
            return None

        behavioral_score = 0.0

        if ransomware_extensions > 0:
            behavioral_score += 0.35

        if ransom_notes > 0:
            behavioral_score += 0.35

        if download_commands > 0:
            behavioral_score += 0.15

        if executable_permissions > 0:
            behavioral_score += 0.15

        score = min(
            1.0,
            (
                float(attack_probability) * 0.60
                + behavioral_score * 0.40
            ),
        )

        severity = (
            "high"
            if (
                ransomware_extensions > 0
                and ransom_notes > 0
            )
            else "medium"
        )

        return CorrelationMatch(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            matched=True,
            severity=severity,
            score=score,
            threat_type="ransomware",
            description=(
                "Machine Learning and behavioral "
                "signals indicate early ransomware activity."
            ),
            evidence={
                "session_id": context.get(
                    "session_id"
                ),
                "ml_prediction": prediction,
                "attack_probability": (
                    attack_probability
                ),
                "ransomware_extension_count": (
                    ransomware_extensions
                ),
                "ransom_note_count": (
                    ransom_notes
                ),
                "download_command_count": (
                    download_commands
                ),
                "executable_permission_count": (
                    executable_permissions
                ),
            },
        )
