"""Data downloaders and loaders for financial benchmark datasets.

💡 Learning Concepts & References:
- What are Financial Benchmarks? Standardized public datasets used to test and train financial AI models.
  - FinQA: Deep financial report question-answering with multi-step arithmetic over balance sheets.
  - Financial PhraseBank: Annotated sentences from financial news for sentiment classification.
- 📖 FinQA Paper & Benchmark: https://github.com/czyssrs/FinQA
- 📖 Financial PhraseBank on Hugging Face: https://huggingface.co/datasets/financial_phrasebank
- 📖 GFG: Working with JSON Data in Python: https://www.geeksforgeeks.org/working-with-json-data-in-python/
"""

from typing import Any


def load_sample_seed_data() -> list[dict[str, Any]]:
    """Starter seed dataset for testing data curation and tokenization.
    
    Why seed examples?
    - Seed examples provide the gold-standard ground truth style of how questions,
      reasoning traces, and responses should be structured.
    """
    return [
        {
            "id": "seed_math_001",
            "task": "financial_math",
            "instruction": "Calculate the Compound Annual Growth Rate (CAGR) for revenue growing from $100M to $200M over 3 years.",
            "thought": "1. Formula: (Ending / Beginning) ^ (1/n) - 1\n2. Ratio: 200 / 100 = 2.0\n3. Annualized power: 2.0 ^ (1/3) - 1 = 1.2599 - 1 = 25.99%",
            "response": "The Compound Annual Growth Rate (CAGR) over 3 years is **25.99%**.",
        },
        {
            "id": "seed_sql_001",
            "task": "text_to_sql",
            "instruction": "Find all equity holdings ordered by market value descending.",
            "thought": "Query the portfolio_positions table, filter for Equities, and sort by market_value in DESC order.",
            "response": "```sql\nSELECT ticker, fund_id, market_value \nFROM portfolio_positions \nWHERE asset_class = 'Equities' \nORDER BY market_value DESC;\n```",
        },
        {
            "id": "seed_compliance_001",
            "task": "compliance_audit",
            "instruction": "A bank holds a Common Equity Tier 1 (CET1) capital ratio of 5.5% against a requirement of 7.0%. Audit this status.",
            "thought": "Under Basel III, minimum CET1 is 4.5% plus a 2.5% conservation buffer = 7.0%. 5.5% is below the required 7.0% threshold.",
            "response": "Verdict: [NON-COMPLIANT]\n\nFindings:\n- Bank CET1 ratio (5.5%) is deficient by 150 basis points relative to the 7.00% Basel III requirement.",
        },
    ]
