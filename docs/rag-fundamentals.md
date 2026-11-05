# RAG Fundamentals - telco-rag-rs

## 1. The RAG Knowledge Hierarchy

### 1.1 Document → Chunk → Embedding → Index

The RAG knowledge hierarchy transforms source documents into searchable units:

```
Document
├── Fiber 500 Product Specification
├── Billing Policy v2026
├── Fiber LOS Troubleshooting Guide

→ Chunks (searchable units)
│   ├── Chunk 1: Product overview (title + key specs)
│   ├── Chunk 2: Download and upload speeds
│   ├── Chunk 3: Installation requirements
│   └── Chunk 4: Troubleshooting steps 1-3

→ Embeddings (numeric representation)
│   ├── Vector d=384 (or 768/1536) for each chunk
│   ├── Semantic space: similar meaning → close vectors
│   └── Generated during ingestion by embedding model

→ Search index
│   ├── Vectors (pgvector column)
│   ├── Text content (for BM25 lexical search)
│   ├── Metadata (document_id, version, domain, etc.)
│   └── Source references (for citations)
```

**Key principle**: The fundamental retrieval unit is usually a **chunk**, not an entire document. Chunks allow precise matching and reduce noise from irrelevant document sections.

### 1.2 Why This Hierarchy Matters
- **Documents** provide stable identity and versioning
- **Chunks** enable granular retrieval and reduce context noise
- **Embeddings** enable semantic search across chunk boundaries
- **Index** enables fast similarity search with metadata filtering

## 2. What is a Document?

### 2.1 Document Definition
A document is the original knowledge source or a logical record derived from it. Documents should have:
- Stable identity (`document_id`)
- Version tracking (`effective_from`, `version`)
- Source type classification
- Domain categorization

### 2.2 Document Examples

| Document Type | Example | document_id Pattern |
|--------------|---------|---------------------|
| Product catalog entry | Fiber 500 service spec | `CAT-FIBER-500` |
| Billing policy | Roaming charge policy | `POL-BILL-ROAMING` |
| Troubleshooting procedure | Fiber LOS red light guide | `TRBL-FIBER-LOS` |
| Technical manual | ONT installation guide | `TM-ONT-SETUP` |
| FAQ article | Billing question answers | `FAQ-BILLING-01` |

### 2.3 Document Metadata Schema

```json
{
  "document_id": "CAT-FIBER-500",
  "title": "Fiber 500 Product Specification",
  "source_type": "product_catalog",
  "domain": "fiber_broadband",
  "version": "3",
  "effective_from": "2026-01-01",
  "language": "en"
}
```

### 2.4 Why Metadata Matters

Metadata is not just descriptive information—it's part of **retrieval correctness** and **access control**:

| Use Case | Metadata Filter |
|----------|----------------|
| Retrieve only fiber broadband docs | `domain = 'fiber_broadband'` |
| Exclude expired policies | `effective_from <= current_date` |
| Restrict internal procedures | `classification = 'internal'` + RBAC check |
| Prefer current product spec | Sort by `effective_from` desc, pick newest |
| Trace answer back to source | `document_id` + `chunk_id` in citations |

**Important**: Without proper metadata, you lose the ability to:
- Filter by product domain or version
- Enforce access control policies
- Provide accurate source citations
- Detect and prevent retrieval poisoning
- Support versioned document retrieval

## 3. What is a Chunk?

### 3.1 Chunk Definition
A chunk is a segment of a document indexed independently. Chunks are the fundamental retrieval unit and should be understandable when retrieved independently (without context from other chunks).

### 3.2 Example Source Document

```
Fiber 500 Service

Download speed: Up to 500 Mbps.
Upload speed: Up to 100 Mbps.
Technology: FTTH.
Installation requires a compatible ONT.
Activation process: 
  1. Schedule appointment
  2. Technician visit
  3. Service validation
  4. Go-live
```

### 3.3 Possible Chunks

