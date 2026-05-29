"""Training entrypoint."""

import json
from pathlib import Path

from datasets import Dataset

from domainmind.training.config import QLoRAConfig
from domainmind.training.lora import attach_lora, build_trainer
from domainmind.training.model import build_model_and_tokenizer


def load_dataset_jsonl(path: Path) -> Dataset:
    texts = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                texts.append({"text": row.get("text", "")})
    return Dataset.from_list(texts)


def run_training(
    cfg: QLoRAConfig,
    train_ds: Dataset | Path,
    eval_ds: Dataset | Path,
):
    if isinstance(train_ds, Path):
        train_ds = load_dataset_jsonl(train_ds)
    if isinstance(eval_ds, Path):
        eval_ds = load_dataset_jsonl(eval_ds)

    model, tokenizer = build_model_and_tokenizer(cfg)
    model = attach_lora(model, cfg)
    trainer = build_trainer(model, tokenizer, train_ds, eval_ds, cfg)
    trainer.train()
    trainer.save_model(cfg.output_dir)
    return trainer
