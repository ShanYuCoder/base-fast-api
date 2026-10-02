from pydantic import BaseModel


class WorkforceCheckInData(BaseModel):
  checked_in: bool
  employee_name: str
  shift_id: str | None = None
  message: str | None = None
