"""Unified document loader dispatcher."""

from pathlib import Path

from domainmind.data.loaders.text_loader import load_text
from domainmind.data.models import RawDocument

LOADERS: dict = {
    ".txt": load_text,
    ".md": load_text,
}


def _register_optional_loaders() -> None:
    try:
        from domainmind.data.loaders.pdf_loader import load_pdf
        LOADERS[".pdf"] = load_pdf
    except ImportError:
        pass
    try:
        from domainmind.data.loaders.docx_loader import load_docx
        LOADERS[".docx"] = load_docx
    except ImportError:
        pass
    try:
        from domainmind.data.loaders.html_loader import load_html
        LOADERS[".html"] = load_html
        LOADERS[".htm"] = load_html
    except ImportError:
        pass


_register_optional_loaders()


def load_document(path: str | Path) -> RawDocument:
    path = Path(path)
    suffix = path.suffix.lower()
    loader = LOADERS.get(suffix)
    if loader is None:
        raise ValueError(f"Unsupported file type: {suffix}")
    return loader(path)
