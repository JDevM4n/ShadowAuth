import pandas as pd
import pytest

from shadowauth.ml.xgboost_trainer import (
    XGBoostTrainer,
)


def test_xgboost_training_and_prediction():

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

    trainer = XGBoostTrainer(
        n_estimators=20,
        max_depth=2,
        learning_rate=0.1,
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

    assert set(predictions).issubset(
        {
            "attack",
            "benign",
        }
    )

    assert set(
        trainer.get_classes()
    ) == {
        "attack",
        "benign",
    }

    assert set(importances.keys()) == {
        "duration_seconds",
        "command_count",
        "download_count",
    }


def test_xgboost_rejects_prediction_before_training():

    trainer = XGBoostTrainer()

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
