# Runbooks

Critical operational guides. Detailed steps live in linked files; this page is the index.

## Before production (M0 / M12)

| Scenario | Document |
|----------|----------|
| Day-1 legal/compliance prerequisites (BAA, GPU quota, OpenAI ZDR, W&B, Route 53) | [runbooks/m0-day1-checklist.md](runbooks/m0-day1-checklist.md) |
| HIPAA/SOC 2 baseline and milestone gates | [runbooks/compliance-checklist.md](runbooks/compliance-checklist.md) |

## Deploy and rollback

| Scenario | Action |
|----------|--------|
| **Production deploy** | Follow [runbooks/deploy-prod.md](runbooks/deploy-prod.md): Terraform prod → ECR push → `kubectl apply` → secrets → ingress → ADOT → Locust |
| **Rollback gateway** | `kubectl argo rollouts undo gateway` or wait for Argo auto-rollback on error rate |
| **vLLM / model bad release** | Revert image tag / S3 model artifact — **needs confirmation** (not step-by-step in repo) |

## Outage response (high level)

| Symptom | Likely cause | First steps |
|---------|--------------|-------------|
| `503` / "vLLM service unavailable" | vLLM pod down or wrong URL | Check `Gateway__VllmBaseUrl`, vLLM deployment health, GPU nodes |
| `429` rate limit | Redis or per-tenant limits | Verify ElastiCache/Redis; adjust `RateLimitPerMinute` if policy allows |
| High p95 (&gt; 4s) | Load or GPU saturation | SNS alert per prod runbook; scale HPA (`hpa-gateway.yaml`), check GPU utilization |
| Retrieval empty / wrong tenant | Wrong `tenant_id` or collection | Verify JWT claim; Qdrant collection `tenant_{id}_docs` |
| PHI concern in logs | Logging misconfiguration | Stop logging; verify tokenized fields only; incident per org policy — **TBD** |

## Local recovery

```bash
docker compose -f infra/compose/docker-compose.yml down -v  # destructive: wipes volumes
docker compose -f infra/compose/docker-compose.yml up -d --build
```

Use only for local dev; never against prod data.
