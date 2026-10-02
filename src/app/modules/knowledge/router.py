from fastapi import APIRouter

from app.common.http.api_response import success
from app.modules.knowledge.schemas.request import KnowledgeQueryRequest
from app.modules.knowledge.services.query_service import KnowledgeQueryService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
_service = KnowledgeQueryService()


@router.post("/query")
async def knowledge_query(body: KnowledgeQueryRequest) -> dict:
  result = await _service.query(body)
  return success(result.model_dump())
