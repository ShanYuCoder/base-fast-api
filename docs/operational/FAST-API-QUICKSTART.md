# FastAPI quickstart

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)

## Local dev

```bash
cd <fast-api-base-checkout>
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 4000 --app-dir src
```

> **AI layer:** SSOT là `.cursor/{skills,rules,extracts}` trên từng repo.

## Verify

```bash
curl -s http://localhost:4000/api/health | jq
make test   # pytest only — không E2E trong repo này
```

## Docs site (MkDocs Material — không pnpm / VitePress)

```bash
./scripts/docs-render    # yaml → docs/features/md/
./scripts/docs-dev       # http://localhost:8001
./scripts/docs-build     # static → site/
# hoặc: make docs-dev · make docs-build
```

## Portal wire

```bash
# apps/web/.env
NEXT_PUBLIC_API_URL=http://127.0.0.1:4000
```

Paths: `apiFetch('/health')` → `GET http://127.0.0.1:4000/api/health`  
E2E Playwright sống ở **portal** — fast chỉ cung cấp API `:4000` + pytest.

## Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```
