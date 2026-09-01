"""Global application settings and configuration management."""

from functools import lru_cache
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    ENV: Literal["development", "testing", "production"] = "development"
    APP_NAME: str = "Financial Intelligence SLM Platform"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    LOGS_DIR: Path = BASE_DIR / "logs"

    # Model & Inference
    BASE_MODEL_NAME: str = "Qwen/Qwen2.5-3B-Instruct"
    ADAPTER_PATH: str = "models/adapters/financial_slm_qlora"
    USE_4BIT: bool = True
    DEVICE: str = "cuda"
    MAX_NEW_TOKENS: int = 1024
    TEMPERATURE: float = 0.2
    TOP_P: float = 0.9

    # Training Parameters (Optimized for 8GB VRAM)
    TRAIN_BATCH_SIZE: int = 1
    GRADIENT_ACCUMULATION_STEPS: int = 8
    LEARNING_RATE: float = 2e-4
    MAX_SEQ_LENGTH: int = 2048
    LORA_R: int = 16
    LORA_ALPHA: int = 32
    LORA_DROPOUT: float = 0.05
    TARGET_MODULES: list[str] = Field(
        default=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ]
    )

    # Storage & DB
    DATABASE_URL: str = "sqlite:///data/financial_warehouse.db"
    VECTOR_DB_URL: str = "http://localhost:6333"
    VECTOR_COLLECTION_NAME: str = "financial_knowledge"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    # Security & Guardrails
    ENABLE_PII_MASKING: bool = True
    ENABLE_SQL_VALIDATION: bool = True
    MAX_QUERY_LIMIT: int = 500
    API_SECRET_KEY: str = "dev-insecure-secret-key-change-in-production"

    # External Tokens
    HF_TOKEN: str | None = None
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Retrieve cached application settings instance."""
    return Settings()
