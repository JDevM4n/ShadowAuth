from fastapi import APIRouter, Depends, Query

from shadowauth.api.dependencies import get_repository
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


router = APIRouter(
    prefix="/api/correlations",
    tags=["correlations"],
)


@router.get("")
def list_correlations(
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
    ),
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
                score,
                threat_type,
                description,
                evidence,
                model_name,
                model_version,
                created_at,
                updated_at
            FROM correlation_results
            ORDER BY score DESC,
                     created_at DESC
            LIMIT %s
            """,
            (
                limit,
            ),
        )

        rows = cursor.fetchall()

    return [
        {
            "correlation_id": row[0],
            "session_id": row[1],
            "rule_id": row[2],
            "rule_name": row[3],
            "severity": row[4],
            "score": row[5],
            "threat_type": row[6],
            "description": row[7],
            "evidence": row[8],
            "model_name": row[9],
            "model_version": row[10],
            "created_at": row[11],
            "updated_at": row[12],
        }
        for row in rows
    ]
