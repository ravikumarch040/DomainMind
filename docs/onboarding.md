# Onboarding

How to run DomainMind locally for development.

## Prerequisites

| Tool | Version / notes |
|------|-----------------|
| Python | 3.11+ with [uv](https://github.com/astral-sh/uv) |
| .NET SDK | 8.x |
| Node.js | 20.x (web CI) |
| Docker | Compose v2 for local stack |
| Terraform | ≥ 1.5 (optional, for infra work) |

AWS credentials only needed for SageMaker/S3/terraform work — not for default local loop.

## Quick start

### 1. Python pipelines

```bash
cd pipelines
uv sync
uv run pytest
```

### 2. Local infrastructure (no PHI)

```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

Starts Postgres, Redis, Qdrant, vLLM mock, gateway, retrieval, eval, orchestrator.

### 3. .NET gateway (standalone alternative)

```bash
cd gateway
dotnet run --project src/DomainMind.Gateway
```

Default: `http://localhost:8080`, Swagger in Development.

### 4. React web UI

```bash
cd apps/web
npm install
npm run dev
```

Vite dev server: `http://localhost:5173` (per architecture doc).

### 5. Environment file

```bash
cp .env.example .env
# Fill OPENAI_API_KEY etc. only if running labeling/eval against real APIs
```

Never use real PHI in local Compose (stated in `docker-compose.yml`).

## Verify health

| Endpoint | Expected |
|----------|----------|
| `GET http://localhost:8080/health` | `{ "status": "ok" }` |
| `GET http://localhost:8001/health` | OK (retrieval) |
| `GET http://localhost:8002/health` | OK (eval) |

## Common commands

```bash
cd pipelines && uv run pytest
cd gateway && dotnet test
cd apps/web && npm test
cd infra/aws/envs/dev && terraform plan
```

## Read next

- [index.md](index.md) — full wiki TOC
- [architecture.md](architecture.md) — system context
- [AGENTS.md](../AGENTS.md) — agent/coding non-negotiables
- [runbooks/m0-day1-checklist.md](runbooks/m0-day1-checklist.md) — before any PHI work
