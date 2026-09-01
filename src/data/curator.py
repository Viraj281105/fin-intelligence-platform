"""Dataset curator for converting raw financial samples into standard ChatML JSONL splits."""

import json
from pathlib import Path
from src.config.settings import get_settings
from src.data.downloaders import load_sample_seed_data
from src.data.synthetic import SyntheticDataGenerator


class DataCurator:
    """Prepares and splits datasets for SFTTrainer training."""

    def __init__(self, output_dir: Path | None = None):
        settings = get_settings()
        self.output_dir = output_dir or (settings.DATA_DIR / "processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generator = SyntheticDataGenerator()

    def build_dataset(self) -> list[dict]:
        """Aggregate seed samples and synthetic data into a unified list."""
        data = []
        data.extend(load_sample_seed_data())
        data.extend(self.generator.generate_math_examples(count=20))
        return data

    def export_chatml_splits(self, train_ratio: float = 0.8) -> dict[str, int]:
        """Convert samples into Hugging Face ChatML format and save train/val JSONL files."""
        dataset = self.build_dataset()
        n_train = int(len(dataset) * train_ratio)
        train_data = dataset[:n_train]
        val_data = dataset[n_train:]

        splits = {
            "train.jsonl": train_data,
            "val.jsonl": val_data,
        }

        counts = {}
        for filename, items in splits.items():
            filepath = self.output_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                for item in items:
                    record = {
                        "messages": [
                            {"role": "system", "content": "You are FinSLM, a financial assistant."},
                            {"role": "user", "content": item["instruction"]},
                            {"role": "assistant", "content": f"<thought>\n{item.get('thought', '')}\n</thought>\n\n{item['response']}"},
                        ]
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
            counts[filename] = len(items)

        return counts
