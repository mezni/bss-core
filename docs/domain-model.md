# Domain Model - telco-rag-rs

## 1. Why We Need a Domain Model

### 1.1 The Version Update Problem
Imagine the telecom knowledge manager updates the Fiber 500 product specification:

**Original document:**
```
Fiber 500
Download: 500 Mbps
Upload: 100 Mbps
```

**Updated document:**
```
Fiber 500
Download: 500 Mbps
Upload: 200 Mbps
```

**What should happen in a production RAG system:**
1. Detect the document update
2. Create a new document version (not silently overwrite)
3. Process the updated content through the pipeline
4. Generate new chunks from the new version
5. Generate new embeddings for new chunks
6. Update the search indexes with new vectors
7. Prevent outdated information from being returned to users
8. Preserve historical versions for auditing and rollback

**Why this matters**: If you only have a document table and vector database, updating a document creates ambiguity:
- Which version is the "current" one?
- What version was the user querying when they got the answer?
- How do you rollback if the new version is incorrect?
- How do you audit changes for compliance?

**A production RAG system needs a domain model that tracks versions, lineages, and lifecycles explicitly.**

### 1.2 Core Domain Entities
We will start with seven core entities, each with distinct responsibilities:

| Entity | Responsibility |
|--------|----------------|
| **KnowledgeSource** | Identifies where knowledge originates |
| **Document** | Represents a logical knowledge document |
| **DocumentVersion** | Represents an immutable document revision |
| **DocumentChunk** | Represents a searchable text segment |
| **Embedding** | Stores vector representation information |
| **IngestionJob** | Tracks document processing |
| **AccessPolicy** | Defines who can access knowledge |

### 2. Entity Relationships

```mermaid
gclassDiagram
    KnowledgeSource "1" -- "*" Document
    Document "1" -- "*" DocumentVersion
    DocumentVersion "1" -- "*" DocumentChunk
    DocumentChunk "1" -- "1" Embedding
    IngestionJob "1" -- "*" Document
    AccessPolicy "1" -- "*" Document
    
    KnowledgeSource : +source_id String
    KnowledgeSource : +name String
    KnowledgeSource : +source_type SourceType
    KnowledgeSource : +location String
    KnowledgeSource : +enabled Boolean
    
    Document : +id Uuid
    Document : +source_id Uuid
    Document : +title String
    Document : +status DocumentStatus
    
    DocumentVersion : +id Uuid
    DocumentVersion : +document_id Uuid
    DocumentVersion : +version String
    DocumentVersion : +content_hash String
    DocumentVersion : +effective_from DateTime<Utc>
    DocumentVersion : +effective_until DateTime<Utc> || optional
    DocumentVersion : +status VersionStatus
    
    DocumentChunk : +id Uuid
    DocumentChunk : +version_id Uuid
    DocumentChunk : +sequence u32
    DocumentChunk : +content String
    DocumentChunk : +metadata Json
    
    Embedding : +chunk_id Uuid
    Embedding : +model_name String
    Embedding : +dimensions usize
    Embedding : +vector Vec<f32>
    Embedding : +created_at DateTime<Utc>
    
    IngestionJob : +id Uuid
    IngestionJob : +document_id Uuid
    IngestionJob : +status JobStatus
    IngestionJob : +started_at DateTime<Utc>
    IngestionJob : +completed_at DateTime<Utc> || optional
    IngestionJob : +chunks_processed Integer
    IngestionJob : +embeddings_generated Integer
    IngestionJob : +error_details Text || optional
    IngestionJob : +retry_count Integer
    
    AccessPolicy : +policy_id Uuid
    AccessPolicy : +document_id Uuid
    AccessPolicy : +access_scope String
    AccessPolicy : +role String
```

### 3. KnowledgeSource

A KnowledgeSource identifies the origin of information. Source identity should be independent of document identity—one source can contain thousands of documents.

**Examples:**

| Source | Example |
|--------|---------|
| Product catalog | Product specifications |
| Billing system export | Billing policies |
| Technical repository | Network manuals |
| Support knowledge base | Troubleshooting articles |
| FAQ repository | Customer questions |

**Example entity:**
```json
{
  "source_id": "SRC-001",
  "name": "Telecom Product Catalog",
  "source_type": "product_catalog",
  "location": "knowledge/catalog/",
  "enabled": true
}
```

**Important**: Source identity is independent of document identity. The same source can yield many documents over time.

### 4. Document and DocumentVersion

These are two distinct concepts that must not be conflated.

**Document**: The logical identity of a knowledge item. It has a stable `document_id` that remains the same across versions.

**DocumentVersion**: A particular revision of that item. Each version is **immutable** after publication; corrections create new versions rather than silently changing historical content.

**Example: CAT-FIBER-500**

```
Document: CAT-FIBER-500

Version 1 (Superseded)
Upload speed: 100 Mbps
Effective: Jan 2026 - Mar 2026

Version 2 (Active)
Upload speed: 200 Mbps
Effective: Apr 2026 - Current
```

