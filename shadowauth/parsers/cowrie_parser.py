import json
from datetime import date, datetime
from uuid import NAMESPACE_URL, uuid5

from shadowauth.models.host_info import HostInfo
from shadowauth.models.network_info import NetworkInfo
from shadowauth.models.normalized_event import NormalizedEvent
from shadowauth.parsers.base_parser import BaseParser


class CowrieParser(BaseParser):
    """
    Parser for Cowrie honeypot events.

    This parser transforms Cowrie's native event format into the
    common NormalizedEvent model used by ShadowAuth.
    """

    @staticmethod
    def _json_default(value):
        """
        Converts non-JSON-native values into a stable
        representation.

        Datetime values are converted to ISO 8601.
        """

        if isinstance(value, (datetime, date)):
            return value.isoformat()

        raise TypeError(
            f"Object of type {type(value).__name__} "
            "is not JSON serializable"
        )

    def parse(self, event: dict) -> NormalizedEvent:
        """
        Convert a Cowrie event into a NormalizedEvent.

        The event_id is deterministic. Importing the exact
        same Cowrie event multiple times generates the same UUID.
        """

        canonical_event = json.dumps(
            event,
            sort_keys=True,
            separators=(",", ":"),
            default=self._json_default,
        )

        event_id = str(
            uuid5(
                NAMESPACE_URL,
                canonical_event,
            )
        )

        # JSON-safe copy for persistence.
        event_data = json.loads(
            canonical_event
        )

        return NormalizedEvent(
            event_id=event_id,

            source="cowrie",

            event_type=event["eventid"],

            event_timestamp=event["timestamp"],

            session_id=event.get("session"),

            native_uid=event.get("uuid"),

            network=NetworkInfo(
                source_ip=event.get("src_ip"),
                source_port=event.get("src_port"),

                destination_ip=event.get("dst_ip"),
                destination_port=event.get("dst_port"),

                protocol=event.get("protocol"),
            ),

            host=HostInfo(
                hostname=event.get("sensor"),
            ),

            data=event_data,

            raw_log=canonical_event,
        )