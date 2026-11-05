# Retrieval Strategy - telco-rag-rs

## 4.1 Embeddings and Vector Search - Stage 4

### 4.1.1 Embedding Concepts
- **Embeddings**: Vector representations of text capturing semantic meaning
- **Dense vectors**: Typically 384-1536 dimensions, cosine similarity metric
- **Normalization**: Unit-normalized vectors for cosine similarity = dot product
- **Model selection**: Trade-off between dimension, quality, and latency

### 4.1.2 Similarity Measures
| Metric | Formula | Use Case |
|--------|---------|----------|
| Cosine similarity | `cos(θ) = (A·B) / (||A|| ||B||)` | Default for semantic search |
| Dot product | `A·B` | Normalized vectors only |
| Euclidean distance | `||A-B||` | Less common, requires normalization |

### 4.1.3 Vector Index Types
| Index | Type | Trade-Off |
|-------|------|-----------|
| HNSW | Hierarchical Navigable Small World | High recall, moderate latency, build cost |
| IVF | Inverted File Index | Low latency, lower recall, high build cost |
| Flat | Exhaustive scan | 100% recall, high query latency |

### 4.1.4 pgvector Implementation
- Store embeddings as `vector(384)` or `vector(768)` column
- Index creation: `CREATE INDEX ON embeddings USING hnsw (embedding vector_cosine_ops)`
- Metadata filtering: `WHERE domain = 'fiber_broadband' AND effective_from <= current_date`
- Query: `ORDER BY embedding <=> query_embedding LIMIT 20`

### 4.1.5 Embedding Model Versioning
- Model identifier stored with each batch
- Re-indexing strategy when model changes
- Backward compatibility for hybrid search with old embeddings

## 4.2 Hybrid Search and Reranking - Stage 5

### 4.2.1 Sparse Lexical Search (BM25)
- **Inverted index**: Term → document mapping with frequencies
- **BM25**: Best Matching 25, parameterized by `k1` and `b`
- **Strengths**: Exact term matching, product code identifiers, numeric values
- **Weaknesses**: Struggles with synonyms, natural language questions

### 4.2.2 Dense Semantic Search
- **Embedding-based**: Query embedding → vector similarity
- **Strengths**: Synonyms, conceptual matching, natural language
- **Weaknesses**: May miss exact product codes, technical identifiers

### 4.2.3 Hybrid Retrieval Strategies

#### 4.2.3.1 Reciprocal Rank Fusion (RRF)
```
RRF score = Σ (1 / (rank + k))
where k = 60 (typical constant)
Combines ranks from multiple systems without normalization
```

#### 4.2.3.2 Weighted Linear Combination
```
Final score = α * dense_score + (1-α) * sparse_score
Requires score normalization, more tuning
```

#### 4.2.3.3 Cascade Retrieval
1. Dense retrieval first (broad coverage)
2. BM25 rerank (exact matching)
3. Final merge with reranking

### 4.2.4 Cross-Encoder Reranking
- **Bi-encoder**: Fast, retrieves top 50-100 candidates
- **Cross-encoder**: Precise scoring of query-document pairs
- Re-rank top N (e.g., 20) using cross-encoder
- Context window limits apply

### 4.2.5 Query Expansion and Rewriting
- **Automatic query expansion**: Add related terms, synonyms
- **LLM-based rewriting**: Rewrite user question for better retrieval
- **Query augmentation**: Add domain context, product identifiers

### 4.2.6 Metadata and Access-Control Filtering
- Pre-filter by: `domain`, `product`, `version`, `language`, `classification`
- Filter after retrieval: Apply access control checks
- Balance between recall and precision

### 4.2.7 Multi-Query Retrieval
- Generate multiple query variants from single user question
- Retrieve for each variant separately
- Combine results with RRF

### 4.2.8 Contextual Compression
- Post-retrieval compression using LLM
- Extract key sentences, remove redundancy
- Preserve citations and source references

## 4.3 Retrieval Evaluation Metrics

### 4.3.1 Recall@K
- Percentage of relevant documents in top K results
- Telecom typical: Recall@10, Recall@20

### 4.3.2 Precision@K
- Percentage of retrieved documents that are relevant

### 4.3.3 Mean Reciprocal Rank (MRR)
- Average of reciprocal ranks of first relevant document

### 4.3.4 NDCG (Normalized Discounted Cumulative Gain)
- Graded relevance assessment
- Positions of highly relevant items matter more

### 4.3.5 Retrieval Reasoning
- Document why a chunk was retrieved
- Show embedding similarity score
- Show BM25 score
- Display rerank result

## 4.4 Exit Criteria - Stages 4-5
- Can explain why a chunk was retrieved using measured results
- Can tune retrieval parameters (top K, fusion coefficient, rerank count)
- Recall@K measured on telecom question dataset
- Can compare dense-only, BM25-only, hybrid, and reranked retrieval results
- Justification of retrieval strategy using data, not intuition