# RAG Lifecycle - telco-rag-rs

## 1. Ingestion Pipeline Responsibilities

### 1.1 Document Ingestion Flow
The ingestion pipeline runs when documents are added or updated in the knowledge base. It transforms raw telecom documents into searchable, indexed units.

```
Document Source --> Loader --> Text Normalization --> Metadata Extraction --> Validation --> Chunking --> Embedding Generation --> Vector Store --> Idempotency Check
```

### 1.2 Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **Parser** | Extract text and tables from source formats (Markdown, PDF, HTML, DOCX, CSV). Preserve headings, table structures, and key formatting. |
| **Normalizer** | Clean and standardize content: remove boilerplate, headers/footers, normalize whitespace, character encoding detection and conversion. |
| **Chunker** | Split content into retrievable units using selected strategy (fixed-size, recursive/structure-aware, semantic, table-aware, parent-child). Preserve context between adjacent chunks. |
| **Metadata processor** | Attach source metadata: document_id, title, source_type, domain, product, version, effective_from date, language, tags. Validate schema and flag violations. |
| **Embedding model** | Convert chunk text into vector representations. Abstract provider behind trait (OpenAI, HuggingFace, mock for testing). Store dimensionality and model identifier with each chunk. |
| **Indexing layer** | Store vectors in pgvector with associated metadata. Create HNSW index for cosine similarity search. Store searchable text for BM25 lexical search. Support incremental updates and change detection. |

### 1.3 Idempotency & Incremental Ingestion
- **Hash-based deduplication**: Compute SHA-256 content hash per document. Skip ingestion if hash already exists in state store.
- **Change detection**: Compare `effective_from` dates and content hashes to detect modifications. Update vector store with delta changes only.
- **Dead-letter queue**: Failed documents routed to DLQ with retry configuration (max attempts, exponential backoff). Manual review interface for problematic documents.

### 1.4 Exit Criteria - Stage 1
- Can explain the complete ingestion pipeline from document source to searchable index
- Understands each component's responsibility and interdependencies
- Can describe idempotency mechanisms and change detection strategies

## 2. Query Pipeline Responsibilities

### 2.1 Query Processing Flow
The query pipeline runs for every user query, transforming a natural language question into a grounded answer with citations.

```
User Question --> API and Authentication --> Query Understanding --> Hybrid Retrieval --> Metadata and ACL Filters --> Reranking --> Context Builder --> LLM Generation --> Answer Validation --> Observability --> Answer + Citations
```

### 2.2 Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **API layer** | Accepts queries via `POST /query`, validates request format, rate limiting, authentication middleware |
| **Authentication** | Identifies the support agent/service, JWT validation, RBAC checks, tenant isolation |
| **Query understanding** | Rewrites or classifies ambiguous questions, detects question category (product features, billing, troubleshooting, policy, unanswerable), extracts entities (product codes, identifiers) |
| **Hybrid retrieval** | Combines dense semantic search (pgvector cosine similarity) and sparse lexical search (BM25 via PostgreSQL full-text). Uses Reciprocal Rank Fusion (RRF) to merge results. Default top-K: 50 candidates, rerank to top 5. |
| **Metadata and ACL filtering** | Pre-filter by: domain, product, version, language, classification. Prevents unauthorized document access. Post-retrieval access control checks. |
| **Reranker** | Cross-encoder re-ranking of top N results (typically 20→5). Improves relevance ordering. Adds latency and cost but significantly improves answer quality. |
| **Context builder** | Selects evidence within the model's token budget (typically 300-800 tokens for context). Orders chunks by relevance. Extracts citations. Handles context truncation strategy. |
| **LLM generator** | Produces natural-language response using constructed prompt (system instruction + retrieved context + user question). Supports multiple providers (OpenAI, Anthropic, mock). Returns structured output with answer, sources, grounded flag. |
| **Answer validator** | Checks citations accuracy, format compliance, grounding requirements. Validates that all cited sources actually support the answer claims. Flags issues for human review. |
| **Observability** | Records latency at each stage, error rates, quality signals (groundedness, citation correctness, tokens used), metric labels (model, provider, stage, question_category). OpenTelemetry integration. |

### 2.3 End-to-End Example: Fiber 500 Upload Speed

#### Step 1: Query
The support agent submits the question through the API:
```
POST /query
{
  "question": "What is the upload speed of Fiber 500?",
  "agent_id": "agent-123"
}
```

#### Step 2: Retrieval
The system searches product documentation and retrieves relevant chunks:

```
Retrieved evidence:
- Document: CAT-FIBER-500
- Chunk ID: chunk-03
- Content: "Fiber 500 provides download speeds up to 500 Mbps and upload speeds up to 100 Mbps."
- Similarity score: 0.94 (cosine similarity)
- BM25 score: 0.87
- Combined (RRF) score: 4.21
```

