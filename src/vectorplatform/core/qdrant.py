import os
from collections.abc import AsyncGenerator

from qdrant_client import AsyncQdrantClient

QDRANT_URL = os.getenv("QDRANT_URL", ":memory:")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

class QdrantConnectionManager:
    _client = None

    @classmethod
    def get_client(cls) -> AsyncQdrantClient:
        if cls._client is None:
            if QDRANT_URL == ":memory:":
                cls._client = AsyncQdrantClient(location=":memory:")
            else:
                cls._client = AsyncQdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        return cls._client


async def get_qdrant_client() -> AsyncGenerator[AsyncQdrantClient, None]:
    yield QdrantConnectionManager.get_client()
