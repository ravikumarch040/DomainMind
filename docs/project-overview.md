# Project overview

## Goals

Build a **production-ready, multi-tenant, HIPAA/SOC 2-aligned** platform for **domain-specific LLMs** (compliance/legal focus) on AWS. The system fine-tunes Mistral 7B with QLoRA, serves via vLLM, augments answers with hybrid RAG, and measures quality with automated eval (RAGAS, ROUGE, BERTScore).

*Source: `README.md`, `docs/architecture.md`.*

## Scope

| In scope | Out of scope (current repo signals) |
|----------|-------------------------------------|
| Data prep, PHI scrubbing, labeling, QLoRA train/merge (`pipelines/`) | Full product roadmap / milestone definitions beyond checklist refs (M0–M12) — **not documented** as a single spec |
| API gateway, retrieval, eval, orchestrator (`gateway/`, `services/`) | Real vLLM in local Docker Compose (uses mock server) |
| React web UI (`apps/web/`) | Production URLs and live AWS account IDs — **needs confirmation** |
| Terraform AWS infra, K8s manifests (`infra/aws/`, `infra/k8s/`) | Non-AWS clouds |
| OpenAPI-first contracts (`shared/openapi/`) | |

## Success criteria

Explicit product KPIs are **not documented** in the repo. Inferred success signals from code and CI:

- Golden eval set present and gated in CI (`evals/golden_set.jsonl`, `.github/workflows/python.yml`).
- PHI scrubber passes tests before chunking (`pipelines/tests/test_phi_scrubber.py`).
- Tenant isolation middleware and contract checks in gateway CI.
- Compliance checklist items in [runbooks/compliance-checklist.md](runbooks/compliance-checklist.md) (many are manual checkboxes).

## Stakeholders / users

- **API clients** — OpenAI-compatible chat via gateway.
- **Web users** — Chat, eval dashboard, admin (inferred from `README.md` service list).
- **Operators / ML engineers** — Pipelines, SageMaker, deploy runbooks.

*Personas and SLAs: **TBD**.*
