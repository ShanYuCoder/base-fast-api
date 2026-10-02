# FastAPI structure — common layer map

> Port từ Laravel `<api-checkout>` và Nest `portal/apps/api` sang `src/app/`.

## Layer layout

```text
src/app/
  main.py                 # FastAPI app, CORS, routers (/api prefix)
  config.py               # pydantic-settings
  common/
    http/                 # envelope + exception handlers
    presenters/           # BaseResource → to_contract()
    pagination.py
    auth/                 # dependencies + policies
    services/             # base read/write, select_item
    mixins/               # timestamps
  clients/                # httpx → integration-base (MES/CMMS/LLM)
  modules/
    health/
    knowledge/
    maintenance/
    agent/
```

## Trait / pattern map

| Laravel / Nest | Python fast (`src/app/`) |
|----------------|--------------------------|
| BaseController + ApiResponse | `common/http/api_response.py` + `exception_handlers.py` |
| BaseResource | `common/presenters/base.py` |
| EntrySearchTrait | `common/services/base_read_service.py` |
| BaseAction / BaseWriteHandler | `common/services/base_write_service.py` |
| BasePolicy | `common/auth/policies.py` |
| FormRequest | `modules/*/schemas/request.py` (Pydantic) |
| BaseMiddleware | Starlette middleware / `Depends()` |
| SelectItemTrait | `common/services/select_item.py` |
| Pagination helper | `common/pagination.py` |
| Module routes | `modules/*/router.py` → `main.py` |

## Envelope (khớp portal `apiFetch`)

Success:

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

Global prefix: **`/api`** — khớp `apps/web/src/lib/api-client.ts`.

## Invariants

- Router mỏng → service → presenter `to_contract()`
- Contract keys = portal `ir/spec.yaml` — không rename layer
- Không CommandBus ceremony
