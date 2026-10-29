from datetime import date

from fastapi import APIRouter, Depends, Query

from shadowauth.api.dependencies import get_repository
from shadowauth.database.postgres_repository import (
    PostgresRepository,
)


router = APIRouter(
    prefix="/api/reports",
    tags=["reports"],
)


@router.get("/summary")
def report_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    repository: PostgresRepository = Depends(
        get_repository
    ),
):
    def period_filter(column: str):
        conditions = []
        parameters = []

        if start_date is not None:
            conditions.append(
                f"{column} >= %s::date"
            )
            parameters.append(start_date)

        if end_date is not None:
            conditions.append(
                f"{column} < (%s::date + INTERVAL '1 day')"
            )
            parameters.append(end_date)

        if not conditions:
            return "", []

        return (
            "WHERE " + " AND ".join(conditions),
            parameters,
        )

    with repository.connection.cursor() as cursor:

        # Sessions
        where, params = period_filter(
            "first_event_timestamp"
        )

        cursor.execute(
            f"""
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
            {where}
            """,
            params,
        )

        session_counts = cursor.fetchone()

        # Attack types
        conditions = [
            "attack_type IS NOT NULL"
        ]
        attack_params = []

        if start_date is not None:
            conditions.append(
                "first_event_timestamp >= %s::date"
            )
            attack_params.append(start_date)

        if end_date is not None:
            conditions.append(
                "first_event_timestamp < "
                "(%s::date + INTERVAL '1 day')"
            )
            attack_params.append(end_date)

        cursor.execute(
            f"""
            SELECT
                attack_type,
                COUNT(*)
            FROM sessions
            WHERE {" AND ".join(conditions)}
            GROUP BY attack_type
            ORDER BY COUNT(*) DESC
            """,
            attack_params,
        )

        attack_types = {
            row[0]: row[1]
            for row in cursor.fetchall()
        }

        # Events
        where, params = period_filter(
            "event_timestamp"
        )

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM normalized_events
            {where}
            """,
            params,
        )

        total_events = cursor.fetchone()[0]

        cursor.execute(
            f"""
            SELECT
                source,
                COUNT(*)
            FROM normalized_events
            {where}
            GROUP BY source
            ORDER BY COUNT(*) DESC
            """,
            params,
        )

        events_by_source = {
            row[0]: row[1]
            for row in cursor.fetchall()
        }

        # Alerts / correlations
        where, params = period_filter(
            "created_at"
        )

        cursor.execute(
            f"""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (
                    WHERE LOWER(severity) = 'high'
                ) AS high
            FROM correlation_results
            {where}
            """,
            params,
        )

        alert_counts = cursor.fetchone()

        cursor.execute(
            f"""
            SELECT
                threat_type,
                COUNT(*)
            FROM correlation_results
            {where}
            GROUP BY threat_type
            ORDER BY COUNT(*) DESC
            """,
            params,
        )

        alerts_by_threat = {
            row[0]: row[1]
            for row in cursor.fetchall()
        }

        # Incidents
        where, params = period_filter(
            "created_at"
        )

        cursor.execute(
            f"""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (
                    WHERE status = 'open'
                ) AS open,
                COUNT(*) FILTER (
                    WHERE status = 'investigating'
                ) AS investigating,
                COUNT(*) FILTER (
                    WHERE status = 'resolved'
                ) AS resolved
            FROM incidents
            {where}
            """,
            params,
        )

        incident_counts = cursor.fetchone()

        # ML scores
        where, params = period_filter(
            "created_at"
        )

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM ml_scores
            {where}
            """,
            params,
        )

        ml_total = cursor.fetchone()[0]

        cursor.execute(
            f"""
            SELECT
                model_name,
                model_version
            FROM ml_scores
            {where}
            ORDER BY created_at DESC
            LIMIT 1
            """,
            params,
        )

        ml_model = cursor.fetchone()

    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date,
        },
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
        "alerts": {
            "total": alert_counts[0],
            "high": alert_counts[1],
            "by_threat": alerts_by_threat,
        },
        "incidents": {
            "total": incident_counts[0],
            "open": incident_counts[1],
            "investigating": incident_counts[2],
            "resolved": incident_counts[3],
        },
        "ml": {
            "scores": ml_total,
            "model_name": (
                ml_model[0]
                if ml_model
                else "random_forest"
            ),
            "model_version": (
                ml_model[1]
                if ml_model
                else "2.0"
            ),
        },
    }
