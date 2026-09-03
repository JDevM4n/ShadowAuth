from shadowauth.dataset.dataset_builder import DatasetBuilder
from shadowauth.dataset.dataset_validator import DatasetValidator


DATASET_PATH = "datasets/dataset.csv"


def main():

    print("=" * 60)
    print("SHADOWAUTH DATASET PIPELINE")
    print("=" * 60)

    print("\n[1/2] Building dataset...")

    builder = DatasetBuilder()

    builder.export_csv(
        DATASET_PATH
    )

    print("\n[2/2] Validating dataset...")

    validator = DatasetValidator(
        DATASET_PATH
    )

    validator.generate_report()

    validations = {
        "columns": validator.validate_columns(),
        "nulls": validator.validate_nulls(),
        "session_ids": validator.validate_session_ids(),
        "ranges": validator.validate_ranges(),
        "sample_count": validator.validate_sample_count(),
        "labels": validator.validate_labels(),
    }

    failed = [
        name
        for name, valid in validations.items()
        if not valid
    ]

    if failed:

        print(
            "\nDataset is NOT ready for "
            "supervised Machine Learning."
        )

        print(
            "Failed validations:",
            ", ".join(failed),
        )

        raise SystemExit(1)

    print(
        "\nDataset is ready for "
        "Machine Learning."
    )


if __name__ == "__main__":
    main()