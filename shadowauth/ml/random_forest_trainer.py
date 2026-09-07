from sklearn.ensemble import RandomForestClassifier

from shadowauth.ml.model_trainer import ModelTrainer


class RandomForestTrainer(ModelTrainer):
    """
    Trains and performs predictions using
    a Random Forest classifier.
    """

    def __init__(
        self,
        n_estimators: int = 100,
        random_state: int = 42,
        class_weight: str = "balanced",
    ):

        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            class_weight=class_weight,
        )

        self.is_trained = False

    def train(
        self,
        x_train,
        y_train,
    ):

        self.model.fit(
            x_train,
            y_train,
        )

        self.is_trained = True

        return self.model

    def predict(
        self,
        x,
    ):

        if not self.is_trained:

            raise RuntimeError(
                "Random Forest model has not "
                "been trained yet."
            )

        return self.model.predict(
            x
        )

    def predict_proba(
        self,
        x,
    ):

        if not self.is_trained:

            raise RuntimeError(
                "Random Forest model has not "
                "been trained yet."
            )

        return self.model.predict_proba(
            x
        )

    def get_feature_importances(
        self,
        feature_names,
    ) -> dict[str, float]:

        if not self.is_trained:

            raise RuntimeError(
                "Random Forest model has not "
                "been trained yet."
            )

        return dict(
            zip(
                feature_names,
                self.model.feature_importances_,
            )
        )