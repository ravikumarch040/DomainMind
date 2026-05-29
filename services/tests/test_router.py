import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.router import route_query
from orchestrator.citation import extract_citations


def test_route():
    assert route_query("Explain HIPAA") == "rag_combined"


def test_citation():
    cites = extract_citations("See [SOURCE: a, b] here.")
    assert len(cites) == 1
