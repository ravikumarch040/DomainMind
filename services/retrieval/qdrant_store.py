"""Qdrant hybrid search with per-tenant collections."""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from retrieval.settings import settings


def tenant_collection(tenant_id: str) -> str:
    return f"tenant_{tenant_id}_docs"


class QdrantStore:
    def __init__(self, url: str | None = None):
        self.client = QdrantClient(url=url or settings.qdrant_url)

    def ensure_collection(self, tenant_id: str, vector_size: int = 1024) -> None:
        name = tenant_collection(tenant_id)
        collections = [c.name for c in self.client.get_collections().collections]
        if name not in collections:
            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    def upsert(
        self,
        tenant_id: str,
        points: list[PointStruct],
    ) -> None:
        self.ensure_collection(tenant_id)
        self.client.upsert(collection_name=tenant_collection(tenant_id), points=points)

    def search(
        self,
        tenant_id: str,
        query_vector: list[float],
        limit: int = 20,
    ) -> list:
        return self.client.search(
            collection_name=tenant_collection(tenant_id),
            query_vector=query_vector,
            limit=limit,
        )
