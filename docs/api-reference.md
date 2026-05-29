# API reference

Public contracts are defined in `shared/openapi/`. Implementations should match specs (spec-first per `AGENTS.md`).

## Gateway — DomainMind API

**Spec:** `shared/openapi/gateway.yaml`  
**Local base URL:** `http://localhost:8080` (OpenAPI server entry)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | None | Liveness |
| `POST` | `/v1/chat/completions` | Bearer JWT and/or `X-API-Key` | OpenAI-shaped chat; header `X-Model-Mode`: `base` \| `fine_tuned` \| `rag` \| `combined` (default `combined`) |

**Responses:** `200` completion, `401` unauthorized, `429` rate limit.

Admin routes exist under `/admin` (inferred from `AdminController`, `RbacMiddleware`) — **not in OpenAPI**; treat as internal until spec added.

## Retrieval service

**Spec:** `shared/openapi/retrieval.yaml`  
**Local base URL:** `http://localhost:8001`

| Method | Path | Body highlights | Description |
|--------|------|-----------------|-------------|
| `GET` | `/health` | — | Liveness |
| `POST` | `/retrieve` | `query`, `tenant_id`, optional `top_k` | Hybrid search + rerank |
| `POST` | `/index` | (schema partial in spec) | Incremental indexing → `202` |

## Eval service

**Spec:** `shared/openapi/eval.yaml`  
**Local base URL:** `http://localhost:8002`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness |
| `POST` | `/eval/run` | Start 4-system comparison (`base`, `fine_tuned`, `rag`, `combined`) → `202` |
| `GET` | `/eval/runs/{run_id}` | Fetch results |

## Orchestrator

**Not in OpenAPI.** Local port **8003** (`docker-compose.yml`). Proxies retrieve + gateway for RAG flows — **inferred from code** (`services/orchestrator/main.py`).

## Upstream (internal)

| Service | Contract | Local port |
|---------|----------|------------|
| vLLM | OpenAI-compatible HTTP | 8000 (mock in Compose) |
| TEI embeddings | HTTP | 8081 (not in local Compose file; referenced in retrieval settings) |

Full request/response schemas: see YAML `components/schemas` in each spec file.
