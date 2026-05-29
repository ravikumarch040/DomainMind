"""Incremental re-indexing by file hash."""

import hashlib
from dataclasses import dataclass

from qdrant_client.models import PointStruct

from retrieval.embedding import embed_texts
from retrieval.qdrant_store import QdrantStore


@dataclass
class ChunkRecord:
    chunk_id: str
    text: str
    doc_name: str
    source: str
    file_hash: str


def file_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


async def index_chunks(
    tenant_id: str,
    chunks: list[ChunkRecord],
    store: QdrantStore | None = None,
) -> int:
    store = store or QdrantStore()
    texts = [c.text for c in chunks]
    vectors = await embed_texts(texts)
    points = [
        PointStruct(
            id=i,
            vector=vec,
            payload={
                "chunk_id": c.chunk_id,
                "text": c.text,
                "doc_name": c.doc_name,
                "source": c.source,
                "file_hash": c.file_hash,
            },
        )
        for i, (c, vec) in enumerate(zip(chunks, vectors))
    ]
    store.upsert(tenant_id, points)
    return len(points)
