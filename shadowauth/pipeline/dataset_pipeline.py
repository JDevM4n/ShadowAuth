from pathlib import Path

import pandas as pd

from shadowauth.dataset.dataset_builder import DatasetBuilder
from shadowauth.dataset.dataset_validator import DatasetValidator


MASTER_DATASET_PATH = "datasets/dataset.csv"
TRAINING_DATASET_PATH = "datasets/training_dataset.csv"

MINIMUM_TRAINING_SAMPLES = 20


def build_training_dataset(
    master_path: str,
    training_path: str,
) -> None:

    dataset = pd.read_csv(
        master_path
    )

    training_dataset = dataset[
        dataset["label"].isin(
            [
                "attack",
                "benign",
            ]
        )
    ].copy()

    Path(training_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    training_dataset.to_csv(
        training_path,
        index=False,
    )

    print(
        f"Training dataset exported to "
        f"{training_path}"
    )

    print(
        f"Labeled sessions: "
        f"{len(training_dataset)}"
    )


def validate_structure(
    validator: DatasetValidator,
) -> bool:

    validations = {
        "columns": validator.validate_columns(),
        "nulls": validator.validate_nulls(),
        "session_ids": validator.validate_session_ids(),
        "ranges": validator.validate_ranges(),
        "labels": validator.validate_labels(),
    }

    failed = [
        name
        for name, valid in validations.items()
        if not valid
    ]

    if failed:

        print(
            "Structural validation failures: "
            + ", ".join(failed)
        )

        return False

    return True


def main():

    print("=" * 60)
    print("SHADOWAUTH DATASET PIPELINE")
    print("=" * 60)

    # -----------------------------------------------------
    # 1. MASTER DATASET
    # -----------------------------------------------------

    print(
        "\n[1/4] Building master dataset..."
    )

    builder = DatasetBuilder()

    builder.export_csv(
        MASTER_DATASET_PATH
    )

    # -----------------------------------------------------
    # 2. TRAINING DATASET
    # -----------------------------------------------------

    print(
        "\n[2/4] Building supervised "
        "training dataset..."
    )

    build_training_dataset(
        master_path=MASTER_DATASET_PATH,
        training_path=TRAINING_DATASET_PATH,
    )

    # -----------------------------------------------------
    # 3. VALIDATE MASTER
    # -----------------------------------------------------

    print(
        "\n[3/4] Validating master dataset..."
    )

    master_validator = DatasetValidator(
        MASTER_DATASET_PATH,
        mode="master",
    )

    master_validator.generate_report()

    if not master_validator.is_ready():

        print(
            "\nMaster dataset validation FAILED."
        )

        raise SystemExit(1)

    # -----------------------------------------------------
    # 4. VALIDATE TRAINING
    # -----------------------------------------------------

    print(
        "\n[4/4] Validating training dataset..."
    )

    training_validator = DatasetValidator(
        TRAINING_DATASET_PATH,
        mode="training",
        minimum_samples=MINIMUM_TRAINING_SAMPLES,
    )

    training_validator.generate_report()

    if not validate_structure(
        training_validator
    ):

        print(
            "\nTraining dataset has structural "
            "validation errors."
        )

        raise SystemExit(1)

    if not training_validator.validate_sample_count():

        print()
        print("=" * 60)
        print(
            "DATA PIPELINE READY"
        )
        print("=" * 60)

        print(
            "Master dataset is valid."
        )

        print(
            "Training dataset is structurally valid."
        )

        print(
            f"More labeled sessions are required "
            f"for supervised training "
            f"({len(training_validator.dataset)}/"
            f"{MINIMUM_TRAINING_SAMPLES})."
        )

        print(
            "Data collection can continue while "
            "the ML pipeline is developed."
        )

        return

    print()
    print("=" * 60)
    print(
        "DATASET READY FOR SUPERVISED "
        "MACHINE LEARNING"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()