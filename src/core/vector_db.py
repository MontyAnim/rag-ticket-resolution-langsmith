from qdrant_client import AsyncQdrantClient
from src.core.config import settings

qdrant_client = AsyncQdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)
