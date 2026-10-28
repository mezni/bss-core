"""Document chunking utilities."""

from telco_rag.chunking.splitter import (
    Chunk,
    chunk_documents,
    chunk_text,
)

__all__ = ["Chunk", "chunk_documents", "chunk_text"]
