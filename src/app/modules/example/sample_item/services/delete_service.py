from app.modules.example.sample_item.services.search_service import _STORE


class SampleItemDeleteService:
  async def delete(self, resource_id: int) -> bool:
    for idx, row in enumerate(_STORE):
      if row.get("id") == resource_id:
        _STORE.pop(idx)
        return True
    return False