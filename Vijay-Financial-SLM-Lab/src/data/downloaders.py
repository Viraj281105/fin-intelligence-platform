"""Data downloaders and loaders for financial benchmark datasets."""

from typing import Any


def load_sample_seed_data() -> list[dict[str, Any]]:
    """Starter seed dataset for testing data curation and tokenization."""
    return [
        {
            "id": "seed_001",
            "task": "financial_math",
            "instruction": "Calculate the Compound Annual Growth Rate (CAGR) for revenue growing from $100M to $200M over 3 years.",
            "thought": "CAGR = (End / Start) ^ (1/n) - 1 = (200 / 100) ^ (1/3) - 1 = 1.2599 - 1 = 25.99%",
            "response": "The Compound Annual Growth Rate (CAGR) over 3 years is **25.99%**.",
        },
        {
            "id": "seed_002",
            "task": "text_to_sql",
            "instruction": "Find all equity holdings ordered by market value descending.",
            "thought": "Query portfolio_positions table filtering for Equities and sorting by market_value DESC.",
            "response": "```sql\nSELECT ticker, market_value FROM portfolio_positions ORDER BY market_value DESC;\n```",
        },
    ]

# TODO: Add functions to fetch datasets from Hugging Face (e.g. datasets.load_dataset("FinQA"))
