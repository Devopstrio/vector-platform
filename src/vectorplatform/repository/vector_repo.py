
import structlog
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sqlalchemy.ext.asyncio import AsyncSession

from vectorplatform.models.schemas import (
    CollectionMetadata,
    CreateCollectionRequest,
    SearchResult,
    VectorSearchRequest,
    VectorUpsertRequest,
)

logger = structlog.get_logger()

class VectorRepository:
    def __init__(self, db: AsyncSession, qdrant: AsyncQdrantClient):
        self.db = db
        self.qdrant = qdrant

    async def create_collection(self, req: CreateCollectionRequest) -> CollectionMetadata:
        # Create in PostgreSQL
        new_meta = CollectionMetadata(
            name=req.name,
            vector_size=req.vector_size,
            distance_metric=req.distance_metric
        )
        self.db.add(new_meta)
        await self.db.commit()
        await self.db.refresh(new_meta)

        # Create in Qdrant
        distance = Distance.COSINE if req.distance_metric.lower() == "cosine" else Distance.EUCLID
        await self.qdrant.create_collection(
            collection_name=req.name,
            vectors_config=VectorParams(size=req.vector_size, distance=distance)
        )
        logger.info("Collection created", name=req.name)
        return new_meta

    async def upsert_vector(self, req: VectorUpsertRequest) -> bool:
        point = PointStruct(
            id=req.id,
            vector=req.vector,
            payload=req.payload or {}
        )
        await self.qdrant.upsert(
            collection_name=req.collection_name,
            points=[point]
        )
        logger.info("Vector upserted", collection=req.collection_name, id=req.id)
        return True

    async def search(self, req: VectorSearchRequest) -> list[SearchResult]:
        response = await self.qdrant.query_points(
            collection_name=req.collection_name,
            query=req.vector,
            limit=req.top_k,
            with_payload=True
        )
        hits = response.points
        logger.info("Search completed", collection=req.collection_name, results=len(hits))
        return [
            SearchResult(id=str(hit.id), score=hit.score, payload=hit.payload)
            for hit in hits
        ]
