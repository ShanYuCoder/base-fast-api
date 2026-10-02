from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common.http.exception_handlers import register_exception_handlers
from app.config import get_settings
from app.generated_routers import ROUTERS
from app.modules.agent.router import router as agent_router
from app.modules.health.router import router as health_router
from app.modules.knowledge.router import router as knowledge_router
from app.modules.maintenance.router import router as maintenance_router
from app.modules.workforce.router import router as workforce_router

API_PREFIX = "/api"


def create_app() -> FastAPI:
  settings = get_settings()
  app = FastAPI(
    title="Factory AI API",
    description="FastAPI backend for Factory AI Platform (platform-base)",
    version="0.1.0",
    docs_url=f"{API_PREFIX}/docs",
    openapi_url=f"{API_PREFIX}/openapi.json",
  )

  app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  register_exception_handlers(app)

  app.include_router(health_router, prefix=API_PREFIX)
  app.include_router(knowledge_router, prefix=API_PREFIX)
  app.include_router(maintenance_router, prefix=API_PREFIX)
  app.include_router(workforce_router, prefix=API_PREFIX)
  app.include_router(agent_router, prefix=API_PREFIX)
  for generated in ROUTERS:
    app.include_router(generated, prefix=API_PREFIX)

  return app


app = create_app()
