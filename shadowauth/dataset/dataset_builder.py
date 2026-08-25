import csv
from pathlib import Path

from shadowauth.database.postgres_repository import PostgresRepository
from shadowauth.extractors.session_feature_extractor import SessionFeatureExtractor


class DatasetBuilder:

    def __init__(self):

        self.repository = PostgresRepository()

        self.extractor = SessionFeatureExtractor()

    def build(self):

        dataset = []

        sessions = self.repository.get_all_sessions()

        for session_id in sessions:

            events = self.repository.get_session(session_id)

            features = self.extractor.extract(
                events,
                label="attack",
            )

            dataset.append(features.model_dump())

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
        ) as csv_file:

            writer = csv.DictWriter(

                csv_file,

                fieldnames=dataset[0].keys()

            )

            writer.writeheader()

            writer.writerows(dataset)

        print(f"Dataset exported to {output_path}")