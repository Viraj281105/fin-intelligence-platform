"""SEC Filing parser scaffold.

💡 Learning Concepts & References:
- What is an SEC 10-K? An annual report required by the U.S. Securities and Exchange Commission (SEC)
  that gives a comprehensive summary of a company's financial performance.
- Key Items:
  - Item 1A: Risk Factors (discloses primary business, market, regulatory, and operational risks).
  - Item 7: Management's Discussion and Analysis (MD&A) of Financial Condition and Results of Operations.
  - Item 8: Financial Statements (Balance Sheet, Income Statement, Cash Flows).
- 📖 SEC Guide: https://www.sec.gov/fast-answers/answersreada10khtm.html
- 📖 GFG: Text Parsing in Python: https://www.geeksforgeeks.org/string-manipulation-in-python/
"""

import re


class SECParser:
    """Parses 10-K and 10-Q SEC reports."""
    
    @staticmethod
    def extract_risk_factors(text: str) -> str:
        """Extract Item 1A Risk Factors from raw filing text using Regex."""
        pattern = r"(?:ITEM\s+1A[\.\s\:\-]+RISK\s+FACTORS)(.*?)(?:ITEM\s+1B|ITEM\s+2|$)"
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return text[:1000]
