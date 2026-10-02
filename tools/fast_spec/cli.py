"""CLI: bundle split + backend mirror (Python-native, no pnpm)."""

from __future__ import annotations

from pathlib import Path

import typer

from fast_spec.api_contract import discover_api_contract_tests, run_contract_case
from fast_spec.backend_mirror import mirror_from_ir_file
from fast_spec.bundle_ir import check_split_bundle, split_bundle_file
from fast_spec.docs_render import render_all
from fast_spec.merge import merge_bundle_file

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command("split")
def split_cmd(
  bundle_paths: list[Path] = typer.Argument(..., help="One or more *.bundle.yaml paths"),
  check: bool = typer.Option(False, "--check", help="Verify IR files match bundle"),
) -> None:
  failed = 0
  for bundle_path in bundle_paths:
    resolved = bundle_path.resolve()
    feature_dir = resolved.parent
    try:
      if check:
        ok, mismatches = check_split_bundle(resolved)
        if not ok:
          failed += 1
          for msg in mismatches:
            typer.echo(f"  - {msg}", err=True)
        else:
          typer.echo(f"spec:split:check OK {bundle_path}")
      else:
        split_bundle_file(resolved)
        mirror = mirror_from_ir_file(feature_dir)
        rel = mirror.relative_to(feature_dir)
        typer.echo(f"spec:split: {bundle_path} → ir/ + {rel}")
    except Exception as exc:  # noqa: BLE001 — CLI boundary
      failed += 1
      typer.echo(f"spec:split: FAIL {bundle_path}: {exc}", err=True)
  raise typer.Exit(code=1 if failed else 0)


@app.command("split-all")
def split_all_cmd(
  root: Path = typer.Option(
    Path("docs/features/yaml"),
    "--root",
    help="Root directory to glob *.bundle.yaml",
  ),
  check: bool = typer.Option(False, "--check"),
) -> None:
  bundles = sorted(root.glob("**/*.bundle.yaml"))
  if not bundles:
    typer.echo(f"No bundles under {root}", err=True)
    raise typer.Exit(code=1)
  split_cmd(bundle_paths=bundles, check=check)


@app.command("merge")
def merge_cmd(
  bundle_paths: list[Path] = typer.Argument(..., help="One or more *.bundle.yaml paths"),
  dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
  failed = 0
  for bundle_path in bundle_paths:
    try:
      merge_bundle_file(bundle_path, dry_run=dry_run)
      typer.echo(f"spec:merge: {bundle_path}")
    except Exception as exc:  # noqa: BLE001
      failed += 1
      typer.echo(f"spec:merge: FAIL {bundle_path}: {exc}", err=True)
  raise typer.Exit(code=1 if failed else 0)


@app.command("render")
def render_cmd(
  yaml_root: Path = typer.Option(Path("docs/features/yaml"), "--yaml-root"),
  md_root: Path = typer.Option(Path("docs/features/md"), "--md-root"),
  no_index: bool = typer.Option(False, "--no-index"),
) -> None:
  try:
    render_all(yaml_root=yaml_root.resolve(), md_root=md_root.resolve(), write_index=not no_index)
  except Exception as exc:  # noqa: BLE001
    typer.echo(f"docs:render: FAIL {exc}", err=True)
    raise typer.Exit(code=1) from exc


@app.command("contract-check")
def contract_check_cmd(
  yaml_root: Path = typer.Option(Path("docs/features/yaml"), "--yaml-root"),
) -> None:
  cases = discover_api_contract_tests(yaml_root.resolve())
  if not cases:
    typer.echo("contract-check: no *.api-test.yaml found")
    raise typer.Exit(code=0)
  failed = 0
  for case in cases:
    case_id = case["data"].get("id") or case["path"].stem
    try:
      run_contract_case(case)
      typer.echo(f"contract-check OK {case_id}")
    except Exception as exc:  # noqa: BLE001
      failed += 1
      typer.echo(f"contract-check FAIL {case_id}: {exc}", err=True)
  raise typer.Exit(code=1 if failed else 0)


if __name__ == "__main__":
  app()
