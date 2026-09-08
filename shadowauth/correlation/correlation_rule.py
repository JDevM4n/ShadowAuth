from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CorrelationMatch:
    """
    Represents the result produced when a correlation
    rule identifies suspicious behavior.
    """

    rule_id: str

    rule_name: str

    matched: bool

    severity: str

    score: float

    threat_type: str

    description: str

    evidence: dict[str, Any] = field(
        default_factory=dict
    )


class CorrelationRule(ABC):
    """
    Base contract for every ShadowAuth correlation rule.
    """

    rule_id: str
    rule_name: str

    @abstractmethod
    def evaluate(
        self,
        context: dict,
    ) -> CorrelationMatch | None:
        """
        Evaluate security context and return a match
        when suspicious behavior is detected.
        """
        raise NotImplementedError
