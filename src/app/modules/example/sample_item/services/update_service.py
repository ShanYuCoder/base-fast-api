from app.modules.example.sample_item.schemas.request import SampleItemUpdateRequest
from app.modules.example.sample_item.services.search_service import _STORE


class SampleItemUpdateService:
  async def update(self, resource_id: int, body: SampleItemUpdateRequest) -> dict | None:
    for row in _STORE:
      if row.get("id") == resource_id:
        row.update(body.model_dump(exclude_none=True))
        return row
    return None