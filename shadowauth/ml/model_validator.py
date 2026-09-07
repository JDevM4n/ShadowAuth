import numpy as np

from sklearn.base import clone
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
)


class ModelValidator:
    """
    Cross-validation utility for ShadowAuth
    supervised Machine Learning models.
    """

    def __init__(
        self,
        n_splits: int = 5,
        n_repeats: int = 3,
        random_state: int = 42,
        minimum_samples: int = 20,
    ):

        self.n_splits = n_splits
        self.n_repeats = n_repeats
        self.random_state = random_state
        self.minimum_samples = minimum_samples

    def validate(
        self,
        estimator,
        x,
        y,
    ) -> dict:

        if len(x) < self.minimum_samples:
            raise ValueError(
                f"At least {self.minimum_samples} "
                "labeled samples are required "
                "for model validation."
            )

        labels = set(y)

        if not labels.issubset(
            {
                "attack",
                "benign",
            }
        ):
            raise ValueError(
                "Validation dataset contains "
                "unsupported labels."
            )

        if len(labels) < 2:
            raise ValueError(
                "Both attack and benign classes "
                "are required."
            )

        class_counts = y.value_counts()

        if (
            class_counts.min()
            < self.n_splits
        ):
            raise ValueError(
                "Each class must contain at least "
                f"{self.n_splits} samples."
            )

        encoded_y = (
            y == "attack"
        ).astype(int)

        cross_validator = (
            RepeatedStratifiedKFold(
                n_splits=self.n_splits,
                n_repeats=self.n_repeats,
                random_state=self.random_state,
            )
        )

        fold_metrics = []

        for train_index, test_index in (
            cross_validator.split(
                x,
                encoded_y,
            )
        ):

            x_train = x.iloc[
                train_index
            ]

            x_test = x.iloc[
                test_index
            ]

            y_train = encoded_y.iloc[
                train_index
            ]

            y_test = encoded_y.iloc[
                test_index
            ]

            model = clone(
                estimator
            )

            model.fit(
                x_train,
                y_train,
            )

            predictions = model.predict(
                x_test
            )

            metrics = {
                "accuracy": accuracy_score(
                    y_test,
                    predictions,
                ),

                "precision": precision_score(
                    y_test,
                    predictions,
                    zero_division=0,
                ),

                "recall": recall_score(
                    y_test,
                    predictions,
                    zero_division=0,
                ),

                "f1_score": f1_score(
                    y_test,
                    predictions,
                    zero_division=0,
                ),
            }

            if hasattr(
                model,
                "predict_proba",
            ):

                probabilities = (
                    model.predict_proba(
                        x_test
                    )[:, 1]
                )

                metrics["roc_auc"] = (
                    roc_auc_score(
                        y_test,
                        probabilities,
                    )
                )

            else:

                metrics["roc_auc"] = None

            fold_metrics.append(
                metrics
            )

        return self._summarize(
            fold_metrics
        )

    def _summarize(
        self,
        fold_metrics,
    ) -> dict:

        result = {
            "folds": len(
                fold_metrics
            )
        }

        metric_names = [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "roc_auc",
        ]

        for metric in metric_names:

            values = [
                fold[metric]
                for fold in fold_metrics
                if fold[metric] is not None
            ]

            if not values:

                result[
                    f"{metric}_mean"
                ] = None

                result[
                    f"{metric}_std"
                ] = None

                continue

            result[
                f"{metric}_mean"
            ] = float(
                np.mean(values)
            )

            result[
                f"{metric}_std"
            ] = float(
                np.std(values)
            )

        return result
