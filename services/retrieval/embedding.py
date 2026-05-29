"""Embedding via HuggingFace TEI."""

import httpx

from retrieval.settings import settings


async def embed_texts(texts: list[str]) -> list[list[float]]:
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{settings.tei_embed_url}/embed",
            json={"inputs": texts},
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data and isinstance(data[0], list):
            return data
        return [item.get("embedding", item) for item in data]


async def rerank(query: str, documents: list[str], top_n: int = 5) -> list[tuple[int, float]]:
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{settings.tei_rerank_url}/rerank",
            json={"query": query, "texts": documents},
        )
        resp.raise_for_status()
        results = resp.json()
        ranked = sorted(
            [(r.get("index", i), r.get("score", 0.0)) for i, r in enumerate(results)],
            key=lambda x: x[1],
            reverse=True,
        )
        return ranked[:top_n]
