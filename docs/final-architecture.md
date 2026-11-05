# Final Architecture Decisions - telco-rag-rs

## Overview
This document summarizes the initial architecture baseline for the telco-rag-rs project, following the architecture-first roadmap from Stage 1 through the initial production-oriented system design.

## Architecture Selection
**Architecture Type**: Advanced RAG (not Naive RAG, not Agentic RAG initially)

Rationale: Better retrieval quality, better handling of telecom terminology (exact product codes + natural language), more control over relevance, easier to evaluate individual stages. Defer Agentic RAG until baseline reliability is established.

## Technology Stack

| Area | Decision | Rationale |
|------|----------|-----------|
| **Backend language** | Rust | Memory safety, concurrency, performance, strong type system |
| **Application architecture** | Clean Architecture | Separation of concerns, testable boundaries, independent deployment |
| **HTTP framework** | Axum | Simple, composable, built on Tower, Rust-idiomatic |
| **Async runtime** | Tokio | Industry standard, mature ecosystem, efficient I/O |
| **Database** | PostgreSQL | Single source of truth, SQL familiarity, vector support via pgvector |
| **Vector search** | pgvector | Co-located with data, no separate infrastructure initially, HNSW indexing |
| **Keyword search** | PostgreSQL full-text search | BM25 lexical search alongside vector search, no extra dependency |
| **Ranking fusion** | Reciprocal Rank Fusion (RRF) | Combines dense + sparse without score normalization, proven effective |
| **Reranking** | Cross-encoder abstraction | Improves candidate ordering, adds ~20-50ms latency, measurable quality gain |
| **Embeddings** | Pluggable provider trait | OpenAI, HuggingFace, mock for testing; swap via env var |
| **LLM provider** | Pluggable provider with fallback | OpenAI, Anthropic, mock; cost tracking, provider-agnostic |
| **Cache** | Redis | Fast lookback, cost reduction, query result caching |
| **Background processing** | Async worker architecture | Tokio-based, job queue for ingestion, batch embedding generation |
| **Observability** | OpenTelemetry + tracing | Standard Rust observability, metric labels per stage/provider |
| **Evaluation** | Custom evaluation framework | Golden datasets, deterministic metrics, LLM-as-a-judge, regression testing |
| **Deployment** | Docker initially | Container security, CI/CD pipelines, Kubernetes when scale requires |

## Target Query Architecture

```mermaid
flowchart TB
    Support_Agent[Support Agent] -->|POST /query| Axum_API[Axum API]
    
    %% Authentication
    Axum_API -->|Auth + RBAC| Auth[Authentication + Authorization]
    
    %% Query Understanding
    Auth -->|Query Router| Query_Understanding[Query Understanding]
    
    %% Retrieval Pipeline
    Query_Understanding -->|Classify| Dense_Retrieval[Dense Retrieval: pgvector]
    Query_Understanding -->|Classify| Sparse_Retrieval[Sparse Retrieval: BM25]
    
    RRF[RRF Fusion: Combine Ranks] -->|Reranker| Reranker[Cross-Encoder Reranker]
    
    ACL[ACL + Metadata Validation] -->|Filter| Reranker
    
    Context_Builder[Context Builder] -->|Select within token budget| LLM_Gateway[LLM Gateway]
    
    LLM_Gateway -->|Generate Answer| LLM[LLM Provider]
    
    Answer_Validator[Answer Validator] -->|Check citations, grounding| Response_Formatter[Response Formatter]
    
    Response_Formatter -->|Answer + Citations| Support_Agent
    
    %% Observability
    OpenTelemetry[OpenTelemetry] -->|Metrics + Traces| All_Components[All Components]
    
    Redis_Cache[Redis Cache] -->|Cache lookback| Dense_Retrieval
    Redis_Cache -->|Cache lookback| Sparse_Retrieval
    
    PostgreSQL[PostgreSQL + pgvector] -->|Store vectors + metadata| Dense_Retrieval
    PostgreSQL -->|Store chunks + metadata| Sparse_Retrieval
    Redis_Cache -->|Cache query results| All_Components
    
    Style Definitions
    classDef support fill:#e3f2fd,stroke:#1976d2,stroke-width:2px;
    classDef api fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef retrieval fill:#fff3e0,orsa:#f57c00,stroke-width:2px;
    classDef llm fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px;
    classDef storage fill:#e0f2f1,stroke:#009688,stroke-width:2px;
    classDef observability fill:#fafafa,stroke:#607d8b,stroke-dash:5,5;
```

