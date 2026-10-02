from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int = 1
    per_page: int = 20
    total: int = 0
    last_page: int = 1


class PaginatedResult(BaseModel, Generic[T]):
    items: list[T] = Field(default_factory=list)
    total: int = 0

    def to_envelope_data(self) -> dict[str, Any]:
        return {"items": self.items, "total": self.total}

    def to_envelope_meta(self, page: int = 1, per_page: int = 20) -> dict[str, Any]:
        last_page = max(1, (self.total + per_page - 1) // per_page) if per_page else 1
        return PaginationMeta(
            page=page,
            per_page=per_page,
            total=self.total,
            last_page=last_page,
        ).model_dump()


def paginate(items: list[Any], page: int = 1, per_page: int = 20) -> PaginatedResult[Any]:
    page = max(1, page)
    per_page = max(1, min(per_page, 100))
    start = (page - 1) * per_page
    slice_items = items[start : start + per_page]
    return PaginatedResult(items=slice_items, total=len(items))
