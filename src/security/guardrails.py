"""Enterprise Guardrails for prompt injection defense and financial output validation."""

import re
from pydantic import BaseModel


class GuardrailCheckResult(BaseModel):
    is_safe: bool
    risk_category: str | None = None
    reason: str | None = None


class FinancialGuardrails:
    """Detects adversarial jailbreaks, system prompt exfiltration, and toxic instructions."""

    INJECTION_PATTERNS = [
        r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions",
        r"reveal\s+(?:the\s+)?system\s+prompt",
        r"you\s+are\s+now\s+(?:DAN|jailbroken|unrestricted)",
        r"disregard\s+all\s+(?:safety|financial)\s+rules",
        r"bypass\s+compliance\s+guardrails",
    ]

    @classmethod
    def check_input_prompt(cls, prompt: str) -> GuardrailCheckResult:
        """Scan user query for prompt injection and jailbreak signatures."""
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, prompt, flags=re.IGNORECASE):
                return GuardrailCheckResult(
                    is_safe=False,
                    risk_category="PROMPT_INJECTION",
                    reason="Input contains adversarial prompt injection patterns attempting to override model directives.",
                )

        return GuardrailCheckResult(is_safe=True)

    @classmethod
    def check_output_safety(cls, output: str) -> GuardrailCheckResult:
        """Verify model output does not leak raw credentials or system prompts."""
        leak_patterns = [
            r"API_KEY\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]",
            r"SECRET_KEY\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]",
        ]
        for pattern in leak_patterns:
            if re.search(pattern, output, flags=re.IGNORECASE):
                return GuardrailCheckResult(
                    is_safe=False,
                    risk_category="CREDENTIAL_LEAKAGE",
                    reason="Model output attempted to expose internal secret keys or system credentials.",
                )

        return GuardrailCheckResult(is_safe=True)