**Why separate them?**
- **Historical auditing**: Trace what the policy said at any point in time
- **Rollback**: Revert to a previous version if new content is incorrect
- **Document change detection**: Identify what changed between versions
- **Re-indexing**: Only re-process chunks for the changed version
- **Effective-date management**: Serve different versions based on `effective_from`
- **Prevention of stale information**: Ensure users get the version effective for their timeframe
- **Compliance**: Maintain record of what was known and when

**A version should be immutable after publication**. A correction creates another version rather than silently changing historical content.

### 5. DocumentChunk

A DocumentChunk is a searchable segment belonging to a particular document version.

**Example entity:**
```json
{
  "chunk_id": "CHK-001",
  "document_id": "CAT-FIBER-500",
  "version_id": "VER-002",
  "sequence": 1,
  "content": "Fiber 500 provides upload speeds up to 200 Mbps.",
  "metadata": {
    "domain": "fiber_broadband",
    "product": "fiber_500",
    "section": "speed"
  }
}
```

**Important properties:**
- Every chunk has a stable identity (`chunk_id`)
- Every chunk belongs to a specific document version (`version_id`)
- Every chunk retains its source information for traceability
- Every chunk can be independently indexed in the vector store
- Every chunk must respect document access permissions (enforced at retrieval time)

**Architecture decision**: Never lose the relationship between a retrieved chunk and its original document version. The `document_id` and `version_id` must always be preserved with each chunk for citation and access control.

### 6. Embedding

An embedding represents the semantic meaning of a chunk as a vector.

**Example:**
```
Chunk: "Fiber 500 provides upload speeds up to 200 Mbps."
Embedding: [0.12, -0.45, 0.78, ...]  (vector in d-dimensional space)
```

**Embedding record should track:**

| Attribute | Purpose |
|-----------|---------|
| `chunk_id` | Original chunk identifier |
| `model_name` | Embedding provider/model (e.g., "text-embedding-3-large") |
| `model_version` | Model revision/version |
| `dimensions` | Vector size (e.g., 384, 768, 1536) |
| `vector` | Numeric representation (list of f32) |
| `created_at` | Generation timestamp |

**Why track the embedding model?**

Suppose you change from one embedding model to another. The resulting vectors may have:
- Different dimensions
- Different semantic space characteristics
- Different similarity distribution patterns

**You must not blindly mix vectors from incompatible embedding models in the same index.** Tracking the model name and version ensures:
- Correct similarity search (same model must be used for query and document embeddings)
- Re-indexing when model changes
- A/B testing of different embedding models
- Cost attribution per model

### 7. IngestionJob and Lifecycle Management

Document ingestion is a workflow, not a single database insert. Recommended lifecycle stages:

```
New → Processing → Validating → Chunking → Embedding → Indexing → Published
     ↑                                   ↓
     └── Failed ← Retry ← Error details ←─
```

**Each ingestion job should record:**
- `job_id`: Identifier for the ingestion run
- `document_id`: Which document this job processes
- `document_version`: Which version this job processes
- `status`: Current stage (New, Processing, Validating, Chunking, Embedding, Indexing, Published, Failed)
- `started_at`: When the job started
- `completed_at`: When the job finished (optional, null if still running)
- `chunks_processed`: Number of chunks produced
- `embeddings_generated`: Number of embeddings created
- `error_details`: Description of what went wrong (optional)
- `retry_count`: How many times this job has been retried

**Critical production concept: Atomic publication**

Imagine 100 chunks need to be indexed, but indexing fails after chunk 60.

**You should not expose a partially indexed version as if it were complete.**

**Safer approach (staged publication):**
1. Build the new version separately (in isolation)
2. Process all chunks (100% completion)
3. Generate all embeddings
4. Validate indexing (verify vector store consistency)
5. **Atomically activate the new version** (mark as published in one transaction)
6. Retire the old version from active retrieval

This ensures users never see partially processed data. Either the new version is fully ready, or the old version remains active.

### 8. Effective Dates and Temporal Knowledge

Telecom policies and products change over time. Must distinguish between:

| Term | Description |
|------|-------------|
| `created_at` | When the record was created (system timestamp) |
| `published_at` | When it became available in the system |
| `effective_from` | When the business rule takes effect |
| `effective_until` | When it stops being effective |

**Example: Billing Policy**

| Policy version | Effective from | Effective until |
|---------------|---------------|----------------|
| Version 1 | Jan 1 | Mar 31 |
| Version 2 | Apr 1 | Current |

**A document can be published but not yet effective.** For example, a new product spec announced in December might not take effect until January 1.

**Retrieval system must consider the effective date**, not simply select the newest document version. Query logic should include:

```sql
WHERE effective_from <= current_date 
  AND (effective_until IS NULL OR effective_until >= current_date)
```

**Particularly important for:**
- Billing policies and rate changes
- Promotional offers and pricing
- Roaming agreements and terms
- Contractual terms and conditions
- Service level agreements (SLAs)

