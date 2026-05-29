# Requirements

High-level only; no formal PRD in repo.

## Business

| ID | Requirement | Source |
|----|-------------|--------|
| B1 | Support regulated workloads (HIPAA/SOC 2 alignment) | `README.md`, compliance runbook |
| B2 | Multi-tenant SaaS isolation (data, vectors, keys) | `docs/architecture.md` (M11) |
| B3 | Domain adaptation for compliance/legal via fine-tuning + RAG | `README.md`, architecture |
| B4 | Measurable quality vs base / fine-tuned / RAG / combined modes | `shared/openapi/eval.yaml`, eval service |

## Functional

| ID | Requirement | Notes |
|----|-------------|-------|
| F1 | OpenAI-compatible `POST /v1/chat/completions` with model modes: `base`, `fine_tuned`, `rag`, `combined` | `shared/openapi/gateway.yaml`, `X-Model-Mode` header |
| F2 | Hybrid retrieval + rerank; per-tenant indexing | `shared/openapi/retrieval.yaml`, `services/retrieval/` |
| F3 | Four-system eval runs with persisted metrics | `shared/openapi/eval.yaml`, `eval_service/db.py` |
| F4 | Data pipeline: load → clean → **PHI scrub before chunk** → dedup → chunk → label → JSONL | `docs/architecture.md`, `AGENTS.md` |
| F5 | QLoRA train on SageMaker; merge adapters from fp16 base | `AGENTS.md`, QLoRA LLD doc |
| F6 | Request logging with tokenized prompt/response (not raw PHI in logs — policy in `AGENTS.md`) | `GatewayDbContext` |
| F7 | Rate limiting | `RateLimitMiddleware`, Redis |

## Non-functional

| ID | Requirement | Notes |
|----|-------------|-------|
| NF1 | Encryption at rest (KMS) for S3, RDS, ElastiCache | Compliance checklist, Terraform modules |
| NF2 | Private subnets; ALB as public ingress | Compliance checklist |
| NF3 | Primary region `us-east-1` | `AGENTS.md`, `.env.example` |
| NF4 | Spec-first APIs | `AGENTS.md` — update OpenAPI before implementation |
| NF5 | Observability: OpenTelemetry gateway; ADOT → X-Ray in prod runbook | `Program.cs`, `infra/k8s/adot/` |
| NF6 | Prod alerts: p95 &gt; 4s, error rate &gt; 1%, GPU &gt; 90% | `runbooks/deploy-prod.md` |

Performance targets and RPO/RTO: **TBD**.
