import csv
from pathlib import Path

from shadowauth.database.postgres_repository import PostgresRepository
from shadowauth.extractors.session_feature_extractor import (
    SessionFeatureExtractor,
)


class DatasetBuilder:

    def __init__(self):

        self.repository = PostgresRepository()

        self.extractor = SessionFeatureExtractor()

    def _resolve_label(self, events) -> str:
        """
        Resolves the label associated with a session.

        Sessions without an explicit label are kept as
        'unlabeled' instead of being automatically classified
        as attacks.
        """

        labels = {
            event.label
            for event in events
            if event.label
        }

        if not labels:
            return "unlabeled"

        if len(labels) > 1:
            raise ValueError(
                f"Session contains conflicting labels: {labels}"
            )

        return next(iter(labels))

    def build(self):

        dataset = []

        sessions = self.repository.get_all_sessions()

        for session_id in sessions:

            events = self.repository.get_session(
                session_id
            )

            label = self._resolve_label(events)

            features = self.extractor.extract(
                events,
                label=label,
            )

            dataset.append(
                features.model_dump()
            )

        return dataset

    def export_csv(
        self,
        output_path: str = "datasets/dataset.csv",
    ):

        dataset = self.build()

        if not dataset:

            print("Dataset is empty.")
            return

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=dataset[0].keys(),
            )

            writer.writeheader()

            writer.writerows(dataset)

        print(
            f"Dataset exported to {output_path}"
        )