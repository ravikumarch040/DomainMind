# Ownership

From `.github/CODEOWNERS` (GitHub auto-review routing). Product/org roles are **not documented**.

| Area | Path(s) | Owner (GitHub) |
|------|---------|----------------|
| Default / entire repo | `*` | `@ravindra-kumar` |
| Data & training pipelines | `/pipelines/` | `@ravindra-kumar` |
| API gateway | `/gateway/` | `@ravindra-kumar` |
| AWS infrastructure | `/infra/aws/` | `@ravindra-kumar` |
| Golden eval set | `/evals/golden_set.jsonl` | `@ravindra-kumar` |

## Suggested ownership map (not in CODEOWNERS)

| Concern | Path | Owner |
|---------|------|-------|
| Frontend | `apps/web/` | **TBD** (falls under `*`) |
| Python services | `services/` | **TBD** |
| Kubernetes / ADOT | `infra/k8s/` | **TBD** |
| OpenAPI contracts | `shared/openapi/` | **TBD** |
| Product / roadmap | — | **needs confirmation** |
| Security / compliance sign-off | — | **needs confirmation** |

Update CODEOWNERS when teams split.
