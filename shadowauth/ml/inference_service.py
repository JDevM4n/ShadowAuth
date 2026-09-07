import pandas as pd

from shadowauth.ml.model_persistence import (
    ModelPersistence,
)


class ModelInferenceService:
    """
    Loads a persisted ShadowAuth model artifact
    and performs inference on new feature vectors.
    """

    def __init__(
        self,
        artifact_path,
    ):

        artifact = ModelPersistence.load(
            artifact_path
        )

        self.trainer = artifact["model"]

        self.feature_names = artifact.get(
            "feature_names"
        )

        self.metadata = artifact.get(
            "metadata",
            {},
        )

    def _prepare_features(
        self,
        features,
    ) -> pd.DataFrame:

        if isinstance(
            features,
            dict,
        ):
            dataframe = pd.DataFrame(
                [features]
            )

        elif isinstance(
            features,
            pd.DataFrame,
        ):
            dataframe = features.copy()

        else:
            raise TypeError(
                "Features must be provided "
                "as a dict or pandas DataFrame."
            )

        if self.feature_names is None:
            raise ValueError(
                "Model artifact does not contain "
                "feature names."
            )

        missing_features = [
            feature
            for feature in self.feature_names
            if feature not in dataframe.columns
        ]

        if missing_features:
            raise ValueError(
                "Missing required features: "
                + ", ".join(
                    missing_features
                )
            )

        return dataframe[
            self.feature_names
        ]

    def predict(
        self,
        features,
    ) -> list[dict]:

        x = self._prepare_features(
            features
        )

        predictions = self.trainer.predict(
            x
        )

        probabilities = None
        classes = None

        if hasattr(
            self.trainer,
            "predict_proba",
        ):

            probabilities = (
                self.trainer.predict_proba(
                    x
                )
            )

            if hasattr(
                self.trainer,
                "get_classes",
            ):
                classes = list(
                    self.trainer.get_classes()
                )

            elif hasattr(
                self.trainer,
                "model",
            ) and hasattr(
                self.trainer.model,
                "classes_",
            ):
                classes = list(
                    self.trainer.model.classes_
                )

        results = []

        for index, prediction in enumerate(
            predictions
        ):

            result = {
                "prediction": str(
                    prediction
                ),
                "attack_probability": None,
            }

            if (
                probabilities is not None
                and classes is not None
                and "attack" in classes
            ):

                attack_index = classes.index(
                    "attack"
                )

                result[
                    "attack_probability"
                ] = float(
                    probabilities[
                        index,
                        attack_index,
                    ]
                )

            results.append(
                result
            )

        return results
