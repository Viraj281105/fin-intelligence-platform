"""Prompt engineering and ChatML formatting templates for FinSLM."""

from src.core.schemas import FinancialTaskType

SYSTEM_PROMPT_CORE = """You are FinSLM, an enterprise financial AI assistant with expertise in corporate finance, SEC filings, financial mathematics, Text-to-SQL, and compliance.

Instructions:
1. Provide step-by-step reasoning inside <thought>...</thought> tags before giving the final answer.
2. For mathematical calculations, state each step explicitly.
3. For database queries, output clean, read-only SQL enclosed in ```sql ... ```.
"""


def get_system_prompt(task_type: FinancialTaskType = FinancialTaskType.GENERAL_FINANCE) -> str:
    """Return the system prompt appropriate for the given financial task."""
    # TODO: Add custom domain-specific prompts for TEXT_TO_SQL, SEC_FILING_QA, etc.
    return SYSTEM_PROMPT_CORE


def build_chatml_messages(
    query: str,
    task_type: FinancialTaskType = FinancialTaskType.GENERAL_FINANCE,
    context: str | None = None,
) -> list[dict[str, str]]:
    """Build standard Hugging Face ChatML messages dictionary list."""
    system_prompt = get_system_prompt(task_type)
    user_content = query
    if context:
        user_content = f"### Context:\n{context}\n\n### Query:\n{query}"

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
