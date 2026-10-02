from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Header, HTTPException

from app.common.http.api_response import UNAUTHENTICATED


@dataclass
class CurrentUser:
    id: int
    name: str
    plant_id: int | None = None
    roles: list[str] | None = None


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    """Stub auth — replace with real token validation."""
    if authorization and authorization.startswith("Bearer "):
        return CurrentUser(id=1, name="stub-user", plant_id=1, roles=["engineer"])
    return CurrentUser(id=0, name="guest", plant_id=None, roles=["guest"])


async def require_user(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    if user.id == 0:
        raise HTTPException(status_code=401, detail=UNAUTHENTICATED)
    return user


async def get_plant_id(user: Annotated[CurrentUser, Depends(get_current_user)]) -> int | None:
    return user.plant_id
