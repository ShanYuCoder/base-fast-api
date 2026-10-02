from app.modules.example.sample_item.schemas.request import SampleItemCreateRequest
from app.modules.example.sample_item.services.search_service import _STORE


class SampleItemCreateService:
  async def create(self, body: SampleItemCreateRequest) -> dict:
    new_id = max((row.get("id", 0) for row in _STORE), default=0) + 1
    item = {"id": new_id, **body.model_dump(exclude_none=True)}
    _STORE.append(item)
    return item