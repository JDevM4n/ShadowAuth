from typing import Literal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from pydantic import BaseModel
from psycopg.types.json import Jsonb

from shadowauth.api.dependencies import get_repository
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


router = APIRouter(
    prefix="/api/incidents",
    tags=["incidents"],
)


class IncidentStatusUpdate(BaseModel):
    status: Literal[
        "open",
        "investigating",
        "resolved",
    ]


def serialize_incident(row):
    return {
        "incident_id": row[0],
        "correlation_id": row[1],
        "session_id": row[2],
        "title": row[3],
        "description": row[4],
        "threat_type": row[5],
        "severity": row[6],
        "status": row[7],
        "evidence": row[8],
        "created_at": row[9],
        "updated_at": row[10],
        "resolved_at": row[11],
    }


@router.get("")
def list_incidents(
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    status: str | None = None,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    conditions = []
    parameters = []

    if status is not None:
        conditions.append(
            "status = %s"
        )
        parameters.append(status)

    where_clause = ""

    if conditions:
        where_clause = (
            "WHERE "
            + " AND ".join(conditions)
        )

    query = f"""
        SELECT
            incident_id,
            correlation_id,
            session_id,
            title,
            description,
            threat_type,
            severity,
            status,
            evidence,
            created_at,
            updated_at,
            resolved_at
        FROM incidents
        {where_clause}
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 4
                WHEN 'high' THEN 3
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 1
                ELSE 0
            END DESC,
            created_at DESC
        LIMIT %s
    """

    parameters.append(limit)

    with repository.connection.cursor() as cursor:
        cursor.execute(
            query,
            parameters,
        )

        rows = cursor.fetchall()

    return [
        serialize_incident(row)
        for row in rows
    ]


@router.post(
    "/from-alert/{correlation_id}"
)
def create_incident_from_alert(
    correlation_id: int,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    with repository.connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                correlation_id,
                session_id,
                rule_id,
                rule_name,
                severity,
                threat_type,
                description,
                evidence
            FROM correlation_results
            WHERE correlation_id = %s
            """,
            (correlation_id,),
        )

        correlation = cursor.fetchone()

        if correlation is None:
            raise HTTPException(
                status_code=404,
                detail="Security alert not found.",
            )

        title = (
            f"{correlation[3]} - "
            f"{correlation[5]}"
        )

        cursor.execute(
            """
            INSERT INTO incidents (
                correlation_id,
                session_id,
                title,
                description,
                threat_type,
                severity,
                status,
                evidence
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'open',
                %s
            )
            ON CONFLICT (correlation_id)
            DO NOTHING
            RETURNING incident_id
            """,
            (
                correlation[0],
                correlation[1],
                title,
                correlation[6],
                correlation[5],
                correlation[4].lower(),
                Jsonb(correlation[7] or {}),
            ),
        )

        created = cursor.fetchone()

        repository.connection.commit()

        cursor.execute(
            """
            SELECT
                incident_id,
                correlation_id,
                session_id,
                title,
                description,
                threat_type,
                severity,
                status,
                evidence,
                created_at,
                updated_at,
                resolved_at
            FROM incidents
            WHERE correlation_id = %s
            """,
            (correlation_id,),
        )

        incident = cursor.fetchone()

    if incident is None:
        raise HTTPException(
            status_code=500,
            detail="Could not create incident.",
        )

    return serialize_incident(incident)


@router.patch(
    "/{incident_id}/status"
)
def update_incident_status(
    incident_id: int,
    update: IncidentStatusUpdate,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    with repository.connection.cursor() as cursor:

        cursor.execute(
            """
            UPDATE incidents
            SET
                status = %s,
                updated_at = CURRENT_TIMESTAMP,
                resolved_at =
                    CASE
                        WHEN %s = 'resolved'
                            THEN CURRENT_TIMESTAMP
                        ELSE NULL
                    END
            WHERE incident_id = %s
            RETURNING
                incident_id,
                correlation_id,
                session_id,
                title,
                description,
                threat_type,
                severity,
                status,
                evidence,
                created_at,
                updated_at,
                resolved_at
            """,
            (
                update.status,
                update.status,
                incident_id,
            ),
        )

        incident = cursor.fetchone()

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found.",
            )

        repository.connection.commit()

    return serialize_incident(incident)
