"""Configuration settings for the Financial SLM Platform.

💡 Learning Concepts & References:
- What is Pydantic Settings? It automatically reads configuration from environment variables (.env files)
  and validates data types (integers, strings, booleans).
- 📖 Reference: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- 📖 GFG Guide: https://www.geeksforgeeks.org/pydantic-python/
"""

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env file.
    
    Why do we separate settings from code?
    - The Twelve-Factor App methodology recommends storing config in the environment
      so you don't accidentally commit secrets or API keys to Git.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General App Settings
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

    # Model Settings (Small Language Model Selection)
    # - Qwen/Qwen2.5-3B-Instruct (Recommended: 3 Billion parameters, superior reasoning)
    # - meta-llama/Llama-3.2-3B-Instruct
    # - microsoft/Phi-3.5-mini-instruct (3.8B)
    BASE_MODEL_NAME: str = "Qwen/Qwen2.5-3B-Instruct"
    ADAPTER_PATH: str = "models/adapters/financial_slm_qlora"
    USE_4BIT: bool = True

    # Training Hyperparameters (Optimized for 8GB VRAM GPU)
    # - Batch Size: Number of training examples processed at once (1 for 8GB VRAM)
    # - Gradient Accumulation: Simulates a larger batch size (8 steps * 1 = batch size of 8)
    # - Learning Rate: How aggressively the model updates its weights (2e-4 = 0.0002)
    # - LoRA Rank (r): Size of the adapter matrices (16 is optimal balance of speed & quality)
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

    # Database Configuration
    DATABASE_URL: str = "sqlite:///data/financial_warehouse.db"


@lru_cache
def get_settings() -> Settings:
    """Singleton getter for application settings.
    
    Why lru_cache? It caches the settings object in memory so we don't re-read
    the disk .env file every time a function asks for settings.
    """
    return Settings()
