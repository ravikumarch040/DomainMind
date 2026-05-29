"""CLI for training pipeline."""

import argparse
from pathlib import Path

from domainmind.training.baseline import run_baseline
from domainmind.training.config import QLoRAConfig
from domainmind.training.merge import merge_and_save
from domainmind.training.splits import load_jsonl, write_splits
from domainmind.training.train import run_training


def main() -> None:
    parser = argparse.ArgumentParser(description="DomainMind training")
    sub = parser.add_subparsers(dest="command", required=True)

    split_p = sub.add_parser("split")
    split_p.add_argument("--input", type=Path, required=True)
    split_p.add_argument("--output-dir", type=Path, default=Path("data/splits"))

    base_p = sub.add_parser("baseline")
    base_p.add_argument("--questions", type=Path, required=True)
    base_p.add_argument("--output", type=Path, default=Path("data/baseline.json"))
    base_p.add_argument("--wandb", action="store_true")

    train_p = sub.add_parser("train")
    train_p.add_argument("--train", type=Path, required=True)
    train_p.add_argument("--eval", type=Path, required=True)
    train_p.add_argument("--output-dir", type=Path, default=Path("outputs"))

    merge_p = sub.add_parser("merge")
    merge_p.add_argument("--base", type=str, required=True)
    merge_p.add_argument("--adapter", type=str, required=True)
    merge_p.add_argument("--output", type=str, required=True)

    args = parser.parse_args()

    if args.command == "split":
        records = load_jsonl(args.input)
        paths = write_splits(records, args.output_dir)
        print(f"Splits written: {paths}")
    elif args.command == "baseline":
        run_baseline(args.questions, args.output, log_wandb=args.wandb)
    elif args.command == "train":
        cfg = QLoRAConfig(output_dir=str(args.output_dir))
        run_training(cfg, args.train, args.eval)
    elif args.command == "merge":
        merge_and_save(args.base, args.adapter, args.output)


if __name__ == "__main__":
    main()
