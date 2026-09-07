import pytest

from shadowauth.ml.model_evaluator import (
    ModelEvaluator,
)


def test_model_evaluator():

    evaluator = ModelEvaluator()

    y_true = [
        "attack",
        "attack",
        "benign",
        "benign",
    ]

    y_pred = [
        "attack",
        "benign",
        "benign",
        "benign",
    ]

    attack_probabilities = [
        0.90,
        0.40,
        0.20,
        0.10,
    ]

    metrics = evaluator.evaluate(
        y_true,
        y_pred,
        attack_probabilities,
    )

    assert metrics["accuracy"] == pytest.approx(
        0.75
    )

    assert metrics["precision"] == pytest.approx(
        1.0
    )

    assert metrics["recall"] == pytest.approx(
        0.5
    )

    assert metrics["f1_score"] == pytest.approx(
        2 / 3
    )

    assert metrics["roc_auc"] == pytest.approx(
        1.0
    )

    assert metrics["confusion_matrix"] == [
        [2, 0],
        [1, 1],
    ]


def test_model_evaluator_without_probabilities():

    evaluator = ModelEvaluator()

    metrics = evaluator.evaluate(
        [
            "attack",
            "benign",
        ],
        [
            "attack",
            "benign",
        ],
    )

    assert metrics["roc_auc"] is None
