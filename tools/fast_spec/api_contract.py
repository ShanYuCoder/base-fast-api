"""Load *.api-test.yaml contract specs for pytest (vitest contract replacement)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterator

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PORTAL_ROOT = Path(os.getenv("PORTAL_ROOT", ROOT.parent / "portal"))
YAML_ROOT = ROOT / "docs/features/yaml"


def _expand(path_str: str) -> Path:
  return Path(os.path.expanduser(path_str)).resolve()


def discover_api_contract_tests(yaml_root: Path | None = None) -> list[dict[str, Any]]:
  root = yaml_root or YAML_ROOT
  cases: list[dict[str, Any]] = []
  patterns = ("*.api-test.yaml", "*.api-test.yml", "testcases/*.api-test.yaml", "testcases/*.api-test.yml")
  seen: set[Path] = set()
  for pattern in patterns:
    for path in sorted(root.glob(f"**/{pattern}")):
      if path in seen:
        continue
      seen.add(path)
      data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
      if data.get("type", "api-contract") != "api-contract":
        continue
      cases.append({"path": path, "data": data, "feature_dir": path.parent if path.parent.name != "testcases" else path.parent.parent})
  return cases


def portal_entity_keys(portal_ir: dict[str, Any]) -> set[str]:
  keys: set[str] = set()
  for entity in portal_ir.get("entities") or []:
    for field in entity.get("fields") or []:
      if key := field.get("key"):
        keys.add(key)
  return keys


def load_backend_spec(feature_dir: Path, backend_rel: str | None) -> dict[str, Any]:
  rel = backend_rel or "backend/01-backend-spec.yaml"
  path = feature_dir / rel
  return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def resolve_portal_ir(data: dict[str, Any], bundle: dict[str, Any] | None) -> Path | None:
  refs = [
    data.get("portalIrSpec"),
    (data.get("contractRef") or {}).get("portalIrSpec"),
    (bundle or {}).get("contractRef", {}).get("portalIrSpec"),
  ]
  for ref in refs:
    if ref:
      path = _expand(str(ref))
      if path.is_file():
        return path
  return None


def assert_contract_keys(
  backend: dict[str, Any],
  portal_keys: set[str],
  *,
  request_model: str | None = None,
  response_model: str | None = None,
) -> list[str]:
  errors: list[str] = []
  requests = backend.get("requests") or {}
  responses = backend.get("responses") or {}

  for model_name, bucket in ((request_model, requests), (response_model, responses)):
    if not model_name:
      continue
    for field in (bucket.get(model_name) or {}).get("fields") or []:
      name = field.get("name")
      if name and name not in portal_keys:
        errors.append(f"portal missing {model_name} key {name}")

  if not request_model and not response_model:
    for bucket_name, bucket in (("requests", requests), ("responses", responses)):
      for model_name, model in bucket.items():
        for field in (model or {}).get("fields") or []:
          name = field.get("name")
          if name and name not in portal_keys:
            errors.append(f"portal missing {bucket_name}.{model_name} key {name}")
  return errors


def iter_contract_test_ids() -> Iterator[str]:
  for case in discover_api_contract_tests():
    data = case["data"]
    yield data.get("id") or case["path"].stem


def run_contract_case(case: dict[str, Any], portal_root: Path | None = None) -> None:
  data = case["data"]
  feature_dir: Path = case["feature_dir"]
  bundle_path = next(feature_dir.glob("*.bundle.yaml"), None)
  bundle = yaml.safe_load(bundle_path.read_text(encoding="utf-8")) if bundle_path else None

  backend = load_backend_spec(feature_dir, data.get("backendSpec"))
  portal_path = resolve_portal_ir(data, bundle)
  portal_root = portal_root or DEFAULT_PORTAL_ROOT

  if portal_path is None:
    default = portal_root / "docs/features/yaml/factory/workforce/ir/spec.yaml"
    portal_path = default if default.is_file() else None

  if portal_path is None or not portal_path.is_file():
    raise AssertionError("portal ir/spec not available for contract test")

  portal_ir = yaml.safe_load(portal_path.read_text(encoding="utf-8")) or {}
  portal_keys = portal_entity_keys(portal_ir)
  assertions = data.get("assertions") or {}
  errors = assert_contract_keys(
    backend,
    portal_keys,
    request_model=assertions.get("requestModel"),
    response_model=assertions.get("responseModel"),
  )
  if errors:
    raise AssertionError("\n".join(errors))
