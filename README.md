# ShadowAuth

> 🚧 **Project Status:** Active Development

ShadowAuth is an open-source modular cybersecurity platform focused on early ransomware and cryptojacking detection through customized honeypots, behavioral analytics, and Machine Learning.

The platform simulates realistic banking and financial environments to capture attacker behavior, generate high-quality security datasets, and support intelligent threat detection.

---

# Overview

ShadowAuth is designed to reproduce realistic cyberattack scenarios while collecting valuable telemetry for security research and defensive engineering.

Rather than being a single application, ShadowAuth is composed of multiple independent modules that can operate separately while integrating into a complete cybersecurity platform.

This repository serves as the implementation platform for **M4N Sentinel**, a research project focused on the early detection of ransomware and cryptojacking attacks through behavioral analysis and Machine Learning.

---

# Vision

ShadowAuth aims to become a modular cybersecurity platform capable of:

- Simulating realistic enterprise infrastructures.
- Capturing attacker behavior using customized honeypots.
- Enriching and normalizing security events.
- Building high-quality Machine Learning datasets.
- Detecting advanced threats through intelligent behavioral models.
- Providing educational value for cybersecurity practitioners and researchers.

---

# Objectives

- Deploy realistic high-interaction honeypots.
- Capture real attacker interactions.
- Normalize and enrich security events.
- Build high-quality datasets for Machine Learning.
- Visualize attacks through dashboards and geolocation.
- Detect ransomware and cryptojacking attacks.
- Correlate security events.
- Generate intelligent alerts.
- Support cybersecurity research and education.

---

# High-Level Architecture

```text
                        Internet
                            │
                            ▼
                 ShadowAuth Honeypot
                  (Customized Cowrie)
                            │
                            ▼
                 Event Collection Pipeline
                            │
                            ▼
                  Event Normalization
                            │
                            ▼
               GeoIP & Threat Enrichment
                            │
                            ▼
          Storage (Wazuh / OpenSearch)
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
 Security Dashboard      Dataset Builder
                                │
                                ▼
                    Feature Engineering
                                │
                                ▼
                     Machine Learning
                                │
                                ▼
                    Threat Correlation
                                │
                                ▼
                  M4N Sentinel Engine
                                │
                                ▼
                      Intelligent Alerts
```

---

# Repository Structure

```text
ShadowAuth/
│
├── cowrie/              # Customized SSH Honeypot
├── normalizer/          # Event normalization
├── dashboard/           # Security dashboards
├── ml/                  # Machine Learning models
├── docs/                # Technical documentation
├── screenshots/         # Demonstrations
├── datasets/            # Generated datasets
├── scripts/             # Helper scripts
└── README.md
```

---

# Development Roadmap

## Phase 1 — Customized Honeypot

- [x] Clone Cowrie from source
- [x] Create isolated Python environment
- [x] Install in editable mode
- [x] Initialize Cowrie
- [x] First local SSH connection
- [x] Verify event logging
- [ ] Financial environment customization
- [ ] Fake users and realistic filesystem
- [ ] SSH banner customization

---

## Phase 2 — Event Processing

- [ ] Log extraction
- [ ] Event normalization
- [ ] GeoIP integration
- [ ] Threat enrichment
- [ ] Event standardization

---

## Phase 3 — Security Visualization

- [ ] Dashboard
- [ ] Attack statistics
- [ ] World attack map
- [ ] Country analysis
- [ ] Credential analytics
- [ ] Session visualization

---

## Phase 4 — Data Engineering

- [ ] Dataset generation
- [ ] Data validation
- [ ] Feature engineering
- [ ] Label generation
- [ ] Data preprocessing

---

## Phase 5 — Machine Learning

- [ ] Model training
- [ ] Behavioral classification
- [ ] Threat detection
- [ ] Model evaluation
- [ ] Performance metrics

---

## Phase 6 — Threat Correlation

- [ ] Event correlation
- [ ] Risk scoring
- [ ] Detection engine
- [ ] Rule integration

---

## Phase 7 — M4N Sentinel Integration

- [ ] Complete platform integration
- [ ] Intelligent alert generation
- [ ] End-to-end validation
- [ ] Final documentation

---

# Technologies

## Cybersecurity

- Cowrie
- Wazuh
- OpenSearch
- GeoIP

## Programming

- Python
- Bash

## Machine Learning

- Scikit-learn
- Pandas
- NumPy

## Infrastructure

- Linux
- Docker

## Version Control

- Git
- GitHub

---

# Current Module

**Phase 1 — Customized Cowrie Honeypot**

Current progress:

- ✅ Source installation
- ✅ Virtual environment
- ✅ Editable installation
- ✅ Initial configuration
- ✅ Local deployment
- ✅ Event collection
- 🚧 Financial environment customization

---

# Design Philosophy

ShadowAuth follows an engineering-first and educational approach.

Every module is:

- Built from source whenever possible.
- Documented in detail.
- Understood before customization.
- Designed to operate independently.
- Integrated progressively into the complete platform.

The objective is not only to build a functional cybersecurity solution but also to understand, document, and explain the internal operation of every component.

---

# Research

ShadowAuth is the implementation platform for the **M4N Sentinel** research project.

The research focuses on the early detection of ransomware and cryptojacking attacks through:

- Honeypots
- Behavioral analytics
- Event correlation
- Machine Learning

The platform will progressively evolve as each research module is implemented.

---

# Current Status

🚧 Active Development

The repository is currently focused on building a customized financial honeypot that will serve as the primary data source for the remaining modules.

Future updates will progressively incorporate event normalization, dashboards, Machine Learning models, and intelligent threat detection.

---

# Contributing

At this stage the project is under active research and development.

Contributions, ideas, discussions, and technical feedback are welcome once the first stable version is released.

---

# License

The project is currently under development.

An open-source license will be added before the first public stable release.
