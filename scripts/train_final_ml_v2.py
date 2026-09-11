import pandas as pd

from shadowauth.ml.model_persistence import ModelPersistence
from shadowauth.ml.random_forest_trainer import RandomForestTrainer


DATASET = "datasets/training_dataset.csv"
MODEL_PATH = "models/random_forest_v2.joblib"


METADATA_COLUMNS = [
    "session_id",
    "source_ip",
    "destination_ip",
    "source_port",
    "destination_port",
    "protocol",
]


def main():

    print("=" * 70)
    print("SHADOWAUTH - FINAL ML V2 TRAINING")
    print("=" * 70)

    dataset = pd.read_csv(
        DATASET
    )

    x = dataset.drop(
        columns=[
            "label",
            *METADATA_COLUMNS,
        ],
        errors="ignore",
    )

    y = dataset["label"]

    print(
        "Training samples:",
        len(dataset),
    )

    print()
    print("Class distribution:")
    print(
        y.value_counts()
    )

    trainer = RandomForestTrainer(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )

    trainer.train(
        x,
        y,
    )

    importances = (
        trainer.get_feature_importances(
            x.columns
        )
    )

    ordered = sorted(
        importances.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    print()
    print("Top features:")

    for feature, importance in ordered[:15]:

        print(
            f"{feature:<35} "
            f"{importance:.4f}"
        )

    metadata = {
        "model_name": "random_forest",
        "model_version": "2.0",
        "training_samples": len(dataset),
        "attack_samples": int(
            (y == "attack").sum()
        ),
        "benign_samples": int(
            (y == "benign").sum()
        ),
        "validation": {
            "method": "3-fold stratified grouped cross-validation",
            "behavior_groups": 18,
            "accuracy_mean": 0.9487,
            "precision_mean": 1.0,
            "recall_mean": 0.9298,
            "f1_mean": 0.9608,
            "roc_auc_mean": 1.0,
        },
    }

    ModelPersistence.save(
        model=trainer,
        path=MODEL_PATH,
        metadata=metadata,
        feature_names=x.columns,
    )

    print()
    print("=" * 70)
    print("FINAL MODEL SAVED")
    print("=" * 70)

    print(
        "Path:",
        MODEL_PATH,
    )

    print(
        "Features:",
        len(x.columns),
    )


if __name__ == "__main__":
    main()
