"""Orchestrator with SSE streaming — M7."""

import json
from typing import AsyncIterator

import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from orchestrator.citation import extract_citations
from orchestrator.prompt_assembly import assemble_prompt
from orchestrator.router import route_query

app = FastAPI(title="DomainMind Orchestrator", version="1.0.0")

RETRIEVAL_URL = "http://localhost:8001"
GATEWAY_URL = "http://localhost:8080"


class ChatRequest(BaseModel):
    query: str
    tenant_id: str = "default"
    system_prompt: str = "You are a compliance and legal expert."
    model_mode: str | None = None


async def stream_chat(req: ChatRequest) -> AsyncIterator[str]:
    mode = req.model_mode or route_query(req.query)
    messages = [{"role": "user", "content": req.query}]

    if mode == "rag_combined":
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{RETRIEVAL_URL}/retrieve",
                json={"query": req.query, "tenant_id": req.tenant_id, "top_k": 5},
            )
            chunks = r.json().get("chunks", []) if r.status_code == 200 else []
        prompt = assemble_prompt(req.system_prompt, req.query, chunks)
        messages = [{"role": "user", "content": prompt}]

    payload = {
        "messages": messages,
        "stream": True,
        "model": "domainmind",
    }
    headers = {"X-Model-Mode": mode}

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            f"{GATEWAY_URL}/v1/chat/completions",
            json=payload,
            headers=headers,
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    yield line + "\n\n"
                elif line.strip():
                    yield f"data: {json.dumps({'token': line})}\n\n"

    citations = extract_citations("")
    yield f"data: {json.dumps({'citations': [c.__dict__ for c in citations]})}\n\n"


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    return EventSourceResponse(stream_chat(req))


@app.get("/health")
async def health():
    return {"status": "ok"}
