# Environments

## AWS accounts (organizational)

| Account | Purpose | Source |
|---------|---------|--------|
| `shared` | Terraform state, ECR, org CloudTrail | `docs/architecture.md` |
| `dev` | Development workloads | Terraform `infra/aws/envs/dev/` |
| `staging` | Pre-prod, load tests | `infra/aws/envs/staging/` |
| `prod` | Production (M12) | `infra/aws/envs/prod/` |

Account IDs and org structure: **needs confirmation**.

## Terraform environments

| Env | State key (S3 backend) | Default region |
|-----|--------------------------|----------------|
| dev | `dev/terraform.tfstate` | `us-east-1` |
| staging | **inferred** — separate env folder | `us-east-1` |
| prod | **inferred** — separate env folder | `us-east-1` |

Backend bucket: `domainmind-terraform-state`, lock table `domainmind-terraform-lock` (dev `main.tf`).

## URLs and endpoints

| Environment | Public API URL | Notes |
|-------------|----------------|-------|
| Local | `http://localhost:8080` (gateway), `5173` (web) | Compose + `dotnet run` / `npm run dev` |
| Dev / staging | **TBD** | Not in repo |
| Prod (example) | `https://api.domainmind.example.com` | Placeholder in `infra/k8s/base/ingress.yaml` and load-test runbook |

Replace `api.domainmind.example.com` with real DNS before go-live (**needs confirmation**).

## Local dependency ports

| Service | Port |
|---------|------|
| Gateway | 8080 |
| Retrieval | 8001 |
| Eval | 8002 |
| Orchestrator | 8003 |
| vLLM (mock) | 8000 |
| Postgres | 5432 |
| Redis | 6379 |
| Qdrant | 6333 / 6334 |
| Web (Vite) | 5173 |
