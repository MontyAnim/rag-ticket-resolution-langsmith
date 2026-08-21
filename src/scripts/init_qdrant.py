import asyncio
from qdrant_client.http.models import Distance, VectorParams, HnswConfigDiff
from src.core.vector_db import qdrant_client
from src.core.config import settings

COLLECTION_NAME = "knowledge_base"
VECTOR_SIZE = 384  # Based on HuggingFace all-MiniLM-L6-v2

async def init_qdrant():
    print(f"Connecting to Qdrant at {settings.QDRANT_URL}...")
    
    # Check if collection exists
    collections = await qdrant_client.get_collections()
    collection_names = [c.name for c in collections.collections]
    
    if COLLECTION_NAME in collection_names:
        print(f"Collection '{COLLECTION_NAME}' already exists. Skipping creation.")
    else:
        print(f"Creating collection '{COLLECTION_NAME}' with {VECTOR_SIZE} dimensions...")
        await qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            ),
            hnsw_config=HnswConfigDiff(
                m=16,
                ef_construct=100
            )
        )
        print("Collection created successfully.")

    print("Creating payload indexes for metadata filtering...")
    # tenant_id is critical for multi-tenant isolation
    await qdrant_client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="tenant_id",
        field_schema="keyword"
    )
    
    await qdrant_client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="doc_id",
        field_schema="keyword"
    )
    print("Payload indexes created.")

if __name__ == "__main__":
    asyncio.run(init_qdrant())
