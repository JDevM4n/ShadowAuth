from shadowauth.database.postgres_repository import (
    PostgresRepository,
)
from shadowauth.extractors.session_feature_extractor import (
    SessionFeatureExtractor,
)
from shadowauth.ml.inference_service import (
    ModelInferenceService,
)


class SessionMLPipeline:
    """
    Executes Machine Learning inference for a
    complete ShadowAuth session.
    """

    def __init__(
        self,
        artifact_path: str,
        model_name: str,
        model_version: str,
        repository=None,
        extractor=None,
        inference_service=None,
    ):

        self.artifact_path = artifact_path
        self.model_name = model_name
        self.model_version = model_version

        self.repository = (
            repository
            or PostgresRepository()
        )

        self.extractor = (
            extractor
            or SessionFeatureExtractor()
        )

        self.inference_service = (
            inference_service
            or ModelInferenceService(
                artifact_path
            )
        )

    def process(
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

        feature_vector = self.extractor.extract(
            events,
            label=ground_truth,
        )

        feature_data = (
            feature_vector.model_dump()
        )

        inference = (
            self.inference_service.predict(
                feature_data
            )[0]
        )

        prediction = inference[
            "prediction"
        ]

        attack_probability = inference[
            "attack_probability"
        ]

        self.repository.save_ml_score(
            session_id=session_id,
            model_name=self.model_name,
            model_version=self.model_version,
            prediction=prediction,
            attack_probability=attack_probability,
            artifact_path=self.artifact_path,
            metadata={
                "ground_truth": ground_truth,
                "ground_truth_modified": False,
            },
        )

        return {
            "session_id": session_id,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "prediction": prediction,
            "attack_probability": (
                attack_probability
            ),
            "ground_truth": ground_truth,
        }
