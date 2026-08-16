# Esta es una clase que representa la información de enriquecimiento externa que se agrega durante el procesamiento de eventos normalizados. Esta clase hereda de BaseModel de la librería Pydantic, lo que nos permite definir un modelo de datos con validación y serialización automática.

from typing import Optional

from pydantic import BaseModel


class EnrichmentInfo(BaseModel):
    """
    External enrichment information added during processing.
    """

    geoip_country: Optional[str] = None

    geoip_asn: Optional[str] = None

    threat_intel_match: Optional[bool] = None

    threat_intel_score: Optional[float] = None