"""Configuration settings for the Financial SLM Platform."""

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    ENV: str = "development"
    APP_NAME: str = "Financial Intelligence SLM Platform"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Directory Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    LOGS_DIR: Path = BASE_DIR / "logs"

    # Model Settings (SLM)
    BASE_MODEL_NAME: str = "Qwen/Qwen2.5-3B-Instruct"
    ADAPTER_PATH: str = "models/adapters/financial_slm_qlora"
    USE_4BIT: bool = True

    # Training Hyperparameters (Tuned for 8GB VRAM GPU)
    TRAIN_BATCH_SIZE: int = 1
    GRADIENT_ACCUMULATION_STEPS: int = 8
    LEARNING_RATE: float = 2e-4
    MAX_SEQ_LENGTH: int = 2048
    LORA_R: int = 16
    LORA_ALPHA: int = 32
    LORA_DROPOUT: float = 0.05
    TARGET_MODULES: list[str] = Field(
        default=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )

    # Database
    DATABASE_URL: str = "sqlite:///data/financial_warehouse.db"


@lru_cache
def get_settings() -> Settings:
    """Singleton getter for application settings."""
    return Settings()
