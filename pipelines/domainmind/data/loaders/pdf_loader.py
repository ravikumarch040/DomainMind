from pathlib import Path

import fitz  # PyMuPDF

from domainmind.data.models import RawDocument


def load_pdf(path: Path) -> RawDocument:
    doc = fitz.open(path)
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    text = "\n\n".join(text_parts)
    return RawDocument(
        text=text,
        source=str(path),
        metadata={"type": "pdf", "pages": len(text_parts)},
        doc_id=path.stem,
    )
