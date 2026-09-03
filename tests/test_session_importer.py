import shadowauth.pipeline.session_importer as importer_module

from shadowauth.pipeline.session_importer import SessionImporter


def test_session_importer(monkeypatch):

    saved_events = []

    class FakeRepository:

        def save_event(self, event):
            saved_events.append(event)

    monkeypatch.setattr(
        importer_module,
        "PostgresRepository",
        FakeRepository,
    )

    importer = SessionImporter()

    importer.import_file(
        "samples/raw/cowrie/controlled-session-01.jsonl"
    )

    assert len(saved_events) == 24

    session_ids = {
        event.session_id
        for event in saved_events
    }

    assert len(session_ids) == 1

    event_ids = {
        event.event_id
        for event in saved_events
    }

    assert len(event_ids) == 24