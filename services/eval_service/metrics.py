"""RAGAS + ROUGE + BERTScore metrics — M8."""

from eval_service.settings import settings


def compute_rouge(prediction: str, reference: str) -> float:
    try:
        from rouge_score import rouge_scorer

        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        scores = scorer.score(reference, prediction)
        return scores["rougeL"].fmeasure
    except Exception:
        return 0.0


def compute_bertscore(prediction: str, reference: str) -> float:
    try:
        from bert_score import score as bert_score_fn

        p, r, f1 = bert_score_fn([prediction], [reference], lang="en", verbose=False)
        return float(f1[0])
    except Exception:
        return 0.0


async def compute_ragas_faithfulness(
    question: str,
    answer: str,
    contexts: list[str],
) -> float:
    """RAGAS faithfulness with pinned judge model."""
    try:
        from ragas import SingleTurnSample
        from ragas.metrics import Faithfulness
        from ragas.llms import llm_factory

        llm = llm_factory(
            model=settings.judge_model,
            provider="openai",
            api_key=settings.openai_api_key or None,
        )
        sample = SingleTurnSample(
            user_input=question,
            response=answer,
            retrieved_contexts=contexts,
        )
        scorer = Faithfulness(llm=llm)
        result = await scorer.single_turn_ascore(sample)
        return float(result)
    except Exception:
        # Fallback heuristic when RAGAS/OpenAI unavailable
        overlap = sum(1 for c in contexts if any(w in answer.lower() for w in c.lower().split()[:20]))
        return min(1.0, overlap / max(len(contexts), 1))
