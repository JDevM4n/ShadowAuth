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


VALID_LABELS = {
    "attack",
    "benign",
    "unlabeled",
}


TRAINING_LABELS = {
    "attack",
    "benign",
}


class DatasetValidator:
    """
    Validates ShadowAuth datasets.

    Modes:

    master:
        Allows attack, benign and unlabeled sessions.

    training:
        Only allows sessions with supervised
        ground-truth labels: attack and benign.
    """

    def __init__(
        self,
        dataset_path: str,
        mode: str = "training",
        minimum_samples: int = 20,
    ):

        if mode not in {
            "master",
            "training",
        }:
            raise ValueError(
                "mode must be 'master' or 'training'"
            )

        self.dataset_path = Path(
            dataset_path
        )

        self.mode = mode

        self.minimum_samples = minimum_samples

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

        if (
            "session_id"
            not in self.dataset.columns
        ):
            return False

        if (
            self.dataset["session_id"]
            .isnull()
            .any()
        ):
            return False

        return (
            self.dataset["session_id"]
            .duplicated()
            .sum()
            == 0
        )

    def validate_labels(self) -> bool:

        if (
            "label"
            not in self.dataset.columns
        ):
            return False

        if (
            self.dataset["label"]
            .isnull()
            .any()
        ):
            return False

        labels = set(
            self.dataset["label"].unique()
        )

        if self.mode == "master":

            return labels.issubset(
                VALID_LABELS
            )

        if not labels.issubset(
            TRAINING_LABELS
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
    ) -> bool:

        return (
            len(self.dataset)
            >= self.minimum_samples
        )

    def is_ready(self) -> bool:

        return all(
            [
                self.validate_columns(),
                self.validate_nulls(),
                self.validate_session_ids(),
                self.validate_ranges(),
                self.validate_labels(),
                self.validate_sample_count(),
            ]
        )

    def generate_report(self) -> None:

        print("=" * 60)
        print(
            "SHADOWAUTH DATASET VALIDATION REPORT"
        )
        print("=" * 60)

        print(
            f"Mode: {self.mode}"
        )

        print(
            f"Dataset: {self.dataset_path}"
        )

        print(
            f"Rows: {len(self.dataset)}"
        )

        print(
            f"Columns: {len(self.dataset.columns)}"
        )

        print(
            f"Columns valid: "
            f"{self.validate_columns()}"
        )

        print(
            f"Null values valid: "
            f"{self.validate_nulls()}"
        )

        print(
            f"Session IDs valid: "
            f"{self.validate_session_ids()}"
        )

        print(
            f"Ranges valid: "
            f"{self.validate_ranges()}"
        )

        print(
            f"Labels valid: "
            f"{self.validate_labels()}"
        )

        print(
            f"Minimum samples "
            f"({self.minimum_samples}) reached: "
            f"{self.validate_sample_count()}"
        )

        print(
            f"Dataset ready: "
            f"{self.is_ready()}"
        )

        if (
            "label"
            in self.dataset.columns
        ):

            print(
                "\nClass distribution:"
            )

            print(
                self.dataset["label"]
                .value_counts(
                    dropna=False
                )
            )

        print("=" * 60)