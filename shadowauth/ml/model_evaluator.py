from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


class ModelEvaluator:
    """
    Evaluates supervised ShadowAuth classifiers.

    The positive security class is 'attack'.
    """

    def evaluate(
        self,
        y_true,
        y_pred,
        attack_probabilities=None,
    ) -> dict:

        metrics = {
            "accuracy": accuracy_score(
                y_true,
                y_pred,
            ),

            "precision": precision_score(
                y_true,
                y_pred,
                pos_label="attack",
                zero_division=0,
            ),

            "recall": recall_score(
                y_true,
                y_pred,
                pos_label="attack",
                zero_division=0,
            ),

            "f1_score": f1_score(
                y_true,
                y_pred,
                pos_label="attack",
                zero_division=0,
            ),

            "confusion_matrix": confusion_matrix(
                y_true,
                y_pred,
                labels=[
                    "benign",
                    "attack",
                ],
            ).tolist(),
        }

        if attack_probabilities is not None:

            binary_true = [
                1 if label == "attack" else 0
                for label in y_true
            ]

            if len(set(binary_true)) >= 2:

                metrics["roc_auc"] = roc_auc_score(
                    binary_true,
                    attack_probabilities,
                )

            else:

                metrics["roc_auc"] = None

        else:

            metrics["roc_auc"] = None

        return metrics
