from pydantic import BaseModel


class SampleItemResource(BaseModel):
  id: int | str | None = None
  name: int | str | None = None
