from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
)

from sklearn.ensemble import (
    RandomForestClassifier,
)

from xgboost import XGBClassifier


class HyperparameterTuner:
    """
    Hyperparameter tuning for ShadowAuth
    supervised classifiers.
    """

    def __init__(
        self,
        cv_splits: int = 3,
        random_state: int = 42,
    ):

        self.cv = StratifiedKFold(
            n_splits=cv_splits,
            shuffle=True,
            random_state=random_state,
        )

        self.random_state = random_state

    def tune_random_forest(
        self,
        x_train,
        y_train,
    ):

        model = RandomForestClassifier(
            random_state=self.random_state,
            class_weight="balanced",
        )

        parameter_grid = {
            "n_estimators": [
                50,
                100,
                200,
            ],
            "max_depth": [
                None,
                5,
                10,
            ],
            "min_samples_split": [
                2,
                5,
            ],
        }

        search = GridSearchCV(
            estimator=model,
            param_grid=parameter_grid,
            scoring="recall",
            cv=self.cv,
            n_jobs=-1,
        )

        search.fit(
            x_train,
            y_train == "attack",
        )

        return {
            "best_params": search.best_params_,
            "best_score": search.best_score_,
            "best_estimator": search.best_estimator_,
        }

    def tune_xgboost(
        self,
        x_train,
        y_train,
    ):

        encoded_y = (
            y_train == "attack"
        ).astype(int)

        model = XGBClassifier(
            random_state=self.random_state,
            eval_metric="logloss",
        )

        parameter_grid = {
            "n_estimators": [
                50,
                100,
                200,
            ],
            "max_depth": [
                2,
                3,
                5,
            ],
            "learning_rate": [
                0.01,
                0.05,
                0.1,
            ],
        }

        search = GridSearchCV(
            estimator=model,
            param_grid=parameter_grid,
            scoring="recall",
            cv=self.cv,
            n_jobs=-1,
        )

        search.fit(
            x_train,
            encoded_y,
        )

        return {
            "best_params": search.best_params_,
            "best_score": search.best_score_,
            "best_estimator": search.best_estimator_,
        }
