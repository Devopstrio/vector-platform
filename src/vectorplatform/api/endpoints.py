from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from qdrant_client import AsyncQdrantClient
from sqlalchemy.ext.asyncio import AsyncSession

from vectorplatform.core.database import get_db_session
from vectorplatform.core.qdrant import get_qdrant_client
from vectorplatform.models.schemas import (
    CollectionResponse,
    CreateCollectionRequest,
    SearchResult,
    VectorSearchRequest,
    VectorUpsertRequest,
)
from vectorplatform.repository.vector_repo import VectorRepository

router = APIRouter()

async def get_vector_repo(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    qdrant: Annotated[AsyncQdrantClient, Depends(get_qdrant_client)]
) -> AsyncGenerator[VectorRepository, None]:
    repo = VectorRepository(db, qdrant)
    yield repo

@router.post("/collections", response_model=CollectionResponse)
async def create_collection(
    req: CreateCollectionRequest,
    repo: Annotated[VectorRepository, Depends(get_vector_repo)]
) -> CollectionResponse:
    try:
        meta = await repo.create_collection(req)
        return CollectionResponse(id=meta.id, name=meta.name, vector_size=meta.vector_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/vectors/upsert")
async def upsert_vector(
    req: VectorUpsertRequest,
    repo: Annotated[VectorRepository, Depends(get_vector_repo)]
) -> dict[str, str]:
    try:
        await repo.upsert_vector(req)
        return {"status": "success", "message": "Vector upserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/vectors/search", response_model=list[SearchResult])
async def search_vectors(
    req: VectorSearchRequest,
    repo: Annotated[VectorRepository, Depends(get_vector_repo)]
) -> list[SearchResult]:
    try:
        results = await repo.search(req)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
