from typing import Any

from app.clients.cmms_client import CmmsClient
from app.clients.mes_client import MesClient
from app.modules.agent.tools.protocol import AgentTool
from app.modules.knowledge.services.query_service import KnowledgeQueryService
from app.modules.knowledge.schemas.request import KnowledgeQueryRequest


class KnowledgeTool:
  name = "knowledge"

  def __init__(self) -> None:
    self._service = KnowledgeQueryService()

  async def run(self, query: str, **kwargs: Any) -> dict[str, Any]:
    result = await self._service.query(KnowledgeQueryRequest(query=query))
    return result.model_dump()


class MesTool:
  name = "mes"

  def __init__(self) -> None:
    self._client = MesClient()

  async def run(self, plant_id: int = 1, **kwargs: Any) -> dict[str, Any]:
    return await self._client.get_downtime(plant_id)


class CmmsTool:
  name = "cmms"

  def __init__(self) -> None:
    self._client = CmmsClient()

  async def run(self, machine_id: str = "M-001", **kwargs: Any) -> dict[str, Any]:
    return await self._client.get_pm_schedule(machine_id)


TOOLS: list[AgentTool] = [KnowledgeTool(), MesTool(), CmmsTool()]
