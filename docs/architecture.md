# Architecture Overview - telco-rag-rs

## 3.1 Architecture Philosophy
**Architecture-first approach**: Understand → Design → Implement → Evaluate → Operate → Defend

The system follows a staged delivery approach where each stage builds upon the previous one, with documentation maintained at every step.

## 3.2 High-Level Architecture

```
+---------------------+      +----------------------+      +----------------------+
|   API Layer (Axum)  | <--> |  Application Services| <--> |  Infrastructure Layer |
+---------------------+      +----------------------+      +----------------------+
        |                           |                             |
        |                           |                             |
        v                           v                             v
+---------------------+      +----------------------+      +----------------------+
|  Request Validation |      |  Query Orchestration|      |  Vector Store (pgvector)|
+---------------------+      +----------------------+      +----------------------+
        |                           |                             |
        |                           |                             |
        v                           v                             v
+---------------------+      +----------------------+      +----------------------+
|  Ingestion Pipeline | ---> |  Retrieval Engine   | ---> |  Embedding Provider   |
+---------------------+      +----------------------+      +----------------------+
```

## 3.3 Component Diagram

### 3.3.1 API Layer (Stage 6+)
- **Framework**: Axum (Rust HTTP)
- **Endpoints**:
  - `POST /query` - Ask a question, get grounded answer with citations
  - `POST /ingest` - Trigger document ingestion pipeline
  - `GET /health` - Health check
  - `GET /metrics` - Prometheus metrics
- **Authentication**: JWT + RBAC (Stage 9)
- **Rate limiting**: Per-tenant (Stage 8)

### 3.3.2 Application Services (Stage 6+)
- **Query Service**: Orchestrates retrieval → reranking → generation
- **Ingestion Service**: Coordinates document loading → chunking → embedding → storage
- **Evaluation Service**: Runs metrics against golden datasets

### 3.3.3 Ingestion Pipeline (Stage 3)
```
Input Documents --> Loaders --> Text Normalization --> Metadata Extraction --> Chunking --> Embeddings --> Vector Store
```

### 3.3.4 Retrieval Engine (Stage 5)
- **Dense retrieval**: pgvector cosine similarity
- **Sparse retrieval**: BM25 via PostgreSQL full-text search
- **Hybrid**: Reciprocal Rank Fusion (RRF) combining both
- **Reranking**: Cross-encoder re-ranking of top N results
- **Metadata filtering**: Domain, product, version, language filters

### 3.3.5 Generation Orchestration (Stage 6)
- **Prompt construction**: System instruction + retrieved context + user question
- **Context budgeting**: Token limit management, truncation strategy
- **Citation extraction**: Map answer references back to source chunks
- **Groundedness check**: Verify answer is supported by evidence
- **Abstention**: Return "I don't know" when confidence is insufficient

## 3.4 Data Flow - Query Path

1. **User submits question** via `POST /query`
2. **Request validation**: Question category, authentication, rate limits
3. **Query expansion** (optional): Rewrite question for better retrieval
4. **Dense retrieval**: Embed question, search pgvector for similar chunks
5. **Sparse retrieval**: BM25 search on text content
6. **Hybrid fusion**: RRF to combine dense + sparse results
7. **Reranking**: Cross-encoder re-rank top 20 → top 5
8. **Metadata filtering**: Apply domain/product filters
9. **Context selection**: Select top K chunks, respect token budget
10. **Prompt construction**: System prompt + context + question
11. **LLM call**: Generate grounded answer with citations
12. **Response formatting**: Answer, sources, grounded flag

## 3.5 Data Flow - Ingestion Path

1. **Document upload** or **source trigger**
2. **Loader**: Parse format (Markdown, PDF, HTML, etc.)
3. **Text normalization**: Remove boilerplates, headers, footers
4. **Metadata extraction**: Parse document_id, domain, product, version
5. **Chunking**: Split into searchable units (strategy-dependent)
6. **Embedding generation**: Call embedding provider API
7. **Vector storage**: Insert into pgvector with metadata
8. **Idempotency check**: Hash-based dedup, skip already-ingested

## 3.6 Technology Stack Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| **Language** | Rust | Memory safety, concurrency, performance |
| **Async runtime** | Tokio | Industry standard, mature ecosystem |
| **HTTP framework** | Axum | Simple, composable, built on Tower |
| **Serialization** | Serde | Universal Rust serialization |
| **Database** | PostgreSQL + pgvector | Single source of truth, SQL familiarity, vector support |
| **Lexical search** | PostgreSQL full-text | No extra dependency for initial version |
| **Vector search** | pgvector | Co-located with data, simple API |
| **Embeddings** | Provider API behind trait | Swappable models, abstraction for testing |
| **LLM provider** | Abstraction layer | Provider-agnostic, fallback/routing |
| **Cache** | Redis (Stage 10) | Fast lookback, cost reduction |
| **Observability** | OpenTelemetry + tracing | Standard Rust observability |
| **Testing** | Cargo tests + integration | Rust testing maturity |

## 3.7 Initial Scale Justification
**Start with PostgreSQL + pgvector + lexical search** because:
- Manageable complexity for Stage 1-5
- No separate infrastructure required initially
- Sufficient for ~10K documents, ~100 questions
- Can introduce dedicated vector search (Pinecone/Weaviate) when scale requires

**Migration path**: When embedding dimension, query volume, or relevance requirements exceed pgvector capabilities, migrate to dedicated vector database while keeping Rust code and architecture identical (trait-based abstraction).

## 3.8 Exit Criteria - Stage 1
You can explain:
- When RAG is appropriate vs. traditional search vs. knowledge graphs/fine-tuning
- What data the system needs (document sources, formats, metadata structure)
- How to measure whether answers are trustworthy (groundedness, citation correctness, abstention rate)
- The architectural trade-offs of the chosen technology stack