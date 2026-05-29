"""SageMaker Model Registry integration — M4."""

import json
from datetime import datetime, timezone


def build_model_card(
    *,
    model_uri: str,
    dataset_dvc_hash: str,
    sweep_run_id: str,
    metrics: dict,
) -> dict:
    return {
        "model_uri": model_uri,
        "lineage": {
            "dataset_dvc_hash": dataset_dvc_hash,
            "sweep_run_id": sweep_run_id,
        },
        "metrics": metrics,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "base_model": "mistralai/Mistral-7B-Instruct-v0.3",
        "domain": "compliance/legal",
    }


def save_model_card(path: str, card: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(card, f, indent=2)
