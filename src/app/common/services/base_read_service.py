from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseReadService(ABC, Generic[T]):
    """Stub read service — port EntrySearchTrait / BaseQuery."""

    @abstractmethod
    async def find_by_id(self, resource_id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, *, page: int = 1, per_page: int = 20, **filters: Any) -> dict[str, Any]:
        raise NotImplementedError
