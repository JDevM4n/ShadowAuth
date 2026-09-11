import hashlib
from collections import defaultdict

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from shadowauth.database.postgres_repository import PostgresRepository
from shadowauth.ml.dataset_splitter import DatasetSplitter
from shadowauth.ml.model_evaluator import ModelEvaluator
from shadowauth.ml.random_forest_trainer import RandomForestTrainer
from shadowauth.ml.xgboost_trainer import XGBoostTrainer


DATASET = "datasets/training_dataset.csv"


def behavioral_fingerprint(
    repo,
    session_id,
):
    events = repo.get_session(session_id)

    commands = []

    for event in events:

        if event.event_type != "cowrie.command.input":
            continue

        command = str(
            event.data.get("input", "")
        ).strip().lower()

        if not command:
            continue

        # Ground-truth markers must never define a group.
        if "shadowauth_controlled_" in command:
            continue

        normalized = " ".join(
            command.split()
        )

        commands.append(normalized)

    if not commands:
        return f"no_commands:{session_id}"

    payload = "\n".join(commands)

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()[:16]


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

    attack_index = classes.index(
        "attack"
    )

    return probabilities[
        :,
        attack_index,
    ]


def run_model(
    name,
    factory,
    x,
    y,
    groups,
):

    cv = StratifiedGroupKFold(
        n_splits=3,
        shuffle=True,
        random_state=42,
    )

    evaluator = ModelEvaluator()

    fold_metrics = []

    print()
    print("=" * 75)
    print(name)
    print("=" * 75)

    for fold, (
        train_idx,
        test_idx,
    ) in enumerate(
        cv.split(
            x,
            y,
            groups,
        ),
        start=1,
    ):

        x_train = x.iloc[train_idx]
        x_test = x.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        train_groups = set(
            groups.iloc[train_idx]
        )

        test_groups = set(
            groups.iloc[test_idx]
        )

        overlap = (
            train_groups
            & test_groups
        )

        print()
        print(
            f"Fold {fold}"
        )

        print(
            "Train samples:",
            len(x_train),
        )

        print(
            "Test samples :",
            len(x_test),
        )

        print(
            "Train groups :",
            len(train_groups),
        )

        print(
            "Test groups  :",
            len(test_groups),
        )

        print(
            "Group overlap:",
            len(overlap),
        )

        print(
            "Train labels:",
            y_train.value_counts().to_dict(),
        )

        print(
            "Test labels :",
            y_test.value_counts().to_dict(),
        )

        trainer = factory()

        trainer.train(
            x_train,
            y_train,
        )

        predictions = trainer.predict(
            x_test
        )

        probabilities = (
            attack_probabilities(
                trainer,
                x_test,
            )
        )

        metrics = evaluator.evaluate(
            y_true=y_test,
            y_pred=predictions,
            attack_probabilities=probabilities,
        )

        fold_metrics.append(
            metrics
        )

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
            "ROC-AUC  :",
            (
                f"{metrics['roc_auc']:.4f}"
                if metrics["roc_auc"] is not None
                else "N/A"
            ),
        )

        print(
            "Confusion:",
            metrics["confusion_matrix"],
        )

    print()
    print("-" * 75)
    print("MEAN METRICS")
    print("-" * 75)

    for key in [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    ]:

        values = [
            metric[key]
            for metric in fold_metrics
            if metric[key] is not None
        ]

        print(
            f"{key:<10}: "
            f"{np.mean(values):.4f} "
            f"+/- {np.std(values):.4f}"
        )


def main():

    dataset = pd.read_csv(
        DATASET
    )

    repo = PostgresRepository()

    groups = []

    for session_id in dataset[
        "session_id"
    ]:

        groups.append(
            behavioral_fingerprint(
                repo,
                session_id,
            )
        )

    groups = pd.Series(
        groups,
        index=dataset.index,
    )

    print("=" * 75)
    print("SHADOWAUTH ML V2 - GROUPED CROSS VALIDATION")
    print("=" * 75)

    print(
        "Labeled sessions:",
        len(dataset),
    )

    print(
        "Behavior groups :",
        groups.nunique(),
    )

    group_sizes = (
        groups.value_counts()
    )

    print()
    print("Largest behavior groups:")

    print(
        group_sizes.head(10)
    )

    splitter = DatasetSplitter(
        DATASET
    )

    metadata = [
        "label",
        *splitter.METADATA_COLUMNS,
    ]

    x = dataset.drop(
        columns=metadata,
        errors="ignore",
    )

    y = dataset["label"]

    run_model(
        "RANDOM FOREST - GROUPED CV",
        RandomForestTrainer,
        x,
        y,
        groups,
    )

    run_model(
        "XGBOOST - GROUPED CV",
        XGBoostTrainer,
        x,
        y,
        groups,
    )


if __name__ == "__main__":
    main()
