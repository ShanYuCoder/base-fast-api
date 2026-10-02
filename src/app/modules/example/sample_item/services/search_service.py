from app.modules.example.sample_item.schemas.request import SampleItemSearchRequest

_STORE: list[dict] = [
  {
    "id": 1,
    "name": "Contract gen pilot A",
    "managers": [{"id": 101, "full_name": "Manager A"}],
  },
  {
    "id": 2,
    "name": "Contract gen pilot B",
    "managers": [{"id": 102, "full_name": "Manager B"}],
  },
  {
    "id": 3,
    "name": "Contract gen pilot C",
    "managers": [{"id": 103, "full_name": "Manager C"}],
  },
]


class SampleItemSearchService:
  async def search(self, query: SampleItemSearchRequest) -> tuple[list[dict], int]:
    start = (query.page - 1) * query.per_page
    items = _STORE[start : start + query.per_page]
    return items, len(_STORE)