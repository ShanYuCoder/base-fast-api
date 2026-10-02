"""Merge ir/{spec,legacy,design}.yaml back into bundle SSOT."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from fast_spec.bundle_schema import BUNDLE_META_KEYS, has_gen_content, partition_ir_spec

_YAML_OPTS = {"default_flow_style": False, "allow_unicode": True, "sort_keys": False, "width": 10_000}


def merge_bundle_file(bundle_path: str | Path, *, dry_run: bool = False) -> dict[str, Any]:
  absolute = Path(bundle_path).resolve()
  ir_dir = absolute.parent / "ir"
  bundle = yaml.safe_load(absolute.read_text(encoding="utf-8")) or {}

  spec_ir = yaml.safe_load((ir_dir / "spec.yaml").read_text(encoding="utf-8")) or {}
  legacy_ir = yaml.safe_load((ir_dir / "legacy.yaml").read_text(encoding="utf-8")) or {}
  design_ir = yaml.safe_load((ir_dir / "design.yaml").read_text(encoding="utf-8")) or {}

  meta, design_spec, gen = partition_ir_spec(spec_ir)

  for key in BUNDLE_META_KEYS:
    if meta.get(key) is not None:
      bundle[key] = meta[key]
  if meta.get("openQuestions") is not None:
    bundle["openQuestions"] = meta["openQuestions"]

  bundle["spec"] = design_spec
  if has_gen_content(gen):
    bundle["gen"] = gen
  else:
    bundle.pop("gen", None)

  legacy_section = dict(legacy_ir)
  legacy_section.pop("id", None)
  bundle["legacy"] = legacy_section

  design_section = dict(design_ir)
  design_section.pop("id", None)
  bundle["design"] = design_section

  if not dry_run:
    absolute.write_text(yaml.dump(bundle, **_YAML_OPTS), encoding="utf-8")

  return {"bundle_path": absolute, "bundle": bundle}
