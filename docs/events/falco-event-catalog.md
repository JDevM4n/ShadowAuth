# Falco Event Catalog

## Overview

This document describes the Falco events analyzed during the implementation of the ShadowAuth Falco Parser.

Unlike Cowrie, which captures attacker interactions with a honeypot, Falco monitors runtime activity in the operating system and generates alerts based on predefined security rules.

---

## Sample Event

Rule:

Terminal shell in container

Priority:

Notice

Source:

syscall

Output:

A shell was spawned in a container

---

## Native Fields

| Field | Description |
|-------|-------------|
| time | Timestamp of the event |
| rule | Name of the Falco rule that generated the alert |
| priority | Native Falco severity |
| hostname | Host where the event occurred |
| source | Event source (usually syscall) |
| output | Human-readable alert description |
| tags | Categories associated with the alert |
| output_fields | Additional event-specific fields |

---

## Output Fields

| Field | Description |
|-------|-------------|
| evt.time | Event timestamp |
| proc.name | Process name |
| proc.pid | Process ID |
| user.name | User executing the process |
| fd.sip | Source IP |
| fd.sport | Source Port |
| fd.cip | Destination IP |
| fd.cport | Destination Port |

---

## Mapping to NormalizedEvent

| Falco Field | NormalizedEvent Field |
|-------------|-----------------------|
| time | event_timestamp |
| rule | event_type |
| rule | rule_name |
| priority | severity / severity_native |
| hostname | host.hostname |
| proc.name | host.process_name |
| proc.pid | host.pid |
| user.name | host.user |
| fd.sip | network.source_ip |
| fd.sport | network.source_port |
| fd.cip | network.destination_ip |
| fd.cport | network.destination_port |

---

## Notes

Falco severity values are represented as text (Emergency, Alert, Critical, Error, Warning, Notice, Informational and Debug).

During normalization, ShadowAuth converts these values into a numeric severity while preserving the original value in `severity_native`.

This allows all event sources to share a common severity scale while retaining the original context provided by Falco.