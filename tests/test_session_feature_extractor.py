import json

from shadowauth.extractors.session_feature_extractor import (
    SessionFeatureExtractor,
)
from shadowauth.parsers.cowrie_parser import CowrieParser


def test_session_feature_extractor():

    events = []
    raw_events = []

    parser = CowrieParser()

    with open(
        "samples/raw/cowrie/controlled-session-01.jsonl",
        encoding="utf-8",
    ) as file:

        for line in file:

            raw_event = json.loads(line)

            raw_events.append(raw_event)
            events.append(
                parser.parse(raw_event)
            )

    extractor = SessionFeatureExtractor()

    features = extractor.extract(
        events,
        label="attack",
    )

    commands = {
        str(event.get("input", "")).strip()
        for event in raw_events
        if (
            event.get("eventid")
            == "cowrie.command.input"
            and event.get("input")
        )
    }

    command_count = sum(
        1
        for event in raw_events
        if event.get("eventid")
        == "cowrie.command.input"
    )

    login_attempts = sum(
        1
        for event in raw_events
        if event.get("eventid")
        in (
            "cowrie.login.failed",
            "cowrie.login.success",
        )
    )

    download_count = sum(
        1
        for event in raw_events
        if event.get("eventid")
        == "cowrie.session.file_download"
    )

    assert features.session_id is not None

    assert features.duration_seconds >= 0

    assert features.command_count == command_count

    assert (
        features.unique_command_count
        == len(commands)
    )

    assert (
        features.unique_command_count
        <= features.command_count
    )

    assert (
        features.login_attempts
        == login_attempts
    )

    assert (
        features.successful_login
        is True
    )

    assert (
        features.download_count
        == download_count
    )

    assert features.process_count == 0

    assert features.shell_spawned is False

    assert (
        features.sensitive_file_access
        is False
    )

    assert features.label == "attack"