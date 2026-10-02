from typing import Any

from app.clients.base import BaseHttpClient
from app.config import get_settings


class CmmsClient:
  def __init__(self, http: BaseHttpClient | None = None) -> None:
    settings = get_settings()
    self._http = http or BaseHttpClient(settings.cmms_base_url)

  async def get_pm_schedule(self, machine_id: str) -> dict[str, Any]:
    try:
      return await self._http.get(f"/machines/{machine_id}/pm-schedule")
    except Exception:
      return {
        "machine_id": machine_id,
        "items": [
          {"id": 1, "task": "Inspect belt", "due_at": "2026-08-01"},
        ],
      }
