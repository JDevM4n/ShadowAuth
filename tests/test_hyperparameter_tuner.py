import pandas as pd

import shadowauth.ml.hyperparameter_tuner as tuner_module
from shadowauth.ml.hyperparameter_tuner import (
    HyperparameterTuner,
)


def test_random_forest_tuning_pipeline(
    monkeypatch,
):

    created_searches = []

    class FakeGridSearchCV:

        def __init__(
            self,
            estimator,
            param_grid,
            scoring,
            cv,
            n_jobs,
        ):

            self.estimator = estimator
            self.param_grid = param_grid
            self.scoring = scoring
            self.cv = cv
            self.n_jobs = n_jobs

            self.best_params_ = {
                "n_estimators": 100,
                "max_depth": 5,
                "min_samples_split": 2,
            }

            self.best_score_ = 0.80
            self.best_estimator_ = estimator

            self.fit_x = None
            self.fit_y = None

            created_searches.append(self)

        def fit(
            self,
            x,
            y,
        ):

            self.fit_x = x
            self.fit_y = list(y)

            return self

    monkeypatch.setattr(
        tuner_module,
        "GridSearchCV",
        FakeGridSearchCV,
    )

    x_train = pd.DataFrame(
        {
            "command_count": [
                1,
                10,
                2,
                12,
            ],
            "duration_seconds": [
                10,
                100,
                15,
                120,
            ],
        }
    )

    y_train = pd.Series(
        [
            "benign",
            "attack",
            "benign",
            "attack",
        ]
    )

    tuner = HyperparameterTuner(
        cv_splits=2,
        random_state=42,
    )

    result = tuner.tune_random_forest(
        x_train,
        y_train,
    )

    search = created_searches[0]

    assert search.scoring == "recall"

    assert search.fit_y == [
        False,
        True,
        False,
        True,
    ]

    assert (
        "n_estimators"
        in search.param_grid
    )

    assert (
        "max_depth"
        in search.param_grid
    )

    assert result["best_score"] == 0.80

    assert result["best_params"] == {
        "n_estimators": 100,
        "max_depth": 5,
        "min_samples_split": 2,
    }


def test_xgboost_tuning_pipeline(
    monkeypatch,
):

    created_searches = []

    class FakeGridSearchCV:

        def __init__(
            self,
            estimator,
            param_grid,
            scoring,
            cv,
            n_jobs,
        ):

            self.estimator = estimator
            self.param_grid = param_grid
            self.scoring = scoring
            self.cv = cv
            self.n_jobs = n_jobs

            self.best_params_ = {
                "n_estimators": 100,
                "max_depth": 3,
                "learning_rate": 0.1,
            }

            self.best_score_ = 0.85
            self.best_estimator_ = estimator

            self.fit_y = None

            created_searches.append(self)

        def fit(
            self,
            x,
            y,
        ):

            self.fit_y = list(y)

            return self

    monkeypatch.setattr(
        tuner_module,
        "GridSearchCV",
        FakeGridSearchCV,
    )

    x_train = pd.DataFrame(
        {
            "command_count": [
                1,
                10,
                2,
                12,
            ],
            "duration_seconds": [
                10,
                100,
                15,
                120,
            ],
        }
    )

    y_train = pd.Series(
        [
            "benign",
            "attack",
            "benign",
            "attack",
        ]
    )

    tuner = HyperparameterTuner(
        cv_splits=2,
        random_state=42,
    )

    result = tuner.tune_xgboost(
        x_train,
        y_train,
    )

    search = created_searches[0]

    assert search.scoring == "recall"

    assert search.fit_y == [
        0,
        1,
        0,
        1,
    ]

    assert (
        "n_estimators"
        in search.param_grid
    )

    assert (
        "max_depth"
        in search.param_grid
    )

    assert (
        "learning_rate"
        in search.param_grid
    )

    assert result["best_score"] == 0.85
