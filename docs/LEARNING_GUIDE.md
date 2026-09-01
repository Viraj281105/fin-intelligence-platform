# 🎓 Step-by-Step Financial SLM Learning Guide

Welcome to the **Financial SLM Project**! This repository is configured as a clean, structured learning platform for building, fine-tuning, and deploying a domain-specialized Small Language Model (SLM) for Finance.

---

## 🗂️ Project Architecture & Learning Roadmap

### Phase 1: Environment & Settings (`src/config/`)
- Open [`src/config/settings.py`](file:///d:/SAS/src/config/settings.py).
- Learn how Pydantic Settings manages environment variables (`.env`).
- Key concepts: `BASE_MODEL_NAME`, `LORA_R`, `LORA_ALPHA`, `BATCH_SIZE`.

### Phase 2: Domain Modeling & Prompting (`src/core/`)
- Open [`src/core/schemas.py`](file:///d:/SAS/src/core/schemas.py) to see how financial requests and responses are structured.
- Open [`src/core/prompts.py`](file:///d:/SAS/src/core/prompts.py) to learn how to craft system prompts using the **ChatML** standard (`system`, `user`, `assistant`).
- Practice: Try adding specialized system prompts for SEC Filings and Compliance checks.

### Phase 3: Financial Data Engineering (`src/data/`)
- Open [`src/data/downloaders.py`](file:///d:/SAS/src/data/downloaders.py) and [`src/data/synthetic.py`](file:///d:/SAS/src/data/synthetic.py).
- Learn how to create synthetic Chain-of-Thought (`<thought>...</thought>`) training examples.
- Open [`src/data/curator.py`](file:///d:/SAS/src/data/curator.py) to see how datasets are shuffled and exported into `data/processed/train.jsonl`.
- Run:
  ```bash
  python src/cli.py curate-data
  ```

### Phase 4: QLoRA 4-Bit SLM Fine-Tuning (`src/training/`)
- Open [`src/training/qlora_trainer.py`](file:///d:/SAS/src/training/qlora_trainer.py).
- Learn how **QLoRA** works:
  1. Quantize the base model into 4-bit (`BitsAndBytesConfig`).
  2. Freeze base weights and attach trainable low-rank adapters (`LoraConfig`).
  3. Use Hugging Face TRL (`SFTTrainer`) to train on your GPU.
- Open [`src/training/inference_engine.py`](file:///d:/SAS/src/training/inference_engine.py) to test model generation.

### Phase 5: Financial Execution Engines (`src/sql/` & `src/analysis/`)
- **Safe SQL Validator** ([`src/sql/validator.py`](file:///d:/SAS/src/sql/validator.py)): Learn how Abstract Syntax Trees (AST) with `sqlglot` block harmful queries like `DROP TABLE`.
- **Financial Math** ([`src/analysis/financial_math.py`](file:///d:/SAS/src/analysis/financial_math.py)): Write formulas for WACC, DCF, and CAGR.
- **Compliance Rules** ([`src/analysis/compliance.py`](file:///d:/SAS/src/analysis/compliance.py)): Implement Basel III and AML structuring checks.

### Phase 6: Security & Guardrails (`src/security/`)
- **PII Masking** ([`src/security/pii_masker.py`](file:///d:/SAS/src/security/pii_masker.py)): Redact SSNs and Credit Cards before logging.
- **Guardrails** ([`src/security/guardrails.py`](file:///d:/SAS/src/security/guardrails.py)): Detect prompt injection and jailbreak attempts.

### Phase 7: REST API & CLI (`src/api/` & `src/cli.py`)
- Open [`src/api/main.py`](file:///d:/SAS/src/api/main.py) and [`src/api/routes.py`](file:///d:/SAS/src/api/routes.py) to see FastAPI routing in action.
- Start the server:
  ```bash
  python src/cli.py serve --port 8000
  ```
  Visit `http://localhost:8000/docs` to test endpoints interactively!

---

## 💡 Peek at the Reference Implementation

If you ever get stuck or want to see a fully working production solution for any file, switch to the reference branch:
```bash
git checkout complete
```
To return to your workspace:
```bash
git checkout main
```
