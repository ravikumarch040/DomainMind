# Security and access

## Auth model

| Mechanism | Usage |
|-----------|--------|
| **Amazon Cognito** | JWT bearer; `Cognito:Authority` in gateway config (`Program.cs`) |
| **API key** | Header `X-API-Key`; OpenAPI `apiKeyAuth`; DB-backed `ApiKey` entity with hashed key |
| **Development** | JWT validation relaxed; chat allowed without auth in Development (`ChatController`, `Program.cs`) |

JWT claims used by middleware:

- `tenant_id` → tenant context
- Standard role claim → RBAC role

Fallback headers (local/testing): `X-Tenant-Id`, `X-Role` (`TenantMiddleware.cs`).

## Roles and permissions

| Role | Write/admin (inferred) |
|------|-------------------------|
| `Admin`, `Editor` | Allowed for non-chat mutating routes / `/admin` |
| `Viewer` (default) | Read-oriented; blocked from `/admin` writes |
| Chat `POST /v1/chat/completions` | Allowed for all authenticated roles (RBAC bypass for that path) |

`ApiKey.Role` defaults to `Viewer` in entity model.

## Tenant isolation (M11)

- JWT `tenant_id` claim
- Qdrant collection per tenant: `tenant_{id}_docs`
- Per-tenant KMS CMK (architecture doc) — **needs confirmation** in application code
- Per-tenant PostgreSQL schema (`search_path`) — documented in architecture; **needs confirmation** in migrations

## Compliance controls (summary)

See [runbooks/compliance-checklist.md](runbooks/compliance-checklist.md): BAA, CloudTrail, Config, GuardDuty, KMS, private VPC, Secrets Manager rotation, RDS `force_ssl`, Presidio PHI scrub, golden-set isolation, tenant isolation CI.

## Secrets

- No secrets in container images (checklist)
- Production: External Secrets Operator → AWS Secrets Manager ARNs (`runbooks/deploy-prod.md`)
- Local: `.env` from `.env.example` — never commit real secrets
