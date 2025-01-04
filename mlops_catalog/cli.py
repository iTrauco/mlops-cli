"""
MLOps Catalog CLI
"""
import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
import yaml

app = typer.Typer(help="MLOps Catalog - Manage your ML experiments and models")
console = Console()

# Sub-commands
model_app = typer.Typer(help="Model management commands")
exp_app = typer.Typer(help="Experiment management commands")
data_app = typer.Typer(help="Data management commands")

app.add_typer(model_app, name="model")
app.add_typer(exp_app, name="exp")
app.add_typer(data_app, name="data")

@model_app.command("register")
def register_model(
    config_file: Path = typer.Argument(..., help="Path to model configuration YAML"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate without registering")
):
    """Register a new model"""
    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
        # Implementation here
        console.print("[green]Model registered successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
