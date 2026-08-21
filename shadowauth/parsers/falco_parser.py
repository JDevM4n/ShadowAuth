import json
from uuid import uuid4

from shadowauth.models.host_info import HostInfo
from shadowauth.models.network_info import NetworkInfo
from shadowauth.models.normalized_event import NormalizedEvent
from shadowauth.parsers.base_parser import BaseParser

SEVERITY_MAP = {
    "Emergency": 10,
    "Alert": 9,
    "Critical": 8,
    "Error": 7,
    "Warning": 6,
    "Notice": 5,
    "Informational": 4,
    "Debug": 3,
}


class FalcoParser(BaseParser):
    """
    Parser for Falco runtime security events.

    This parser transforms Falco's native JSON format into the
    common NormalizedEvent model used by ShadowAuth.
    """

    def parse(self, event: dict) -> NormalizedEvent:

        output_fields = event.get("output_fields", {})

        return NormalizedEvent(

    event_id=str(uuid4()),

    source="falco",

    event_type=event.get("rule"),

    rule_name=event.get("rule"),

    severity=SEVERITY_MAP.get(
        event.get("priority"),
        0
    ),

    severity_native=event.get("priority"),

    event_timestamp=event.get("time"),

    network=NetworkInfo(

        source_ip=output_fields.get("fd.sip"),

        source_port=output_fields.get("fd.sport"),

        destination_ip=output_fields.get("fd.cip"),

        destination_port=output_fields.get("fd.cport"),

    ),

    host=HostInfo(

        hostname=event.get("hostname"),

        process_name=output_fields.get("proc.name"),

        pid=output_fields.get("proc.pid"),

        user=output_fields.get("user.name"),

    ),

    data=event,

    raw_log=json.dumps(event)

)