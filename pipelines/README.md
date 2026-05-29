# DomainMind Pipelines

```bash
uv sync --extra dev
uv run pytest
uv run domainmind-data --input ../data/fixtures --output ../data/dataset.jsonl --skip-synthetic
uv run domainmind-train split --input ../data/dataset.jsonl --output-dir ../data/splits
```
