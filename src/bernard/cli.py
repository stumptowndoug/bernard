from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from bernard.config import initialize_project

app = typer.Typer(help="Bernard: local-first, chat-first terminal SQL assistant")
console = Console()


@app.command()
def init(path: Annotated[Path | None, typer.Argument()] = None) -> None:
    """Initialize local Bernard project state."""
    target = path if path is not None else Path.cwd()
    paths = initialize_project(target)
    console.print(f"Initialized project state at {paths.state_dir}")
    console.print(f"Config file: {paths.config_file}")


@app.command()
def connect(kind: str, target: str) -> None:
    """Register and validate a connection (stub)."""
    console.print(f"Connect is not implemented yet. kind={kind}, target={target}")


@app.command()
def schema(table: str | None = None) -> None:
    """Inspect schema and catalog details (stub)."""
    if table is None:
        console.print("Schema inspection is not implemented yet.")
        return
    console.print(f"Schema inspection is not implemented yet for table={table}")


@app.command()
def profile(table: str | None = None) -> None:
    """Build or refresh profile metrics (stub)."""
    if table is None:
        console.print("Profiling is not implemented yet.")
        return
    console.print(f"Profiling is not implemented yet for table={table}")


@app.command()
def chat() -> None:
    """Start interactive chat mode (stub)."""
    console.print("Chat mode is not implemented yet.")


@app.command()
def ask(question: str) -> None:
    """Ask one natural-language question (stub)."""
    console.print(f"Ask is not implemented yet. question={question}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
