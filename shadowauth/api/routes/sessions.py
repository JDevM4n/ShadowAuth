from fastapi import APIRouter, Depends, HTTPException, Query

from shadowauth.api.dependencies import get_repository
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


router = APIRouter(
    prefix="/api/sessions",
    tags=["sessions"],
)


@router.get("")
def list_sessions(
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    label: str | None = None,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    with repository.connection.cursor() as cursor:

        if label:
            cursor.execute(
                """
                SELECT
                    session_id,
                    sources,
                    first_event_timestamp,
                    last_event_timestamp,
                    event_count,
                    label,
                    attack_type,
                    label_source,
                    label_confidence,
                    data_origin
                FROM sessions
                WHERE label = %s
                ORDER BY last_event_timestamp DESC
                LIMIT %s OFFSET %s
                """,
                (
                    label,
                    limit,
                    offset,
                ),
            )

        else:
            cursor.execute(
                """
                SELECT
                    session_id,
                    sources,
                    first_event_timestamp,
                    last_event_timestamp,
                    event_count,
                    label,
                    attack_type,
                    label_source,
                    label_confidence,
                    data_origin
                FROM sessions
                ORDER BY last_event_timestamp DESC
                LIMIT %s OFFSET %s
                """,
                (
                    limit,
                    offset,
                ),
            )

        rows = cursor.fetchall()

    return [
        {
            "session_id": row[0],
            "sources": row[1],
            "first_event_timestamp": row[2],
            "last_event_timestamp": row[3],
            "event_count": row[4],
            "label": row[5],
            "attack_type": row[6],
            "label_source": row[7],
            "label_confidence": row[8],
            "data_origin": row[9],
        }
        for row in rows
    ]


@router.get("/{session_id}")
def get_session(
    session_id: str,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    with repository.connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                session_id,
                sources,
                first_event_timestamp,
                last_event_timestamp,
                event_count,
                label,
                attack_type,
                label_source,
                label_confidence,
                labeled_at,
                data_origin,
                metadata,
                created_at,
                updated_at
            FROM sessions
            WHERE session_id = %s
            """,
            (
                session_id,
            ),
        )

        row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return {
        "session_id": row[0],
        "sources": row[1],
        "first_event_timestamp": row[2],
        "last_event_timestamp": row[3],
        "event_count": row[4],
        "label": row[5],
        "attack_type": row[6],
        "label_source": row[7],
        "label_confidence": row[8],
        "labeled_at": row[9],
        "data_origin": row[10],
        "metadata": row[11],
        "created_at": row[12],
        "updated_at": row[13],
    }


@router.get("/{session_id}/events")
def get_session_events(
    session_id: str,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    events = repository.get_session(
        session_id
    )

    if not events:
        raise HTTPException(
            status_code=404,
            detail="Session not found or empty",
        )

    return [
        event.model_dump(
            mode="json"
        )
        for event in events
    ]


@router.get("/{session_id}/ml")
def get_session_ml(
    session_id: str,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    score = repository.get_ml_score(
        session_id=session_id,
        model_name="random_forest",
        model_version="2.0",
    )

    if score is None:
        raise HTTPException(
            status_code=404,
            detail="ML score not found",
        )

    return score


@router.get("/{session_id}/correlations")
def get_session_correlations(
    session_id: str,
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    results = repository.get_correlation_results(
        session_id
    )

    return results
