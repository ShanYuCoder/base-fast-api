from __future__ import annotations

import json
from pathlib import Path

VALID_STATUS = {"planned", "implemented"}
VALID_KIND = {"dependency", "helper", "service", "policy", "client", "mixin"}
REQUIRED_ENTRY = {"status", "tag", "kind"}


def repo_root() -> Path:
  return Path(__file__).resolve().parent.parent.parent


def load_registry(root: Path | None = None) -> dict:
  root = root or repo_root()
  path = root / "registries" / "common.registry.json"
  return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(root: Path | None = None) -> list[str]:
  root = root or repo_root()
  data = load_registry(root)
  errors: list[str] = []

  if data.get("version") != 1:
    errors.append("version must be 1")

  entries: dict = data.get("entries") or {}
  alias_index: dict = data.get("aliasIndex") or {}

  for eid, entry in entries.items():
    if not isinstance(entry, dict):
      errors.append(f"entries.{eid}: must be object")
      continue
    missing = REQUIRED_ENTRY - set(entry.keys())
    if missing:
      errors.append(f"entries.{eid}: missing {sorted(missing)}")
    status = entry.get("status")
    if status not in VALID_STATUS:
      errors.append(f"entries.{eid}: invalid status {status!r}")
    kind = entry.get("kind")
    if kind not in VALID_KIND:
      errors.append(f"entries.{eid}: invalid kind {kind!r}")
    tag = entry.get("tag", "")
    if not tag.startswith("#common:"):
      errors.append(f"entries.{eid}: tag must start with #common:")
    if status == "implemented":
      for field in ("path", "symbol"):
        if not entry.get(field):
          errors.append(f"entries.{eid}: {field} required when implemented")
      rel = entry.get("path")
      if rel and not (root / rel).exists():
        errors.append(f"entries.{eid}: path not found: {rel}")

  for alias, target in alias_index.items():
    if target not in entries:
      errors.append(f"aliasIndex[{alias!r}]: unknown entry {target!r}")

  return errors
