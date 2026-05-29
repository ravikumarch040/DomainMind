# M0 Day-1 Critical Path

File these tickets before writing production PHI code:

1. **AWS BAA** — AWS Artifact → review → sign
2. **GPU quota** — Service Quotas: `g5.2xlarge` 16 vCPU, `g5.12xlarge` 48 vCPU in `us-east-1`
3. **OpenAI ZDR** — Enterprise API key for labeler + RAGAS judge
4. **W&B Enterprise BAA** — procurement for `domainmind-qlora` project
5. **Route 53** — confirm hosted zone for ACM certs (M12)

Until BAA is signed, use synthetic/de-identified data only in W&B and OpenAI calls.
