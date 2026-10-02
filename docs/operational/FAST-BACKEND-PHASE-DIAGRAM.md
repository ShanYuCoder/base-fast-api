# Fast backend phase diagram

```mermaid
flowchart TD
  SPEC["portal ir/spec.yaml"]
  BS["/fast-spec\nbackend/01-backend-spec.yaml"]
  GRILL["/grill-fast-spec"]
  CODE["/fast-code\nfast_gen write"]
  UNIT["fast-unit-gen"]
  RUN["uvicorn :4000"]
  WIRE["portal /wire"]

  SPEC --> BS
  BS --> GRILL
  GRILL --> CODE
  CODE --> UNIT
  UNIT --> RUN
  RUN --> WIRE
```

| Phase | Skill | Output |
|-------|-------|--------|
| Contract | portal `/contract` | `packages/models` |
| Backend spec | `/fast-spec` | `backend/01-backend-spec.yaml` |
| Audit | `/grill-fast-spec` | approval on spec |
| Code | `/fast-code` | `src/app/modules/*` |
| Test | pytest | `tests/` |
| Wire | portal `/wire` | FE services → fast |

Hub: [TEAM-AI-BACKEND-WORKFLOW.md](https://github.com/raintr91/base_docs/blob/1.0.0/platform/toolchain/TEAM-AI-BACKEND-WORKFLOW.md)
