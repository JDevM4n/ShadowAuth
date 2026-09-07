import pytest

from shadowauth.pipeline.session_ml_pipeline import (
    SessionMLPipeline,
)


class FakeFeatureVector:

    def model_dump(self):
        return {
            "duration_seconds": 120,
            "command_count": 10,
            "label": "unlabeled",
        }


class FakeRepository:

    def __init__(self):
        self.saved_score = None

    def get_session(self, session_id):
        return [object(), object()]

    def get_session_label(self, session_id):
        return "unlabeled"

    def save_ml_score(self, **kwargs):
        self.saved_score = kwargs


class EmptyRepository:

    def get_session(self, session_id):
        return []


class FakeExtractor:

    def extract(
        self,
        events,
        label="unlabeled",
    ):
        assert len(events) == 2
        assert label == "unlabeled"

        return FakeFeatureVector()


class FakeInferenceService:

    def predict(self, features):

        assert features[
            "duration_seconds"
        ] == 120

        return [
            {
                "prediction": "attack",
                "attack_probability": 0.93,
            }
        ]


def test_session_ml_pipeline():

    repository = FakeRepository()

    pipeline = SessionMLPipeline(
        artifact_path="models/test.joblib",
        model_name="random_forest",
        model_version="v1",
        repository=repository,
        extractor=FakeExtractor(),
        inference_service=FakeInferenceService(),
    )

    result = pipeline.process(
        "session-001"
    )

    assert result[
        "session_id"
    ] == "session-001"

    assert result[
        "prediction"
    ] == "attack"

    assert result[
        "attack_probability"
    ] == 0.93

    assert result[
        "ground_truth"
    ] == "unlabeled"

    assert repository.saved_score[
        "prediction"
    ] == "attack"

    assert repository.saved_score[
        "attack_probability"
    ] == 0.93

    assert repository.saved_score[
        "artifact_path"
    ] == "models/test.joblib"

    assert repository.saved_score[
        "metadata"
    ][
        "ground_truth_modified"
    ] is False


def test_session_ml_pipeline_rejects_empty_session():

    pipeline = SessionMLPipeline(
        artifact_path="models/test.joblib",
        model_name="random_forest",
        model_version="v1",
        repository=EmptyRepository(),
        extractor=FakeExtractor(),
        inference_service=FakeInferenceService(),
    )

    with pytest.raises(
        ValueError,
        match="Session not found or empty",
    ):
        pipeline.process(
            "missing-session"
        )
