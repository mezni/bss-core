"""Embedding generation interfaces and providers."""

from telco_rag.embeddings.provider import (
    EmbeddedChunk,
    OpenAIEmbeddingProvider,
)

__all__ = ["EmbeddedChunk", "OpenAIEmbeddingProvider"]
