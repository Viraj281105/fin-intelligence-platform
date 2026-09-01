"""Interactive Command Line Interface for FinSLM Platform."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import typer
import uvicorn
from rich.console import Console
from src.core.schemas import FinancialTaskType
from src.data.curator import DataCurator
from src.training.qlora_trainer import SLMTrainer
from src.training.inference_engine import inference_engine

app = typer.Typer(name="fin-slm", help="Financial SLM Developer CLI")
console = Console()


@app.command()
def curate_data():
    """Build and export ChatML datasets into data/processed/."""
    console.print("[bold green]Generating training dataset splits...[/bold green]")
    curator = DataCurator()
    counts = curator.export_chatml_splits()
    console.print(f"[bold cyan]Completed! Created splits: {counts}[/bold cyan]")


@app.command()
def train():
    """Start QLoRA fine-tuning training loop."""
    trainer = SLMTrainer()
    trainer.train()


@app.command()
def query(text: str, task: str = "general_finance"):
    """Test model inference from the terminal."""
    resp = inference_engine.generate(query=text, task_type=FinancialTaskType(task))
    console.print(f"[bold green]Answer:[/bold green] {resp.answer}")


@app.command()
def serve(port: int = 8000):
    """Launch the FastAPI server."""
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    app()
