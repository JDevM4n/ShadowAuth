import argparse
import json
from pathlib import Path

from shadowauth.database.postgres_repository import (
    PostgresRepository,
)
from shadowauth.parsers.falco_parser import (
    FalcoParser,
)


def count_falco_events(
    repository: PostgresRepository,
) -> int:

    with repository.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM normalized_events
            WHERE source = 'falco'
            """
        )

        row = cursor.fetchone()

    return int(row[0])


def main() -> None:

    parser_cli = argparse.ArgumentParser(
        description=(
            "Import Falco JSONL events "
            "into ShadowAuth PostgreSQL"
        )
    )

    parser_cli.add_argument(
        "file",
        type=Path,
    )

    args = parser_cli.parse_args()

    if not args.file.exists():
        raise FileNotFoundError(
            args.file
        )

    falco_parser = FalcoParser()
    repository = PostgresRepository()

    before = count_falco_events(
        repository
    )

    processed = 0

    with args.file.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1,
        ):

            line = line.strip()

            if not line:
                continue

            try:
                raw_event = json.loads(
                    line
                )
            except json.JSONDecodeError as exc:

                raise ValueError(
                    f"Invalid JSON on line "
                    f"{line_number}: {exc}"
                ) from exc

            event = falco_parser.parse(
                raw_event
            )

            repository.save_event(
                event
            )

            processed += 1

    after = count_falco_events(
        repository
    )

    print("=" * 70)
    print("SHADOWAUTH FALCO IMPORT")
    print("=" * 70)
    print(
        "JSONL:",
        args.file,
    )
    print(
        "Processed:",
        processed,
    )
    print(
        "Falco events before:",
        before,
    )
    print(
        "Falco events after :",
        after,
    )
    print(
        "New events         :",
        after - before,
    )

    repository.connection.close()


if __name__ == "__main__":
    main()
