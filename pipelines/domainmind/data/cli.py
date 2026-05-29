"""CLI for data pipeline."""

import argparse
from pathlib import Path

from domainmind.data.pipeline import run_pipeline
from domainmind.data.quality_report import generate_quality_report
from domainmind.settings import settings


def main() -> None:
    parser = argparse.ArgumentParser(description="DomainMind data pipeline")
    parser.add_argument("--input", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/dataset.jsonl"))
    parser.add_argument("--skip-synthetic", action="store_true")
    parser.add_argument("--max-chunks", type=int, default=None)
    args = parser.parse_args()

    stats = run_pipeline(
        args.input,
        args.output,
        skip_synthetic=args.skip_synthetic,
        max_chunks=args.max_chunks,
    )
    generate_quality_report(stats, args.output.parent / "quality_report.json")
    print(f"Pipeline complete: {stats}")


if __name__ == "__main__":
    main()