**Chunk 1:**
```
Fiber 500 Service.
Download speed: Up to 500 Mbps.
Upload speed: Up to 100 Mbps.
```

**Chunk 2:**
```
Fiber 500 Service.
Technology: FTTH.
Installation requires a compatible ONT.
```

**Chunk 3:**
```
Activation process:
  1. Schedule appointment
  2. Technician visit
  3. Service validation
  4. Go-live
```

**Note**: The product title "Fiber 500 Service" is repeated in each chunk. This is called **contextual metadata** or **contextualized chunk text**. It helps chunks remain understandable when retrieved independently.

### 3.4 Chunking Strategies

| Strategy | Description | Best Use |
|----------|-------------|----------|
| **Fixed-size** | Split by token or character count | Simple text, uniform documents |
| **Recursive** | Split by paragraphs, sentences, then smaller units | General documents, mixed content |
| **Structure-aware** | Respect headings, sections, tables | **Telecom manuals** (recommended) |
| **Semantic** | Split based on topic changes | Long narrative documents |
| **Parent-child** | Retrieve small chunks, provide larger sections | Complex procedures with dependencies |

### 3.5 Initial Recommendation for Telecom
**Use structure-aware chunking for telecom documentation**, with recursive splitting as a fallback.

**Anti-patterns to avoid**:
- Splitting a troubleshooting procedure in the middle of a step
- Separating a table's values from its headers
- Chunking across major section boundaries (e.g., separating "Product Overview" from "Specifications")

## 4. Chunk Size and Overlap

### 4.1 Chunk Size Trade-offs

| Chunk Size | Precision | Context Completeness |
|------------|-----------|---------------------|
| **Small** (100-200 tokens) | Higher precision retrieval | May lose broader context |
| **Medium** (300-500 tokens) | Good balance | Most common starting point |
| **Large** (500+ tokens) | More context per chunk | May introduce irrelevant information |

### 4.2 Overlap Strategy
Overlap repeats some text between neighboring chunks to preserve continuity:

```
Chunk 1: tokens   1–100
Chunk 2: tokens  81–180   (81-100 overlap)
Chunk 3: tokens 161–260   (161-180 overlap)
```

**Recommended initial values for telco corpus**:
- **Chunk size**: 300–500 tokens
- **Overlap**: 50–75 tokens
- Respect document headings and section boundaries
- Keep tables and procedural steps intact where possible

**Note**: These are starting values for experiments, not universal optimal settings. Measure Recall@K and adjust based on retrieval quality.

### 4.3 Example with 100-token chunks and 20-token overlap

```
Chunk 1: tokens   1–100
Chunk 2: tokens  81–180   (81-100 = 20 token overlap)
Chunk 3: tokens 161–260   (161-180 = 20 token overlap)
```

## 5. What is an Embedding?

### 5.1 Embedding Definition
An embedding is a numerical representation of text in a vector space. A text embedding model transforms text into a vector:

```
f(text) → ℝ^d
```

**Simplified illustration**:

```
"How do I fix a red LOS light?"
        ↓
[0.12, -0.34, 0.81, 0.05, ...]  (vector in d-dimensional space)
```

The vector may contain hundreds or thousands of dimensions (common: 384, 768, 1536 depending on model).

### 5.2 Semantic Similarity in Vector Space

Text with similar meaning should generally have vectors that are close together, even when the wording differs:

- **Query**: "My fiber connection has a red LOS light."
- **Document**: "Troubleshooting loss of optical signal on an ONT."

These texts have different words but related meanings → embeddings should have high cosine similarity.

### 5.3 Cosine Similarity

A common measure of semantic alignment:

```
sim(q, d) = (q · d) / (||q|| ||d||)
```

Where:
- `q` is the query embedding
- `d` is a document-chunk embedding
- Higher similarity → closer semantic alignment

**Important**: Similarity is **not** a calibrated probability that the answer is correct. It's a relative measure for ranking and retrieval.

## 6. Tokens and Context Windows