## Key Design Decisions

### 1. Advanced RAG Over Naive RAG
- **Hybrid retrieval** (dense + BM25 via RRF)
- **Cross-encoder reranking** of top candidates
- **Metadata/ACL filtering** within retrieval boundary
- **Context budgeting** and groundedness validation
- **Citation verification** and abstention logic

### 2. PostgreSQL + pgvector Over Dedicated Vector Database
- **Single database**: No separate infrastructure initially
- **SQL everywhere**: Filter by metadata and vector search in same statement
- **Transaction safety**: Vector updates and metadata changes atomic
- **Familiar developer experience**: Rust developers know PostgreSQL
- **Trait-based abstraction**: Can migrate to Qdrant/Weaviate later without domain model changes

### 3. RRF Over Dense-Only or BM25-Only
- **Combines semantic matching** (natural language questions) **with exact terminology** (product codes, abbreviations)
- **No score normalization needed**: RRF works on ranks only
- **Telecom-specific**: Handles "my internet is not working" + "CAT-FIBER-500" in same pipeline

### 4. Cross-Encoder Reranking Over Dense Similarity Alone
- **Significant relevance improvement**: Especially for technical questions where keyword matching matters
- **Measurable quality gains**: Track via Recall@K, groundedness, MRR on evaluation dataset
- **Incremental cost**: ~20-50ms latency per query, worth it for customer-facing support

### 5. Pluggable Providers (Embeddings + LLM)
- **Testable with mock implementations**: Unit tests use deterministic vectors/calls
- **Swap via environment variable**: No code changes required
- **Cost tracking**: Model and version stored per-batch for attribution
- **Provider-agnostic**: Avoid vendor lock-in, can A/B test different models

### 6. Atomic Publication Over Partial Indexing
- **Never expose partially indexed version** as complete
- **Staged publication**: Build new version in isolation, process all chunks, generate all embeddings, validate, then atomically activate
- **Retire old version** from active retrieval
- **Users never see partial data**: Either new version fully ready, or old version remains active

### 7. Effective Date Management
- **Distinguish**: created_at, published_at, effective_from, effective_until
- **Temporal query logic**: `WHERE effective_from <= current_date AND (effective_until IS NULL OR effective_until >= current_date)`
- **Particularly important for**: Billing policies, promotions, roaming, contractual terms

### 8. Access Control Enforced Before LLM Retrieval
- **LLM must never receive documents** user is not authorized to access
- **Enforcement points**: Pre-retrieval filter, post-retrieval check, LLM input sanitization
- **Prevents**: Information leakage, prompt injection, compliance violations, retrieval poisoning

### 9. Deferred Capabilities (Deliberately Postponed)
| Capability | When to Introduce |
|------------|-------------------|
| Knowledge graphs | When entity relationships justify them |
| Agentic RAG | After baseline retrieval is reliable |
| Multi-agent orchestration | Only for demonstrated multi-step requirements |
| Dedicated vector database | When PostgreSQL benchmarks justify migration |
| Distributed ingestion | When ingestion volume requires it |
| Fine-tuning | When evaluation shows prompting and retrieval insufficient |

## Evaluation Metrics Targets

| Metric | Target (Stage 7) | Measurement Method |
|--------|-----------------|-------------------|
| Recall@10 | ≥ 0.60 | Golden dataset of 100+ telecom questions |
| Groundedness | ≥ 0.80 | LLM-as-judge per answer |
| Citation correctness | ≥ 0.90 | Automatic verification |
| Correct abstention rate | ≥ 0.75 | Unanswerable questions |
| Query latency p95 | ≤ 500ms | OpenTelemetry timing |
| Reranking quality gain | ≥ 15% MRR improvement | A/B test vs. no rerank |

