import pytest

from app.modules.example.sample_item.services.search_service import SampleItemSearchService
from app.modules.example.sample_item.schemas.request import SampleItemSearchRequest


@pytest.mark.asyncio
async def test_sample_item_search_returns_items():
  service = SampleItemSearchService()
  items, total = await service.search(SampleItemSearchRequest())
  assert total >= 0
  assert isinstance(items, list)