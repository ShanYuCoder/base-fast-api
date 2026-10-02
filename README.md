# fast-api-base

FastAPI backend base — phục vụ FE portal/Next, harness AI (code lane).

**Path:** `~/workspace/fast-api-base`

## Quick start

```bash
cd ~/workspace/fast-api-base
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 4000 --app-dir src
```

- API: http://localhost:4000/api
- Swagger: http://localhost:4000/api/docs
- Health: http://localhost:4000/api/health

## Tests

```bash
make test   # pytest — API + *.api-test.yaml
```

## Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```

## Envelope (portal-compatible)

```json
{
  "success": true,
  "code": 200,
  "message": "Success",
  "user_message": null,
  "data": {},
  "meta": null,
  "trace_id": null
}
```

## AI harness (code lane)

Skills: `/api` · `/wire` · `/unit` (+ grill-*) · `/platform-base` · `/platform-mark`  
Gen / gaps: **Artifactgraph MCP** (khi dùng từ FE product) hoặc runners trên repo này.

SSOT harness: `.cursor/` tại repo này (Platform DNA / toolkit `init` sync).
