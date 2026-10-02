from __future__ import annotations

import json
import sys
from pathlib import Path

import typer

TOOLS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS_DIR))

from platform_common.registry import load_registry, repo_root, validate_registry  # noqa: E402

app = typer.Typer(help="Platform common registry — validate registries/common.registry.json")


@app.command("validate")
def validate_cmd() -> None:
  errors = validate_registry()
  if errors:
    for err in errors:
      typer.echo(f"ERROR: {err}", err=True)
    raise typer.Exit(1)
  typer.echo("platform-common.registry: OK")


@app.command("show")
def show_cmd() -> None:
  data = load_registry()
  typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
  app()
