# Known issues

Major open issues visible in repo (not an issue tracker).

| Issue | Impact | Source |
|-------|--------|--------|
| Production hostname is placeholder `api.domainmind.example.com` | Ingress/DNS must be configured before prod | `infra/k8s/base/ingress.yaml` |
| Terraform CI uses `continue-on-error` on init/validate | Infra drift may not fail PRs | `.github/workflows/terraform.yml` |
| Tenant isolation dotnet job uses `\|\| true` | Test failures may not block merge | `.github/workflows/dotnet.yml` |
| Eval faithfulness gate is placeholder (file count only) | Quality regressions may slip | `.github/workflows/python.yml` |
| SME eval content incomplete | `/eval` SME path returns stub | `services/eval_service/main.py` — `"SME content TBD"` |
| Local stack uses vLLM **mock**, not real inference | Local behavior ≠ prod GPU serving | `infra/compose/docker-compose.yml` |
| TEI services not defined in Compose | Full RAG path may need extra local setup | Compose vs `RetrievalSettings` |
| Compliance checklist items largely unchecked in repo | Manual attestation required | `runbooks/compliance-checklist.md` |

GitHub Issues / project board: **not linked in repo** — **TBD**.
