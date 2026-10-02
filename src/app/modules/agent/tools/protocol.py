from typing import Any, Protocol


class AgentTool(Protocol):
  name: str

  async def run(self, **kwargs: Any) -> dict[str, Any]:
    ...
