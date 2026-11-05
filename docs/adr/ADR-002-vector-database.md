# ADR-002: Vector Database Selection

## Status
Accepted

## Context
The telco-rag-rs project needs a vector database to store chunk embeddings and perform similarity search. The choice must balance retrieval quality, metadata filtering capabilities, operational complexity, and migration path. The system will initially handle ~10K document chunks growing to potentially 100K+ as the knowledge base expands.

## Decision
Start with **PostgreSQL + pgvector** as the recommended starting point.

### Rationale
- **Relational data and vectors together**: Schemas, metadata, and vectors in one database eliminates need for separate data synchronization
- **Metadata filtering and SQL**: Native SQL `WHERE` clauses filter by domain, product, version, language, access scope alongside vector similarity
- **Transactions and mature backup ecosystem**: Point-in-time recovery, familiar backup strategies, no separate infrastructure to operate
- **Good for first production implementation**: Sufficient for ~10K-50K chunks, covers Stage 1-7 evaluation requirements
- **Trait-based abstraction**: Rust repository interfaces hide implementation, enabling migration without domain model changes

### Migration Path
When benchmarks or operational requirements justify, migrate to dedicated vector database:

| Trigger | Target System |
|---------|--------------|
| pgvector performance below requirements (latency/throughput) | Qdrant or Weaviate |
| Need for advanced indexing (beyond HNSW) | Qdrant |
| Requirement for distributed search across clusters | Weaviate |
| Significant cost savings from specialized hardware | Platform-specific options |

### Rust Abstraction
Keep the database behind Rust repository interfaces:

```rust
pub trait ChunkRepository {
    async fn find_similar(
        &self,
        query_embedding: &[f32],
        k: usize,
        filters: &ChunkFilter,
    ) -> Result<Vec<RetrievedChunk>, RepositoryError>;
    
    async fn save(&self, chunk: &EmbeddedChunk) -> Result<(), RepositoryError>;
    async fn update(&self, chunk: &EmbeddedChunk) -> Result<(), RepositoryError>;
    async fn delete(&self, chunk_id: &Uuid) -> Result<(), RepositoryError>;
}
```

## Alternatives Considered

### Qdrant
- **Pros**: Purpose-built vector search, payload filtering, advanced indexing, strong hybrid search capabilities
- **Cons**: Additional service to operate, separate infrastructure, data synchronization layer, learning curve
- **Verdict**: Strong option when vector retrieval becomes a dedicated scaling concern (Stage 8+)

### Weaviate
- **Pros**: Vector-first architecture, hybrid search capabilities, schema and metadata management, GraphQL/REST API
- **Cons**: Operational complexity, separate cluster, less familiar SQL-based workflows
- **Verdict**: Another option for a dedicated retrieval platform when scale justifies

### Elasticsearch
- **Pros**: Mature lexical search (BM25), BM25 and vector search, good for large-scale search workloads
- **Cons**: Additional operational complexity, JSON-document model vs. relational, less efficient vector operations compared to pgvector for moderate scales
- **Verdict**: Useful when lexical search is primary workload and vector search is secondary

## Consequences

### Positive
- **Single database**: No separate infrastructure initially, simpler ops, lower cost
- **SQL everywhere**: Queries can filter by metadata and perform vector search in same statement
- **Transaction safety**: Vector updates and metadata changes in same transaction
- **Familiar developer experience**: Rust developers know PostgreSQL, pgvector
- **Migration delayable**: Trait-based abstraction means swap later without domain model changes

### Negative
- **Scale limitations**: pgvector may not meet requirements at very large scale (100K+ chunks, high QPS)
- **Indexing**: HNSW index build time, parameter tuning required
- **Feature gap**: Missing some advanced vector search features (faceted search, geo, etc.) of dedicated systems

## Related ADRs
- ADR-001: Advanced RAG architecture
- ADR-003: Embedding provider abstraction
- ADR-004: Hybrid retrieval with RRF

## Status Timeline
- Stage 4 (Embeddings): Implement pgvector storage and similarity search
- Stage 5 (Hybrid retrieval): Add BM25 full-text search alongside pgvector
- Stage 6-7: Tune HNSW parameters, measure Recall@K
- Stage 8+: Evaluate migration triggers, migrate if required