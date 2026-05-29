# DomainMind — Agent Guidelines

## Stack

- **Python 3.11+** with `uv` in `pipelines/` and `services/`
- **.NET 8** in `gateway/`
- **React 18 + TypeScript + Vite + Tailwind** in `apps/web/`
- **Terraform** in `infra/aws/`
- **AWS** primary region `us-east-1`

## Non-negotiables

1. Never train on prompt tokens — use `DataCollatorForCompletionOnlyLM`.
2. `model.config.use_cache = False` during training.
3. Merge LoRA adapters from **fp16 base**, never 4-bit quantized base.
4. Use `tokenizer.apply_chat_template` — never hand-roll chat formats.
5. PHI scrubber runs **before** chunking in the data pipeline.
6. Golden test set never appears in train/val splits.
7. Do not log raw PHI to W&B — metrics and redacted samples only.

## Commands

```bash
cd pipelines && uv run pytest
cd gateway && dotnet test
cd apps/web && npm test
cd infra/aws/envs/dev && terraform plan
```

## OpenAPI spec-first

Implement services against `shared/openapi/*.yaml`. Update spec before implementation.
