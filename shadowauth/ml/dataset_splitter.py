from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetSplitter:
    """
    Splits a dataset into training and testing sets.
    """

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

        x = self.dataset.drop(
            columns=["label"]
        )

        y = self.dataset["label"]

        return train_test_split(
            x,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y,
        )