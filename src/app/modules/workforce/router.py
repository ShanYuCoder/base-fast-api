from fastapi import APIRouter

from app.common.http.api_response import success
from app.modules.workforce.schemas.request import WorkforceCheckInRequest
from app.modules.workforce.services.check_in_service import WorkforceCheckInService

router = APIRouter(prefix="/workforce", tags=["workforce"])
_service = WorkforceCheckInService()


@router.post("/check-in")
async def workforce_check_in(body: WorkforceCheckInRequest) -> dict:
  result = await _service.check_in(body)
  return success(result.model_dump(), message="Checked in successfully")
