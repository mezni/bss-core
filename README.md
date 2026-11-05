# telco-rag-rs

Rust implementation of a Retrieval-Augmented Generation (RAG) platform for telecommunications.

## Project Structure

- **Core library** - `src/lib.rs` - Main RAG system implementation
- **Embeddings** - Vector search and similarity using pgvector
- **Document processing** - Ingestion, chunking, and preprocessing pipelines
- **Vector store** - Hybrid search and reranking capabilities
- **Evaluation** - Quality engineering and performance optimization

## Recent Changes

- System requirements and scope definition
- pgvector storage and similarity search implementation
- Document ingestion pipeline
- Embedding generation

## Development

```bash
# Build
cargo build

# Test
cargo test
```