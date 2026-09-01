"""Data schemas for dataset curation and instruction tuning."""

from pydantic import BaseModel, Field
from src.core.schemas import FinancialTaskType


class FinancialTrainingExample(BaseModel):
    id: str = Field(..., description="Unique sample identifier")
    task_type: FinancialTaskType
    instruction: str = Field(..., description="User prompt or task definition")
    context: str | None = Field(default=None, description="Optional background context or schema")
    reasoning: str | None = Field(default=None, description="Chain-of-thought derivation inside <thought>")
    response: str = Field(..., description="Ground truth answer or SQL or math calculation")
    metadata: dict = Field(default_factory=dict, description="Metadata tags (source, difficulty, domain)")

    def to_chatml(self) -> dict:
        """Convert sample to Hugging Face standard messages format for SFTTrainer."""
        from src.core.prompts import get_system_prompt_for_task
        
        system_prompt = get_system_prompt_for_task(self.task_type)
        user_text = self.instruction
        if self.context:
            user_text = f"### Reference Context / Schema:\n{self.context}\n\n### User Query:\n{self.instruction}"
        
        assistant_text = ""
        if self.reasoning:
            assistant_text += f"<thought>\n{self.reasoning.strip()}\n</thought>\n\n"
        assistant_text += self.response.strip()

        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": assistant_text},
            ]
        }
