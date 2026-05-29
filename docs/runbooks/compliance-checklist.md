# HIPAA / SOC 2 Compliance Checklist

## M0 baseline

- [ ] AWS BAA signed
- [ ] CloudTrail org-trail → dedicated log account, S3 Object Lock 7yr
- [ ] AWS Config HIPAA conformance pack enabled
- [ ] GuardDuty + Security Hub org-wide
- [ ] KMS CMK per environment; S3/RDS/ElastiCache encrypted
- [ ] VPC private subnets only; ALB sole public ingress
- [ ] Secrets Manager rotation enabled; no secrets in images
- [ ] RDS `force_ssl=1`, deletion protection on

## M1 data

- [ ] Presidio PHI scrubber before chunking
- [ ] CI test: synthetic PHI fixture → zero matches post-scrub
- [ ] OpenAI ZDR enrolled for labeler

## M8 eval

- [ ] RAGAS judge pinned `gpt-4o-2024-08-06`
- [ ] Golden set never in train/val

## M11 tenancy

- [ ] Tenant isolation integration test in CI (required check)
- [ ] Per-tenant schema + Qdrant collection verified
