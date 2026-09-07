import pandas as pd
import pytest

from shadowauth.ml.isolation_forest_trainer import (
    IsolationForestTrainer,
)


def test_isolation_forest_training_and_prediction():

    x_train = pd.DataFrame(
        {
            "duration_seconds": [
                10, 11, 9, 12, 10,
                11, 9, 10, 200,
            ],
            "command_count": [
                1, 1, 2, 1, 2,
                1, 1, 2, 30,
            ],
            "download_count": [
                0, 0, 0, 0, 0,
                0, 0, 0, 5,
            ],
        }
    )

    trainer = IsolationForestTrainer(
        n_estimators=50,
        contamination=0.15,
        random_state=42,
    )

    trainer.train(
        x_train
    )

    predictions = trainer.predict(
        x_train
    )

    scores = trainer.anomaly_score(
        x_train
    )

    assert trainer.is_trained is True

    assert len(predictions) == len(
        x_train
    )

    assert len(scores) == len(
        x_train
    )

    assert set(predictions).issubset(
        {
            "normal",
            "anomaly",
        }
    )

    assert (
        scores[-1]
        > scores[:-1].mean()
    )


def test_isolation_forest_rejects_prediction_before_training():

    trainer = IsolationForestTrainer()

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
        trainer.anomaly_score(x)
