from pydantic import BaseModel, Field

from fastapi import APIRouter

from app.common.http.api_response import success
from app.modules.agent.tools import TOOLS

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentChatRequest(BaseModel):
  message: str = Field(min_length=1)
  tool: str | None = None


@router.post("/chat")
async def agent_chat(body: AgentChatRequest) -> dict:
  tool_name = body.tool or "knowledge"
  tool = next((t for t in TOOLS if t.name == tool_name), TOOLS[0])
  result = await tool.run(query=body.message, plant_id=1, machine_id="M-001")
  return success({"tool": tool.name, "result": result})
