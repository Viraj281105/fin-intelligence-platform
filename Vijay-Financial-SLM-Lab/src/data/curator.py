"""Dataset curator for converting raw financial samples into standard ChatML JSONL splits.

💡 Learning Concepts & References:
- What is Dataset Curation? The process of cleaning, deduplicating, standardizing format,
  and splitting data into Training and Validation sets.
- Why split into Train and Validation?
  - Training Set (~80-90%): The data the AI studies and learns from.
  - Validation Set (~10-20%): An unseen exam used to check if the AI really understood
    the material or simply memorized it ("overfitting").
- 📖 GFG: Train and Test Datasets in Machine Learning: https://www.geeksforgeeks.org/how-to-split-a-dataset-into-train-and-test-sets-using-python/
- 📖 Hugging Face Datasets Library: https://huggingface.co/docs/datasets/index
"""

import json
from pathlib import Path
from src.config.settings import get_settings
from src.data.downloaders import load_sample_seed_data
from src.data.synthetic import SyntheticDataGenerator


class DataCurator:
    """Prepares, formats, and splits datasets for Hugging Face SFTTrainer."""

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
        """Convert samples into Hugging Face ChatML format and save train/val JSONL files.
        
        File Format (.jsonl):
        Each line is a single independent JSON object containing {"messages": [...]}.
        """
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
                            {"role": "system", "content": "You are FinSLM, an enterprise financial AI assistant."},
                            {"role": "user", "content": item["instruction"]},
                            {"role": "assistant", "content": f"<thought>\n{item.get('thought', '')}\n</thought>\n\n{item['response']}"},
                        ]
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
            counts[filename] = len(items)

        return counts
