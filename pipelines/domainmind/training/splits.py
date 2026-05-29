"""Train/val/test splits stratified by source."""

import json
import random
from pathlib import Path
from collections import defaultdict


def load_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def stratified_split(
    records: list[dict],
    *,
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    seed: int = 42,
    source_key: str = "source",
) -> tuple[list[dict], list[dict], list[dict]]:
    """Split stratified by document source to avoid leakage."""
    random.seed(seed)
    by_source: dict[str, list[dict]] = defaultdict(list)
    for i, r in enumerate(records):
        src = r.get(source_key, r.get("source_chunk", str(i))[:32])
        by_source[src].append(r)

    train, val, test = [], [], []
    for _src, group in by_source.items():
        random.shuffle(group)
        n = len(group)
        n_train = max(1, int(n * train_ratio))
        n_val = max(0, int(n * val_ratio))
        train.extend(group[:n_train])
        val.extend(group[n_train : n_train + n_val])
        test.extend(group[n_train + n_val :])

    return train, val, test


def write_splits(
    records: list[dict],
    output_dir: Path,
) -> tuple[Path, Path, Path]:
    train, val, test = stratified_split(records)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for name, data in [("train", train), ("val", val), ("test", test)]:
        p = output_dir / f"{name}.jsonl"
        with p.open("w", encoding="utf-8") as f:
            for r in data:
                f.write(json.dumps(r) + "\n")
        paths.append(p)
    return tuple(paths)
