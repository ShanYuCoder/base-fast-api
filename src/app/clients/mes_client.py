from typing import Any

from app.clients.base import BaseHttpClient
from app.config import get_settings


class MesClient:
  def __init__(self, http: BaseHttpClient | None = None) -> None:
    settings = get_settings()
    self._http = http or BaseHttpClient(settings.mes_base_url)

  async def get_downtime(self, plant_id: int) -> dict[str, Any]:
    try:
      payload = await self._http.get(f"/plants/{plant_id}/downtime")
      if isinstance(payload, dict) and payload.get("success") and "data" in payload:
        return payload["data"]
      return payload
    except Exception:
      return {
        "plant_id": plant_id,
        "items": [
          {"machine_id": "M-001", "minutes": 12, "reason": "mock-downtime"},
        ],
      }

  async def list_alarms(self, plant_id: int) -> dict[str, Any]:
    return {
      "plant_id": plant_id,
      "items": [
        {"id": 1, "machine_id": "M-001", "code": "ALM-100", "severity": "warning"},
      ],
    }
