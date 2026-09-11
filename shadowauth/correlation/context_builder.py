from shadowauth.database.postgres_repository import (
    PostgresRepository,
)
from shadowauth.extractors.session_feature_extractor import (
    SessionFeatureExtractor,
)


class CorrelationContextBuilder:
    """
    Builds the common security context consumed by
    ShadowAuth correlation rules.
    """

    def __init__(
        self,
        repository=None,
        extractor=None,
        model_name: str = "random_forest",
        model_version: str = "2.0",
    ):

        self.repository = (
            repository
            or PostgresRepository()
        )

        self.extractor = (
            extractor
            or SessionFeatureExtractor()
        )

        self.model_name = model_name
        self.model_version = model_version

    def build(
        self,
        session_id: str,
    ) -> dict:

        events = self.repository.get_session(
            session_id
        )

        if not events:
            raise ValueError(
                f"Session not found or empty: "
                f"{session_id}"
            )

        ground_truth = (
            self.repository.get_session_label(
                session_id
            )
        )

        feature_vector = (
            self.extractor.extract(
                events,
                label=ground_truth,
            )
        )

        ml_score = (
            self.repository.get_ml_score(
                session_id=session_id,
                model_name=self.model_name,
                model_version=self.model_version,
            )
        )

        return {
            "session_id": session_id,
            "ground_truth": ground_truth,
            "events": events,
            "features": (
                feature_vector.model_dump()
            ),
            "ml_score": ml_score,
        }
