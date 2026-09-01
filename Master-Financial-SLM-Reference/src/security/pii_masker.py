"""Financial PII Redaction and Data Leakage Prevention Engine."""

import re
from typing import Tuple


class FinancialPIIMasker:
    """Masks sensitive financial PII (SSNs, Account numbers, Credit cards, IBANs) before logging."""

    PATTERNS = {
        # Social Security Numbers (XXX-XX-XXXX)
        "SSN": (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),
        # Credit Card Numbers (13-19 digits with optional dashes/spaces)
        "CREDIT_CARD": (r"\b(?:\d{4}[ -]?){3}\d{4}\b|\b\d{15,16}\b", "[REDACTED_CARD]"),
        # Bank Account / Routing numbers (9-12 digits)
        "BANK_ACCOUNT": (r"\b(?:ACCT|ACCOUNT|ROUTING)[:\s#]*(\d{8,14})\b", "[REDACTED_ACCOUNT]"),
        # International Bank Account Numbers (IBAN)
        "IBAN": (r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b", "[REDACTED_IBAN]"),
    }

    @classmethod
    def mask_text(cls, text: str) -> Tuple[str, int]:
        """Redact sensitive patterns from text and return (sanitized_text, count_of_redactions)."""
        redacted = text
        total_redactions = 0

        for p_name, (pattern, replacement) in cls.PATTERNS.items():
            matches = re.findall(pattern, redacted, flags=re.IGNORECASE)
            if matches:
                total_redactions += len(matches)
                redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)

        return redacted, total_redactions
