"""Inference engine scaffold for FinSLM.

💡 Learning Concepts & References:
- What is Model Inference? Running a trained model to generate answers for new, unseen user questions.
- Key Generation Parameters:
  - `temperature`: Controls creativity (0.0 = deterministic and factual; 0.7 = creative). For Finance, use 0.1-0.2.
  - `max_new_tokens`: Maximum length of the generated response in tokens (~3/4 words per token).
  - `top_p` (Nucleus Sampling): Probability threshold for picking candidate next-words.
- 📖 Hugging Face Generation Strategies: https://huggingface.co/docs/transformers/generation_strategies
- 📖 GFG: Text Generation with Transformers: https://www.geeksforgeeks.org/text-generation-using-transformers/
"""

import time
from src.core.schemas import FinancialTaskType, QueryResponse
from src.core.prompts import build_chatml_messages
from src.config.settings import get_settings


class InferenceEngine:
    """Handles model loading, prompt tokenization, and response generation."""

    def __init__(self):
        self.settings = get_settings()

    def generate(
        self,
        query: str,
        task_type: FinancialTaskType = FinancialTaskType.GENERAL_FINANCE,
        context: str | None = None,
    ) -> QueryResponse:
        """Run inference on the model and return structured response with reasoning traces.
        
        To connect to your real trained weights:
        1. Tokenize prompt: `inputs = tokenizer(prompt_text, return_tensors='pt')`
        2. Generate tokens: `output = model.generate(**inputs, max_new_tokens=1024, temperature=0.2)`
        3. Decode text: `answer = tokenizer.decode(output[0])`
        """
        start_time = time.perf_counter()
        
        # Educational baseline response for quick developer testing
        reasoning = (
            f"1. Recognized financial query under domain '{task_type.value}'.\n"
            f"2. Formatted prompt with system instructions and Chain-of-Thought directives.\n"
            f"3. Ready to route query through specialized execution tools."
        )
        answer = f"FinSLM Analysis: Successfully processed '{query}' under task mode [{task_type.value}]."
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return QueryResponse(
            task_type=task_type,
            reasoning_trace=reasoning,
            answer=answer,
            latency_ms=round(elapsed_ms, 2),
        )


inference_engine = InferenceEngine()
