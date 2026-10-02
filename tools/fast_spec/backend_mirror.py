"""Mirror backend adapter subset for fast_gen input path."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

BACKEND_KEYS = ["feature", "approval", "codegen", "api", "requests", "responses"]
_YAML_OPTS = {"default_flow_style": False, "allow_unicode": True, "sort_keys": False, "width": 10_000}


def mirror_backend_spec(feature_dir: str | Path, ir_spec: dict[str, Any]) -> Path:
  adapter = {key: ir_spec[key] for key in BACKEND_KEYS if ir_spec.get(key) is not None}
  target = Path(feature_dir) / "backend" / "01-backend-spec.yaml"
  target.parent.mkdir(parents=True, exist_ok=True)
  target.write_text(yaml.dump(adapter, **_YAML_OPTS), encoding="utf-8")
  return target


def mirror_from_ir_file(feature_dir: str | Path) -> Path:
  ir_path = Path(feature_dir) / "ir" / "spec.yaml"
  raw = ir_path.read_text(encoding="utf-8")
  ir = yaml.safe_load(re.sub(r"^#.*\n", "", raw, count=1)) or {}
  return mirror_backend_spec(feature_dir, ir)
