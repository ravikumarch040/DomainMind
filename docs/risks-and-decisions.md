# Risks and decisions

## Top risks

| Risk | Mitigation (in repo) | Residual |
|------|----------------------|----------|
| PHI in training/logs/vendor APIs | Presidio before chunk; no raw PHI to W&B; BAA/ZDR checklists | Vendor misconfiguration — operational |
| Cross-tenant data leak | Tenant middleware, per-tenant Qdrant collections, isolation tests | DB schema isolation — **needs confirmation** |
| Fine-tune on prompt tokens | `DataCollatorForCompletionOnlyLM` (`AGENTS.md`) | Implementation discipline |
| Bad merge from 4-bit base | Merge from fp16 base only (`AGENTS.md`) | Operator error |
| Golden set contamination | Excluded from train/val; CI golden file gate | Split logic bugs |
| GPU quota / cost | M0 quota checklist; g5 instance types in runbooks | AWS approval delays |
| Prod deploy without BAA | M0 checklist blocks PHI until signed | Process compliance |

## Key architecture / technology decisions

| Decision | Rationale (inferred) | Status |
|----------|----------------------|--------|
| **Mistral 7B Instruct v0.3** + QLoRA | Domain adaptation with manageable GPU cost | Documented in architecture |
| **vLLM on EKS** | OpenAI-compatible high-throughput serving | README diagram |
| **Hybrid RAG** (BGE + Qdrant + rerank) | Retrieval quality for compliance docs | Architecture |
| **.NET 8 gateway** | Auth, routing, rate limits, central policy enforcement | Stack in `AGENTS.md` |
| **FastAPI** for retrieval/eval | Python ML ecosystem alignment | `services/` |
| **OpenAPI spec-first** | Contract stability across services | `AGENTS.md` |
| **Terraform multi-account** | Blast radius + env isolation | `docs/architecture.md` |
| **Argo Rollouts** for gateway | Progressive delivery + rollback | `infra/k8s/argocd/` |
| **Cognito JWT** + API keys | Human + machine clients | Gateway auth |
| **Postgres 16 + Redis + Qdrant** | Relational metadata, rate limits, vectors | Infra modules / Compose |

ADR log format: **not documented** — decisions are spread across `AGENTS.md`, architecture, and runbooks.
