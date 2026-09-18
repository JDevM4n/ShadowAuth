from fastapi import APIRouter, Depends, Query

from shadowauth.api.dependencies import get_repository
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


router = APIRouter(
    prefix="/api/events",
    tags=["events"],
)


@router.get("")
def list_events(
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    source: str | None = None,
    session_id: str | None = None,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    conditions = []
    parameters = []

    if source is not None:
        conditions.append(
            "source = %s"
        )
        parameters.append(
            source
        )

    if session_id is not None:
        conditions.append(
            "session_id = %s"
        )
        parameters.append(
            session_id
        )

    where_clause = ""

    if conditions:
        where_clause = (
            "WHERE "
            + " AND ".join(conditions)
        )

    query = f"""
        SELECT
            event_id,
            source,
            event_type,
            rule_id,
            rule_name,
            event_timestamp,
            session_id,
            severity,
            severity_native,
            network,
            host,
            data
        FROM normalized_events
        {where_clause}
        ORDER BY event_timestamp DESC
        LIMIT %s OFFSET %s
    """

    parameters.extend(
        [
            limit,
            offset,
        ]
    )

    with repository.connection.cursor() as cursor:
        cursor.execute(
            query,
            parameters,
        )

        rows = cursor.fetchall()

    return [
        {
            "event_id": str(row[0]),
            "source": row[1],
            "event_type": row[2],
            "rule_id": row[3],
            "rule_name": row[4],
            "event_timestamp": row[5],
            "session_id": row[6],
            "severity": row[7],
            "severity_native": row[8],
            "network": row[9],
            "host": row[10],
            "data": row[11],
        }
        for row in rows
    ]
