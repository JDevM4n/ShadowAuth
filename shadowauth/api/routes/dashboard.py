from fastapi import APIRouter, Depends

from shadowauth.api.dependencies import get_repository
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"],
)


@router.get("/summary")
def dashboard_summary(
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    with repository.connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (
                    WHERE label = 'attack'
                ) AS attacks,
                COUNT(*) FILTER (
                    WHERE label = 'benign'
                ) AS benign,
                COUNT(*) FILTER (
                    WHERE label = 'unlabeled'
                ) AS unlabeled
            FROM sessions
            """
        )

        session_counts = cursor.fetchone()

        cursor.execute(
            """
            SELECT
                attack_type,
                COUNT(*)
            FROM sessions
            WHERE attack_type IS NOT NULL
            GROUP BY attack_type
            ORDER BY COUNT(*) DESC
            """
        )

        attack_types = {
            row[0]: row[1]
            for row in cursor.fetchall()
        }

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM normalized_events
            """
        )

        total_events = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT
                source,
                COUNT(*)
            FROM normalized_events
            GROUP BY source
            ORDER BY COUNT(*) DESC
            """
        )

        events_by_source = {
            row[0]: row[1]
            for row in cursor.fetchall()
        }

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM correlation_results
            """
        )

        correlation_count = (
            cursor.fetchone()[0]
        )

        cursor.execute(
            """
            SELECT
                threat_type,
                COUNT(*)
            FROM correlation_results
            GROUP BY threat_type
            ORDER BY COUNT(*) DESC
            """
        )

        correlations_by_type = {
            row[0]: row[1]
            for row in cursor.fetchall()
        }

    return {
        "sessions": {
            "total": session_counts[0],
            "attack": session_counts[1],
            "benign": session_counts[2],
            "unlabeled": session_counts[3],
        },
        "attack_types": attack_types,
        "events": {
            "total": total_events,
            "by_source": events_by_source,
        },
        "correlations": {
            "total": correlation_count,
            "by_type": correlations_by_type,
        },
        "ml": {
            "model_name": "random_forest",
            "model_version": "2.0",
        },
    }
