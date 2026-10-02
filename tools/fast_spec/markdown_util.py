"""Markdown table + YAML block helpers for docs:render."""

from __future__ import annotations

import json
from typing import Any

import yaml

MD_NONE = "_None_"
_YAML_OPTS = {"default_flow_style": False, "allow_unicode": True, "sort_keys": False, "width": 10_000}


def yaml_block(value: Any) -> str:
  if value is None or value == {} or value == []:
    return MD_NONE
  return f"```yaml\n{yaml.dump(value, **_YAML_OPTS).strip()}\n```"


def render_table(headers: list[str], rows: list[list[str]]) -> str:
  if not rows:
    return MD_NONE
  lines = [
    "| " + " | ".join(headers) + " |",
    "| " + " | ".join(["---"] * len(headers)) + " |",
  ]
  for row in rows:
    lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
  return "\n".join(lines)


def format_inline(value: Any) -> str:
  if isinstance(value, str):
    return value
  return f"`{json.dumps(value, ensure_ascii=False)}`"


def render_bullets(items: list[Any] | None) -> str:
  if not items:
    return MD_NONE
  return "\n".join(f"- {format_inline(item)}" for item in items)
