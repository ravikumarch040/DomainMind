"""FastAPI retrieval service — M6."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from retrieval.embedding import embed_texts, rerank
from retrieval.indexer import ChunkRecord, index_chunks
from retrieval.qdrant_store import QdrantStore
from retrieval.settings import settings

app = FastAPI(title="DomainMind Retrieval", version="1.0.0")


class RetrieveRequest(BaseModel):
    query: str
    tenant_id: str
    top_k: int = 5


class Chunk(BaseModel):
    chunk_id: str
    text: str
    score: float
    source: str
    doc_name: str


class RetrieveResponse(BaseModel):
    chunks: list[Chunk]


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/retrieve", response_model=RetrieveResponse)
async def retrieve(req: RetrieveRequest):
    store = QdrantStore()
    vectors = await embed_texts([req.query])
    if not vectors:
        raise HTTPException(500, "Embedding failed")
    hits = store.search(req.tenant_id, vectors[0], limit=20)
    if not hits:
        return RetrieveResponse(chunks=[])

    docs = [h.payload.get("text", "") for h in hits]
    ranked = await rerank(req.query, docs, top_n=req.top_k)

    chunks = []
    for idx, score in ranked:
        hit = hits[idx]
        chunks.append(
            Chunk(
                chunk_id=hit.payload.get("chunk_id", str(hit.id)),
                text=hit.payload.get("text", ""),
                score=score,
                source=hit.payload.get("source", ""),
                doc_name=hit.payload.get("doc_name", ""),
            )
        )
    return RetrieveResponse(chunks=chunks)


class IndexRequest(BaseModel):
    tenant_id: str
    chunks: list[dict]


@app.post("/index", status_code=202)
async def index_documents(req: IndexRequest):
    records = [
        ChunkRecord(
            chunk_id=c["chunk_id"],
            text=c["text"],
            doc_name=c.get("doc_name", ""),
            source=c.get("source", ""),
            file_hash=c.get("file_hash", ""),
        )
        for c in req.chunks
    ]
    count = await index_chunks(req.tenant_id, records)
    return {"indexed": count}
