"""Data quality dashboard report generator."""

import json
from pathlib import Path


def generate_quality_report(stats: dict, output_path: Path) -> None:
    report = {
        "summary": stats,
        "checks": {
            "min_chunks": stats.get("chunks", 0) >= 10,
            "p95_reasonable": stats.get("p95", 0) <= 2048,
            "dedup_rate_ok": stats.get("duplicates", 0) / max(stats.get("loaded", 1), 1) < 0.5,
        },
    }
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = f"""# Data Quality Report

## Token distribution
- p50: {stats.get('p50', 'N/A')}
- p95: {stats.get('p95', 'N/A')} (use for max_seq_length)
- p99: {stats.get('p99', 'N/A')}
- max: {stats.get('max', 'N/A')}

## Pipeline stats
- Documents loaded: {stats.get('loaded', 0)}
- Rejected (quality): {stats.get('rejected_clean', 0)}
- Duplicates removed: {stats.get('duplicates', 0)}
- PHI entities scrubbed: {stats.get('phi_scrubbed', 0)}
- Chunks: {stats.get('chunks', 0)}
- Training records: {stats.get('records', 0)}
"""
    output_path.with_suffix(".md").write_text(md, encoding="utf-8")
