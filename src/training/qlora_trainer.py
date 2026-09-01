"""QLoRA 4-bit fine-tuning pipeline optimized for consumer GPUs (8GB VRAM)."""

import os
import torch
from pathlib import Path
from dataclasses import dataclass, field
from src.config.settings import get_settings


@dataclass
class FinancialTrainingArguments:
    """Configurable training hyper-parameters."""
    model_name: str = "Qwen/Qwen2.5-3B-Instruct"
    output_dir: str = "models/adapters/financial_slm_qlora"
    train_file: str = "data/processed/train.jsonl"
    val_file: str = "data/processed/val.jsonl"
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 1
    gradient_accumulation_steps: int = 8
    learning_rate: float = 2e-4
    max_seq_length: int = 2048
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    logging_steps: int = 10
    save_steps: int = 100
    save_total_limit: int = 2
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"
    fp16: bool = False
    bf16: bool = True
    use_gradient_checkpointing: bool = True


class FinancialQLoRATrainer:
    """Enterprise fine-tuning trainer using QLoRA 4-bit quantization and TRL SFTTrainer."""

    def __init__(self, args: FinancialTrainingArguments | None = None):
        self.settings = get_settings()
        self.args = args or FinancialTrainingArguments(
            model_name=self.settings.BASE_MODEL_NAME,
            output_dir=self.settings.ADAPTER_PATH,
            per_device_train_batch_size=self.settings.TRAIN_BATCH_SIZE,
            gradient_accumulation_steps=self.settings.GRADIENT_ACCUMULATION_STEPS,
            learning_rate=self.settings.LEARNING_RATE,
            max_seq_length=self.settings.MAX_SEQ_LENGTH,
            lora_r=self.settings.LORA_R,
            lora_alpha=self.settings.LORA_ALPHA,
            lora_dropout=self.settings.LORA_DROPOUT,
        )

    def train(self) -> str:
        """Run the QLoRA training loop."""
        try:
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
                BitsAndBytesConfig,
                TrainingArguments,
            )
            from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
            from trl import SFTTrainer
            from datasets import load_dataset
        except ImportError as e:
            raise RuntimeError(
                f"Missing ML dependencies: {e}. Please run `pip install -r requirements.txt`"
            )

        print(f"🚀 Starting QLoRA training for model: {self.args.model_name}")
        print(f"💾 Target output directory: {self.args.output_dir}")

        # Check CUDA capability
        compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

        # 1. 4-bit Quantization Configuration
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=True,
        )

        # 2. Load Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.args.model_name,
            trust_remote_code=True,
        )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"

        # 3. Load 4-bit Base Model
        model = AutoModelForCausalLM.from_pretrained(
            self.args.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=compute_dtype,
            trust_remote_code=True,
        )

        model = prepare_model_for_kbit_training(
            model,
            use_gradient_checkpointing=self.args.use_gradient_checkpointing,
        )

        # 4. LoRA Adapter Configuration
        peft_config = LoraConfig(
            r=self.args.lora_r,
            lora_alpha=self.args.lora_alpha,
            lora_dropout=self.args.lora_dropout,
            target_modules=self.settings.TARGET_MODULES,
            bias="none",
            task_type="CAUSAL_LM",
        )

        # 5. Load Dataset
        train_path = Path(self.args.train_file)
        if not train_path.exists():
            raise FileNotFoundError(
                f"Training dataset not found at {train_path}. Run dataset curation first!"
            )

        dataset = load_dataset(
            "json",
            data_files={"train": str(train_path)},
            split="train",
        )

        # 6. SFT Training Arguments
        training_args = TrainingArguments(
            output_dir=self.args.output_dir,
            num_train_epochs=self.args.num_train_epochs,
            per_device_train_batch_size=self.args.per_device_train_batch_size,
            gradient_accumulation_steps=self.args.gradient_accumulation_steps,
            learning_rate=self.args.learning_rate,
            logging_steps=self.args.logging_steps,
            save_steps=self.args.save_steps,
            save_total_limit=self.args.save_total_limit,
            warmup_ratio=self.args.warmup_ratio,
            lr_scheduler_type=self.args.lr_scheduler_type,
            fp16=(compute_dtype == torch.float16),
            bf16=(compute_dtype == torch.bfloat16),
            gradient_checkpointing=self.args.use_gradient_checkpointing,
            optim="paged_adamw_8bit",
            report_to="none",
        )

        # 7. Initialize Trainer
        trainer = SFTTrainer(
            model=model,
            train_dataset=dataset,
            peft_config=peft_config,
            max_seq_length=self.args.max_seq_length,
            tokenizer=tokenizer,
            args=training_args,
        )

        print("⚡ Commencing training loop...")
        trainer.train()

        # 8. Save Final LoRA Adapter & Tokenizer
        os.makedirs(self.args.output_dir, exist_ok=True)
        trainer.model.save_pretrained(self.args.output_dir)
        tokenizer.save_pretrained(self.args.output_dir)
        print(f"✅ Training completed! Adapter saved to: {self.args.output_dir}")

        return self.args.output_dir
