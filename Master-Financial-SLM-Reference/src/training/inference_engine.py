"""Inference engine supporting 4-bit quantized SLMs with streaming and domain reasoning extraction."""

import time
import re
from typing import AsyncGenerator
from src.config.settings import get_settings
from src.core.schemas import FinancialTaskType, QueryResponse
from src.core.prompts import build_chatml_prompt


class FinancialInferenceEngine:
    """Enterprise inference engine with automatic quantization and streaming generation."""

    def __init__(self):
        self.settings = get_settings()
        self.model = None
        self.tokenizer = None
        self._is_loaded = False

    def load_model(self):
        """Lazy load tokenizer and 4-bit model onto GPU/CPU."""
        if self._is_loaded:
            return

        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

            print(f"🧠 Loading tokenizer: {self.settings.BASE_MODEL_NAME}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.settings.BASE_MODEL_NAME,
                trust_remote_code=True,
            )

            # Check if CUDA is available
            if torch.cuda.is_available() and self.settings.USE_4BIT:
                compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=compute_dtype,
                    bnb_4bit_use_double_quant=True,
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.settings.BASE_MODEL_NAME,
                    quantization_config=bnb_config,
                    device_map="auto",
                    torch_dtype=compute_dtype,
                    trust_remote_code=True,
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.settings.BASE_MODEL_NAME,
                    device_map="auto",
                    torch_dtype=torch.float32,
                    trust_remote_code=True,
                )

            # Check for LoRA adapter
            adapter_dir = self.settings.BASE_DIR / self.settings.ADAPTER_PATH
            if adapter_dir.exists() and (adapter_dir / "adapter_config.json").exists():
                print(f"🧩 Attaching LoRA adapter from {adapter_dir}")
                from peft import PeftModel
                self.model = PeftModel.from_pretrained(self.model, str(adapter_dir))

            self._is_loaded = True
            print("✅ Model loaded successfully!")

        except Exception as e:
            print(f"⚠️ GPU/HuggingFace model load skipped (Running in dev/mock inference mode): {e}")
            self._is_loaded = False

    def generate(
        self,
        query: str,
        task_type: FinancialTaskType = FinancialTaskType.GENERAL_FINANCE,
        context: str | None = None,
    ) -> QueryResponse:
        """Execute synchronous model inference and parse structured output."""
        start_time = time.perf_counter()

        if not self._is_loaded:
            self.load_model()

        if self._is_loaded and self.model is not None and self.tokenizer is not None:
            import torch
            messages = build_chatml_prompt(query, task_type, context)
            prompt_text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
            inputs = self.tokenizer(prompt_text, return_tensors="pt").to(self.model.device)
            
            with torch.no_grad():
                output_tokens = self.model.generate(
                    **inputs,
                    max_new_tokens=self.settings.MAX_NEW_TOKENS,
                    temperature=self.settings.TEMPERATURE,
                    top_p=self.settings.TOP_P,
                    do_sample=(self.settings.TEMPERATURE > 0),
                    pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
                )

            gen_tokens = output_tokens[0][inputs.input_ids.shape[1]:]
            raw_response = self.tokenizer.decode(gen_tokens, skip_special_tokens=True)
            token_count = len(gen_tokens)
        else:
            # High-fidelity mock response for local testing & development without downloading weights
            raw_response = self._generate_rule_based_response(query, task_type, context)
            token_count = len(raw_response.split())

        latency_ms = (time.perf_counter() - start_time) * 1000

        # Extract <thought> tag if present
        thought_match = re.search(r"<thought>(.*?)</thought>", raw_response, re.DOTALL)
        reasoning = thought_match.group(1).strip() if thought_match else None
        cleaned_answer = re.sub(r"<thought>.*?</thought>", "", raw_response, flags=re.DOTALL).strip()

        # Extract SQL if present
        sql_match = re.search(r"```sql\s*(.*?)\s*```", raw_response, re.DOTALL)
        sql_query = sql_match.group(1).strip() if sql_match else None

        return QueryResponse(
            task_type=task_type,
            reasoning_trace=reasoning,
            answer=cleaned_answer,
            sql_query=sql_query,
            latency_ms=round(latency_ms, 2),
            tokens_generated=token_count,
        )

    def _generate_rule_based_response(
        self,
        query: str,
        task_type: FinancialTaskType,
        context: str | None = None,
    ) -> str:
        """Deterministic rule-based financial response engine for offline/test environments."""
        match task_type:
            case FinancialTaskType.TEXT_TO_SQL:
                return (
                    "<thought>\n"
                    "1. Target table identified from schema\n"
                    "2. Enforce read-only SELECT and safe aggregation\n"
                    "</thought>\n"
                    "```sql\n"
                    "SELECT ticker, market_value, unrealized_gain_loss \n"
                    "FROM portfolio_positions \n"
                    "ORDER BY market_value DESC \n"
                    "LIMIT 10;\n"
                    "```\n\n"
                    "This query retrieves the top 10 positions ordered by market value."
                )
            case FinancialTaskType.FINANCIAL_MATH:
                return (
                    "<thought>\n"
                    "Compute metric using standard corporate finance formulas.\n"
                    "</thought>\n"
                    "<calculation>\n"
                    "Result = 14.85%\n"
                    "</calculation>\n\n"
                    "The calculated financial metric is **14.85%**."
                )
            case FinancialTaskType.COMPLIANCE_AUDIT:
                return (
                    "<thought>\n"
                    "Check thresholds against Basel III and BSA/AML requirements.\n"
                    "</thought>\n"
                    "Verdict: [COMPLIANT]\n\n"
                    "### Findings:\n"
                    "- All key capital adequacy and liquidity coverage ratios exceed statutory minimums."
                )
            case _:
                return (
                    "<thought>\n"
                    "Analyze query under financial domain knowledge.\n"
                    "</thought>\n"
                    f"Financial Intelligence Analysis: Processed query '{query}' with standard corporate finance best practices."
                )


# Global inference engine singleton
inference_engine = FinancialInferenceEngine()
