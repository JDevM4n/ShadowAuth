from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetSplitter:
    """
    Splits a dataset into training and testing sets.
    """

    METADATA_COLUMNS = [
        "session_id",
        "source_ip",
        "destination_ip",
        "protocol",
    ]

    def __init__(
        self,
        dataset_path: str,
    ):

        self.dataset = pd.read_csv(
            Path(dataset_path)
        )

    def split(
        self,
        test_size: float = 0.2,
        random_state: int = 42,
    ):

        if "label" not in self.dataset.columns:
            raise ValueError(
                "Dataset does not contain label column."
            )

        if self.dataset["label"].isnull().any():
            raise ValueError(
                "Dataset contains unlabeled samples."
            )

        if self.dataset["label"].eq(
            "unlabeled"
        ).any():

            raise ValueError(
                "Dataset contains unlabeled sessions."
            )

        class_counts = (
            self.dataset["label"]
            .value_counts()
        )

        if len(class_counts) < 2:

            raise ValueError(
                "At least two classes are required "
                "for supervised training."
            )

        if (class_counts < 2).any():

            raise ValueError(
                "Each class must contain at least "
                "two samples before splitting."
            )

        columns_to_drop = [
            "label",
            *self.METADATA_COLUMNS,
        ]

        x = self.dataset.drop(
            columns=columns_to_drop,
            errors="ignore",
        )

        y = self.dataset["label"]

        return train_test_split(
            x,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y,
        )