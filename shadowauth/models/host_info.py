from typing import Optional

from pydantic import BaseModel


class HostInfo(BaseModel):
    """
    Host metadata related to a security event.
    """

    hostname: Optional[str] = None

    process_name: Optional[str] = None

    pid: Optional[int] = None
    ppid: Optional[int] = None

    cmdline: Optional[str] = None

    user: Optional[str] = None

    file_path: Optional[str] = None

    container_id: Optional[str] = None

    k8s_namespace: Optional[str] = None
    k8s_pod: Optional[str] = None