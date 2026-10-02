from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseWriteService(ABC, Generic[T]):
    """Stub write service — port BaseAction / BaseWriteHandler."""

    @abstractmethod
    async def create(self, payload: dict[str, Any]) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, resource_id: int, payload: dict[str, Any]) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, resource_id: int) -> None:
        raise NotImplementedError
