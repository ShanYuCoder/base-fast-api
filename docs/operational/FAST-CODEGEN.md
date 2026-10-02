# Fast codegen

> **R2/R3:** Product Code + architecture → [`base-docs`](https://github.com/raintr91/base_docs) · E2E plans → [`base-tests`](https://github.com/raintr91/base_test) · gen: `pnpm portal:gen --id …` / `pnpm testcase:gen --id …` · [Hub split](https://github.com/raintr91/base_test/blob/main/docs/HUBS.md) / [Docs hub](https://github.com/raintr91/base_docs) / [Tests hub](https://github.com/raintr91/base_test/blob/main/docs/TESTS-HUB.md)

> **Codegen SSOT:** Codegenkit fastapi adapter (`adapters/fastapi/{codegen,unitgen}/`).  
> Product repo **không** giữ root `codegen/` / `unitgen/` — sau `codegenkit init --type=be --adapter=fastapi` toolkit sync.  
> Spec split vẫn Python-native trên repo này (`./scripts/spec-split`).

## Commands

```bash
cd <fast-api-base-checkout>
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
codegenkit init --type=be --adapter=fastapi --yes --project-root=.

# Bundle → ir/{spec,legacy,design} + backend/01-backend-spec.yaml
./scripts/spec-split `base-docs` Product Code (prefer `--id`)
./scripts/spec-split-all
./scripts/docs-render

# Codegen / unitgen (Codegenkit CLI)
codegenkit api-gen:dry --adapter=fastapi --project-root=. -- --spec <…/backend/01-backend-spec.yaml>
codegenkit api-gen --adapter=fastapi --project-root=. -- --spec <…/backend/01-backend-spec.yaml>
codegenkit api-unit-gen --adapter=fastapi --project-root=. -- --spec <…/backend/01-backend-spec.yaml>

# Hoặc Makefile
make fast-gen-dry SPEC=...
make fast-gen SPEC=...
make docs-dev                  # MkDocs :8001
make test
```

## Feature layout

```text
`docs/features/` (stub only — SSOT on hubs) / 
  yaml/{domain}/{function}/
    {function}.bundle.yaml      # portal-feature-bundle/v1
    ir/spec.yaml · legacy.yaml · design.yaml
    backend/01-backend-spec.yaml
    backend/02-openapi.yaml
    {function}.api-test.yaml    # pytest contract (thay vitest)
    testcases/
    generated/
  md/{domain}/{function}/       # ./scripts/docs-render
```

Contract keys: portal `ir/spec.yaml` · `contractRef.portalIrSpec` in bundle.

Hub: [FEATURE-ARTIFACT-FLOWS](https://github.com/raintr91/base_docs/blob/1.0.0/platform/toolchain/FEATURE-ARTIFACT-FLOWS.md) · [FAST-ARTIFACT-COMMANDS](./FAST-ARTIFACT-COMMANDS.md) · portal [REPO-SPLIT-MAP](https://github.com/raintr91/base_docs/blob/1.0.0/platform/toolchain/REPO-SPLIT-MAP.md)
