from shadowauth.correlation.correlation_rule import (
    CorrelationMatch,
    CorrelationRule,
)


class CorrelationEngine:
    """
    Executes correlation rules against a common
    ShadowAuth security context.
    """

    def __init__(
        self,
        rules: list[CorrelationRule] | None = None,
    ):

        self.rules = rules or []

    def add_rule(
        self,
        rule: CorrelationRule,
    ) -> None:

        self.rules.append(
            rule
        )

    def evaluate(
        self,
        context: dict,
    ) -> list[CorrelationMatch]:

        matches = []

        for rule in self.rules:

            result = rule.evaluate(
                context
            )

            if (
                result is not None
                and result.matched
            ):
                matches.append(
                    result
                )

        return matches
