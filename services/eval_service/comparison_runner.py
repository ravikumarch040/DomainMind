"""4-system comparison runner."""

import json
import uuid
from pathlib import Path

import httpx

from eval_service.db import save_result
from eval_service.metrics import compute_bertscore, compute_rouge, compute_ragas_faithfulness
from eval_service.settings import settings

SYSTEMS = ["base", "fine_tuned", "rag", "combined"]


def load_golden_set(path: Path | None = None) -> list[dict]:
    path = path or Path(settings.golden_set_path)
    records = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


async def get_answer(
    question: str,
    system_mode: str,
    tenant_id: str = "default",
) -> tuple[str, list[str]]:
    contexts: list[str] = []
    async with httpx.AsyncClient(timeout=60.0) as client:
        if system_mode in ("rag", "combined"):
            r = await client.post(
                f"{settings.retrieval_url}/retrieve",
                json={"query": question, "tenant_id": tenant_id},
            )
            if r.status_code == 200:
                contexts = [c["text"] for c in r.json().get("chunks", [])]

        headers = {"X-Model-Mode": system_mode}
        r = await client.post(
            f"{settings.gateway_url}/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": question}],
                "model": "domainmind",
            },
            headers=headers,
        )
        if r.status_code == 200:
            data = r.json()
            answer = data["choices"][0]["message"]["content"]
            return answer, contexts
    return "", contexts


async def run_comparison(run_id: str | None = None) -> dict:
    run_id = run_id or str(uuid.uuid4())
    golden = load_golden_set()
    summary: dict[str, dict[str, float]] = {s: {} for s in SYSTEMS}

    for item in golden:
        question = item["instruction"]
        reference = item.get("expected_answer", "")

        for system in SYSTEMS:
            answer, contexts = await get_answer(question, system)
            rouge = compute_rouge(answer, reference)
            bert = compute_bertscore(answer, reference)
            faith = await compute_ragas_faithfulness(question, answer, contexts)

            for metric, score in [
                ("rouge_l", rouge),
                ("bertscore", bert),
                ("faithfulness", faith),
            ]:
                save_result(
                    run_id=run_id,
                    model_version="v0.1.0",
                    system_mode=system,
                    metric_name=metric,
                    score=score,
                    judge_model=settings.judge_model,
                )
                summary[system].setdefault(metric, []).append(score)

    aggregated = {
        system: {m: sum(v) / len(v) for m, v in metrics.items()}
        for system, metrics in summary.items()
    }
    return {"run_id": run_id, "aggregated": aggregated}
