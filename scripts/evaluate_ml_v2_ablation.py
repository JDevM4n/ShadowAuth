from shadowauth.ml.dataset_splitter import DatasetSplitter
from shadowauth.ml.model_evaluator import ModelEvaluator
from shadowauth.ml.random_forest_trainer import RandomForestTrainer
from shadowauth.ml.xgboost_trainer import XGBoostTrainer


DATASET = "datasets/training_dataset.csv"

DROP_FEATURES = [
    "download_command_count",
]


def attack_probabilities(
    trainer,
    x,
):

    probabilities = trainer.predict_proba(x)

    if isinstance(
        trainer,
        RandomForestTrainer,
    ):
        classes = list(
            trainer.model.classes_
        )

    else:
        classes = list(
            trainer.get_classes()
        )

    index = classes.index("attack")

    return probabilities[:, index]


def evaluate_model(
    name,
    trainer,
    x_train,
    x_test,
    y_train,
    y_test,
):

    trainer.train(
        x_train,
        y_train,
    )

    predictions = trainer.predict(
        x_test
    )

    probabilities = attack_probabilities(
        trainer,
        x_test,
    )

    evaluator = ModelEvaluator()

    metrics = evaluator.evaluate(
        y_true=y_test,
        y_pred=predictions,
        attack_probabilities=probabilities,
    )

    print()
    print("=" * 65)
    print(name)
    print("=" * 65)

    print(
        f"Accuracy : {metrics['accuracy']:.4f}"
    )
    print(
        f"Precision: {metrics['precision']:.4f}"
    )
    print(
        f"Recall   : {metrics['recall']:.4f}"
    )
    print(
        f"F1       : {metrics['f1_score']:.4f}"
    )
    print(
        f"ROC-AUC  : {metrics['roc_auc']:.4f}"
    )
    print(
        "Confusion:",
        metrics["confusion_matrix"],
    )

    importances = (
        trainer.get_feature_importances(
            x_train.columns
        )
    )

    print("\nTop features:")

    for feature, value in sorted(
        importances.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:12]:

        print(
            f"{feature:<35} {value:.4f}"
        )


def main():

    splitter = DatasetSplitter(
        DATASET
    )

    (
        x_train,
        x_test,
        y_train,
        y_test,
    ) = splitter.split(
        test_size=0.20,
        random_state=42,
    )

    x_train = x_train.drop(
        columns=DROP_FEATURES,
        errors="ignore",
    )

    x_test = x_test.drop(
        columns=DROP_FEATURES,
        errors="ignore",
    )

    print("=" * 65)
    print("SHADOWAUTH ML V2 - ABLATION TEST")
    print("=" * 65)

    print(
        "Removed features:",
        DROP_FEATURES,
    )

    print(
        "Train:",
        len(x_train)
    )

    print(
        "Test :",
        len(x_test)
    )

    evaluate_model(
        "RANDOM FOREST WITHOUT DOWNLOAD_COMMAND_COUNT",
        RandomForestTrainer(),
        x_train,
        x_test,
        y_train,
        y_test,
    )

    evaluate_model(
        "XGBOOST WITHOUT DOWNLOAD_COMMAND_COUNT",
        XGBoostTrainer(),
        x_train,
        x_test,
        y_train,
        y_test,
    )


if __name__ == "__main__":
    main()
