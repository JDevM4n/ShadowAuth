# Taxonomía de Eventos - ShadowAuth

## Propósito

Este documento define la clasificación funcional de los eventos procesados por ShadowAuth.

Su objetivo es desacoplar la plataforma de herramientas específicas como Cowrie, permitiendo que múltiples fuentes de datos compartan una misma clasificación lógica.

---

# Session

## Descripción

Eventos relacionados con el ciclo de vida de una sesión.

### Eventos

- cowrie.session.connect
- cowrie.session.closed

### Utilidad

- Inicio de sesión
- Fin de sesión
- Duración
- Correlación temporal

---

# Authentication

## Descripción

Eventos relacionados con la autenticación de usuarios.

### Eventos

- cowrie.login.failed
- cowrie.login.success

### Utilidad

- Fuerza bruta
- Credenciales válidas
- Identificación de usuarios objetivo

---

# Command

## Descripción

Eventos que representan acciones ejecutadas por el atacante.

### Eventos

- cowrie.command.input
- cowrie.command.failed

### Utilidad

- Reconocimiento
- Enumeración
- Persistencia
- Descarga de malware
- Feature Engineering

---

# File Activity

## Descripción

Eventos relacionados con archivos.

### Eventos

- cowrie.session.file_download

### Utilidad

- Malware
- Scripts
- Payloads
- Evidencia

---

# Telemetry

## Descripción

Información técnica sobre el cliente.

### Eventos

- cowrie.client.version
- cowrie.client.kex
- cowrie.client.fingerprint
- cowrie.client.size
- cowrie.client.var
- cowrie.session.params

### Utilidad

- Fingerprinting
- Caracterización del cliente
- Información adicional

---

# Logging

## Descripción

Eventos relacionados con registros internos.

### Eventos

- cowrie.log.closed

### Utilidad

- Auditoría
- Cierre de registros