from pydantic import BaseModel, Field


class KnowledgeQueryRequest(BaseModel):
  query: str = Field(min_length=1)
  plant_id: int | None = None


class CitationItem(BaseModel):
  source: str
  excerpt: str
  page: int | None = None


class KnowledgeQueryResponse(BaseModel):
  answer: str
  citations: list[CitationItem]
