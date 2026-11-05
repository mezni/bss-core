# ADR-004: Hybrid Retrieval with Reciprocal Rank Fusion

## Status
Accepted

## Context
The telco-rag-rs project must combine dense semantic search (pgvector cosine similarity) and sparse lexical search (BM25 via PostgreSQL full-text search) into a unified retrieval pipeline. Telecom queries contain both natural language ("my internet is not working") and exact identifiers ("CAT-FIBER-500", "GPON", "ONT", plan codes).

## Decision
Use **Hybrid Retrieval with Reciprocal Rank Fusion (RRF)** as the initial ranking fusion strategy.

### RRF Implementation
```
RRF(d) = Σ (1 / (k + rank_r(d)))
```
where:
- `d`: candidate chunk
- `R`: ranking result sets (dense, sparse)
- `k`: smoothing constant = 60 (standard default)
- `rank_r(d)`: document's position in ranking r

### Pipeline Flow
1. **Dense retrieval**: Query embedding → pgvector cosine similarity → top 50 candidates
2. **Sparse retrieval**: Query text → PostgreSQL BM25 → top 50 candidates
3. **RRF fusion**: Combine ranks from both rankings → compute RRF score for each chunk
4. **Reranking**: Cross-encoder re-rank top N (e.g., 20 → 5) using query-chunk relevance
5. **Metadata filtering**: Apply ACL filters after reranking (or pre-filter if very restrictive)
6. **Context selection**: Select top K within token budget (typically 3-8 chunks)

### Why RRF?
- **No score normalization needed**: Does not require BM25 scores and vector similarity scores to be on the same numerical scale
- **Simple**: Only requires ranks, not raw scores
- **Proven**: Empirically effective for combining heterogeneous retrieval systems
- **Telecom suitability**: Handles both semantic matching and exact terminology identification

### Example from ADR-001 reference table:
```
Chunk   BM25 rank  Dense rank  RRF score (k=60)
A       1          4           1/61 + 1/64 ≈ 0.032
B       3          1           1/63 + 1/61 ≈ 0.033
C       2          3           1/62 + 1/63 ≈ 0.032
D       5          2           1/65 + 1/62 ≈ 0.031
```
Chunk B ranks highest via RRF despite not being #1 in either individual ranking, demonstrating RRF's value in combining signals.

### Candidate Set Size
- **Retrieve**: 50+ candidates from hybrid fusion
- **Rerank**: Top 20 → cross-encoder re-rank
- **Select**: Top 3-8 chunks within token budget (300-800 tokens)
- **Reserve**: Tokens for system prompt + question + answer output

## Alternatives Considered

### Dense-Only Retrieval
- **Pros**: Simpler, lower latency
- **Cons**: Struggles with exact product codes, technical identifiers, abbreviations. Telecom queries mix natural language and codes.

### BM25-Only Retrieval
- **Pros**: Good at exact term matching
- **Cons**: Struggles with synonyms, conceptual matching, natural language questions

### Weighted Linear Combination
- **Pros**: Can weight dense vs sparse based on query type
- **Cons**: Requires score normalization, more tuning, less robust than RRF

## Consequences

### Positive
- **Best of both worlds**: Semantic matching + exact terminology identification
- **Telecom-specific**: Handles "my internet is not working" (semantic) + "CAT-FIBER-500" (exact code)
- **No score normalization**: RRF avoids needing BM25 ⇄ vector similarity conversion
- **Tunable**: Candidate set size, rerank count, k constant all adjustable
- **Measurable**: Can A/B test dense-only vs hybrid vs BM25-only on evaluation dataset

### Negative
- **Additional latency**: Two retrieval calls instead of one (+~20-40ms)
- **Increased complexity**: More components to operate and monitor
- **Reranking dependency**: RRF provides initial ranking, but cross-encoder reranking adds further latency+cost

## Related ADRs
- ADR-001: Advanced RAG architecture
- ADR-002: Vector database selection
- ADR-005: Reranking strategy

## Status Timeline
- Stage 5 (Hybrid retrieval): Implement BM25 + pgvector + RRF fusion
- Stage 5 (Reranking): Implement cross-encoder candidate re-ranking
- Stage 7 (Evaluation): A/B test dense-only vs hybrid vs BM25-only on telecom question dataset
- Stage 7+: Tune candidate set sizes, rerank counts based on measured Recall@K