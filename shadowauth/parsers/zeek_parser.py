import json
from datetime import date, datetime, timezone
from uuid import NAMESPACE_URL, uuid5

from shadowauth.models.network_info import NetworkInfo
from shadowauth.models.normalized_event import NormalizedEvent
from shadowauth.parsers.base_parser import BaseParser


class ZeekParser(BaseParser):
    """
    Parser for Zeek network telemetry.

    Initial supported log types:
    - conn
    - dns

    Zeek events are normalized into ShadowAuth's
    common NormalizedEvent schema.
    """

    @staticmethod
    def _json_default(value):
        if isinstance(value, (datetime, date)):
            return value.isoformat()

        raise TypeError(
            f"Object of type {type(value).__name__} "
            "is not JSON serializable"
        )

    @staticmethod
    def _parse_timestamp(value) -> datetime:
        if value is None:
            raise ValueError(
                "Zeek event does not contain 'ts'."
            )

        if isinstance(value, datetime):
            return value

        # Zeek normally represents ts as Unix epoch seconds.
        try:
            return datetime.fromtimestamp(
                float(value),
                tz=timezone.utc,
            )

        except (TypeError, ValueError):
            pass

        # Allows ISO timestamps in controlled samples.
        try:
            return datetime.fromisoformat(
                str(value).replace(
                    "Z",
                    "+00:00",
                )
            )

        except ValueError as exc:
            raise ValueError(
                f"Invalid Zeek timestamp: {value}"
            ) from exc

    @staticmethod
    def _to_int(value):
        if value is None:
            return None

        try:
            return int(value)

        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_float(value):
        if value is None:
            return None

        try:
            return float(value)

        except (TypeError, ValueError):
            return None

    @staticmethod
    def _detect_log_type(
        event: dict,
    ) -> str:

        explicit_type = (
            event.get("log_type")
            or event.get("_log_type")
            or event.get("_path")
        )

        if explicit_type:
            return (
                str(explicit_type)
                .lower()
                .replace(".log", "")
            )

        # DNS-specific fields.
        if (
            "query" in event
            or "qtype_name" in event
            or "rcode_name" in event
        ):
            return "dns"

        # Connection-specific fields.
        if (
            "conn_state" in event
            or "orig_bytes" in event
            or "resp_bytes" in event
            or "orig_pkts" in event
            or "resp_pkts" in event
        ):
            return "conn"

        return "event"

    def parse(
        self,
        event: dict,
    ) -> NormalizedEvent:

        canonical_event = json.dumps(
            event,
            sort_keys=True,
            separators=(",", ":"),
            default=self._json_default,
        )

        event_id = str(
            uuid5(
                NAMESPACE_URL,
                f"zeek:{canonical_event}",
            )
        )

        event_data = json.loads(
            canonical_event
        )

        log_type = self._detect_log_type(
            event
        )

        duration_seconds = self._to_float(
            event.get("duration")
        )

        duration_ms = (
            duration_seconds * 1000
            if duration_seconds is not None
            else None
        )

        return NormalizedEvent(
            event_id=event_id,

            source="zeek",

            event_type=f"zeek.{log_type}",

            event_timestamp=self._parse_timestamp(
                event.get("ts")
            ),

            # Zeek UID identifies the native
            # connection/event, not a ShadowAuth
            # ground-truth session.
            session_id=None,

            native_uid=event.get("uid"),

            network=NetworkInfo(
                source_ip=event.get(
                    "id.orig_h"
                ),

                source_port=self._to_int(
                    event.get(
                        "id.orig_p"
                    )
                ),

                destination_ip=event.get(
                    "id.resp_h"
                ),

                destination_port=self._to_int(
                    event.get(
                        "id.resp_p"
                    )
                ),

                protocol=event.get(
                    "proto"
                ),

                conn_state=event.get(
                    "conn_state"
                ),

                duration_ms=duration_ms,

                bytes_sent=self._to_int(
                    event.get(
                        "orig_bytes"
                    )
                ),

                bytes_received=self._to_int(
                    event.get(
                        "resp_bytes"
                    )
                ),

                packets_sent=self._to_int(
                    event.get(
                        "orig_pkts"
                    )
                ),

                packets_received=self._to_int(
                    event.get(
                        "resp_pkts"
                    )
                ),
            ),

            data=event_data,

            raw_log=canonical_event,
        )
