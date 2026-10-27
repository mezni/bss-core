"""Domain models for document ingestion."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Document:
    """A validated source document ready for downstream processing."""

    document_id: str
    title: str
    document_type: str
    content: str
    metadata: dict[str, Any]
    source_path: str
