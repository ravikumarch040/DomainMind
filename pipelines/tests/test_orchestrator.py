from orchestrator.prompt_assembly import assemble_prompt
from orchestrator.router import route_query
from orchestrator.citation import extract_citations


def test_route_factual():
    assert route_query("What is SOC 2?") == "fine_tuned_only"


def test_route_open_ended():
    assert route_query("Explain the difference between HIPAA and HITECH") == "rag_combined"


def test_assemble_prompt_includes_sources():
    prompt = assemble_prompt(
        "System",
        "User q",
        [{"doc_name": "soc2.pdf", "chunk_id": "1", "text": "SOC 2 content", "score": 0.9}],
    )
    assert "[SOURCE: soc2.pdf, 1]" in prompt


def test_extract_citations():
    text = "Answer per [SOURCE: hipaa-guide, chunk-42] requirements."
    cites = extract_citations(text)
    assert len(cites) == 1
    assert cites[0].doc_name == "hipaa-guide"
