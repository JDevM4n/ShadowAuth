import numpy as np
from sklearn.ensemble import IsolationForest

from shadowauth.ml.model_trainer import ModelTrainer


class IsolationForestTrainer(ModelTrainer):
    """
    Unsupervised anomaly detection using
    Isolation Forest.
    """

    def __init__(
        self,
        n_estimators: int = 100,
        contamination="auto",
        random_state: int = 42,
    ):

        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state,
        )

        self.is_trained = False

    def train(
        self,
        x_train,
        y_train=None,
    ):

        self.model.fit(
            x_train
        )

        self.is_trained = True

        return self.model

    def predict(
        self,
        x,
    ):

        if not self.is_trained:

            raise RuntimeError(
                "Isolation Forest model has not "
                "been trained yet."
            )

        predictions = self.model.predict(
            x
        )

        return np.where(
            predictions == -1,
            "anomaly",
            "normal",
        )

    def anomaly_score(
        self,
        x,
    ):

        if not self.is_trained:

            raise RuntimeError(
                "Isolation Forest model has not "
                "been trained yet."
            )

        return -self.model.decision_function(
            x
        )
