"""Synthetic financial data generator scaffold for generating Chain-of-Thought training pairs."""

import random
from typing import Any


class SyntheticDataGenerator:
    """Generates synthetic financial instruction-response pairs for fine-tuning."""

    def __init__(self, seed: int = 42):
        random.seed(seed)

    def generate_math_examples(self, count: int = 10) -> list[dict[str, Any]]:
        """Generate synthetic financial arithmetic / valuation problems."""
        examples = []
        for i in range(count):
            start_val = random.randint(50, 200)
            end_val = start_val * random.randint(2, 4)
            years = random.randint(2, 5)
            cagr = ((end_val / start_val) ** (1 / years)) - 1.0
            
            examples.append({
                "id": f"synth_math_{i}",
                "task": "financial_math",
                "instruction": f"Calculate the CAGR for an investment that grew from ${start_val} to ${end_val} in {years} years.",
                "thought": f"Formula: (Ending/Beginning)^(1/n) - 1. Calculation: ({end_val}/{start_val})^(1/{years}) - 1 = {cagr*100:.2f}%.",
                "response": f"The CAGR is **{cagr*100:.2f}%** over {years} years.",
            })
        return examples

    # TODO: Implement generate_sql_examples() and generate_compliance_examples()
