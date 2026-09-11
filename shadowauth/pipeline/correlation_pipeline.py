from shadowauth.correlation.context_builder import (
    CorrelationContextBuilder,
)
from shadowauth.correlation.correlation_engine import (
    CorrelationEngine,
)
from shadowauth.correlation.rules.credential_compromise_rule import (
    CredentialCompromiseRule,
)
from shadowauth.correlation.rules.cryptojacking_behavior_rule import (
    CryptojackingBehaviorRule,
)
from shadowauth.correlation.rules.ransomware_behavior_rule import (
    RansomwareBehaviorRule,
)
from shadowauth.correlation.rules.suspicious_session_rule import (
    SuspiciousSessionRule,
)
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


class CorrelationPipeline:

    def __init__(
        self,
        repository=None,
        model_name: str = "random_forest",
        model_version: str = "2.0",
    ):

        self.repository = (
            repository
            or PostgresRepository()
        )

        self.model_name = model_name
        self.model_version = model_version

        self.context_builder = (
            CorrelationContextBuilder(
                repository=self.repository,
                model_name=model_name,
                model_version=model_version,
            )
        )

        self.engine = CorrelationEngine(
            rules=[
                SuspiciousSessionRule(),
                CredentialCompromiseRule(),
                RansomwareBehaviorRule(),
                CryptojackingBehaviorRule(),
            ]
        )

    def process(
        self,
        session_id: str,
    ) -> dict:

        context = self.context_builder.build(
            session_id
        )

        matches = self.engine.evaluate(
            context
        )

        for match in matches:

            self.repository.save_correlation_result(
                session_id=session_id,
                rule_id=match.rule_id,
                rule_name=match.rule_name,
                severity=match.severity,
                score=match.score,
                threat_type=match.threat_type,
                description=match.description,
                evidence=match.evidence,
                model_name=self.model_name,
                model_version=self.model_version,
            )

        return {
            "session_id": session_id,
            "matches": matches,
            "match_count": len(matches),
        }
