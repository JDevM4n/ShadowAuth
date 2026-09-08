from shadowauth.correlation.correlation_engine import (
    CorrelationEngine,
)
from shadowauth.correlation.correlation_rule import (
    CorrelationMatch,
    CorrelationRule,
)


class AlwaysMatchRule(
    CorrelationRule
):

    rule_id = "TEST-001"

    rule_name = "Always Match"

    def evaluate(
        self,
        context: dict,
    ) -> CorrelationMatch:

        return CorrelationMatch(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            matched=True,
            severity="high",
            score=0.90,
            threat_type="test",
            description="Controlled test match.",
            evidence={
                "session_id": context.get(
                    "session_id"
                )
            },
        )


class NeverMatchRule(
    CorrelationRule
):

    rule_id = "TEST-002"

    rule_name = "Never Match"

    def evaluate(
        self,
        context: dict,
    ):

        return None


def test_correlation_engine_returns_matches():

    engine = CorrelationEngine(
        rules=[
            AlwaysMatchRule(),
            NeverMatchRule(),
        ]
    )

    results = engine.evaluate(
        {
            "session_id": "session-001",
        }
    )

    assert len(results) == 1

    match = results[0]

    assert match.rule_id == "TEST-001"

    assert match.rule_name == "Always Match"

    assert match.severity == "high"

    assert match.score == 0.90

    assert match.evidence[
        "session_id"
    ] == "session-001"


def test_correlation_engine_add_rule():

    engine = CorrelationEngine()

    engine.add_rule(
        AlwaysMatchRule()
    )

    results = engine.evaluate(
        {
            "session_id": "session-002",
        }
    )

    assert len(results) == 1
