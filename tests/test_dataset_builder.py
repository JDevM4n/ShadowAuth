import json

import shadowauth.dataset.dataset_builder as dataset_builder_module
from shadowauth.dataset.dataset_builder import DatasetBuilder
from shadowauth.parsers.cowrie_parser import CowrieParser


def test_dataset_builder(
    monkeypatch,
    tmp_path,
):

    events = []

    parser = CowrieParser()

    with open(
        "samples/raw/cowrie/controlled-session-01.jsonl",
        encoding="utf-8",
    ) as file:

        for line in file:

            raw_event = json.loads(line)

            events.append(
                parser.parse(raw_event)
            )

    session_id = events[0].session_id

    class FakeRepository:

        def get_all_sessions(self):

            return [session_id]

        def get_session(
            self,
            requested_session_id,
        ):

            assert (
                requested_session_id
                == session_id
            )

            return events

        def get_session_label(
            self,
            requested_session_id,
        ):

            assert (
                requested_session_id
                == session_id
            )

            return "attack"

    monkeypatch.setattr(
        dataset_builder_module,
        "PostgresRepository",
        FakeRepository,
    )

    builder = DatasetBuilder()

    dataset = builder.build()

    assert len(dataset) == 1

    row = dataset[0]

    assert (
        row["session_id"]
        == session_id
    )

    assert (
        row["command_count"]
        > 0
    )

    assert (
        row["unique_command_count"]
        > 0
    )

    assert (
        row["unique_command_count"]
        <= row["command_count"]
    )

    assert row["label"] == "attack"

    output_file = (
        tmp_path / "dataset.csv"
    )

    builder.export_csv(
        str(output_file)
    )

    assert output_file.exists()