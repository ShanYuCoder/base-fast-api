from collections.abc import Callable
from typing import Any

import httpx

from app.config import Settings, get_settings


class BaseHttpClient:
  def __init__(self, base_url: str, timeout: float = 30.0) -> None:
    self._base_url = base_url.rstrip("/")
    self._timeout = timeout

  async def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
    async with httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout) as client:
      response = await client.get(path, **kwargs)
      response.raise_for_status()
      return response.json()

  async def post(self, path: str, json: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
    async with httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout) as client:
      response = await client.post(path, json=json, **kwargs)
      response.raise_for_status()
      return response.json()


def build_client(base_url: str) -> BaseHttpClient:
  return BaseHttpClient(base_url)


def client_from_settings(getter: Callable[[Settings], str]) -> BaseHttpClient:
  settings: Settings = get_settings()
  return build_client(getter(settings))
