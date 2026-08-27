from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
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

        self.dataset_path = Path(dataset_path)

        self.dataset = pd.read_csv(
            self.dataset_path
        )

    def validate_columns(self) -> bool:
        """
        Validates required columns.
        """

        dataset_columns = set(self.dataset.columns)

        missing = set(REQUIRED_COLUMNS) - dataset_columns

        if missing:

            print(f"Missing columns: {missing}")

            return False

        return True

    def validate_nulls(self) -> bool:
        """
        Validates missing values.
        """

        return self.dataset.isnull().sum().sum() == 0

    def validate_duplicates(self) -> bool:
        """
        Validates duplicated rows.
        """

        return self.dataset.duplicated().sum() == 0

    def validate_labels(self) -> bool:
        """
        Validates that the label column exists
        and contains no missing values.
        """

        if "label" not in self.dataset.columns:

            return False

        return self.dataset["label"].notna().all()

    def generate_report(self) -> None:
        """
        Prints a validation report.
        """

        print("=" * 50)
        print("DATASET VALIDATION REPORT")
        print("=" * 50)

        print(f"Rows: {len(self.dataset)}")
        print(f"Columns: {len(self.dataset.columns)}")
        print(f"Columns valid: {self.validate_columns()}")
        print(f"Null values: {self.validate_nulls()}")
        print(f"Duplicated rows: {self.validate_duplicates()}")
        print(f"Labels valid: {self.validate_labels()}")

        print("=" * 50)