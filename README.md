# ShadowAuth

> 🚧 **Status:** Active Research & Development

ShadowAuth is an open-source modular cybersecurity platform focused on the early detection of ransomware and cryptojacking through customized honeypots, behavioral analytics, event correlation, and Machine Learning.

The project captures real attacker activity from the Internet, normalizes heterogeneous security events, and generates high-quality datasets for intelligent threat detection.

---

# Overview

ShadowAuth is the implementation platform for the **M4N Sentinel** research project.

The platform is designed to simulate realistic financial infrastructures, collect attacker telemetry, normalize security events, engineer behavioral features, and train Machine Learning models capable of detecting advanced cyber threats.

Rather than being a single application, ShadowAuth is composed of independent but integrated modules that progressively build a complete behavioral detection platform.

---

# Vision

ShadowAuth aims to become an open cybersecurity platform capable of:

- Deploying realistic financial honeypots.
- Capturing real attacker behavior.
- Collecting host telemetry.
- Normalizing heterogeneous security events.
- Building high-quality Machine Learning datasets.
- Detecting ransomware and cryptojacking through behavioral analysis.
- Correlating security events across multiple sources.
- Providing educational value for cybersecurity research.

---

# Objectives

- Deploy customized high-interaction honeypots.
- Capture real attacker sessions from the Internet.
- Normalize events from multiple sources.
- Correlate attacker activity.
- Generate reproducible security datasets.
- Engineer behavioral features.
- Train Machine Learning models.
- Detect malicious behavior.
- Generate intelligent security alerts.

---

# High-Level Architecture

```text
                    Internet
                        │
                        ▼
            Customized Cowrie Honeypot
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
   Cowrie JSON Logs             Falco Events
         │                             │
         ▼                             ▼
      Cowrie Parser             Falco Parser
         └──────────────┬──────────────┘
                        ▼
                 Event Normalizer
                        │
                        ▼
                  PostgreSQL Storage
                        │
                        ▼
              Session Feature Extraction
                        │
                        ▼
                Machine Learning Engine
                        │
                        ▼
               Threat Correlation Engine
                        │
                        ▼
           Dashboard & Intelligent Alerts
```

---

# Repository Structure

```text
ShadowAuth/
│
├── cowrie/              # Customized SSH honeypot
├── normalizer/          # Event normalization
├── parsers/             # Event parsers
├── ml/                  # Machine Learning
├── dashboard/           # Visualization
├── datasets/            # Generated datasets
├── docs/                # Technical documentation
├── screenshots/         # Demonstrations
├── scripts/             # Helper scripts
└── README.md
```

---

# Quick Start

Clone the repository:

```bash
git clone https://github.com/JDevM4n/ShadowAuth.git
cd ShadowAuth/cowrie
```

Configure the honeypot:

```bash
bash shadowauth/setup.sh
```

Create the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Cowrie:

```bash
pip install -U pip setuptools setuptools-scm wheel
pip install -e .
```

Start the honeypot:

```bash
python -m cowrie.scripts.cowrie start
```

Check status:

```bash
python -m cowrie.scripts.cowrie status
```

---

# Current Features

## Honeypot

- ✅ Customized Cowrie SSH honeypot
- ✅ Banco Andino financial environment
- ✅ Realistic banking filesystem
- ✅ Fake authentication infrastructure
- ✅ SSH banner customization
- ✅ Internet deployment
- ✅ Real attacker telemetry collection
- ✅ JSON session logging
- ✅ Reproducible installation

---

# Development Roadmap

## Phase 1 — Financial Honeypot

- [x] Clone Cowrie from source
- [x] Editable installation
- [x] Banco Andino customization
- [x] Financial filesystem
- [x] SSH customization
- [x] Internet deployment
- [x] Real attack collection
- [x] Reproducible installation

---

## Phase 2 — Event Processing

- [x] Session logging
- [ ] Cowrie parser
- [ ] Falco integration
- [ ] Falco parser
- [ ] Event normalization
- [ ] Event enrichment

---

## Phase 3 — Data Platform

- [ ] PostgreSQL integration
- [ ] Event persistence
- [ ] Dataset generation
- [ ] Feature extraction

---

## Phase 4 — Machine Learning

- [ ] Feature engineering
- [ ] Model training
- [ ] Behavioral detection
- [ ] Model evaluation

---

## Phase 5 — Threat Correlation

- [ ] Event correlation
- [ ] Risk scoring
- [ ] Detection engine
- [ ] Intelligent alerts

---

## Phase 6 — Visualization

- [ ] Dashboard
- [ ] Attack statistics
- [ ] Geolocation
- [ ] Session analytics

---

# Technologies

## Cybersecurity

- Cowrie
- Falco
- OpenSearch *(planned)*
- Wazuh *(planned)*

## Backend

- Python
- PostgreSQL
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

# Design Philosophy

ShadowAuth follows an engineering-first approach.

Every module is:

- Built from source whenever possible.
- Fully documented.
- Understood before customization.
- Independently testable.
- Progressively integrated into the complete platform.

The objective is not only to build a cybersecurity platform, but also to understand and document every internal component involved in modern threat detection.

---

# Research

ShadowAuth is the implementation platform for the **M4N Sentinel** research project.

The research investigates the early detection of ransomware and cryptojacking through:

- Customized honeypots
- Host telemetry
- Event normalization
- Behavioral feature engineering
- Machine Learning
- Threat correlation

---

# Current Status

🚧 **Active Development**

Current milestone:

- ✅ Financial SSH honeypot operational
- ✅ Capturing real attacker telemetry from the Internet
- 🚧 Integrating Falco
- 🚧 Building the event normalization pipeline
- 🚧 PostgreSQL persistence layer
- 🚧 Feature engineering
- 🚧 Behavioral Machine Learning

---

# Contributing

The project is currently under active research and development.

Bug reports, discussions, ideas, and technical feedback are welcome.

---

# License

An open-source license will be added before the first stable release.