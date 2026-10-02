from pydantic import BaseModel, Field


class SampleItemSearchRequest(BaseModel):
  page: int = Field(default=1, ge=1)
  per_page: int = Field(default=20, ge=1, le=100)


class SampleItemCreateRequest(BaseModel):
  name: str | None = None


class SampleItemUpdateRequest(BaseModel):
  name: str | None = None
