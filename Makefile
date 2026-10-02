# Fast API base — Makefile (Python-native; codegen via Codegenkit)

.PHONY: spec-split spec-split-all spec-merge docs-render docs-dev docs-build fast-gen fast-gen-dry fast-openapi contract-check test

VENV := .venv
PY := $(VENV)/bin/python
export PYTHONPATH := tools:src

spec-split:
	./scripts/spec-split $(BUNDLE)

spec-split-all:
	./scripts/spec-split-all

spec-merge:
	./scripts/spec-merge $(BUNDLE)

docs-render:
	./scripts/docs-render

docs-dev:
	./scripts/docs-dev

docs-build:
	./scripts/docs-build

# Codegen / unitgen SSOT: Codegenkit fastapi adapter (synced by init).
# Staging copy for review: codegenkit/adapters/fastapi/_staging-from-fast-api-base/
fast-gen-dry:
	codegenkit api-gen:dry --adapter=fastapi --project-root=. -- --spec $(SPEC)

fast-gen:
	codegenkit api-gen --adapter=fastapi --project-root=. -- --spec $(SPEC) $(if $(FORCE),--force,)

fast-openapi:
	@echo "openapi export: use codegenkit api-gen (fastapi) — see docs/operational/FAST-CODEGEN.md"

contract-check:
	$(PY) -m fast_spec.cli contract-check

test:
	$(PY) -m pytest tests/ -q
