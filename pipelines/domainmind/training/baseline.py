"""Zero-shot baseline evaluation — M2."""

import json
from pathlib import Path

from domainmind.settings import settings
from domainmind.training.inference import InferenceWrapper


def run_baseline(
    questions_path: Path,
    output_path: Path,
    *,
    log_wandb: bool = False,
) -> list[dict]:
    wrapper = InferenceWrapper(settings.base_model_name)
    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    if isinstance(questions, dict):
        questions = questions.get("questions", [])

    results = []
    for q in questions:
        instruction = q if isinstance(q, str) else q.get("instruction", "")
        prompt = wrapper.format_chat(settings.system_prompt, instruction)
        gen = wrapper.generate(prompt, max_new_tokens=256)
        results.append({"instruction": instruction, "response": gen.text})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    if log_wandb:
        try:
            import wandb

            wandb.init(project=settings.wandb_project, job_type="baseline")
            wandb.log({"baseline_samples": len(results)})
            for i, r in enumerate(results[:5]):
                wandb.log({f"baseline/sample_{i}": r["response"][:500]})
            wandb.finish()
        except Exception:
            pass

    return results
