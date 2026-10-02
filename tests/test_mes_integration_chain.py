import os

import httpx
import pytest

from app.clients.mes_client import MesClient


class _FakeHttp:
    async def get(self, path: str) -> dict:
        return {
            "success": True,
            "code": 200,
            "message": "Retrieved successfully",
            "data": {
                "plant_id": 1,
                "items": [
                    {
                        "machine_id": "M-001",
                        "minutes": 12,
                        "reason": "integration-mock-downtime",
                    },
                ],
            },
        }


@pytest.mark.asyncio
async def test_mes_client_unwraps_integration_envelope():
    client = MesClient(http=_FakeHttp())
    data = await client.get_downtime(1)
    assert data["plant_id"] == 1
    assert data["items"][0]["machine_id"] == "M-001"
    assert data["items"][0]["reason"] == "integration-mock-downtime"


INTEGRATION_URL = os.getenv("MES_BASE_URL", "http://127.0.0.1:4100")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_mes_client_live_integration_chain():
    try:
        async with httpx.AsyncClient(timeout=2.0) as hc:
            health = await hc.get(f"{INTEGRATION_URL}/health")
    except httpx.ConnectError:
        pytest.skip("integration server not running")
    if health.status_code != 200:
        pytest.skip("integration server not healthy")

    client = MesClient()
    data = await client.get_downtime(1)
    assert data["plant_id"] == 1
    assert len(data["items"]) >= 1
    assert "machine_id" in data["items"][0]
