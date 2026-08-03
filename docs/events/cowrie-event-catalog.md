# Cowrie Event Catalog

## Propósito

Este documento registra los tipos de eventos observados en la instalación
de Cowrie utilizada por ShadowAuth.

Los eventos fueron generados mediante una sesión SSH controlada contra el
honeypot financiero Banco Andino.

## Experimento 01

- Sensor: auth-node-01
- Fuente: Cowrie
- Protocolo: SSH
- Puerto de laboratorio: 2222
- Archivo de muestra: samples/raw/controlled-session-01.jsonl
- Tipo de prueba: interacción controlada local

## Acciones ejecutadas

1. Conexión SSH.
2. Intento de autenticación fallido.
3. Autenticación exitosa.
4. Exploración del sistema de archivos.
5. Lectura de archivos simulados.
6. Ejecución de comandos.
7. Ejecución de comando inexistente.
8. Intento de descarga.
9. Cierre de sesión.

## Eventos observados

| Event ID | Descripción | Campos observados | Utilidad futura |
|---|---|---|---|
| Pendiente | Pendiente | Pendiente | Pendiente |

## Observaciones

- Los eventos se almacenan en formato JSON Lines.
- Cada línea representa un evento independiente.
- Los eventos relacionados comparten un identificador de sesión.
- El evento original debe conservarse durante la normalización.
