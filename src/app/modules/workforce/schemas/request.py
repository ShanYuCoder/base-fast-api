from pydantic import BaseModel, Field


class WorkforceCheckInRequest(BaseModel):
  badge_id: str = Field(min_length=1)
  station_id: str | None = None
  plant_id: int | None = None
