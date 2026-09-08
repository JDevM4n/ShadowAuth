import pytest

from shadowauth.correlation.context_builder import (
    CorrelationContextBuilder,
)


class FakeFeatureVector:

    def model_dump(self):
        return {
            "session_id": "session-001",
            "command_count": 5,
            "download_count": 1,
            "label": "unlabeled",
        }


class FakeExtractor:

    def extract(
        self,
        events,
        label="unlabeled",
    ):

        assert len(events) == 2
        assert label == "unlabeled"

        return FakeFeatureVector()


class FakeRepository:

    def get_session(
        self,
        session_id,
    ):
        return [
            object(),
            object(),
        ]

    def get_session_label(
        self,
        session_id,
    ):
        return "unlabeled"

    def get_ml_score(
        self,
        session_id,
        model_name,
        model_version,
    ):
        return {
            "prediction": "attack",
            "attack_probability": 0.93,
        }


class EmptyRepository:

    def get_session(
        self,
        session_id,
    ):
        return []


def test_context_builder():

    builder = CorrelationContextBuilder(
        repository=FakeRepository(),
        extractor=FakeExtractor(),
        model_name="random_forest",
        model_version="v1",
    )

    context = builder.build(
        "session-001"
    )

    assert (
        context["session_id"]
        == "session-001"
    )

    assert (
        context["ground_truth"]
        == "unlabeled"
    )

    assert len(
        context["events"]
    ) == 2

    assert (
        context["features"]["command_count"]
        == 5
    )

    assert (
        context["ml_score"][
            "prediction"
        ]
        == "attack"
    )

    assert (
        context["ml_score"][
            "attack_probability"
        ]
        == 0.93
    )


def test_context_builder_rejects_missing_session():

    builder = CorrelationContextBuilder(
        repository=EmptyRepository(),
        extractor=FakeExtractor(),
    )

    with pytest.raises(
        ValueError,
        match="Session not found or empty",
    ):
        builder.build(
            "missing-session"
        )
