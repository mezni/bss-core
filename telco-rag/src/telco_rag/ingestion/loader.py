"""Load a directory of telecom knowledge documents."""

from pathlib import Path

from telco_rag.ingestion.models import Document
from telco_rag.ingestion.parser import (
    DocumentParseError,
    parse_document_file,
)


def load_documents(corpus_dir: Path) -> list[Document]:
    """Load Markdown documents and reject duplicate document IDs."""
    corpus_dir = corpus_dir.resolve()

    if not corpus_dir.is_dir():
        raise FileNotFoundError(f"Corpus directory does not exist: {corpus_dir}")

    documents: list[Document] = []
    seen_ids: set[str] = set()

    for path in sorted(corpus_dir.rglob("*.md")):
        document = parse_document_file(path, corpus_dir)

        if document.document_id in seen_ids:
            raise DocumentParseError(f"Duplicate document_id: {document.document_id}")

        seen_ids.add(document.document_id)
        documents.append(document)

    return documents
