"""FastAPI eval service — M8."""

import asyncio
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

from eval_service.comparison_runner import run_comparison
from eval_service.db import init_db
from eval_service.settings import settings

app = FastAPI(title="DomainMind Eval", version="1.0.0")

_jobs: dict[str, dict] = {}


class EvalRunRequest(BaseModel):
    run_id: str | None = None
    systems: list[str] | None = None


@app.on_event("startup")
def startup():
    try:
        init_db()
    except Exception:
        pass


@app.get("/health")
async def health():
    return {"status": "ok", "judge_model": settings.judge_model}


@app.post("/eval/run", status_code=202)
async def eval_run(req: EvalRunRequest, background_tasks: BackgroundTasks):
    run_id = req.run_id or "pending"

    async def _job():
        result = await run_comparison(req.run_id)
        _jobs[result["run_id"]] = {"status": "completed", "result": result}

    rid = req.run_id or "async"
    _jobs[rid] = {"status": "running"}
    background_tasks.add_task(lambda: asyncio.run(_job()))
    return {"run_id": rid, "status": "accepted"}


@app.get("/eval/runs/{run_id}")
async def get_run(run_id: str):
    job = _jobs.get(run_id)
    if not job:
        return {"run_id": run_id, "status": "unknown"}
    return job


@app.get("/eval/golden-set")
async def golden_set():
    path = Path(settings.golden_set_path)
    if not path.exists():
        return {"count": 0, "note": "SME content TBD"}
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    return {"count": len(lines), "path": str(path)}
