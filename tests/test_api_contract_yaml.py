"""YAML-driven API contract tests (replaces vitest spec contract)."""

from __future__ import annotations

import pytest

from fast_spec.api_contract import discover_api_contract_tests, run_contract_case


def _case_id(case: dict) -> str:
  return case["data"].get("id") or case["path"].stem


@pytest.mark.parametrize(
  "case",
  discover_api_contract_tests(),
  ids=_case_id,
)
def test_api_contract_yaml(case: dict) -> None:
  run_contract_case(case)
