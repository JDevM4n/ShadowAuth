# Esta es una clase que representa un evento normalizado en el sistema. Un evento normalizado es un evento que ha sido procesado y transformado para cumplir con un esquema común, lo que permite su análisis y correlación con otros eventos de diferentes fuentes. La clase NormalizedEvent hereda de BaseModel de la librería Pydantic, lo que nos permite definir un modelo de datos con validación y serialización automática.
# network, host, enrichment son clases y no un dict porque se quiere tener una estructura más clara y definida para cada uno de estos campos, en lugar de simplemente almacenar datos sin un formato específico. Al utilizar clases, se pueden definir atributos y métodos específicos para cada tipo de información, lo que facilita la validación, el acceso y la manipulación de los datos relacionados con la red, el host y el enriquecimiento.
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from shadowauth.models.enrichment_info import EnrichmentInfo
from shadowauth.models.host_info import HostInfo
from shadowauth.models.network_info import NetworkInfo


class NormalizedEvent(BaseModel):
    """
    Canonical event shared by every supported telemetry source.
    """

    event_id: str

    schema_version: str = "1.0"

    source: str

    event_type: str

    rule_id: Optional[str] = None
    rule_name: Optional[str] = None

    mitre_technique: Optional[str] = None

    event_timestamp: datetime

    ingest_timestamp: datetime = Field(default_factory=datetime.utcnow) #el field default_factory se utiliza para establecer un valor predeterminado para el campo ingest_timestamp. En este caso, se está utilizando la función datetime.utcnow() como valor predeterminado, lo que significa que si no se proporciona un valor para ingest_timestamp al crear una instancia de NormalizedEvent, se asignará automáticamente la fecha y hora actual en formato UTC.

    network: NetworkInfo = Field(default_factory=NetworkInfo)

    host: HostInfo = Field(default_factory=HostInfo)

    session_id: Optional[str] = None # en la mayoria de los casos se usa optional[str] = None para indicar que el campo puede ser una cadena de texto o None, lo que significa que no es obligatorio proporcionar un valor para ese campo al crear una instancia de NormalizedEvent. Esto permite que el modelo sea flexible y pueda adaptarse a diferentes tipos de eventos que pueden o no tener un session_id asociado.

    native_uid: Optional[str] = None

    severity: Optional[int] = None

    severity_native: Optional[str] = None

    label: Optional[str] = None

    enrichment: EnrichmentInfo = Field(default_factory=EnrichmentInfo)

    data: dict[str, Any] = Field(default_factory=dict)

    raw_log: Optional[str] = None