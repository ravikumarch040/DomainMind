# Configuration

## Key config files

| Path | Purpose |
|------|---------|
| `gateway/src/DomainMind.Gateway/appsettings.json` | Connection strings, Gateway URLs, Redis, Cognito |
| `gateway/src/DomainMind.Gateway/appsettings.Development.json` | Dev overrides |
| `.env.example` | Root template for pipelines / local secrets |
| `infra/aws/envs/dev/terraform.tfvars.example` | Terraform variables sample |
| `infra/compose/docker-compose.yml` | Local service env wiring |
| `shared/openapi/*.yaml` | API contracts |
| `pipelines/` project config | Training/data (`pyproject.toml`, pipeline configs — see QLoRA doc) |

## Environment variables (representative)

### Root / pipelines (`.env.example`)

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Labeling / judge |
| `WANDB_API_KEY` | Training metrics (no raw PHI per `AGENTS.md`) |
| `AWS_REGION` | Default `us-east-1` |
| `SAGEMAKER_ROLE_ARN` | Training jobs |
| `DATABASE_URL` | Postgres |

### Gateway (appsettings / Compose)

| Key | Purpose |
|-----|---------|
| `ConnectionStrings__Default` | PostgreSQL |
| `Redis__ConnectionString` | Rate limit |
| `Gateway__VllmBaseUrl` / `VllmBaseModelUrl` | Inference upstream |
| `Gateway__RateLimitPerMinute` | Default 60 |
| `Cognito__Authority` | JWT issuer |
| `ASPNETCORE_URLS` | Bind address |

### Retrieval (`RetrievalSettings`)

| Env (pydantic) | Default |
|----------------|---------|
| `QDRANT_URL` | `http://localhost:6333` |
| `TEI_EMBED_URL` / `TEI_RERANK_URL` | localhost TEI ports |
| `DATABASE_URL`, `REDIS_URL` | Local Postgres / Redis |

### Eval (`EvalSettings`)

| Env | Default |
|-----|---------|
| `DATABASE_URL` | Local Postgres |
| `GATEWAY_URL` / `RETRIEVAL_URL` | Service URLs |
| `JUDGE_MODEL` | `gpt-4o-2024-08-06` |
| `FAITHFULNESS_THRESHOLD` | `0.75` |
| `GOLDEN_SET_PATH` | `evals/golden_set.jsonl` |

## Secrets strategy

| Layer | Approach |
|-------|----------|
| Local | `.env` gitignored; Compose uses dev-only passwords |
| CI | GitHub secrets (not listed in repo) — **needs confirmation** |
| Prod | AWS Secrets Manager + External Secrets Operator; KMS CMK per env |
| Images | No embedded secrets (compliance checklist) |

Rotation: RDS master password via `manage_master_user_password` (Terraform RDS module).
