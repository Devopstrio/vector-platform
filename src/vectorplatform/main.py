from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI

from vectorplatform.api.endpoints import router as vector_router
from vectorplatform.core.database import engine
from vectorplatform.models.schemas import Base

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # In a real system, use Alembic for migrations instead of create_all
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Vector Platform API",
    description="Enterprise Vector Database Abstraction",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(vector_router, prefix="/v1", tags=["Vector Platform"])

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}

def start() -> None:
    logger.info("Starting Vector Platform API on 0.0.0.0:8018")
    uvicorn.run("vectorplatform.main:app", host="0.0.0.0", port=8018, reload=True)

if __name__ == "__main__":
    start()
