from pathlib import Path

from shadowauth.ml.dataset_splitter import DatasetSplitter
from shadowauth.ml.model_evaluator import ModelEvaluator
from shadowauth.ml.model_persistence import ModelPersistence
from shadowauth.ml.random_forest_trainer import RandomForestTrainer
from shadowauth.ml.xgboost_trainer import XGBoostTrainer


DATASET = "datasets/training_dataset.csv"


def get_attack_probabilities(
    trainer,
    x_test,
):
    probabilities = trainer.predict_proba(
        x_test
    )

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

    attack_index = classes.index(
        "attack"
    )

    return probabilities[
        :,
        attack_index,
    ]


def show_metrics(
    name,
    metrics,
):
    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    print(
        f"Accuracy : "
        f"{metrics['accuracy']:.4f}"
    )

    print(
        f"Precision: "
        f"{metrics['precision']:.4f}"
    )

    print(
        f"Recall   : "
        f"{metrics['recall']:.4f}"
    )

    print(
        f"F1       : "
        f"{metrics['f1_score']:.4f}"
    )

    roc_auc = metrics.get(
        "roc_auc"
    )

    print(
        "ROC-AUC  :",
        (
            f"{roc_auc:.4f}"
            if roc_auc is not None
            else "N/A"
        ),
    )

    print(
        "Confusion:",
        metrics[
            "confusion_matrix"
        ],
    )


def show_importances(
    name,
    trainer,
    feature_names,
):
    importances = (
        trainer
        .get_feature_importances(
            feature_names
        )
    )

    ordered = sorted(
        importances.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    print()
    print(
        f"TOP FEATURES - {name}"
    )

    for feature, importance in ordered[:12]:

        print(
            f"{feature:<35} "
            f"{importance:.4f}"
        )


def main():

    print("=" * 70)
    print("SHADOWAUTH ML V2 EVALUATION")
    print("=" * 70)

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

    print(
        "Training samples:",
        len(x_train),
    )

    print(
        "Testing samples :",
        len(x_test),
    )

    print()
    print(
        "Training labels:"
    )
    print(
        y_train.value_counts()
    )

    print()
    print(
        "Testing labels:"
    )
    print(
        y_test.value_counts()
    )

    evaluator = ModelEvaluator()

    models = {
        "random_forest": (
            RandomForestTrainer()
        ),
        "xgboost": (
            XGBoostTrainer()
        ),
    }

    results = {}

    for name, trainer in models.items():

        print()
        print(
            f"Training {name}..."
        )

        trainer.train(
            x_train,
            y_train,
        )

        predictions = (
            trainer.predict(
                x_test
            )
        )

        attack_probabilities = (
            get_attack_probabilities(
                trainer,
                x_test,
            )
        )

        metrics = evaluator.evaluate(
            y_true=y_test,
            y_pred=predictions,
            attack_probabilities=(
                attack_probabilities
            ),
        )

        results[name] = metrics

        show_metrics(
            name.upper(),
            metrics,
        )

        show_importances(
            name.upper(),
            trainer,
            x_train.columns,
        )

        artifact_path = Path(
            f"models/{name}_v2.joblib"
        )

        ModelPersistence.save(
            model=trainer,
            path=artifact_path,
            feature_names=x_train.columns,
            metadata={
                "model_version": "2.0",
                "dataset": DATASET,
                "training_samples": (
                    len(x_train)
                ),
                "testing_samples": (
                    len(x_test)
                ),
                "metrics": metrics,
            },
        )

        print(
            "\nSaved:",
            artifact_path,
        )

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for name, metrics in results.items():

        print(
            f"{name:<15} "
            f"F1={metrics['f1_score']:.4f} "
            f"Recall={metrics['recall']:.4f} "
            f"Precision={metrics['precision']:.4f} "
            f"AUC={metrics['roc_auc']:.4f}"
        )

    print()
    print(
        "NOTE: no final winner is selected "
        "from a single holdout split."
    )

    print(
        "Cross-validation will be used "
        "before selecting the production model."
    )


if __name__ == "__main__":
    main()