### 6.1 What are Tokens?

LLMs process text as tokens, not simply words. A token may be:

- A complete word: "fiber"
- Part of a word: "on" + "t" → "ONT" might be 1-3 tokens
- Punctuation: "." 
- A number or technical identifier: "8472" may be separate tokens
- "ONT-8472" could be 1 token or multiple depending on tokenizer

### 6.2 Context Window

The context window is the maximum amount of input and output the model can process in one request.

**Typical context limits by model**:

| Model | Context Window |
|-------|---------------|
| gpt-4o | 128,000 tokens |
| gpt-4-turbo | 128,000 tokens |
| claude-3-opus | 200,000 tokens |
| claude-3-sonnet | 200,000 tokens |

### 6.3 RAG Prompt Budgeting

A RAG prompt must budget for:

```
System prompt + Question + Retrieved context + Output tokens ≤ Model context limit
```

**Typical budget breakdown** (gpt-4o, 128K context):

| Component | Estimated Tokens | Percentage |
|-----------|-----------------|------------|
| System instruction | 50-100 | <1% |
| User question | 10-50 | <1% |
| Retrieved context | 300-800 | 2-6% |
| Answer output | 100-300 | <1% |
| **Total used** | **~500-1,300** | **<1%** |
| **Remaining** | **~126,700** | **~99%** |

### 6.4 Why Context Budgeting Matters

Retrieval should not blindly send every matching document to the LLM because:

1. **Token limits**: 50 chunks × 100 tokens = 5,000 tokens, quickly eating budget
2. **Diminishing returns**: Additional chunks add noise, not proportionally more value
3. **Cost impact**: More tokens = more LLM cost per query
4. **Quality degradation**: Overly long context may dilute focus, reduce answer quality

### 6.5 Context Assembly Strategy

1. Retrieve candidate chunks (typically 50+ candidates)
2. **Rerank by relevance** (cross-encoder, reduce to top 20)
3. Remove duplicates and redundant evidence
4. **Select chunks within the token budget** (typically 3-8 chunks, 300-800 tokens total)
5. Preserve source metadata for citations (document_id, chunk_id)
6. **Reserve enough tokens for the answer** (100-300 tokens minimum)
7. Output the grounded answer with citations

## 7. The Complete Transformation Pipeline

```
Source Document
       ↓
Parse Text and Structure
       ↓
Create Chunks (structure-aware, with contextual metadata)
       ↓
Attach Metadata (document_id, version, domain, section, effective_from)
       ↓
Embedding Model (generate query embedding & chunk embeddings)
       ↓
Vector Index (pgvector HNSW + BM25 lexical index)
       ↓
User Query
       ↓
Query Embedding (same model, same dimensionality)
       ↓
Similarity Search (cosine similarity + BM25 + RRF hybrid)
       ↓
Relevant Chunks (reranked, filtered, within token budget)
       ↓
Context Budgeting (select + reserve for answer)
       ↓
LLM Generation (system prompt + selected context + question)
       ↓
Answer with Sources (citations, grounded flag)
```

## 8. Rust Data Model Concept

For telco-rag-rs, a retrieved chunk might eventually be represented like this:

```rust
pub struct DocumentChunk {
    pub chunk_id: String,
    pub document_id: String,
    pub content: String,
    pub metadata: ChunkMetadata,
}

pub struct ChunkMetadata {
    pub title: String,
    pub domain: String,
    pub version: String,
    pub section: Option<String>,
    pub effective_from: Option<String>,
}

pub struct EmbeddedChunk {
    pub chunk: DocumentChunk,
    pub embedding: Vec<f32>,
}
```

**Note**: This is a learning model. Later, we will refine identifiers, dates, metadata types, and embedding dimensions into stronger domain types with proper validation.

## 9. Practical Exercise

### Exercise: Analyze a troubleshooting document and create chunks

**Step 1**: Take one troubleshooting document (e.g., "Fiber LOS Red Light Troubleshooting Guide")

