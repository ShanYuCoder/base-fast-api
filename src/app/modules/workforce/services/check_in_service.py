from app.modules.workforce.schemas.request import WorkforceCheckInRequest
from app.modules.workforce.schemas.response import WorkforceCheckInData


class WorkforceCheckInService:
  async def check_in(self, body: WorkforceCheckInRequest) -> WorkforceCheckInData:
    return WorkforceCheckInData(
      checked_in=True,
      employee_name=f"Worker-{body.badge_id}",
      shift_id="SHIFT-A",
      message="Stub check-in OK",
    )
