from pathlib import Path

import pytest

from telco_rag.ingestion import (
    DocumentParseError,
    load_documents,
    parse_document,
)

CORPUS_DIR = Path("data/synthetic")


def test_parse_valid_document() -> None:
    text = """---
document_id: TEST-001
title: Test Document
document_type: troubleshooting_runbook
version: "1.0"
status: active
access_level: internal
source_type: synthetic
domain: broadband
---

# Troubleshooting

Check the gateway connection.
"""

    document = parse_document(text, "test.md")

    assert document.document_id == "TEST-001"
    assert document.title == "Test Document"
    assert document.metadata["domain"] == "broadband"
    assert document.content.startswith("# Troubleshooting")
    assert document.source_path == "test.md"


def test_reject_document_without_front_matter() -> None:
    with pytest.raises(DocumentParseError, match="front matter"):
        parse_document("# No metadata\nSome content.")


def test_reject_missing_required_metadata() -> None:
    text = """---
document_id: TEST-002
title: Missing Version
---

Some content.
"""

    with pytest.raises(DocumentParseError, match="version"):
        parse_document(text)


def test_reject_empty_document_content() -> None:
    text = """---
document_id: TEST-003
title: Empty Document
document_type: runbook
version: "1.0"
status: active
access_level: internal
source_type: synthetic
---
"""

    with pytest.raises(DocumentParseError, match="content"):
        parse_document(text)


def test_load_synthetic_corpus() -> None:
    documents = load_documents(CORPUS_DIR)

    assert len(documents) == 6
    assert len({doc.document_id for doc in documents}) == 6


def test_loaded_documents_have_relative_source_paths() -> None:
    documents = load_documents(CORPUS_DIR)

    assert all(doc.source_path.endswith(".md") for doc in documents)
    assert all(not Path(doc.source_path).is_absolute() for doc in documents)
