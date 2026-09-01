"""Inference engine scaffold for FinSLM."""

import time
from src.core.schemas import FinancialTaskType, QueryResponse
from src.core.prompts import build_chatml_messages
from src.config.settings import get_settings


class InferenceEngine:
    """Handles model loading and prompt generation."""

    def __init__(self):
        self.settings = get_settings()

    def generate(
        self,
        query: str,
        task_type: FinancialTaskType = FinancialTaskType.GENERAL_FINANCE,
        context: str | None = None,
    ) -> QueryResponse:
        """Run inference on the model and return structured response."""
        start_time = time.perf_counter()
        
        # Educational mock response for quick testing
        reasoning = "1. Identified user intent\n2. Applied financial knowledge principles"
        answer = f"FinSLM Analysis: Successfully processed '{query}' under task mode {task_type.value}."
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return QueryResponse(
            task_type=task_type,
            reasoning_trace=reasoning,
            answer=answer,
            latency_ms=round(elapsed_ms, 2),
        )


inference_engine = InferenceEngine()
