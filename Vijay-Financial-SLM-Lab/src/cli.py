"""Interactive Command Line Interface for FinSLM Platform.

💡 Learning Concepts & References:
- What is Typer? A Python library for building powerful Command Line Interfaces (CLI) easily.
- What is Rich? A Python library for rich text and beautiful formatting (tables, colors) in terminal.
- 📖 Typer Official Docs: https://typer.tiangolo.com/
- 📖 Rich Official Docs: https://rich.readthedocs.io/en/stable/
- 📖 GFG: Command Line Arguments in Python: https://www.geeksforgeeks.org/command-line-arguments-in-python/
"""

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

app = typer.Typer(
    name="fin-slm",
    help="🏦 Financial SLM Developer CLI - Manage data, training, queries, and serving",
)
console = Console()


@app.command()
def curate_data():
    """Build and export ChatML datasets into data/processed/."""
    console.print("[bold green]🚀 Generating training dataset splits...[/bold green]")
    curator = DataCurator()
    counts = curator.export_chatml_splits()
    console.print(f"[bold cyan]✅ Completed! Created splits: {counts}[/bold cyan]")


@app.command()
def train():
    """Start QLoRA fine-tuning training loop on GPU."""
    console.print("[bold yellow]⚡ Commencing QLoRA 4-bit fine-tuning...[/bold yellow]")
    trainer = SLMTrainer()
    trainer.train()


@app.command()
def query(
    text: str = typer.Argument(..., help="Financial query text"),
    task: str = typer.Option("general_finance", help="Task type (e.g. financial_math, text_to_sql)"),
):
    """Test model inference from the terminal."""
    console.print(f"[bold blue]🔍 Querying FinSLM [{task}]:[/bold blue] {text}")
    resp = inference_engine.generate(query=text, task_type=FinancialTaskType(task))
    console.print(f"[bold green]💡 FinSLM Output:[/bold green]\n{resp.answer}")


@app.command()
def serve(port: int = typer.Option(8000, help="Port to run FastAPI server")):
    """Launch the FastAPI server."""
    console.print(f"[bold green]🌐 Starting API Server at http://0.0.0.0:{port}...[/bold green]")
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    app()
