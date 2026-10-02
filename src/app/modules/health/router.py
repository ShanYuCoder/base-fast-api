from fastapi import APIRouter

from app.common.http.api_response import success

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
  return success({"status": "ok"})
