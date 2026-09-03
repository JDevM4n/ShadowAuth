from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "session_id",
    "duration_seconds",
    "command_count",
    "unique_command_count",
    "login_attempts",
    "successful_login",
    "download_count",
    "source_ip",
    "destination_ip",
    "source_port",
    "destination_port",
    "protocol",
    "process_count",
    "shell_spawned",
    "sensitive_file_access",
    "max_severity",
    "average_severity",
    "session_hour",
    "weekend",
    "label",
]


class DatasetValidator:
    """
    Validates datasets before they are used for
    Machine Learning training.
    """

    def __init__(
        self,
        dataset_path: str,
    ):

        self.dataset_path = Path(
            dataset_path
        )

        self.dataset = pd.read_csv(
            self.dataset_path
        )

    def validate_columns(self) -> bool:

        dataset_columns = set(
            self.dataset.columns
        )

        missing = (
            set(REQUIRED_COLUMNS)
            - dataset_columns
        )

        if missing:

            print(
                f"Missing columns: {missing}"
            )

            return False

        return True

    def validate_nulls(self) -> bool:

        return (
            self.dataset
            .isnull()
            .sum()
            .sum()
            == 0
        )

    def validate_session_ids(self) -> bool:

        if "session_id" not in self.dataset.columns:
            return False

        if self.dataset["session_id"].isnull().any():
            return False

        return (
            self.dataset["session_id"]
            .duplicated()
            .sum()
            == 0
        )

    def validate_labels(self) -> bool:

        if "label" not in self.dataset.columns:
            return False

        if self.dataset["label"].isnull().any():
            return False

        if (
            self.dataset["label"]
            .eq("unlabeled")
            .any()
        ):
            return False

        return (
            self.dataset["label"]
            .nunique()
            >= 2
        )

    def validate_ranges(self) -> bool:

        non_negative_columns = [
            "duration_seconds",
            "command_count",
            "unique_command_count",
            "login_attempts",
            "download_count",
            "process_count",
            "max_severity",
            "average_severity",
        ]

        for column in non_negative_columns:

            if (
                self.dataset[column] < 0
            ).any():

                return False

        if not (
            self.dataset["session_hour"]
            .between(0, 23)
            .all()
        ):
            return False

        if (
            self.dataset[
                "unique_command_count"
            ]
            >
            self.dataset[
                "command_count"
            ]
        ).any():

            return False

        return True

    def validate_sample_count(
        self,
        minimum: int = 20,
    ) -> bool:

        return (
            len(self.dataset)
            >= minimum
        )

    def generate_report(self) -> None:

        print("=" * 60)
        print("SHADOWAUTH DATASET VALIDATION REPORT")
        print("=" * 60)

        print(
            f"Rows: {len(self.dataset)}"
        )

        print(
            f"Columns: {len(self.dataset.columns)}"
        )

        print(
            f"Columns valid: {self.validate_columns()}"
        )

        print(
            f"Null values valid: {self.validate_nulls()}"
        )

        print(
            f"Session IDs valid: {self.validate_session_ids()}"
        )

        print(
            f"Ranges valid: {self.validate_ranges()}"
        )

        print(
            f"Minimum samples reached: "
            f"{self.validate_sample_count()}"
        )

        print(
            f"Supervised labels valid: "
            f"{self.validate_labels()}"
        )

        if "label" in self.dataset.columns:

            print("\nClass distribution:")

            print(
                self.dataset["label"]
                .value_counts(
                    dropna=False
                )
            )

        print("=" * 60)