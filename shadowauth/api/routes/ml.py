from fastapi import APIRouter, Depends, Query

from shadowauth.api.dependencies import get_repository
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


router = APIRouter(
    prefix="/api/ml",
    tags=["machine-learning"],
)


@router.get("/scores")
def list_ml_scores(
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    with repository.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                score_id,
                session_id,
                model_name,
                model_version,
                prediction,
                attack_probability,
                anomaly_score,
                artifact_path,
                metadata,
                created_at,
                updated_at
            FROM ml_scores
            ORDER BY attack_probability DESC NULLS LAST,
                     updated_at DESC
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
            "score_id": row[0],
            "session_id": row[1],
            "model_name": row[2],
            "model_version": row[3],
            "prediction": row[4],
            "attack_probability": row[5],
            "anomaly_score": row[6],
            "artifact_path": row[7],
            "metadata": row[8],
            "created_at": row[9],
            "updated_at": row[10],
        }
        for row in rows
    ]
