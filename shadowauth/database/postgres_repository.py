import json
import os

import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

from shadowauth.models.enrichment_info import EnrichmentInfo
from shadowauth.models.host_info import HostInfo
from shadowauth.models.network_info import NetworkInfo
from shadowauth.models.normalized_event import NormalizedEvent


load_dotenv()


class PostgresRepository:

    def __init__(self):

        self.connection = psycopg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def save_event(
        self,
        event: NormalizedEvent,
    ) -> None:

        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO normalized_events (

                    event_id,
                    schema_version,
                    source,
                    event_type,
                    rule_id,
                    rule_name,
                    mitre_technique,
                    event_timestamp,
                    ingest_timestamp,
                    session_id,
                    native_uid,
                    severity,
                    severity_native,
                    label,
                    network,
                    host,
                    enrichment,
                    data,
                    raw_log

                )

                VALUES (

                    %s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s

                )

                ON CONFLICT (event_id) DO NOTHING

                RETURNING event_id
                """,
                (
                    event.event_id,
                    event.schema_version,
                    event.source,
                    event.event_type,
                    event.rule_id,
                    event.rule_name,
                    event.mitre_technique,
                    event.event_timestamp,
                    event.ingest_timestamp,
                    event.session_id,
                    event.native_uid,
                    event.severity,
                    event.severity_native,
                    event.label,
                    Jsonb(
                        event.network.model_dump()
                    ),
                    Jsonb(
                        event.host.model_dump()
                    ),
                    Jsonb(
                        event.enrichment.model_dump()
                    ),
                    Jsonb(
                        event.data
                    ),
                    (
                        Jsonb(
                            json.loads(
                                event.raw_log
                            )
                        )
                        if event.raw_log
                        else None
                    ),
                ),
            )

            inserted_event = cursor.fetchone()

            # Only update/create the session when the
            # normalized event was actually inserted.
            #
            # This prevents event_count from increasing
            # when the same event is imported again.
            if (
                inserted_event
                and event.session_id
            ):

                self._upsert_session(
                    cursor=cursor,
                    event=event,
                )

        self.connection.commit()

    def _upsert_session(
        self,
        cursor,
        event: NormalizedEvent,
    ) -> None:

        cursor.execute(
            """
            INSERT INTO sessions (

                session_id,
                sources,
                first_event_timestamp,
                last_event_timestamp,
                event_count,
                label,
                data_origin

            )

            VALUES (

                %s,
                ARRAY[%s]::TEXT[],
                %s,
                %s,
                1,
                'unlabeled',
                'unknown'

            )

            ON CONFLICT (session_id)

            DO UPDATE SET

                sources = CASE

                    WHEN %s = ANY(sessions.sources)
                        THEN sessions.sources

                    ELSE array_append(
                        sessions.sources,
                        %s
                    )

                END,

                first_event_timestamp = LEAST(
                    sessions.first_event_timestamp,
                    EXCLUDED.first_event_timestamp
                ),

                last_event_timestamp = GREATEST(
                    sessions.last_event_timestamp,
                    EXCLUDED.last_event_timestamp
                ),

                event_count = (
                    sessions.event_count + 1
                ),

                updated_at = CURRENT_TIMESTAMP
            """,
            (
                event.session_id,
                event.source,
                event.event_timestamp,
                event.event_timestamp,
                event.source,
                event.source,
            ),
        )

    def get_session(
        self,
        session_id: str,
    ) -> list[NormalizedEvent]:

        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT

                    event_id,
                    schema_version,
                    source,
                    event_type,
                    rule_id,
                    rule_name,
                    mitre_technique,
                    event_timestamp,
                    ingest_timestamp,
                    session_id,
                    native_uid,
                    severity,
                    severity_native,
                    label,
                    network,
                    host,
                    enrichment,
                    data,
                    raw_log

                FROM normalized_events

                WHERE session_id = %s

                ORDER BY event_timestamp
                """,
                (
                    session_id,
                ),
            )

            rows = cursor.fetchall()

        events = []

        for row in rows:

            events.append(
                NormalizedEvent(
                    event_id=str(
                        row[0]
                    ),
                    schema_version=row[1],
                    source=row[2],
                    event_type=row[3],
                    rule_id=row[4],
                    rule_name=row[5],
                    mitre_technique=row[6],
                    event_timestamp=row[7],
                    ingest_timestamp=row[8],
                    session_id=row[9],
                    native_uid=row[10],
                    severity=row[11],
                    severity_native=row[12],
                    label=row[13],
                    network=NetworkInfo(
                        **row[14]
                    ),
                    host=HostInfo(
                        **row[15]
                    ),
                    enrichment=EnrichmentInfo(
                        **row[16]
                    ),
                    data=row[17],
                    raw_log=(
                        json.dumps(
                            row[18]
                        )
                        if row[18] is not None
                        else None
                    ),
                )
            )

        return events

    def get_session_label(
        self,
        session_id: str,
    ) -> str:

        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT label

                FROM sessions

                WHERE session_id = %s
                """,
                (
                    session_id,
                ),
            )

            row = cursor.fetchone()

        if row is None:
            return "unlabeled"

        return (
            row[0]
            or "unlabeled"
        )

    def get_all_sessions(
        self,
    ) -> list[str]:

        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT session_id

                FROM sessions

                ORDER BY session_id
                """
            )

            rows = cursor.fetchall()

        return [
            row[0]
            for row in rows
        ]
    def save_ml_score(
        self,
        session_id: str,
        model_name: str,
        model_version: str,
        prediction: str,
        attack_probability: float | None = None,
        anomaly_score: float | None = None,
        artifact_path: str | None = None,
        metadata: dict | None = None,
    ) -> None:

        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO ml_scores (
                    session_id,
                    model_name,
                    model_version,
                    prediction,
                    attack_probability,
                    anomaly_score,
                    artifact_path,
                    metadata
                )

                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s
                )

                ON CONFLICT (
                    session_id,
                    model_name,
                    model_version
                )

                DO UPDATE SET
                    prediction = EXCLUDED.prediction,
                    attack_probability = EXCLUDED.attack_probability,
                    anomaly_score = EXCLUDED.anomaly_score,
                    artifact_path = EXCLUDED.artifact_path,
                    metadata = EXCLUDED.metadata,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    session_id,
                    model_name,
                    model_version,
                    prediction,
                    attack_probability,
                    anomaly_score,
                    artifact_path,
                    Jsonb(metadata or {}),
                ),
            )

        self.connection.commit()

    def get_ml_score(
        self,
        session_id: str,
        model_name: str,
        model_version: str,
    ) -> dict | None:

        with self.connection.cursor() as cursor:

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

                WHERE session_id = %s
                  AND model_name = %s
                  AND model_version = %s
                """,
                (
                    session_id,
                    model_name,
                    model_version,
                ),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return {
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

    def save_correlation_result(
        self,
        session_id: str,
        rule_id: str,
        rule_name: str,
        severity: str,
        score: float,
        threat_type: str,
        description: str,
        evidence: dict | None,
        model_name: str,
        model_version: str,
    ) -> None:

        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO correlation_results (

                    session_id,
                    rule_id,
                    rule_name,
                    severity,
                    score,
                    threat_type,
                    description,
                    evidence,
                    model_name,
                    model_version

                )

                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )

                ON CONFLICT (
                    session_id,
                    rule_id,
                    model_name,
                    model_version
                )

                DO UPDATE SET

                    rule_name = EXCLUDED.rule_name,
                    severity = EXCLUDED.severity,
                    score = EXCLUDED.score,
                    threat_type = EXCLUDED.threat_type,
                    description = EXCLUDED.description,
                    evidence = EXCLUDED.evidence,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    session_id,
                    rule_id,
                    rule_name,
                    severity,
                    score,
                    threat_type,
                    description,
                    Jsonb(evidence or {}),
                    model_name,
                    model_version,
                ),
            )

        self.connection.commit()

    def get_correlation_results(
        self,
        session_id: str,
    ) -> list[dict]:

        with self.connection.cursor() as cursor:

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

                WHERE session_id = %s

                ORDER BY score DESC, created_at
                """,
                (
                    session_id,
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
