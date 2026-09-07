import pandas as pd
import pytest

from shadowauth.ml.model_persistence import (
    ModelPersistence,
)
from shadowauth.ml.random_forest_trainer import (
    RandomForestTrainer,
)


def test_save_and_load_trained_model(
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
        n_estimators=20,
        random_state=42,
    )

    trainer.train(
        x_train,
        y_train,
    )

    model_path = (
        tmp_path
        / "random_forest.joblib"
    )

    ModelPersistence.save(
        model=trainer,
        path=model_path,
        metadata={
            "model_type": "random_forest",
            "purpose": "test",
        },
        feature_names=x_train.columns,
    )

    assert model_path.exists()

    artifact = ModelPersistence.load(
        model_path
    )

    assert (
        artifact["artifact_version"]
        == "1.0"
    )

    assert (
        artifact["metadata"]["model_type"]
        == "random_forest"
    )

    assert artifact["feature_names"] == [
        "duration_seconds",
        "command_count",
    ]

    loaded_trainer = (
        ModelPersistence.load_model(
            model_path
        )
    )

    original_predictions = (
        trainer.predict(
            x_train
        )
    )

    loaded_predictions = (
        loaded_trainer.predict(
            x_train
        )
    )

    assert (
        original_predictions.tolist()
        == loaded_predictions.tolist()
    )


def test_load_missing_model():

    with pytest.raises(
        FileNotFoundError
    ):

        ModelPersistence.load(
            "models/does-not-exist.joblib"
        )
