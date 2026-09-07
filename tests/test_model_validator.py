import pandas as pd
import pytest

from sklearn.ensemble import RandomForestClassifier

from shadowauth.ml.model_validator import ModelValidator


def test_model_validator_cross_validation():

    benign_count = 20
    attack_count = 20

    x = pd.DataFrame(
        {
            "duration_seconds":
                list(range(10, 10 + benign_count))
                +
                list(range(100, 100 + attack_count)),

            "command_count":
                [1] * benign_count
                +
                [10] * attack_count,

            "download_count":
                [0] * benign_count
                +
                [2] * attack_count,
        }
    )

    y = pd.Series(
        ["benign"] * benign_count
        +
        ["attack"] * attack_count
    )

    validator = ModelValidator(
        n_splits=4,
        n_repeats=2,
        minimum_samples=20,
        random_state=42,
    )

    model = RandomForestClassifier(
        n_estimators=20,
        random_state=42,
    )

    result = validator.validate(
        model,
        x,
        y,
    )

    assert result["folds"] == 8

    assert 0 <= result["accuracy_mean"] <= 1
    assert 0 <= result["precision_mean"] <= 1
    assert 0 <= result["recall_mean"] <= 1
    assert 0 <= result["f1_score_mean"] <= 1
    assert 0 <= result["roc_auc_mean"] <= 1


def test_model_validator_rejects_small_dataset():

    x = pd.DataFrame(
        {
            "command_count": [
                1,
                2,
                10,
                12,
            ]
        }
    )

    y = pd.Series(
        [
            "benign",
            "benign",
            "attack",
            "attack",
        ]
    )

    validator = ModelValidator(
        n_splits=2,
        minimum_samples=20,
    )

    model = RandomForestClassifier(
        random_state=42,
    )

    with pytest.raises(
        ValueError,
        match="At least 20 labeled samples",
    ):
        validator.validate(
            model,
            x,
            y,
        )
