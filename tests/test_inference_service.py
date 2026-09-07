import pandas as pd
import pytest

from shadowauth.ml.inference_service import (
    ModelInferenceService,
)
from shadowauth.ml.model_persistence import (
    ModelPersistence,
)
from shadowauth.ml.random_forest_trainer import (
    RandomForestTrainer,
)


def create_artifact(
    tmp_path,
):

    x_train = pd.DataFrame(
        {
            "duration_seconds": [
                10,
                20,
                100,
                120,
            ],
            "command_count": [
                1,
                2,
                10,
                12,
            ],
            "download_count": [
                0,
                0,
                1,
                2,
            ],
        }
    )

    y_train = pd.Series(
        [
            "benign",
            "benign",
            "attack",
            "attack",
        ]
    )

    trainer = RandomForestTrainer(
        n_estimators=50,
        random_state=42,
    )

    trainer.train(
        x_train,
        y_train,
    )

    path = (
        tmp_path
        / "shadowauth-model.joblib"
    )

    ModelPersistence.save(
        model=trainer,
        path=path,
        metadata={
            "model_type": "random_forest",
        },
        feature_names=x_train.columns,
    )

    return path


def test_inference_from_saved_model(
    tmp_path,
):

    artifact_path = create_artifact(
        tmp_path
    )

    service = ModelInferenceService(
        artifact_path
    )

    result = service.predict(
        {
            "duration_seconds": 110,
            "command_count": 11,
            "download_count": 2,
        }
    )

    assert len(result) == 1

    assert result[0]["prediction"] in {
        "attack",
        "benign",
    }

    assert (
        result[0]["attack_probability"]
        is not None
    )

    assert (
        0.0
        <= result[0]["attack_probability"]
        <= 1.0
    )


def test_inference_accepts_dataframe(
    tmp_path,
):

    artifact_path = create_artifact(
        tmp_path
    )

    service = ModelInferenceService(
        artifact_path
    )

    x = pd.DataFrame(
        {
            "duration_seconds": [
                15,
                115,
            ],
            "command_count": [
                1,
                11,
            ],
            "download_count": [
                0,
                2,
            ],
        }
    )

    result = service.predict(
        x
    )

    assert len(result) == 2


def test_inference_rejects_missing_features(
    tmp_path,
):

    artifact_path = create_artifact(
        tmp_path
    )

    service = ModelInferenceService(
        artifact_path
    )

    with pytest.raises(
        ValueError,
        match="Missing required features",
    ):

        service.predict(
            {
                "duration_seconds": 100,
            }
        )

