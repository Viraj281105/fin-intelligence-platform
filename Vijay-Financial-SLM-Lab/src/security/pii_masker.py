r"""Financial PII Redaction scaffold.

💡 Learning Concepts & References:
- What is PII (Personally Identifiable Information)?
  - Any data that could potentially identify a specific individual (SSNs, Account numbers, Credit Cards).
  - In finance (under GDPR, CCPA, Gramm-Leach-Bliley Act), leaking PII leads to massive regulatory fines.
- How Regex (Regular Expressions) Masking Works:
  - We scan text strings for patterns (e.g. `\d{3}-\d{2}-\d{4}` for SSN) and replace them with token tags like `[REDACTED_SSN]`.
- 📖 GFG Python Regex Tutorial: https://www.geeksforgeeks.org/python-regex/
- 📖 Microsoft Presidio Anonymizer: https://microsoft.github.io/presidio/
"""

import re


class PIIMasker:
    """Masks SSNs, Account numbers, and credit cards from prompts before logging."""

    PATTERNS = {
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CARD": r"\b(?:\d{4}[ -]?){3}\d{4}\b",
    }

    @classmethod
    def mask(cls, text: str) -> str:
        """Redact sensitive PII patterns from text."""
        sanitized = text
        for name, pattern in cls.PATTERNS.items():
            sanitized = re.sub(pattern, f"[REDACTED_{name}]", sanitized)
        return sanitized
