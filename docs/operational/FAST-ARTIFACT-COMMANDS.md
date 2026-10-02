# Fast artifact — lệnh script

> **R2/R3:** Product Code + architecture → [`base-docs`](https://github.com/raintr91/base_docs) · E2E plans → [`base-tests`](https://github.com/raintr91/base_test) · gen: `pnpm portal:gen --id …` / `pnpm testcase:gen --id …` · [Hub split](https://github.com/raintr91/base_test/blob/main/docs/HUBS.md) / [Docs hub](https://github.com/raintr91/base_docs) / [Tests hub](https://github.com/raintr91/base_test/blob/main/docs/TESTS-HUB.md)

> Chạy trong `<fast-api-base-checkout>`. Spec/docs = Python + shell. Codegen/unitgen = **Codegenkit** (không giữ root `codegen/` / `unitgen/`).

| Lệnh | Mục đích |
|------|----------|
| `./scripts/spec-split <bundle.yaml>` | `portal-feature-bundle/v1` → `ir/*` + `backend/01-backend-spec.yaml` |
| `./scripts/spec-split --check <bundle.yaml>` | Verify IR |
| `./scripts/spec-split-all` | Glob mọi `*.bundle.yaml` |
| `./scripts/spec-merge <bundle.yaml>` | `ir/*` → bundle SSOT |
| `./scripts/docs-render` | bundle → ``docs/features/` (stub only — SSOT on hubs) / md/` |
| `./scripts/docs-dev` | MkDocs Material preview `:8001` (thay VitePress) |
| `./scripts/docs-build` | Static site → `site/` |
| `codegenkit api-gen:dry --adapter=fastapi … -- --spec …` | Plan scaffold |
| `codegenkit api-gen --adapter=fastapi … -- --spec …` | Write `src/app/modules/...` |
| `codegenkit api-unit-gen --adapter=fastapi … -- --spec …` | pytest scaffold |
| `./registries/validate-common validate` | Validate `registries/common.registry.json` |
| `./registries/validate-common show` | Print common registry |
| `make test` / `.venv/bin/pytest` | API + yaml contract — **không Playwright** |

## Docs preview

```bash
./scripts/docs-render && ./scripts/docs-dev
# mở http://localhost:8001
```

## Pilot

```bash
codegenkit init --type=be --adapter=fastapi --yes --project-root=.
./scripts/spec-split `base-docs` Product Code (prefer `--id`)
codegenkit api-gen --adapter=fastapi --project-root=. -- --spec `base-docs` Product Code (prefer `--id`)
make test
```

Portal hub: [FEATURE-ARTIFACT-COMMANDS](https://github.com/raintr91/base_docs/blob/1.0.0/platform/toolchain/FEATURE-ARTIFACT-COMMANDS.md)
