from abc import ABC, abstractmethod

from shadowauth.features.feature_vector import FeatureVector
from shadowauth.models.normalized_event import NormalizedEvent


class FeatureExtractor(ABC):
    """
    Base class for feature extraction.

    Converts one or more NormalizedEvent objects into a FeatureVector
    that can be consumed by the Machine Learning pipeline.
    """

    @abstractmethod
    def extract(
        self,
        events: list[NormalizedEvent],
        label: str = "attack",
    ) -> FeatureVector:
        pass