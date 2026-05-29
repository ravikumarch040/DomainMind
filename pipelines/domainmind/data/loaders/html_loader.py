from pathlib import Path

from bs4 import BeautifulSoup

from domainmind.data.models import RawDocument


def load_html(path: Path) -> RawDocument:
    html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    return RawDocument(
        text=text,
        source=str(path),
        metadata={"type": "html"},
        doc_id=path.stem,
    )
