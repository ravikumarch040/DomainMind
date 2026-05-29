"""Citation extraction from LLM responses."""

import re
from dataclasses import dataclass

SOURCE_PATTERN = re.compile(r"\[SOURCE:\s*([^,\]]+),\s*([^\]]+)\]")


@dataclass
class Citation:
    doc_name: str
    chunk_id: str
    url: str | None = None


def extract_citations(text: str, source_map: dict[str, str] | None = None) -> list[Citation]:
    source_map = source_map or {}
    citations = []
    for match in SOURCE_PATTERN.finditer(text):
        doc_name = match.group(1).strip()
        chunk_id = match.group(2).strip()
        key = f"{doc_name}:{chunk_id}"
        citations.append(
            Citation(
                doc_name=doc_name,
                chunk_id=chunk_id,
                url=source_map.get(key),
            )
        )
    return citations
