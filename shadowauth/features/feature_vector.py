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

    # ---------- Behavioral threat indicators ----------

    failed_login_count: int = 0

    download_command_count: int = 0

    executable_permission_count: int = 0

    ransomware_extension_count: int = 0

    ransom_note_count: int = 0

    cpu_recon_count: int = 0

    cryptomining_indicator_count: int = 0

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

    # ---------- Machine Learning ----------

    label: str = "unlabeled"