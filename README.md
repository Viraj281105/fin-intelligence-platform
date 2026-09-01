# 🏦 Financial Intelligence SLM Platform (FinSLM) - Starter Scaffold

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2+-ee4c2c.svg)](https://pytorch.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers%20%7C%20PEFT%20%7C%20TRL-yellow.svg)](https://huggingface.co/)

> **A clean, modular starter scaffold for building, fine-tuning, and deploying a Financial Small Language Model (SLM) from scratch.**

---

## 🧭 Overview

This repository is designed as a structured workspace to learn and build an enterprise-grade Financial AI system. It provides the clean architecture, folder layout, type definitions, configurations, and test suite so you can implement each module step-by-step.

### 5 Specialized Financial Domains to Build:
1. **🛡️ Text-to-SQL & Financial DB Querying**: Safe NL-to-SQL generation and AST validation.
2. **📄 SEC Filings QA (10-K, 10-Q)**: Document analysis and financial table parsing.
3. **🔢 Quantitative Financial Math**: Formulas for DCF, WACC, DuPont ROE, and CAGR.
4. **📈 Market Sentiment Intelligence**: Financial sentiment scoring on earnings calls.
5. **⚖️ Regulatory Risk & Compliance**: Basel III capital ratios and AML transaction auditing.

---

## 📁 Repository Structure

```
fin-intelligence-platform/
│
├── pyproject.toml               # Project metadata & build dependencies
├── requirements.txt             # Core Python & ML requirements
├── .env.example                 # Environment configuration template
├── README.md                    # Starter documentation
│
├── docs/
│   └── LEARNING_GUIDE.md        # Step-by-step guide to building each module
│
├── data/
│   ├── raw/                     # Place raw financial datasets here
│   └── processed/               # Output directory for curated ChatML splits
│
├── models/
│   ├── base/                    # Base SLM weights (e.g. Qwen2.5-3B, Llama-3.2-3B)
│   └── adapters/                # Directory where your trained LoRA adapters will be saved
│
├── src/
│   ├── config/                  # Settings & environment configuration
│   ├── core/                    # Domain schemas & ChatML prompt templates
│   ├── data/                    # Dataset loaders, synthetic generators & curator
│   ├── training/                # QLoRA 4-bit trainer & inference engine
│   ├── sql/                     # Text-to-SQL validator & database executor
│   ├── analysis/                # Financial math, SEC parser & compliance rules
│   ├── security/                # PII masking & prompt injection guardrails
│   ├── api/                     # FastAPI REST API & routes
│   └── cli.py                   # Developer CLI tool (`fin-slm`)
│
└── tests/
    └── unit/                    # Starter unit test suite
```

---

## 🚀 Quickstart

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv .venv
# Activate:
source .venv/bin/activate    # Linux / macOS
# .venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
cp .env.example .env
```

### 2. Run the Starter Tests
```bash
pytest -v
```

### 3. Generate Seed Dataset Splits
```bash
python src/cli.py curate-data
```

### 4. Launch the Interactive API Server
```bash
python src/cli.py serve --port 8000
```
Open interactive docs in your browser at: 👉 `http://localhost:8000/docs`

---

## 📖 Step-by-Step Learning Guide
Check out [`docs/LEARNING_GUIDE.md`](docs/LEARNING_GUIDE.md) for a detailed walkthrough on how to implement each module.

> **💡 Reference Branch Available:**
> If you ever want to see a fully completed, working reference implementation of any component, switch to the reference branch:
> ```bash
> git checkout complete
> ```
