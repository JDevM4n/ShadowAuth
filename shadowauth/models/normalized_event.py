#CONTRATO PARA QUE LOS EVENTOS NORMALIZADOS TENGAN UNA ESTRUCTURA DEFINIDA Y SE PUEDAN VALIDAR AUTOMATICAMENTE

from datetime import datetime #esto es para poder usar el tipo de dato datetime en la clase NormalizedEvent
from typing import Optional #esto es para poder usar el tipo de dato Optional en la clase NormalizedEvent

from pydantic import BaseModel # aca importamos la clase BaseModel de la libreria pydantic, que nos permite crear modelos de datos con validación y serialización automática.

class NormalizedEvent(BaseModel): #aca definimos la clase NormalizedEvent que hereda de BaseModel, lo que nos permite definir un modelo de datos con validación y serialización automática.
    """
    NormalizedEvent is a Pydantic model that represents a normalized event in the system.
    It contains various attributes that describe the event, including its type, timestamp,
    and any additional metadata associated with it.
    """
    
    event_id: str
    schema_version: str = "1.0"

    source: str
    event_type: str

    event_timestamp: datetime

    session_id: Optional[str] = None