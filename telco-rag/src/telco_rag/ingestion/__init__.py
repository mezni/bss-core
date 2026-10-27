"""Telecom document ingestion."""

from telco_rag.ingestion.loader import load_documents
from telco_rag.ingestion.models import Document
from telco_rag.ingestion.parser import (
    DocumentParseError,
    parse_document,
    parse_document_file,
)

__all__ = [
    "Document",
    "DocumentParseError",
    "load_documents",
    "parse_document",
    "parse_document_file",
]
