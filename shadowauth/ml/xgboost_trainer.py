from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

from shadowauth.ml.model_trainer import ModelTrainer


class XGBoostTrainer(ModelTrainer):
    """
    Supervised binary classification using XGBoost.
    """

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 3,
        learning_rate: float = 0.1,
        random_state: int = 42,
    ):

        self.model = XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            eval_metric="logloss",
        )

        self.label_encoder = LabelEncoder()

        self.is_trained = False

    def train(
        self,
        x_train,
        y_train,
    ):

        encoded_labels = (
            self.label_encoder.fit_transform(
                y_train
            )
        )

        self.model.fit(
            x_train,
            encoded_labels,
        )

        self.is_trained = True

        return self.model

    def predict(
        self,
        x,
    ):

        if not self.is_trained:

            raise RuntimeError(
                "XGBoost model has not been "
                "trained yet."
            )

        encoded_predictions = (
            self.model.predict(x)
        )

        return (
            self.label_encoder.inverse_transform(
                encoded_predictions.astype(int)
            )
        )

    def predict_proba(
        self,
        x,
    ):

        if not self.is_trained:

            raise RuntimeError(
                "XGBoost model has not been "
                "trained yet."
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
                "XGBoost model has not been "
                "trained yet."
            )

        return dict(
            zip(
                feature_names,
                self.model.feature_importances_,
            )
        )

    def get_classes(
        self,
    ):

        if not self.is_trained:

            raise RuntimeError(
                "XGBoost model has not been "
                "trained yet."
            )

        return self.label_encoder.classes_
