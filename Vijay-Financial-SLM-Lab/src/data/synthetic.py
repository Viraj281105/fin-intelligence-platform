"""Synthetic financial data generator scaffold for generating Chain-of-Thought training pairs.

💡 Learning Concepts & References:
- What is Synthetic Data in AI? Data generated programmatically using algorithms or teacher models
  instead of collecting manual human annotations.
- Why is it critical for Finance?
  1. We can mathematically verify every calculation before feeding it to the AI.
  2. We can create tens of thousands of varied scenarios (different numbers, tickers, tax rates).
- 📖 Reference: https://huggingface.co/blog/synthetic-data-save-the-world
- 📖 GFG: Random Module in Python: https://www.geeksforgeeks.org/python-random-module/
"""

import random
from typing import Any


class SyntheticDataGenerator:
    """Generates synthetic financial instruction-response pairs for fine-tuning.
    
    How to expand this:
    - Add methods for WACC generation, DuPont ROE decomposition, and SQL scenario permutations.
    """

    def __init__(self, seed: int = 42):
        random.seed(seed)

    def generate_math_examples(self, count: int = 10) -> list[dict[str, Any]]:
        """Generate synthetic financial arithmetic / valuation problems with verified math."""
        examples = []
        for i in range(count):
            start_val = random.randint(50, 200)
            end_val = start_val * random.randint(2, 4)
            years = random.randint(2, 5)
            cagr = ((end_val / start_val) ** (1 / years)) - 1.0
            
            examples.append({
                "id": f"synth_math_{i:04d}",
                "task": "financial_math",
                "instruction": f"Calculate the CAGR for an investment that grew from ${start_val}M to ${end_val}M in {years} years.",
                "thought": (
                    f"1. Beginning Value = ${start_val}M, Ending Value = ${end_val}M, Period = {years} years.\n"
                    f"2. Ratio = {end_val} / {start_val} = {end_val/start_val:.4f}\n"
                    f"3. CAGR = ({end_val/start_val:.4f}) ^ (1/{years}) - 1 = {cagr*100:.2f}%."
                ),
                "response": f"The Compound Annual Growth Rate (CAGR) is **{cagr*100:.2f}%** over {years} years.",
            })
        return examples