#### Step 3: Context assembly
The relevant chunk and its source metadata are added to the LLM prompt:

```
System Instruction: You are a telco support assistant. Answer the user's question using only the provided context. If the context does not contain the answer, state that the information is unavailable. Provide source citations for all claims.

Retrieved Context:
Document: CAT-FIBER-500, "Fiber 500 Service"
Chunk: chunk-03
Content: "Fiber 500 provides download speeds up to 500 Mbps and upload speeds up to 100 Mbps."

User Question: What is the upload speed of Fiber 500?
```

#### Step 4: Generation
The LLM answers using the supplied evidence:

```
Answer: Fiber 500 provides upload speeds of up to 100 Mbps.

Sources:
- CAT-FIBER-500, chunk-03

Grounded: true
```

#### Step 5: Answer validation
The system validates that:
- All answer claims are supported by retrieved citations
- Citations accurately reference document_id and chunk_id
- Format matches expected schema
- No hallucinated information included

#### Step 6: Response
```
{
  "answer": "Fiber 500 provides upload speeds of up to 100 Mbps.",
  "sources": [
    {
      "document_id": "CAT-FIBER-500",
      "chunk_id": "chunk-03"
    }
  ],
  "grounded": true,
  "confidence": 0.92
}
```

### 2.4 What Happens When Retrieval Fails

#### Example Question: "Does Fiber 500 include free installation in my neighborhood?"

The knowledge base may contain product details but no neighborhood-specific installation information.

#### Correct Behavior:
1. **Retrieve** the available product documentation (Fiber 500 specs, general installation procedures)
2. **Determine** that the evidence does not answer the location-specific question
3. **Avoid** inventing an installation offer (hallucination prevention)
4. **Explain** that the information is unavailable based on current knowledge
5. **Direct** the agent to an authorized service-availability or pricing system if needed

#### Rationale:
- A production system should not force an answer simply because the LLM can generate one
- Abstention is a core RAG concept when retrieval confidence is insufficient
- Better to direct to correct system than provide potentially wrong information

### 2.5 Architecture Trade-offs & Initial Decisions

| Decision | Trade-off | Initial Decision |
|----------|-----------|------------------|
| **Small vs. large chunks** | Precision vs. context completeness | **Small chunks (512 tokens)** for telecom domain. Product codes and technical identifiers benefit from precise matching, while larger context may be needed for troubleshooting procedures. Start small, evaluate Recall@K, adjust if needed. |
| **Dense vs. hybrid retrieval** | Semantic matching vs. exact terminology | **Hybrid retrieval (RRF + reranking)** for telecom. Questions contain both natural language ("upload speed") and exact identifiers ("Fiber 500", "ONT", "GPON"). Hybrid ensures both semantic relevance and exact terminology matching. |
| **More retrieved chunks vs. reranking** | Better recall vs. more noise and tokens / Better relevance vs. additional latency and cost | **Retrieve top 50, rerank to top 5** using cross-encoder. More chunks increase recall risk of noise; reranking improves precision at cost of latency (~50-100ms per query) and rerank model cost. Initial decision favors quality over speed for customer-facing support. |

### 2.6 Component Mapping to Modular Rust Services

```rust
// Core traits (defined in telco-rag-domain, implemented in respective crates)

pub trait Retriever {
    async fn retrieve(
        &self,
        query: &str,
    ) -> Result<Vec<RetrievedChunk>, RetrievalError>;
}

pub trait Reranker {
    async fn rerank(
        &self,
        query: &str,
        chunks: Vec<RetrievedChunk>,
    ) -> Result<Vec<RetrievedChunk>, RerankError>;
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

// Service composition in telco-rag-application

pub struct QueryPipeline {
    retriever: Box<dyn Retriever>,
    reranker: Box<dyn Reranker>,
    generator: Box<dyn AnswerGenerator>,
    validator: Box<dyn AnswerValidator>,
    observability: OpenTelemetry,
}
```

### 2.7 Exit Criteria - Stage 1 (Expanded)
You should be able to explain:
- Why ingestion and query processing are separate pipelines (different timing, different responsibilities, independent scaling)
- How documents become searchable (loader → normalizer → chunker → embedding → indexing)
- How retrieved chunks become LLM context (retrieval → reranking → context builder → prompt construction)
- Why citations and abstention are necessary (traceability, hallucination prevention, user trust)
- Why retrieval and generation need independent evaluation (different failure modes, different metrics, different improvement levers)
- How the components map to modular Rust services (trait-based architecture, independent deployment, testable boundaries)