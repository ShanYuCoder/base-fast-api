from fastapi import APIRouter, Depends, HTTPException

from app.common.http.api_response import success
from app.modules.example.sample_item.presenters.sample_item_presenter import SampleItemPresenter
from app.modules.example.sample_item.schemas.request import (
  SampleItemSearchRequest,
  SampleItemCreateRequest,
  SampleItemUpdateRequest,
)
from app.modules.example.sample_item.services.search_service import SampleItemSearchService
from app.modules.example.sample_item.services.create_service import SampleItemCreateService
from app.modules.example.sample_item.services.update_service import SampleItemUpdateService
from app.modules.example.sample_item.services.delete_service import SampleItemDeleteService

router = APIRouter(prefix="/sample-items", tags=["example"])
_search = SampleItemSearchService()
_create = SampleItemCreateService()
_update = SampleItemUpdateService()
_delete = SampleItemDeleteService()


@router.get("")
async def search_sample_item(query: SampleItemSearchRequest = Depends()) -> dict:
  items, total = await _search.search(query)
  data = {"items": [SampleItemPresenter(i).to_contract() for i in items], "total": total}
  return success(data, message="Retrieved successfully", meta={"pagination": {"page": query.page, "per_page": query.per_page, "total": total}})


@router.post("")
async def create_sample_item(body: SampleItemCreateRequest) -> dict:
  item = await _create.create(body)
  return success(SampleItemPresenter(item).to_contract(), message="Created successfully", code=201)


@router.patch("/{id}")
async def update_sample_item(id: int, body: SampleItemUpdateRequest) -> dict:
  item = await _update.update(id, body)
  if item is None:
    raise HTTPException(status_code=404, detail="Not Found")
  return success(SampleItemPresenter(item).to_contract(), message="Updated successfully")


@router.delete("/{id}")
async def delete_sample_item(id: int) -> dict:
  ok = await _delete.delete(id)
  if not ok:
    raise HTTPException(status_code=404, detail="Not Found")
  return success({"success": True})
