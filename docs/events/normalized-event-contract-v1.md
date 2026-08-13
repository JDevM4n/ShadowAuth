# Normalized Event Contract v1.0

## Propósito

Este documento define el formato estándar que utilizará ShadowAuth para representar cualquier evento recibido desde una fuente externa.

El objetivo es desacoplar la plataforma de herramientas específicas como Cowrie, permitiendo que todas las fuentes compartan un mismo esquema antes de ser procesadas por el resto del pipeline.

---

## Esquema

```json
{
  "event_id": "uuid",

  "schema_version": "1.0",

  "source": "cowrie",

  "event_type": "command.input",

  "timestamp": "2026-08-12T20:15:00Z",

  "host": "auth-node-01",

  "session_id": "7954f7782c6f",

  "network": {

      "source_ip": "192.168.1.20",

      "destination_ip": "192.168.1.100",

      "destination_port": 2222,

      "protocol": "ssh"

  },

  "severity": "medium",

  "data": {

  },

  "raw_log": "{ ... evento original ... }"
}
```

---

# Descripción de los campos

| Campo | Descripción |
|--------|-------------|
| event_id | Identificador único generado por ShadowAuth. |
| schema_version | Versión del contrato normalizado. |
| source | Herramienta que originó el evento (Cowrie, Falco, Zeek, etc.). |
| event_type | Tipo de evento según la taxonomía de ShadowAuth. |
| timestamp | Fecha y hora original del evento. |
| host | Equipo o sensor que generó el evento. |
| session_id | Identificador de la sesión asociada. |
| network | Información básica de red cuando exista. |
| severity | Nivel de severidad asignado por ShadowAuth. |
| data | Campos específicos de la herramienta de origen. |
| raw_log | Evento original completo para auditoría y trazabilidad. |

---

# Diseño

Los campos comunes representan la información mínima necesaria para cualquier fuente de eventos.

La información específica de cada herramienta se conserva dentro del objeto `data`, evitando perder información y permitiendo extender la plataforma sin modificar el contrato principal.

---

# Extensibilidad

En futuras versiones podrán incorporarse nuevos campos como:

- MITRE ATT&CK
- Threat Intelligence
- GeoIP
- Contenedores
- Kubernetes
- Cloud Metadata

sin afectar la compatibilidad con la versión 1.0.


## Reglas

Todo evento normalizado deberá cumplir las siguientes reglas:

- Debe poseer un event_id único.
- Debe indicar la fuente que generó el evento.
- Debe utilizar un event_type perteneciente a la taxonomía de ShadowAuth.
- Debe conservar el evento original en raw_log.
- La información específica de la herramienta deberá almacenarse dentro del objeto data.

## Decisiones de diseño

Se decidió almacenar la información específica de cada herramienta dentro del objeto data para evitar modificar el contrato principal cuando se incorporen nuevas fuentes de eventos.

De esta manera, ShadowAuth puede extenderse sin afectar la compatibilidad con versiones anteriores del contrato.