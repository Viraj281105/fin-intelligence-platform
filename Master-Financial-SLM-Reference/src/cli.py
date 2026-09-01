"""Command Line Interface for Financial Intelligence SLM Platform."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import typer
import uvicorn
from rich.console import Console
from rich.table import Table
from src.core.schemas import FinancialTaskType
from src.data.curator import FinancialDataCurator
from src.training.qlora_trainer import FinancialQLoRATrainer
from src.training.export import ModelExporter
from src.training.inference_engine import inference_engine
from src.sql.executor import SafeSQLExecutor
from src.analysis.financial_math import FinancialCalculator
from src.config.settings import get_settings

app = typer.Typer(
    name="fin-slm",
    help="🏦 Financial Intelligence Platform SLM Management CLI",
    add_completion=False,
)
console = Console()


@app.command()
def curate_data(
    num_sql: int = typer.Option(150, help="Number of synthetic Text-to-SQL pairs"),
    num_math: int = typer.Option(150, help="Number of synthetic financial math pairs"),
    num_compliance: int = typer.Option(100, help="Number of synthetic compliance pairs"),
):
    """Generate, curate, and split financial training datasets into ChatML JSONL."""
    console.print("[bold green]🚀 Commencing Financial Dataset Curation...[/bold green]")
    curator = FinancialDataCurator()
    counts = curator.curate_and_export()

    table = Table(title="📊 Dataset Curation Summary")
    table.add_column("Split File", style="cyan")
    table.add_column("Sample Count", style="magenta")
    for file, count in counts.items():
        table.add_row(file, str(count))

    console.print(table)
    console.print("[bold green]✅ Datasets saved to data/processed/[/bold green]")


@app.command()
def train(
    epochs: int = typer.Option(3, help="Number of training epochs"),
    batch_size: int = typer.Option(1, help="Per-device batch size"),
    lr: float = typer.Option(2e-4, help="Learning rate"),
):
    """Run QLoRA 4-bit parameter-efficient fine-tuning on the SLM."""
    console.print(f"[bold cyan]⚡ Starting QLoRA 4-bit Training (Epochs: {epochs}, LR: {lr})...[/bold cyan]")
    trainer = FinancialQLoRATrainer()
    trainer.args.num_train_epochs = epochs
    trainer.args.per_device_train_batch_size = batch_size
    trainer.args.learning_rate = lr
    out_dir = trainer.train()
    console.print(f"[bold green]✅ Model adapter successfully trained and saved to: {out_dir}[/bold green]")


@app.command()
def query(
    text: str = typer.Argument(..., help="Financial natural language prompt"),
    task: str = typer.Option("general_finance", help="Task type: text_to_sql, financial_math, sec_filing_qa, sentiment_analysis, compliance_audit"),
):
    """Run local inference on the financial SLM."""
    task_type = FinancialTaskType(task.lower())
    console.print(f"[bold yellow]🔍 Querying FinSLM [{task_type.value}]:[/bold yellow] {text}\n")
    
    resp = inference_engine.generate(query=text, task_type=task_type)
    
    if resp.reasoning_trace:
        console.print("[bold blue]🧠 Chain of Thought Reasoning:[/bold blue]")
        console.print(f"{resp.reasoning_trace}\n")

    console.print("[bold green]💡 FinSLM Output:[/bold green]")
    console.print(resp.answer)
    console.print(f"\n[dim]Latency: {resp.latency_ms:.1f}ms | Tokens: {resp.tokens_generated}[/dim]")


@app.command()
def sql_exec(
    sql: str = typer.Argument(..., help="Raw SQL query string"),
):
    """Validate safety and execute SQL query on financial warehouse."""
    console.print(f"[bold yellow]🛡️ Validating & Executing SQL:[/bold yellow]\n{sql}\n")
    executor = SafeSQLExecutor()
    res = executor.execute_query(sql)

    if not res.success:
        console.print(f"[bold red]❌ SQL Error: {res.error}[/bold red]")
        return

    table = Table(title=f"📊 Execution Results ({res.row_count} rows, {res.execution_time_ms}ms)")
    for col in res.columns:
        table.add_column(col, style="cyan")
    for row in res.rows:
        table.add_row(*[str(row.get(c, "")) for c in res.columns])

    console.print(table)


@app.command()
def calculate_wacc(
    equity: float = typer.Option(..., help="Equity Value in USD"),
    debt: float = typer.Option(..., help="Debt Value in USD"),
    cost_equity: float = typer.Option(..., help="Cost of Equity (e.g. 0.10 for 10%)"),
    cost_debt: float = typer.Option(..., help="Pre-tax Cost of Debt (e.g. 0.05 for 5%)"),
    tax_rate: float = typer.Option(0.21, help="Corporate tax rate (default 0.21)"),
):
    """Calculate Weighted Average Cost of Capital (WACC) with step verification."""
    result = FinancialCalculator.calculate_wacc(
        cost_of_equity=cost_equity,
        cost_of_debt=cost_debt,
        equity_value=equity,
        debt_value=debt,
        tax_rate=tax_rate,
    )
    console.print(f"[bold green]📊 {result.metric_name}: {result.result}%[/bold green]")
    for step in result.steps:
        console.print(f"  {step}")
    console.print(f"\n[italic]{result.interpretation}[/italic]")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host address"),
    port: int = typer.Option(8000, help="Port number"),
    reload: bool = typer.Option(False, help="Enable auto-reload for development"),
):
    """Launch the production FastAPI REST server."""
    console.print(f"[bold green]🌐 Starting FinSLM API Server at http://{host}:{port}...[/bold green]")
    uvicorn.run("src.api.main:app", host=host, port=port, reload=reload)


@app.command()
def export(
    output_dir: str = typer.Option("models/finetuned/financial_slm_merged", help="Output directory for merged weights")
):
    """Fuse LoRA adapter weights with base model and export as SafeTensors."""
    exporter = ModelExporter()
    out = exporter.merge_and_save_safetensors(output_dir)
    console.print(f"[bold green]✅ Model merged and exported to: {out}[/bold green]")


if __name__ == "__main__":
    app()
