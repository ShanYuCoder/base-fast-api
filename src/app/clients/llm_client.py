from typing import Any


class LlmClient:
  """Stub LLM client — wire to real provider later."""

  async def complete(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
    return {
      "text": f"[stub-llm] {prompt[:120]}",
      "model": kwargs.get("model", "stub"),
    }
