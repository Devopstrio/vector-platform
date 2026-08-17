import uuid
from typing import Any

from pydantic import BaseModel
from sqlalchemy import JSON, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# SQLAlchemy Models
class Base(DeclarativeBase):
    pass

class CollectionMetadata(Base):
    __tablename__ = "collections"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    vector_size: Mapped[int]
    distance_metric: Mapped[str]
    metadata_config: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

# Pydantic Schemas
class CreateCollectionRequest(BaseModel):
    name: str
    vector_size: int
    distance_metric: str = "Cosine"

class CollectionResponse(BaseModel):
    id: str
    name: str
    vector_size: int

class VectorUpsertRequest(BaseModel):
    collection_name: str
    id: str
    vector: list[float]
    payload: dict[str, Any] | None = None

class VectorSearchRequest(BaseModel):
    collection_name: str
    vector: list[float]
    top_k: int = 5
    filter_payload: dict[str, Any] | None = None

class SearchResult(BaseModel):
    id: str
    score: float
    payload: dict[str, Any] | None = None
