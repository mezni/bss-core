# ADR-003: Embedding Provider Abstraction

## Status
Accepted

## Context
The telco-rag-rs project must select embedding models for semantic search while maintaining flexibility to swap models as quality/cost requirements evolve. Embedding models directly affect retrieval quality, dimensionality, and provider costs. The system must support English telecom documentation, with potential future multilingual support (English/French for Canadian telecom).

## Decision
Implement an **EmbeddingProvider trait** in Rust. The application code must not depend directly on a specific embedding vendor.

### Trait Contract
```rust
pub trait EmbeddingProvider: Send + Sync {
    fn embed(&self, text: &str) -> Result<Vec<f32>, EmbeddingError>;
    fn dimensions(&self) -> usize;
    fn model_name(&self) -> &str;
    fn model_version(&self) -> &str;
    fn supports_multilingual(&self) -> bool;
}
```

### Concrete Implementations
1. **OpenAIEmbedding**: `text-embedding-ada-002` (1536 dimensions, English/multilingual)
2. **OpenAIEmbedding**: `text-embedding-3-large` (3072 dimensions, improved quality)
3. **HuggingFaceEmbedding**: `all-MPNet-base-v2` (768 dimensions, local/offline capable)
4. **HuggingFaceEmbedding**: `all-MiniLM-L6-v2` (384 dimensions, fast, good quality)
5. **MockEmbedding**: Deterministic vectors for unit testing

### Multilingual Considerations
For a Canadian telecom knowledge base, multilingual retrieval deserves particular attention:
- A customer might ask in French while relevant technical documentation is in English
- Do not assume translation or embedding models will handle it correctly
- **Benchmark multilingual retrieval** rather than assume models will handle it
- Consider separate embedding models or translation pipeline if multilingual quality is insufficient

### Provider Configuration
- Environment variable driven: `EMBEDDING_PROVIDER=openai|huggingface|mock`
- Fallback chain: OpenAI → HuggingFace → Mock
- Cost tracking per model per query
- Token usage logging with metric labels

### Why Not Direct Provider Calls Throughout Codebase?
- **Pros**: Simpler initial setup
- **Cons**: Tight coupling, hard to test, no model switching, poor separation of concerns, no cost tracking

### Why Not Single Model Hard-Coded?
- **Pros**: Simplest code
- **Cons**: No experimentation, no A/B testing, locked into provider, no fallback

## Consequences

### Positive
- **Testable with mock embeddings**: Unit tests use deterministic vectors
- **Easy model swapping**: Change `EMBEDDING_PROVIDER` env var, no code changes
- **Provider-agnostic**: Switch OpenAI↔HuggingFace with config change
- **Cost tracking**: Model and version stored per-batch for cost attribution
- **Multilingual ready**: Can swap in multilingual model if benchmarks warrant

### Negative
- **Slightly more initial code**: Trait implementation for each provider
- **Runtime dispatch**: Trait object overhead (negligible compared to embedding computation)
- **Compatibility concern**: Must ensure query and document embeddings use same model/version

## Related ADRs
- ADR-001: Advanced RAG architecture
- ADR-002: Vector database selection
- ADR-005: Reranking strategy

## Status Timeline
- Stage 4 (Embeddings): Implement trait + OpenAI implementation + Mock for testing
- Stage 7 (Evaluation): Measure retrieval quality per model on golden dataset
- Stage 11 (Optimization): Compare costs, switch model if better quality/cost ratio
- Ongoing: Add new embedding implementations as needed, deprecate old models