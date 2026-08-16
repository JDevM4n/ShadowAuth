import json
from uuid import uuid4

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

    def parse(self, event: dict) -> NormalizedEvent:
        """
        Convert a Cowrie event into a NormalizedEvent.
        """

        return NormalizedEvent(
            event_id=str(uuid4()),
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

            data=event,

            raw_log=json.dumps(event),
        )