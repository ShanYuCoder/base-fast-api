from abc import ABC, abstractmethod

from app.common.auth.dependencies import CurrentUser


class BasePolicy(ABC):
    """Port of Laravel BasePolicy."""

    @abstractmethod
    def view_any(self, user: CurrentUser) -> bool:
        raise NotImplementedError

    @abstractmethod
    def view(self, user: CurrentUser, resource_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create(self, user: CurrentUser) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: CurrentUser, resource_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user: CurrentUser, resource_id: int) -> bool:
        raise NotImplementedError

    def authorize(self, allowed: bool, message: str = "Forbidden") -> None:
        from fastapi import HTTPException

        from app.common.http.api_response import FORBIDDEN

        if not allowed:
            raise HTTPException(status_code=403, detail=message or FORBIDDEN)


class AllowAllPolicy(BasePolicy):
    def view_any(self, user: CurrentUser) -> bool:
        return True

    def view(self, user: CurrentUser, resource_id: int) -> bool:
        return True

    def create(self, user: CurrentUser) -> bool:
        return True

    def update(self, user: CurrentUser, resource_id: int) -> bool:
        return True

    def delete(self, user: CurrentUser, resource_id: int) -> bool:
        return True