### 9. Access Control at the Knowledge Level

Not every user should retrieve every document. Two document categories:

| Role | Product catalog | Internal procedures |
|------|-----------------|---------------------|
| Support Agent | Yes | Limited |
| Technical Agent | Yes | Yes |
| Supervisor | Yes | Yes |
| Knowledge Manager | Manage | Manage |

**Access control must be enforced before or within retrieval**, not merely by hiding information in the final LLM answer.

**Critical**: The LLM must never receive documents the requesting user is not authorized to access. This prevents:
- Information leakage through context injection
- Prompt injection via unauthorized documents
- Compliance violations (GDPR, industry regulations)
- Retrieval poisoning attacks

**Enforcement points:**
1. **Pre-retrieval**: Filter by `access_policy` before vector search
2. **Post-retrieval**: Check each chunk's access policy before including in context
3. **LLM input sanitization**: Remove any document references user couldn't access

### 10. Proposed Rust Domain Model

```rust
use chrono::{DateTime, Utc};
use uuid::Uuid;

#[derive(Debug, Clone)]
pub struct KnowledgeSource {
    pub id: Uuid,
    pub name: String,
    pub source_type: SourceType,
    pub location: String,
}

#[derive(Debug, Clone)]
pub enum SourceType {
    ProductCatalog,
    BillingPolicy,
    Troubleshooting,
    TechnicalManual,
    Faq,
}

#[derive(Debug, Clone)]
pub struct Document {
    pub id: Uuid,
    pub source_id: Uuid,
    pub title: String,
    pub status: DocumentStatus,
}

#[derive(Debug, Clone)]
pub enum DocumentStatus {
    Active,
    Archived,
    Deleted,
}

#[derive(Debug, Clone)]
pub struct DocumentVersion {
    pub id: Uuid,
    pub document_id: Uuid,
    pub version: String,
    pub content_hash: String,
    pub effective_from: DateTime<Utc>,
    pub effective_until: Option<DateTime<Utc>>,
}

#[derive(Debug, Clone)]
pub struct DocumentChunk {
    pub id: Uuid,
    pub version_id: Uuid,
    pub sequence: u32,
    pub content: String,
}

#[derive(Debug, Clone)]
pub struct EmbeddedChunk {
    pub chunk_id: Uuid,
    pub model_name: String,
    pub dimensions: usize,
    pub vector: Vec<f32>,
}
```

**Note**: This is a conceptual first version. Later, we will introduce:
- Domain-specific ID types (stronger typing than generic Uuid)
- Stronger invariants (e.g., `effective_from` must be before `effective_until`)
- Typed version states (instead of simple enums)
- Repository interfaces for persistence abstraction

### 11. Recommended Documentation Structure

```
telco-rag-rs/
└── docs/
    ├── requirements.md
    ├── architecture.md
    ├── rag-lifecycle.md
    ├── rag-fundamentals.md
    └── domain-model.md  ← NEW
```

**For `docs/domain-model.md`, document:**

1. **Domain entities and responsibilities** - The 7 entities and what each owns
2. **Entity relationships** - Mermaid diagram and cardinalities (1:N, 1:1, etc.)
3. **Document versioning strategy** - Document vs DocumentVersion, immutability, version lineage
4. **Chunk and embedding relationships** - Chunk belongs to version, embedding tracks model provenance
5. **Ingestion lifecycle** - Job states, atomic publication, retry logic
6. **Effective-date management** - created_at/published_at/effective_from/effective_until distinction
7. **Access-control boundaries** - Role-based policies, enforcement before retrieval
8. **Atomic publication strategy** - Staged publishing, never expose partial indexes

---

## Summary - Stage 1 Domain Model Exit Criteria

You should be able to explain:

1. **Why a domain model is necessary** - Version updates, audit trails, rollback, stale data prevention
2. **The 7 core domain entities** - KnowledgeSource, Document, DocumentVersion, DocumentChunk, Embedding, IngestionJob, AccessPolicy and their responsibilities
3. **Document vs DocumentVersion distinction** - Logical identity vs. immutable revision, why separate them
4. **DocumentChunk important properties** - Stable identity, version binding, source retention, independent indexing, access permission respect
5. **Embedding tracking requirements** - Model name, version, dimensions, why incompatibility matters
6. **IngestionJob lifecycle** - States (New→Processing→...→Published), atomic publication, error handling
7. **Effective date management** - Distinguishing created_at/published_at/effective_from/effective_until, temporal query logic
8. **Access control boundaries** - Enforcement before LLM retrieval, role-based policies, never sending unauthorized docs to LLM
9. **Rust domain model** - The trait/types proposed, conceptual first version

**Git commit:**
```
git add docs/domain-model.md
git commit -m "telco-rag-rs: document domain model with 7 entities and versioning"
```

**Practical exercise** (from earlier): Create 3-5 chunks from a troubleshooting document, verify each can be understood independently. Document the chunking decisions and metadata attached to each chunk.