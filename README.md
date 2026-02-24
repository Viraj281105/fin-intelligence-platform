# 🏦  Financial Intelligence Platform

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://docs.docker.com/compose/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)](https://huggingface.co/)
![GitHub stars](https://img.shields.io/github/stars/Viraj281105/fin-intelligence-platform?style=social)

> **Enterprise-grade controlled LLM platform for converting complex financial natural language queries into validated SQL — with governance, security, and explainable outputs.**

---

## 🧭 Overview

The ** Financial Intelligence Platform** is a production-ready, security-first AI system designed for the financial domain. It enables analysts, risk teams, and business users to query complex financial databases using plain English — while enforcing enterprise-grade guardrails at every step.

Core capabilities:

- **Natural Language → SQL** via fine-tuned and RAG-augmented LLMs
- **Query validation & safety** before any database execution
- **Explainable outputs** with reasoning traces
- **Governance & audit logging** for compliance
- **Secure multi-tenant API** with role-based access control

---

## ⚙️ Architecture

The platform is organized into modular layers:

| Layer | Description |
|-------|-------------|
| `src/api/` | FastAPI REST endpoints, request routing, auth middleware |
| `src/core/` | Core business logic, query orchestration, session management |
| `src/llm/` | LLM interface, prompt templates, model loading |
| `src/rag/` | Retrieval-Augmented Generation pipeline, vector store integration |
| `src/sql/` | SQL generation, validation, sanitization, execution engine |
| `src/security/` | Input/output guardrails, PII detection, injection prevention |
| `src/pipelines/` | End-to-end inference pipelines, chaining logic |
| `src/utils/` | Shared helpers, formatters, logging utilities |
| `src/config/` | Environment config, settings management |

---

## 📁 Repository Structure

```
fin-intel/
│
├── .gitignore
├── .gitattributes
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── .env.example                  # Environment variable template (copy to .env)
├── .vscode/
│   └── settings.json
│
├── docs/
│   ├── architecture/             # System design diagrams
│   ├── api/                      # API reference docs
│   ├── ml/                       # Model documentation
│   ├── security/                 # Security policies and threat models
│   └── decisions/                # Architecture Decision Records (ADRs)
│
├── data/
│   ├── raw/                      # Raw financial datasets (not tracked)
│   ├── processed/                # Cleaned, structured data
│   ├── synthetic/                # Synthetically generated training data
│   ├── embeddings/               # Precomputed vector embeddings
│   └── samples/                  # Sample queries and test fixtures
│
├── models/
│   ├── base/                     # Base model weights
│   ├── finetuned/                # Domain fine-tuned checkpoints
│   └── adapters/                 # LoRA / PEFT adapter weights
│
├── src/
│   ├── api/
│   ├── core/
│   ├── llm/
│   ├── rag/
│   ├── sql/
│   ├── security/
│   ├── pipelines/
│   ├── utils/
│   └── config/
│
├── notebooks/                    # Jupyter notebooks for EDA & model experiments
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── data/
│
├── scripts/                      # Setup, migration, and utility scripts
│
├── docker/                       # Dockerfiles and Compose configs
│
└── logs/                         # Runtime logs (not tracked)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Viraj281105/fin-intelligence-platform.git
cd fin-intelligence-platform
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Then edit `.env` and fill in your values:

```env
# LLM
HF_TOKEN=<your-huggingface-token>
MODEL_NAME=<model-id>

# Database
DATABASE_URL=<your-db-connection-string>

# API
SECRET_KEY=<your-secret-key>
API_ENV=development
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 3. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. Run with Docker (Recommended)

```bash
cd docker
docker compose up --build
```

### 5. Run Locally (Development)

```bash
uvicorn src.api.main:app --reload --port 8000
```

API will be available at: 👉 `http://localhost:8000`
Interactive docs at: 👉 `http://localhost:8000/docs`

---

## 🧪 Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/
```

---

## 🔒 Security

This platform is built with security-first principles:

- **SQL injection prevention** via query sanitization and parameterization
- **PII detection** before logging or exposing outputs
- **Input/output guardrails** to prevent prompt injection and data leakage
- **JWT-based authentication** with role-based access control
- **Audit logging** for all query executions

See [`docs/security/`](docs/security/) for the full threat model and security policy.

---

## 📚 Documentation

| Document | Location |
|----------|----------|
| System Architecture | `docs/architecture/` |
| API Reference | `docs/api/` |
| ML & Model Details | `docs/ml/` |
| Security Policy | `docs/security/` |
| Design Decisions (ADRs) | `docs/decisions/` |

---

## 🗺️ Roadmap

- [x] Project scaffold & repository structure
- [ ] LLM integration (base inference pipeline)
- [ ] RAG pipeline with vector store
- [ ] NL → SQL core engine
- [ ] SQL validation & safety layer
- [ ] REST API with authentication
- [ ] Fine-tuning pipeline for financial domain
- [ ] Governance & audit logging
- [ ] Docker Compose production setup
- [ ] CI/CD pipeline

---

## 👤 Author

**Viraj Jadhao**
📂 [github.com/Viraj281105](https://github.com/Viraj281105)

---

## ⚖️ License

*License not yet specified — to be added.*

---

**Status**: 🚧 Active Development — Scaffold Complete
