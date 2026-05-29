"""Query routing: factual vs open-ended."""

OPEN_ENDED_KEYWORDS = [
    "explain",
    "compare",
    "analyze",
    "why",
    "how does",
    "implications",
    "difference between",
]


def route_query(query: str) -> str:
    """
    Returns mode: 'fine_tuned_only' or 'rag_combined'.
    Simple factual → fine-tuned only; complex/open-ended → RAG + fine-tuned.
    """
    q = query.lower()
    if any(kw in q for kw in OPEN_ENDED_KEYWORDS):
        return "rag_combined"
    if len(query.split()) <= 12 and query.strip().endswith("?"):
        return "fine_tuned_only"
    return "rag_combined"
