"""Data models for the ingestion pipeline."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RawDocument:
    text: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)
    doc_id: str = ""

    def __post_init__(self) -> None:
        if not self.doc_id:
            self.doc_id = self.source
