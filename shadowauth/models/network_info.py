from typing import Optional

from pydantic import BaseModel


class NetworkInfo(BaseModel):
    """
    Network-related information associated with a security event.
    """

    source_ip: Optional[str] = None
    source_port: Optional[int] = None

    destination_ip: Optional[str] = None
    destination_port: Optional[int] = None

    protocol: Optional[str] = None
    direction: Optional[str] = None

    conn_state: Optional[str] = None

    duration_ms: Optional[float] = None

    bytes_sent: Optional[int] = None
    bytes_received: Optional[int] = None

    packets_sent: Optional[int] = None
    packets_received: Optional[int] = None