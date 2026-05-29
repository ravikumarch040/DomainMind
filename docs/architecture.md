# DomainMind Architecture

## System context

DomainMind adapts Mistral 7B Instruct v0.3 to compliance/legal domains via QLoRA, serves via vLLM on EKS, augments with hybrid RAG (BGE embeddings + Qdrant), and evaluates with RAGAS + ROUGE + BERTScore.

## Data flow

```
Raw docs → Loaders → Clean → PHI Scrub → Dedup → Chunk → GPT-4o Label → Format → JSONL
                                                                              ↓
                                                                    SageMaker QLoRA Train
                                                                              ↓
                                                                    Merge fp16 → S3 → vLLM
```

## Service boundaries

| Service | Port (local) | Responsibility |
|---------|--------------|----------------|
| Gateway | 8080 | Auth, routing, rate limit, request logging |
| Retrieval | 8001 | Embed, hybrid search, rerank |
| Eval | 8002 | RAGAS runner, comparison jobs |
| vLLM | 8000 | OpenAI-compatible inference |
| Web | 5173 | Chat, eval dashboard, admin |

## Multi-tenancy (M11)

- JWT `tenant_id` claim from Cognito
- Per-tenant PostgreSQL schema (`search_path`)
- Per-tenant Qdrant collection `tenant_{id}_docs`
- Per-tenant KMS CMK for envelope encryption

## AWS accounts

| Account | Purpose |
|---------|---------|
| shared | Terraform state, ECR, org CloudTrail |
| dev | Development workloads |
| staging | Pre-prod, load tests |
| prod | Production (M12) |
