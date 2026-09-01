"""SEC Filing (10-K, 10-Q, 8-K) document parser and section analyzer."""

import re
from typing import TypedDict


class SECFilingSection(TypedDict):
    section_id: str
    title: str
    content: str


class SECFilingParser:
    """Extracts critical items (Item 1A Risk Factors, Item 7 MD&A) from SEC filings."""

    SECTION_PATTERNS = {
        "ITEM_1A": r"(?:ITEM\s+1A[\.\s\:\-]+RISK\s+FACTORS)(.*?)(?:ITEM\s+1B|ITEM\s+2|$)",
        "ITEM_7": r"(?:ITEM\s+7[\.\s\:\-]+MANAGEMENT[\'’]S\s+DISCUSSION\s+AND\s+ANALYSIS)(.*?)(?:ITEM\s+7A|ITEM\s+8|$)",
        "ITEM_8": r"(?:ITEM\s+8[\.\s\:\-]+FINANCIAL\s+STATEMENTS)(.*?)(?:ITEM\s+9|$)",
    }

    @classmethod
    def parse_filing_text(cls, raw_text: str) -> dict[str, SECFilingSection]:
        """Segment raw 10-K text into standard structured disclosure sections."""
        extracted: dict[str, SECFilingSection] = {}

        for key, pattern in cls.SECTION_PATTERNS.items():
            match = re.search(pattern, raw_text, flags=re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1).strip()
                title = key.replace("_", " ").title()
                extracted[key] = {
                    "section_id": key,
                    "title": title,
                    "content": content[:10000],  # Keep reasonable snippet
                }

        return extracted

    @classmethod
    def extract_tables_from_markdown(cls, text: str) -> list[str]:
        """Extract markdown format financial tables from document text."""
        table_pattern = r"(\|.+?\|\n\|[-:\s|]+?\n(?:\|.+?\|\n?)+)"
        tables = re.findall(table_pattern, text)
        return [t.strip() for t in tables]
