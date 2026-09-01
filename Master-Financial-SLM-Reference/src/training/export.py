"""Export and fuse LoRA adapters with base model into standalone SafeTensors / GGUF models."""

import os
from pathlib import Path
from src.config.settings import get_settings


class ModelExporter:
    """Handles merging LoRA weights with base model and quantization export."""

    def __init__(self, base_model_name: str | None = None, adapter_path: str | None = None):
        settings = get_settings()
        self.base_model_name = base_model_name or settings.BASE_MODEL_NAME
        self.adapter_path = adapter_path or settings.ADAPTER_PATH

    def merge_and_save_safetensors(self, output_path: str = "models/finetuned/financial_slm_merged") -> str:
        """Merge LoRA adapter into full base model weights and save as SafeTensors."""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
        import torch

        print(f"🔄 Loading base model: {self.base_model_name}")
        tokenizer = AutoTokenizer.from_pretrained(self.base_model_name, trust_remote_code=True)
        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            torch_dtype=torch.float16,
            device_map="cpu",
            trust_remote_code=True,
        )

        print(f"🧩 Loading LoRA adapter: {self.adapter_path}")
        model = PeftModel.from_pretrained(base_model, self.adapter_path)
        
        print("🔗 Fusing adapter weights with base model...")
        merged_model = model.merge_and_unload()

        os.makedirs(output_path, exist_ok=True)
        print(f"💾 Saving merged model to: {output_path}")
        merged_model.save_pretrained(output_path, safe_serialization=True)
        tokenizer.save_pretrained(output_path)

        print("✅ SafeTensors export complete!")
        return output_path
