from pathlib import Path

from domainmind.data.models import RawDocument


def load_text(path: Path) -> RawDocument:
    text = path.read_text(encoding="utf-8", errors="replace")
    return RawDocument(
        text=text,
        source=str(path),
        metadata={"type": "text"},
        doc_id=path.stem,
    )