**Step 2**: Manually create 3–5 chunks following structure-aware chunking principles

**Step 3**: Check whether each chunk can be understood independently

**Example troubleshooting document**:

```
Fiber Loss of Signal (LOS) Troubleshooting

Red Light on ONT Indicator

A solid red LOS light on the Optical Network Terminal (ONT) indicates 
loss of optical signal. This may be caused by:

1. Physical layer issues
   - Broken or disconnected fiber optic cable
   - Bent or kinked fiber patch cords
   - Water damage to outdoor fiber infrastructure

2. Equipment issues
   - Faulty ONT unit
   - Incorrect ONT configuration
   - Power cycling required

3. Network issues
   - External plant damage
   - Service provider outage
   - Splitter or node problems

Troubleshooting steps:

Step 1: Visually inspect fiber cables for damage.
Step 2: Check all connections are secure.
Step 3: Power cycle the ONT (unplug 30 seconds, replug).
Step 4: If red light persists, contact support.

Required tools: Fiber optic power meter, light source.
Safety: Do not look directly into fiber endfaces.
```

**Your 3–5 manually created chunks** (ensure each is independently understandable):

```
Chunk A: Fiber LOS Troubleshooting - Red Light on ONT Indicator
  (A solid red LOS light on the Optical Network Terminal (ONT) indicates loss of optical signal. May be caused by physical layer issues, equipment issues, or network issues.)

Chunk B: Physical Layer Causes - Fiber Cable Issues
  (Broken or disconnected fiber optic cable, bent or kinked fiber patch cords, water damage to outdoor fiber infrastructure.)

Chunk C: Troubleshooting Steps - Power Cycle ONT
  (Power cycle the ONT: unplug 30 seconds, replug. If red light persists after power cycling, contact support.)

Chunk D: Required Tools and Safety
  (Required tools: Fiber optic power meter, light source. Safety: Do not look directly into fiber endfaces.)

Chunk E: Escalation Procedure
  (If red light persists after visual inspection, connection checks, and power cycling, contact support with ONT model, serial number, and error timestamp.)
```

### Verification: Can each chunk be understood independently?

- **Chunk A**: ✅ States the problem (red LOS light = loss of optical signal) and three cause categories
- **Chunk B**: ✅ Lists specific physical layer issues (broken cable, kinks, water damage)
- **Chunk C**: ✅ Gives concrete action (power cycle 30 seconds, when to escalate)
- **Chunk D**: ✅ Provides tools and safety warning (important for field technicians)
- **Chunk E**: ✅ Clear escalation path with required information (model, serial, timestamp)

**Exit criteria**: Each chunk should be understandable without referring to other chunks or the original document. If a chunk requires context from another chunk, restructure the chunking.

---

## Summary - Stage 1 Exit Criteria

You should be able to explain:

1. **Difference between documents and chunks**: Documents have stable identity/version; chunks are independent retrieval units with contextual metadata
2. **Why metadata is essential**: Enables filtering, governance, access control, source traceability, versioned retrieval
3. **Three chunking strategies and trade-offs**: Fixed-size (simple), recursive (general), structure-aware (telecom docs) - with anti-patterns to avoid
4. **How embeddings represent semantic meaning**: Text → vector in d-dimensional space; similar meaning → close vectors in cosine space
5. **How cosine similarity works**: `(q·d) / (||q|| ||d||)` - relative ranking measure, NOT calibrated probability
6. **How context-window budgeting affects retrieval**: Must balance retrieved chunks against system prompt + question + answer output; should not blindly send all matching chunks
7. **Initial chunking configuration for telecom documents**: 300-500 tokens size, 50-75 tokens overlap, structure-aware respecting headings/sections/tables

**Practical exercise completed**: Manually created 3-5 chunks from troubleshooting document, verified each can be understood independently.

**Git commit**: 
```
git add docs/rag-fundamentals.md
git commit -m "telco-rag-rs: document RAG fundamentals knowledge hierarchy"
```