## Rust Domain Model Highlights

```rust
// Core traits (telco-rag-domain crate)

pub trait Retriever {
    async fn retrieve(
        &self,
        query: &str,
        filters: &ChunkFilter,
    ) -> Result<Vec<RetrievedChunk>, RetrievalError>;
}

pub trait Reranker {
    async fn rerank(
        &self,
        query: &str,
        chunks: Vec<RetrievedChunk>,
    ) -> Result<Vec<RerankedChunk>, RerankError>;
}

pub trait AnswerGenerator {
    async fn generate(
        &self,
        request: GenerationRequest,
    ) -> Result<GeneratedAnswer, GenerationError>;
}

pub trait AnswerValidator {
    async fn validate(
        &self,
        answer: &GeneratedAnswer,
        citations: &[Citation],
    ) -> Result<ValidationResult, ValidationError>;
}

// Service composition (telco-rag-application crate)

pub struct QueryPipeline {
    retriever: Box<dyn Retriever>,
    reranker: Box<dyn Reranker>,
    generator: Box<dyn AnswerGenerator>,
    validator: Box<dyn AnswerValidator>,
    observability: OpenTelemetry,
}
```

## Documentation Structure

```
telco-rag-rs/
├── Cargo.toml
├── README.md
├── docs/
│   ├── requirements.md
│├── architecture.md
│   ├── domain-model.md
│   ├── rag-lifecycle.md
│   ├── rag-fundamentals.md
│   ├── retrieval-strategy.md
│   ├── evaluation.md
│   └── adr/
│       ├── ADR-001-rag-architecture.md
│       ├── ADR-002-vector-database.md
│       ├── ADR-003-embedding-provider.md
│       ├── ADR-004-hybrid-retrieval.md
│       └── ADR-005-reranking.md
│   └── (Stage 2-12 docs as project progresses)
├── crates/
│   ├── telco-rag-domain/
│   ├── telco-rag-application/
│   ├── telco-rag-ingestion/
│   ├── telco-rag-retrieval/
│   ├── telco-rag-llm/
│   ├── telco-rag-api/
│   └── telco-rag-evaluation/
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── retrieval/
│   ├── evaluation/
│   └── security/
├── evals/
│   ├── datasets/
│   └── reports/
└── deploy/
    ├── docker/
    └── monitoring/
```

## Next Steps - Stage 2 Startup

1. **Write docs/requirements.md** (already done - Stage 1 complete)
2. **Write docs/domain-model.md** (already done - Stage 1 complete)
3. **Begin Stage 2**: Rust foundations for RAG engineering
   - Ownership and borrowing
   - Structs, enums, traits
   - Generics and trait objects
   - Result, Option, error handling
   - Async Rust and Tokio
   - Streams and channels
   - Serde JSON and configuration
   - Testing and tracing
   - Cargo workspaces modular project structure

4. **Implement Stage 3**: Document ingestion and knowledge engineering
   - Loaders for Markdown, PDF, HTML, DOCX, CSV
   - Text normalization and boilerplate removal
   - Metadata extraction and schema validation
   - Document versioning and content hashing
   - Chunking strategies (structure-aware recommended)
   - Idempotent incremental ingestion

5. **Continue through roadmap** at own pace, re-evaluating architecture decisions at each stage gate.

## Git Commands for This Baseline

```bash
# Add all documentation files
git add docs/ crates/ Cargo.toml

# Commit with descriptive message
git commit -m "telco-rag-rs: add comprehensive Stage 1 documentation and ADRs"

# Push to remote
git push origin main
```

---
*This architecture baseline follows the architecture-first roadmap, with deliberate deferrals to prevent unnecessary complexity. Each decision includes measurable exit criteria and evaluation targets for Stage 7 quality gates.*