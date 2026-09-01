"""Prompt injection guardrails scaffold."""
import re

class Guardrails:
    """Blocks adversarial prompt injection attempts."""

    @staticmethod
    def is_safe(prompt: str) -> bool:
        """Check if prompt contains override attack signatures."""
        if re.search(r"ignore\s+previous\s+instructions", prompt, flags=re.I):
            return False
        return True
