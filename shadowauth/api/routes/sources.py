from fastapi import APIRouter, Depends

from shadowauth.api.dependencies import get_repository
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


router = APIRouter(
    prefix="/api/sources",
    tags=["sources"],
)


SOURCE_CATALOG = [
    {
        "source_id": "cowrie",
        "name": "Cowrie SSH Honeypot",
        "source_type": "Honeypot",
        "protocol": "SSH / TCP 2222",
        "format": "JSON",
        "integration": "NormalizedEvent",
        "honeypot_linked": True,
    },
    {
        "source_id": "falco",
        "name": "Falco Runtime Security",
        "source_type": "Runtime Security",
        "protocol": "Host telemetry",
        "format": "JSONL",
        "integration": "JSONL importer",
        "honeypot_linked": False,
    },
    {
        "source_id": "zeek",
        "name": "Zeek Network Telemetry",
        "source_type": "Network",
        "protocol": "Network logs",
        "format": "Zeek",
        "integration": "Parser support",
        "honeypot_linked": False,
    },
]


@router.get("")
def list_sources(
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    with repository.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                source,
                COUNT(*) AS total_events,
                MIN(event_timestamp) AS first_event,
                MAX(event_timestamp) AS last_event,
                MAX(event_timestamp)
                    >= (
                        CURRENT_TIMESTAMP::timestamp
                        - INTERVAL '15 minutes'
                    ) AS telemetry_recent
            FROM normalized_events
            GROUP BY source
            ORDER BY source
            """
        )

        rows = cursor.fetchall()

    telemetry = {
        row[0]: {
            "events": row[1],
            "first_event": row[2],
            "last_event": row[3],
            "telemetry_recent": bool(row[4]),
        }
        for row in rows
    }

    sources = []

    for definition in SOURCE_CATALOG:
        stats = telemetry.get(
            definition["source_id"]
        )

        if stats is None:
            status = "supported"
            events = 0
            first_event = None
            last_event = None
        else:
            status = (
                "recent"
                if stats["telemetry_recent"]
                else "stale"
            )

            events = stats["events"]
            first_event = stats["first_event"]
            last_event = stats["last_event"]

        sources.append(
            {
                **definition,
                "status": status,
                "events": events,
                "first_event": first_event,
                "last_event": last_event,
            }
        )

    return {
        "total": len(sources),
        "with_telemetry": sum(
            1
            for source in sources
            if source["events"] > 0
        ),
        "stale": sum(
            1
            for source in sources
            if source["status"] == "stale"
        ),
        "honeypot_linked": sum(
            1
            for source in sources
            if source["honeypot_linked"]
        ),
        "sources": sources,
    }
