from shadowauth.correlation.rules.suspicious_session_rule import (
    SuspiciousSessionRule,
)


def test_suspicious_session_rule_matches():

    rule = SuspiciousSessionRule()

    context = {
        "session_id": "session-attack-001",

        "ml_score": {
            "prediction": "attack",
            "attack_probability": 0.93,
        },

        "features": {
            "command_count": 10,
            "download_count": 1,
        },
    }

    result = rule.evaluate(
        context
    )

    assert result is not None

    assert result.matched is True
    assert result.rule_id == "CORR-001"
    assert result.severity == "high"
    assert result.score == 0.93

    assert (
        result.evidence["session_id"]
        == "session-attack-001"
    )


def test_suspicious_session_rule_requires_behavior():

    rule = SuspiciousSessionRule()

    context = {
        "session_id": "session-002",

        "ml_score": {
            "prediction": "attack",
            "attack_probability": 0.95,
        },

        "features": {
            "command_count": 0,
            "download_count": 0,
        },
    }

    result = rule.evaluate(
        context
    )

    assert result is None


def test_suspicious_session_rule_requires_ml_signal():

    rule = SuspiciousSessionRule()

    context = {
        "session_id": "session-003",

        "ml_score": {
            "prediction": "benign",
            "attack_probability": 0.20,
        },

        "features": {
            "command_count": 15,
            "download_count": 2,
        },
    }

    result = rule.evaluate(
        context
    )

    assert result is None


def test_suspicious_session_rule_medium_severity():

    rule = SuspiciousSessionRule()

    context = {
        "session_id": "session-004",

        "ml_score": {
            "prediction": "attack",
            "attack_probability": 0.85,
        },

        "features": {
            "command_count": 5,
            "download_count": 0,
        },
    }

    result = rule.evaluate(
        context
    )

    assert result is not None
    assert result.severity == "medium"
