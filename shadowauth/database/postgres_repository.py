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
                    Jsonb(event.network.model_dump()),
                    Jsonb(event.host.model_dump()),
                    Jsonb(event.enrichment.model_dump()),
                    Jsonb(event.data),
                    Jsonb(json.loads(event.raw_log)),
                ),
            )

        self.connection.commit()

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
                (session_id,),
            )

            rows = cursor.fetchall()

        events = []

        for row in rows:

            events.append(

                NormalizedEvent(

                    event_id=str(row[0]),
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

                    network=NetworkInfo(**row[14]),
                    host=HostInfo(**row[15]),
                    enrichment=EnrichmentInfo(**row[16]),

                    data=row[17],
                    raw_log=json.dumps(row[18]),

                )

            )

        return events