from abc import ABC, abstractmethod
from typing import Any


class BasePresenter(ABC):
    """Port of Nest/Laravel BaseResource — entity → contract keys."""

    @abstractmethod
    def to_contract(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def collection(cls, items: list[Any]) -> list[dict[str, Any]]:
        return [item.to_contract() if hasattr(item, "to_contract") else cls._wrap(item) for item in items]

    @staticmethod
    def _wrap(item: Any) -> dict[str, Any]:
        if isinstance(item, dict):
            return item
        if hasattr(item, "model_dump"):
            return item.model_dump()
        return dict(item)
