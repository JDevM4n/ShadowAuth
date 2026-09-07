import pandas as pd
import pytest

from shadowauth.ml.random_forest_trainer import (
    RandomForestTrainer,
)


def test_random_forest_training_and_prediction():

    x_train = pd.DataFrame(
        {
            "duration_seconds": [
                10,
                15,
                120,
                150,
            ],
            "command_count": [
                1,
                2,
                10,
                15,
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
        n_estimators=20,
        random_state=42,
    )

    trainer.train(
        x_train,
        y_train,
    )

    predictions = trainer.predict(
        x_train
    )

    probabilities = trainer.predict_proba(
        x_train
    )

    importances = (
        trainer.get_feature_importances(
            x_train.columns
        )
    )

    assert trainer.is_trained is True

    assert len(predictions) == 4

    assert probabilities.shape == (
        4,
        2,
    )

    assert set(importances.keys()) == {
        "duration_seconds",
        "command_count",
        "download_count",
    }

    assert pytest.approx(
        sum(importances.values()),
        rel=1e-6,
    ) == 1.0


def test_random_forest_rejects_prediction_before_training():

    trainer = RandomForestTrainer()

    x = pd.DataFrame(
        {
            "duration_seconds": [10],
            "command_count": [1],
        }
    )

    with pytest.raises(
        RuntimeError
    ):

        trainer.predict(x)

    with pytest.raises(
        RuntimeError
    ):

        trainer.predict_proba(x)
