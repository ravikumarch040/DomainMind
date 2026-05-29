# Testing strategy

## What exists

| Layer | Tooling | Location / CI |
|-------|---------|----------------|
| **Pipelines unit** | pytest, ruff | `pipelines/tests/` — PHI scrubber, splits, cleaning, config; `python.yml` (excludes `test_train_integration.py`) |
| **Gateway unit/integration** | xUnit | `gateway/tests/DomainMind.Gateway.Tests/` — chat, tenant isolation; `dotnet.yml` |
| **Services** | Import smoke only in CI | `python.yml` — no dedicated pytest job for `services/` |
| **Web** | Vitest (`npm test`) | `apps/web/` — **not in** `web.yml` CI (build only) |
| **Terraform** | validate, fmt | `terraform.yml` on `infra/aws/**` |
| **Eval gate** | Golden set file presence/count | `python.yml` `eval-gate` job (faithfulness threshold placeholder) |
| **Compliance** | Manual checklist | `runbooks/compliance-checklist.md` |
| **Load** | Locust | `infra/loadtest/` — manual per prod runbook |

## Gaps / missing (high level)

| Area | Status |
|------|--------|
| End-to-end tests (gateway → vLLM → retrieval) | **Not documented** in CI |
| `services/` automated tests | Minimal / absent in CI |
| Web tests in CI | Missing from `web.yml` |
| `test_train_integration.py` | Ignored in default CI |
| Full RAGAS faithfulness gate vs threshold | Placeholder in CI comment |
| Staging/prod smoke after deploy | Manual runbook only |

## How to run locally

```bash
cd pipelines && uv sync && uv run pytest
cd gateway && dotnet test
cd apps/web && npm test
cd infra/aws/envs/dev && terraform plan
```

Per `AGENTS.md`.

## Test data rules

- No PHI in local Compose (`docker-compose.yml` header).
- Golden set never in train/val (`AGENTS.md`).
- Synthetic PHI fixtures for scrubber tests (`compliance-checklist.md` M1).
