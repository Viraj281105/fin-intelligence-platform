"""QLoRA fine-tuning training scaffold for Small Language Models (SLMs).

💡 Learning Concepts & References:
- What is LoRA (Low-Rank Adaptation)?
  - Instead of modifying all 3 Billion parameters (which requires massive VRAM and compute),
    LoRA freezes the base model and inserts tiny trainable matrix pairs (rank r=16).
  - This reduces trainable parameters by >99% without sacrificing model accuracy!
- What is QLoRA?
  - LoRA + 4-bit Quantization (NormalFloat4). The base weights are loaded in 4 bits instead of 16 bits.
  - This shrinks memory usage from ~16GB VRAM down to ~5.5GB VRAM, allowing training on your RTX 5070 GPU!
- 📖 Hugging Face PEFT Guide: https://huggingface.co/docs/peft/index
- 📖 Hugging Face TRL (Transformer Reinforcement Learning) & SFTTrainer: https://huggingface.co/docs/trl/sft_trainer
- 📖 GFG: Fine-Tuning LLMs Explained: https://www.geeksforgeeks.org/fine-tuning-in-machine-learning/
"""

import os
from pathlib import Path
from src.config.settings import get_settings


class SLMTrainer:
    """Trainer class for parameter-efficient fine-tuning (PEFT/QLoRA)."""

    def __init__(self):
        self.settings = get_settings()

    def train(self) -> str:
        """Execute QLoRA 4-bit fine-tuning.
        
        Step-by-step guidance for writing the training loop:
        ----------------------------------------------------
        1. Setup 4-bit quantization config:
           `bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4')`
        2. Load Tokenizer & Model:
           `tokenizer = AutoTokenizer.from_pretrained(self.settings.BASE_MODEL_NAME)`
           `model = AutoModelForCausalLM.from_pretrained(..., quantization_config=bnb_config)`
        3. Prepare model for k-bit training:
           `model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)`
        4. Configure LoRA:
           `peft_config = LoraConfig(r=self.settings.LORA_R, lora_alpha=self.settings.LORA_ALPHA, target_modules=...)`
        5. Initialize Hugging Face SFTTrainer:
           `trainer = SFTTrainer(model=model, train_dataset=dataset, peft_config=peft_config, ...)`
        6. Start training:
           `trainer.train()` and `trainer.model.save_pretrained(self.settings.ADAPTER_PATH)`
        """
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
            from peft import LoraConfig, prepare_model_for_kbit_training
            from trl import SFTTrainer
            from datasets import load_dataset
        except ImportError as e:
            raise RuntimeError(f"ML dependencies missing: {e}. Run `pip install -r requirements.txt`")

        print(f"🚀 Initializing QLoRA training scaffold for model: {self.settings.BASE_MODEL_NAME}")
        # Follow steps 1-6 above or peek at ../Master-Financial-SLM-Reference/src/training/qlora_trainer.py
        return self.settings.ADAPTER_PATH
