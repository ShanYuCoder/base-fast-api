"""Split portal-feature-bundle → ir/{spec,legacy,design}.yaml"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from fast_spec.bundle_schema import BUNDLE_META_KEYS, merge_ir_spec, partition_spec_section

_YAML_OPTS = {"default_flow_style": False, "allow_unicode": True, "sort_keys": False, "width": 10_000}


def _dump(data: dict[str, Any]) -> str:
  return yaml.dump(data, **_YAML_OPTS).rstrip()


def build_ir_from_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
  meta: dict[str, Any] = {}
  for key in BUNDLE_META_KEYS:
    if bundle.get(key) is not None:
      meta[key] = bundle[key]
  if bundle.get("openQuestions") is not None:
    meta["openQuestions"] = bundle["openQuestions"]

  design_spec, gen = partition_spec_section(bundle.get("spec") or {}, bundle.get("gen") or {})
  spec = merge_ir_spec(meta, design_spec, gen)
  legacy = {"id": bundle["id"], **(bundle.get("legacy") or {})}
  design = {"id": bundle["id"], **(bundle.get("design") or {})}
  return {"spec": spec, "legacy": legacy, "design": design}


def split_bundle_file(bundle_path: str | Path, *, dry_run: bool = False) -> dict[str, Any]:
  absolute = Path(bundle_path).resolve()
  ir_dir = absolute.parent / "ir"
  bundle = yaml.safe_load(absolute.read_text(encoding="utf-8")) or {}

  if not bundle.get("id"):
    raise ValueError(f"Bundle missing id: {bundle_path}")

  ir = build_ir_from_bundle(bundle)
  if not dry_run:
    ir_dir.mkdir(parents=True, exist_ok=True)
    header = f"# Generated from {absolute.name} — ./scripts/spec-split\n"
    (ir_dir / "spec.yaml").write_text(header + _dump(ir["spec"]) + "\n", encoding="utf-8")
    (ir_dir / "legacy.yaml").write_text(header + _dump(ir["legacy"]) + "\n", encoding="utf-8")
    (ir_dir / "design.yaml").write_text(header + _dump(ir["design"]) + "\n", encoding="utf-8")

  return {"bundle_path": absolute, "ir_dir": ir_dir, **ir}


def check_split_bundle(bundle_path: str | Path) -> tuple[bool, list[str]]:
  absolute = Path(bundle_path).resolve()
  ir_dir = absolute.parent / "ir"
  bundle = yaml.safe_load(absolute.read_text(encoding="utf-8")) or {}
  expected = build_ir_from_bundle(bundle)
  mismatches: list[str] = []

  for name in ("spec", "legacy", "design"):
    ir_path = ir_dir / f"{name}.yaml"
    if not ir_path.is_file():
      mismatches.append(f"{name}.yaml missing")
      continue
    actual = yaml.safe_load(ir_path.read_text(encoding="utf-8")) or {}
    if _dump(expected[name]) != _dump(actual):
      mismatches.append(f"{name}.yaml out of sync with bundle")

  return len(mismatches) == 0, mismatches
