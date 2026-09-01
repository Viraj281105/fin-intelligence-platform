"""Loaders and formatters for open-source financial benchmark datasets."""

from pathlib import Path
from src.core.schemas import FinancialTaskType
from src.data.schemas import FinancialTrainingExample


def get_financial_phrasebank_samples() -> list[FinancialTrainingExample]:
    """Curated seed samples from Financial PhraseBank for market sentiment fine-tuning."""
    raw_samples = [
        (
            "Operating profit rose to EUR 13.1 mn from EUR 8.7 mn in the corresponding period in 2024.",
            "BULLISH",
            "The company reports a substantial YoY increase in operating profit (+50.6%), which indicates strengthening operational efficiency and profitability.",
            "Sentiment: [BULLISH]\nConfidence: 0.95\nCatalysts: Operating profit expansion from EUR 8.7 mn to EUR 13.1 mn YoY."
        ),
        (
            "Net sales decreased by 14% to EUR 124.3 million due to severe component shortages and supply chain bottlenecks.",
            "BEARISH",
            "Double-digit revenue contraction caused by external macroeconomic/supply chain headwinds.",
            "Sentiment: [BEARISH]\nConfidence: 0.92\nDownside Risks: 14% revenue drop and operational supply disruption."
        ),
        (
            "The company's board of directors will propose a regular dividend of EUR 0.25 per share, in line with last year's payout.",
            "NEUTRAL",
            "Dividend payout is unchanged and consistent with historical baseline without unexpected variance.",
            "Sentiment: [NEUTRAL]\nConfidence: 0.90\nSummary: Stable cash return policy matching prior year baseline."
        ),
    ]

    examples = []
    for idx, (text, label, reason, resp) in enumerate(raw_samples):
        examples.append(
            FinancialTrainingExample(
                id=f"phrasebank_seed_{idx}",
                task_type=FinancialTaskType.SENTIMENT_ANALYSIS,
                instruction=f"Classify the financial sentiment of the following corporate update:\n\"{text}\"",
                context=None,
                reasoning=reason,
                response=resp,
                metadata={"source": "financial_phrasebank", "label": label},
            )
        )
    return examples


def get_finqa_seed_samples() -> list[FinancialTrainingExample]:
    """Curated seed samples from FinQA / financial reports for multi-step financial math & table reasoning."""
    raw_samples = [
        {
            "id": "finqa_seed_001",
            "context": "Table: Consolidated Statements of Operations (in millions)\n- Total Net Sales 2024: $383,285\n- Total Net Sales 2023: $394,328\n- Cost of Sales 2024: $214,137\n- Cost of Sales 2023: $223,546",
            "instruction": "What was the gross profit margin in fiscal 2024, and how did it change in basis points compared to 2023?",
            "reasoning": (
                "1. Gross Profit 2024 = Net Sales ($383,285) - Cost of Sales ($214,137) = $169,148 million.\n"
                "2. Gross Margin 2024 = $169,148 / $383,285 = 44.131%.\n"
                "3. Gross Profit 2023 = Net Sales ($394,328) - Cost of Sales ($223,546) = $170,782 million.\n"
                "4. Gross Margin 2023 = $170,782 / $394,328 = 43.309%.\n"
                "5. Basis point change = (44.131% - 43.309%) * 10,000 = +82.2 bps."
            ),
            "response": (
                "<calculation>\n"
                "Gross Margin 2024 = (383285 - 214137) / 383285 = 44.131%\n"
                "Gross Margin 2023 = (394328 - 223546) / 394328 = 43.309%\n"
                "Delta (bps) = (0.44131 - 0.43309) * 10000 = +82 bps\n"
                "</calculation>\n\n"
                "In fiscal 2024, the Gross Profit Margin was **44.13%**, representing an expansion of **82 basis points** YoY compared to 43.31% in 2023."
            ),
        }
    ]

    return [
        FinancialTrainingExample(
            id=s["id"],
            task_type=FinancialTaskType.FINANCIAL_MATH,
            instruction=s["instruction"],
            context=s["context"],
            reasoning=s["reasoning"],
            response=s["response"],
            metadata={"source": "finqa_benchmark"},
        )
        for s in raw_samples
    ]
