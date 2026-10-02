"""portal-feature-bundle/v1 — design spec vs gen split."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

BUNDLE_SCHEMA = "portal-feature-bundle/v1"

BUNDLE_META_KEYS = [
  "id",
  "title",
  "status",
  "owner",
  "summary",
  "specOrigin",
  "grillStatus",
]

GEN_TOP_KEYS = ["codegen", "tags"]
GEN_UI_KEYS = ["filters", "columns", "composition", "testIds"]


def _prune_gen(gen: dict[str, Any]) -> dict[str, Any]:
  out = dict(gen)
  ui = out.get("ui")
  if isinstance(ui, dict) and not ui:
    out.pop("ui", None)
  return out if out else {}


def partition_spec_section(
  spec_section: dict[str, Any] | None = None,
  bundle_gen: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
  design_spec = dict(spec_section or {})
  gen = deepcopy(bundle_gen or {})

  for key in GEN_TOP_KEYS:
    if design_spec.get(key) is not None and gen.get(key) is None:
      gen[key] = design_spec[key]
    design_spec.pop(key, None)

  ui = design_spec.get("ui")
  if isinstance(ui, dict):
    gen_ui = dict(gen.get("ui") or {})
    ui_copy = dict(ui)
    for key in GEN_UI_KEYS:
      if ui_copy.get(key) is not None and gen_ui.get(key) is None:
        gen_ui[key] = ui_copy[key]
      ui_copy.pop(key, None)
    design_spec["ui"] = ui_copy
    if gen_ui:
      gen["ui"] = gen_ui

  return design_spec, _prune_gen(gen)


def merge_ir_spec(
  meta: dict[str, Any],
  design_spec: dict[str, Any] | None = None,
  gen: dict[str, Any] | None = None,
) -> dict[str, Any]:
  ir = {**meta, **(design_spec or {})}
  gen = gen or {}

  for key in GEN_TOP_KEYS:
    if gen.get(key) is not None:
      ir[key] = gen[key]

  gen_ui = gen.get("ui")
  if isinstance(gen_ui, dict):
    ir_ui = dict(ir.get("ui") or {})
    for key in GEN_UI_KEYS:
      if gen_ui.get(key) is not None:
        ir_ui[key] = gen_ui[key]
    if ir_ui:
      ir["ui"] = ir_ui

  return ir


def partition_ir_spec(ir_spec: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
  ir_spec = ir_spec or {}
  meta: dict[str, Any] = {}
  for key in BUNDLE_META_KEYS:
    if ir_spec.get(key) is not None:
      meta[key] = ir_spec[key]
  if ir_spec.get("openQuestions") is not None:
    meta["openQuestions"] = ir_spec["openQuestions"]

  spec_body = dict(ir_spec)
  for key in [*BUNDLE_META_KEYS, "openQuestions"]:
    spec_body.pop(key, None)

  design_spec, gen = partition_spec_section(spec_body, {})
  return meta, design_spec, gen


def has_gen_content(gen: dict[str, Any] | None = None) -> bool:
  gen = gen or {}
  if any(gen.get(k) is not None for k in GEN_TOP_KEYS):
    return True
  ui = gen.get("ui")
  if isinstance(ui, dict) and any(ui.get(k) is not None for k in GEN_UI_KEYS):
    return True
  return False
