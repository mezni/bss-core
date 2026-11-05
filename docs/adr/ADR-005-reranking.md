# ADR-005: Reranking Strategy

## Status
Accepted

## Context
Vector retrieval finds candidate chunks but ranks them primarily by similarity score, which may not reflect true relevance to the user's question. Reranking improves the ordering of retrieved candidates using a more precise relevance model.

## Decision
Retrieve a configurable candidate set (initially 20-30 chunks), then rerank using a **cross-encoder** relevance model, then select a smaller evidence set for LLM context.

### Reranking Pipeline
```
1. Hybrid retrieval (RRF) → 50 candidates
2. Cross-encoder re-rank → top 5-8
3. Token budget selection → 3-8 chunks for LLM context
4. Preserve citations for selected chunks
```

### Cross-Encoder Implementation
- **Model**: `ms-marco-MiniLM-L-6-v2` or similar cross-encoder fine-tuned on query-document relevance
- **Input**: `[query, chunk_content]` pair
- **Output**: Relevance score (typically 0-1 or logits)
- **Batch processing**: Score multiple chunks efficiently

### Example from User Story
```
User question: "What causes a red LOS light on my ONT?"

Initial retrieval (dense + RRF):
Chunk           Initial rank
General fiber installation   1
Optical signal troubleshooting 2
ONT device specifications      3
Router Wi-Fi troubleshooting   4

After cross-encoder reranking:
Chunk                           Reranked position
Optical signal troubleshooting  1
ONT device specifications       2
General fiber installation      3
Router Wi-Fi troubleshooting    4
```

**Result**: "Optical signal troubleshooting" moves to #1 because the cross-encoder recognizes it's most relevant to LOS light questions. "Router Wi-Fi troubleshooting" drops to #4 (irrelevant to fiber LOS).

### Candidate Set Size Tuning
- **Initial retrieval**: 50 chunks (dense + BM25 + RRF)
- **Rerank**: Top 20 cross-encoded
- **Select**: Top 3-8 within token budget
- **Token budget**: ~300-800 tokens for context (varies by LLM model)
- **Reserve**: Tokens for system prompt + user question + answer output

### Why Not Rerank All Candidates?
- **Cost**: Cross-encoder calls scale with candidate count
- **Latency**: More chunks = more model inference time
- **Diminishing returns**: Quality gains taper off after ~20-30 reranked items

### Why Not Use Dense Similarity Score Alone?
- Vector similarity is fast but coarse
- Cannot capture query-chunk semantic alignment as precisely as cross-encoder
- Reranking step is worth the incremental cost for customer-facing support

## Consequences

### Positive
- **Significant relevance improvement**: Reranking typically improves MRR and groundedness scores
- **Telecom suitability**: Correctly prioritizes technical troubleshooting chunks over general product descriptions
- **Measurable**: Can track rerank quality per question category
- **Tunable**: Candidate set size, model choice, selection count all adjustable based on evaluation

### Negative
- **Additional latency**: Cross-encoder inference per query (~20-50ms depending on model)
- **Additional cost**: Reranker model call per query (typically cheaper than LLM but not free)
- **More components**: One more step in the pipeline to operate and monitor
- **Model dependence**: Reranker quality depends on chosen model and fine-tuning

## Related ADRs
- ADR-001: Advanced RAG architecture
- ADR-004: Hybrid retrieval with RRF (feeds into reranking)
- ADR-003: Embedding provider abstraction

## Status Timeline
- Stage 5 (Retrieval): Implement cross-encoder reranking after RRF fusion
- Stage 5-6: Tune candidate set sizes (50 retrieved → 20 reranked → 8 selected)
- Stage 7 (Evaluation): Measure impact on Recall@K, groundedness, answer quality
- Stage 7+: A/B test different cross-encoder models, adjust based on metrics
- Production: Monitor reranking latency/cost, set budgets/alerts