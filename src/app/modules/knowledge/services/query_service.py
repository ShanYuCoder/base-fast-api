from app.modules.knowledge.schemas.request import CitationItem, KnowledgeQueryRequest, KnowledgeQueryResponse


class KnowledgeQueryService:
  async def query(self, payload: KnowledgeQueryRequest) -> KnowledgeQueryResponse:
    return KnowledgeQueryResponse(
      answer=f"Stub answer for: {payload.query}",
      citations=[
        CitationItem(
          source="SOP-MAINT-001",
          excerpt="Follow lockout/tagout before maintenance.",
          page=3,
        ),
      ],
    )
