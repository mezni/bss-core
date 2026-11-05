# ADR-001: Advanced RAG Architecture

## Status
Accepted

## Context
The telco-rag-rs project needs to select a RAG architecture that balances retrieval quality, operational complexity, and production readiness for a telecommunications support platform. The architecture must handle product specifications, billing policies, troubleshooting procedures, and technical documentation while providing grounded answers with citations.

## Decision
Select **Advanced RAG** as the foundation architecture, not Naive RAG. This includes:

- Hybrid retrieval (dense + sparse combined via RRF)
- Reranking with cross-encoder
- Metadata and ACL filtering within retrieval boundary
- Context budgeting and groundedness validation
- Citation verification and abstention logic
- Separate ingestion and query pipelines with staged publication

## Alternatives Considered

### Naive RAG (Architecture A)
- **Verdict**: Build as experimental baseline only, not production foundation
- **Reason**: Weak handling of ambiguous queries, no sophisticated ranking, limited retrieval optimization. Suitable for experimentation but insufficient for customer-facing telecom support where answer correctness is critical.

### Agentic RAG (Architecture C)
- **Verdict**: Defer to Stage 7+ after baseline reliability is established
- **Reason**: More difficult to control, more expensive, more latency, greater security and evaluation requirements. Only consider after deterministic RAG pipeline has measurable quality.

### Advanced RAG (Selected)
- **Verdict**: Foundation of initial production-oriented system
- **Reason**: Better retrieval quality, better handling of telecom terminology (exact product codes + natural language), more control over relevance, easier to evaluate individual stages.

## Consequences

### Positive
- **Measurable quality**: Each stage (retrieval, reranking, context assembly) can be independently evaluated
- **Telecom suitability**: Hybrid search handles both semantic meaning ("my internet is not working") and exact identifiers ("CAT-FIBER-500", "GPON", "LOS")
- **Operability**: ACL filtering enforced within retrieval boundary, prevents unauthorized document exposure
- **Observability**: Each component emits metrics (latency, retrieval quality, grounding scores)
- **Migration path**: Trait-based abstractions allow vector database or LLM provider swaps

### Negative
- **More components**: Hybrid retrieval + reranking + context budgeting + ACL filtering increases operational complexity
- **Additional latency**: Reranking step adds ~50-100ms per query (measurable and tunable)
- **Implementation overhead**: More code to maintain, more configuration options
- **Cost**: Additional embedding and reranker calls per query

## Related ADRs
- ADR-002: Vector database selection (PostgreSQL + pgvector)
- ADR-003: Embedding provider abstraction
- ADR-004: Hybrid retrieval with RRF
- ADR-005: Reranking strategy

## Status Timeline
- Stage 4-5 (Embeddings + Retrieval): Implement hybrid retrieval with RRF
- Stage 6 (Generation): Implement context budgeting, citation format
- Stage 7 (Evaluation): Measure retrieval quality per architecture component
- Stage 8+: Consider Agentic RAG if baseline quality insufficient