# Deployment

## CI/CD (GitHub Actions)

| Workflow | Trigger | Actions |
|----------|---------|---------|
| `python.yml` | `main`, `develop` | `uv` sync, ruff, pytest (pipelines); services import smoke; golden-set eval gate |
| `dotnet.yml` | `main`, `develop` | restore, build, test; tenant-isolation grep contract |
| `web.yml` | `main`, `develop` | `npm ci` / install, `npm run build` |
| `terraform.yml` | `infra/aws/**` | `terraform validate`, `fmt -check` (continue-on-error on init) |

Deploy to AWS/EKS from CI: **not documented** (no CD workflow in repo).

## Infrastructure provision

```bash
cd infra/aws/envs/dev && terraform init && terraform plan
```

Repeat for `staging` / `prod` with appropriate credentials and tfvars. Modules include VPC, KMS, S3, ECR, EKS, RDS, ElastiCache, Cognito (`infra/aws/envs/dev/main.tf`).

## Application deploy (Kubernetes)

Production steps from [runbooks/deploy-prod.md](runbooks/deploy-prod.md):

1. Prerequisites: GPU quota, ACM cert, Terraform applied to prod, ECR images tagged.
2. `kubectl apply -f infra/k8s/base/`
3. External Secrets Operator → Secrets Manager ARNs
4. Ingress with ACM cert ARN (`${ACM_CERT_ARN}`)
5. Verify ADOT → X-Ray
6. Load test with Locust (`infra/loadtest/locustfile.py`)

**Rollout:** Argo Rollouts on gateway (`infra/k8s/argocd/rollout-gateway.yaml`); auto-rollback on error spike; manual `kubectl argo rollouts undo gateway`.

## Container images

Dockerfiles under `infra/docker/` for gateway, retrieval, eval, orchestrator. Built via Compose locally; prod expects ECR push (**version tags** per prod runbook).

## Offline / ML deploy

QLoRA on SageMaker → merge → S3 → vLLM image/model mount. Details: [DomainMind_QLoRA_Pipeline.md](DomainMind_QLoRA_Pipeline.md).
