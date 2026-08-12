# Catálogo Técnico de Eventos - Cowrie

## Evento 1

### Event ID

cowrie.session.connect

### Descripción

Se genera cuando un cliente establece una nueva conexión SSH con el honeypot. Este evento marca el inicio del ciclo de vida de una sesión y permite identificar todas las acciones posteriores asociadas al mismo identificador de sesión.

### Momento de generación

Se produce inmediatamente después de establecer una conexión SSH con el servidor, antes del proceso de autenticación.

### Categoría

Session

### Campos observados

| Campo | Descripción |
|--------|-------------|
| session | Identificador único de la sesión. |
| timestamp | Fecha y hora del evento. |
| protocol | Protocolo utilizado. |
| src_ip | Dirección IP del cliente. |
| src_port | Puerto de origen. |
| dst_ip | Dirección IP del honeypot. |
| dst_port | Puerto del servicio SSH. |
| sensor | Sensor que generó el evento. |

### Utilidad para ShadowAuth

Permite identificar el inicio de una sesión y relacionar cronológicamente todos los eventos posteriores.

### Representación normalizada (propuesta)

```json
{
    "event_type":"session.connect",
    "source":"cowrie",
    "session_id":"...",
    "timestamp":"...",
    "src_ip":"...",
    "dst_ip":"...",
    "protocol":"ssh"
}
```

### ¿Debe normalizarse?

Sí.

### Observaciones

Todos los eventos posteriores compartirán el mismo identificador de sesión.

---

## Evento 2

### Event ID

cowrie.login.failed

### Descripción

Se genera cuando un intento de autenticación contra el honeypot falla. Puede corresponder a credenciales incorrectas o a un método de autenticación no aceptado.

### Momento de generación

Durante el proceso de autenticación, antes de conceder acceso al sistema.

### Categoría

Authentication

### Campos observados

| Campo | Descripción |
|--------|-------------|
| session | Identificador de la sesión. |
| username | Usuario utilizado. |
| password | Contraseña utilizada (cuando existe). |
| timestamp | Momento del intento. |
| src_ip | Dirección IP del cliente. |
| protocol | Protocolo utilizado. |
| sensor | Sensor que registró el evento. |

### Utilidad para ShadowAuth

Permite detectar intentos de acceso fallidos y posibles ataques de fuerza bruta.

### Representación normalizada (propuesta)

```json
{
    "event_type":"authentication.failed",
    "source":"cowrie",
    "session_id":"...",
    "username":"...",
    "src_ip":"...",
    "timestamp":"..."
}
```

### ¿Debe normalizarse?

Sí.

### Observaciones

En la muestra existen intentos mediante clave pública y mediante usuario/contraseña.

---

## Evento 3

### Event ID

cowrie.login.success

### Descripción

Se genera cuando la autenticación es exitosa y el usuario obtiene acceso al honeypot.

### Momento de generación

Después de validar correctamente las credenciales.

### Categoría

Authentication

### Campos observados

| Campo | Descripción |
|--------|-------------|
| session | Identificador de sesión. |
| username | Usuario autenticado. |
| password | Contraseña aceptada. |
| timestamp | Fecha y hora. |
| src_ip | Dirección IP del cliente. |
| sensor | Sensor que registró el evento. |

### Utilidad para ShadowAuth

Marca el inicio de la interacción del atacante con el sistema.

### Representación normalizada

```json
{
    "event_type":"authentication.success",
    "source":"cowrie",
    "session_id":"...",
    "username":"...",
    "src_ip":"...",
    "timestamp":"..."
}
```

### ¿Debe normalizarse?

Sí.

---

## Evento 4

### Event ID

cowrie.command.input

### Descripción

Registra cada comando ejecutado por el atacante durante la sesión.

### Momento de generación

Cada vez que el usuario envía un comando al honeypot.

### Categoría

Command

### Campos observados

| Campo | Descripción |
|--------|-------------|
| session | Identificador de sesión. |
| input | Comando ejecutado. |
| timestamp | Momento de ejecución. |
| src_ip | Dirección IP del cliente. |
| sensor | Sensor que registró el evento. |

### Utilidad para ShadowAuth

Es el evento más importante para analizar comportamiento y extraer características para Machine Learning.

### Representación normalizada

```json
{
    "event_type":"command.input",
    "source":"cowrie",
    "session_id":"...",
    "command":"...",
    "timestamp":"..."
}
```

### ¿Debe normalizarse?

Sí.

---

## Evento 5

### Event ID

cowrie.command.failed

### Descripción

Se genera cuando el atacante intenta ejecutar un comando inexistente o no soportado por el honeypot.

### Momento de generación

Después de enviar un comando que no puede ejecutarse.

### Categoría

Command

### Campos observados

| Campo | Descripción |
|--------|-------------|
| session | Identificador de sesión. |
| input | Comando ejecutado. |
| timestamp | Fecha y hora. |
| sensor | Sensor que registró el evento. |

### Utilidad para ShadowAuth

Permite conocer herramientas o comandos que el atacante esperaba encontrar.

### Representación normalizada

```json
{
    "event_type":"command.failed",
    "source":"cowrie",
    "session_id":"...",
    "command":"...",
    "timestamp":"..."
}
```

### ¿Debe normalizarse?

Sí.

---

## Evento 6

### Event ID

cowrie.session.file_download

### Descripción

Registra la descarga de un archivo solicitada por el atacante mediante el honeypot.

### Momento de generación

Después de ejecutar un comando de descarga exitoso (por ejemplo, wget).

### Categoría

File

### Campos observados

| Campo | Descripción |
|--------|-------------|
| session | Identificador de sesión. |
| url | URL descargada. |
| outfile | Ruta donde se almacenó. |
| shasum | Hash SHA-256 del archivo. |
| duplicate | Indica si el archivo ya existía. |
| timestamp | Fecha y hora. |

### Utilidad para ShadowAuth

Permite analizar malware, scripts y artefactos descargados durante un ataque.

### Representación normalizada

```json
{
    "event_type":"file.download",
    "source":"cowrie",
    "session_id":"...",
    "url":"...",
    "sha256":"...",
    "timestamp":"..."
}
```

### ¿Debe normalizarse?

Sí.

---

## Evento 7

### Event ID

cowrie.session.closed

### Descripción

Indica que la sesión SSH ha finalizado.

### Momento de generación

Cuando el cliente cierra la conexión o esta se pierde.

### Categoría

Session

### Campos observados

| Campo | Descripción |
|--------|-------------|
| session | Identificador de sesión. |
| duration_ms | Duración total de la sesión. |
| timestamp | Momento del cierre. |
| sensor | Sensor que registró el evento. |

### Utilidad para ShadowAuth

Permite calcular la duración de la interacción y determinar el cierre del ciclo de vida de una sesión.

### Representación normalizada

```json
{
    "event_type":"session.closed",
    "source":"cowrie",
    "session_id":"...",
    "duration_ms":"...",
    "timestamp":"..."
}
```

### ¿Debe normalizarse?

Sí.

### Observaciones

Este evento marca el final de la sesión y permite completar la reconstrucción cronológica de la actividad del atacante.