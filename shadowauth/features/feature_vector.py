from pydantic import BaseModel


class FeatureVector(BaseModel):

    # ---------- Session ----------

    session_id: str

    duration_seconds: int

    command_count: int

    unique_command_count: int

    login_attempts: int

    successful_login: bool

    download_count: int

    # ---------- Network ----------

    source_ip: str | None = None

    destination_ip: str | None = None

    source_port: int | None = None

    destination_port: int | None = None

    protocol: str | None = None

    # ---------- Host ----------

    process_count: int

    shell_spawned: bool

    sensitive_file_access: bool

    # ---------- Severity ----------

    max_severity: int

    average_severity: float

    # ---------- Time ----------

    session_hour: int

    weekend: bool