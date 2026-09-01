"""Dataset curation, validation, tokenization analytics, and train/eval/test splitting."""

import json
import random
from pathlib import Path
from src.config.settings import get_settings
from src.data.schemas import FinancialTrainingExample
from src.data.downloaders import (
    get_financial_phrasebank_samples,
    get_finqa_seed_samples,
)
from src.data.synthetic import SyntheticFinancialDataGenerator


class FinancialDataCurator:
    """Consolidates, cleans, and splits financial datasets for SLM training."""

    def __init__(self, output_dir: Path | None = None):
        settings = get_settings()
        self.output_dir = output_dir or (settings.DATA_DIR / "processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generator = SyntheticFinancialDataGenerator()

    def build_full_dataset(
        self,
        num_sql: int = 150,
        num_math: int = 150,
        num_compliance: int = 100,
    ) -> list[FinancialTrainingExample]:
        """Aggregate synthetic data and benchmark seeds into unified dataset."""
        examples: list[FinancialTrainingExample] = []

        # 1. Open Benchmark seeds
        examples.extend(get_financial_phrasebank_samples())
        examples.extend(get_finqa_seed_samples())

        # 2. Synthetic domain generators
        examples.extend(self.generator.generate_text_to_sql_dataset(num_sql))
        examples.extend(self.generator.generate_financial_math_dataset(num_math))
        examples.extend(self.generator.generate_compliance_dataset(num_compliance))

        return examples

    def curate_and_export(
        self,
        train_ratio: float = 0.85,
        val_ratio: float = 0.10,
        seed: int = 42,
    ) -> dict[str, int]:
        """Generate, shuffle, split, and save ChatML JSONL files for SFT training."""
        examples = self.build_full_dataset()
        random.seed(seed)
        random.shuffle(examples)

        total = len(examples)
        n_train = int(total * train_ratio)
        n_val = int(total * val_ratio)

        train_split = examples[:n_train]
        val_split = examples[n_train : n_train + n_val]
        test_split = examples[n_train + n_val :]

        splits = {
            "train.jsonl": train_split,
            "val.jsonl": val_split,
            "test.jsonl": test_split,
        }

        counts = {}
        for filename, split_data in splits.items():
            filepath = self.output_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                for item in split_data:
                    chatml_record = item.to_chatml()
                    f.write(json.dumps(chatml_record, ensure_ascii=False) + "\n")
            counts[filename] = len(split_data)

        return counts
