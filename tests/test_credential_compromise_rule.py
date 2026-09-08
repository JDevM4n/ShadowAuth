from types import SimpleNamespace

from shadowauth.correlation.rules.credential_compromise_rule import (
    CredentialCompromiseRule,
)


def make_event(
    event_type,
):
    return SimpleNamespace(
        event_type=event_type
    )


def test_credential_compromise_rule_matches():

    rule = CredentialCompromiseRule()

    context = {
        "session_id": "attack-session",

        "events": [
            make_event(
                "cowrie.login.failed"
            ),
            make_event(
                "cowrie.login.failed"
            ),
            make_event(
                "cowrie.login.success"
            ),
        ],

        "features": {
            "command_count": 10,
            "download_count": 1,
        },

        "ml_score": {
            "prediction": "attack",
            "attack_probability": 0.70,
        },
    }

    result = rule.evaluate(
        context
    )

    assert result is not None

    assert result.rule_id == "CORR-002"

    assert result.matched is True

    assert result.severity == "high"

    assert result.score == 0.90

    assert (
        result.evidence[
            "failed_logins"
        ]
        == 2
    )

    assert (
        result.evidence[
            "successful_logins"
        ]
        == 1
    )

    assert (
        result.evidence[
            "command_count"
        ]
        == 10
    )

    assert (
        result.evidence[
            "download_count"
        ]
        == 1
    )


def test_rule_requires_failed_logins():

    rule = CredentialCompromiseRule()

    context = {
        "events": [
            make_event(
                "cowrie.login.success"
            )
        ],

        "features": {
            "command_count": 10,
            "download_count": 1,
        },
    }

    assert (
        rule.evaluate(context)
        is None
    )


def test_rule_requires_successful_login():

    rule = CredentialCompromiseRule()

    context = {
        "events": [
            make_event(
                "cowrie.login.failed"
            ),
            make_event(
                "cowrie.login.failed"
            ),
        ],

        "features": {
            "command_count": 10,
            "download_count": 1,
        },
    }

    assert (
        rule.evaluate(context)
        is None
    )


def test_rule_requires_post_auth_activity():

    rule = CredentialCompromiseRule()

    context = {
        "events": [
            make_event(
                "cowrie.login.failed"
            ),
            make_event(
                "cowrie.login.failed"
            ),
            make_event(
                "cowrie.login.success"
            ),
        ],

        "features": {
            "command_count": 0,
            "download_count": 0,
        },
    }

    assert (
        rule.evaluate(context)
        is None
    )
