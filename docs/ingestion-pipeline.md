# Document Ingestion and Knowledge Engineering - telco-rag-rs

## 3.1 Ingestion Pipeline Overview
The ingestion pipeline transforms raw telecom documents into searchable knowledge chunks with proper metadata. This is Stage 3 of the roadmap.

## 3.2 Document Loaders
Supported formats and source connectors:

| Format | Connector Type | Example Source |
|--------|---------------|----------------|
| Markdown | `MarkdownLoader` | Product catalogs, FAQs, troubleshooting guides |
| PDF | `PdfLoader` | Technical manuals, policy documents |
| HTML | `HtmlLoader` | Web-based documentation, support portals |
| CSV | `CsvLoader` | structured data tables, device configurations |
| DOCX | `DocxLoader` | Word-processed documentation |

### Loader Responsibilities
- Parse document format into raw text
- Extract embedded metadata (titles, headers, timestamps)
- Handle encoding detection and normalization
- Flag corrupted or unsupported files for dead-letter queue

## 3.3 Text Normalization
Boilerplate removal and text cleaning steps:

1. **Header/footer removal**: Strip document metadata, page numbers
2. **Table extraction**: Preserve table structure (table-aware chunking)
3. **Link resolution**: Convert relative URLs to absolute, extract link text
4. **Character normalization**: Unicode normalization, special character handling
5. **Whitespace cleanup**: Collapse multiple spaces, normalize line endings

### Normalization Rules
- Remove "CONFIDENTIAL" watermarks and document headers
- Strip "Page X of Y" footers
- Extract table captions and surround with text context
- Preserve list structures and bullet points

## 3.4 Metadata Extraction
Schema-validated metadata extraction from documents:

```json
{
  "document_id": "CAT-FIBER-500",
  "title": "Fiber 500 Service",
  "source_type": "product_catalog",
  "domain": "fiber_broadband",
  "product": "fiber_500",
  "version": "2026-01",
  "effective_from": "2026-01-01",
  "language": "en",
  "tags": ["fiber", "broadband", "500mbps"],
  "author": "Telco Documentation Team",
  "last_updated": "2026-01-15"
}
```

### Mandatory Fields
- `document_id`: Unique identifier (format: `CAT-{type}-{code}`)
- `title`: Human-readable document title
- `source_type`: `product_catalog`, `policy`, `troubleshooting`, `faq`, `technical_manual`, `procedure`
- `domain`: High-level domain (`fiber_broadband`, `mobile`, `tv`, `billing`, `technical`)
- `effective_from`: ISO date string, version activation date

### Optional Fields
- `product`: Specific product code or plan name
- `version`: Document version string
- `language`: ISO 639-1 language code
- `tags`: Free-form tag array for categorization

## 3.5 Chunking Strategies
Document splitting into searchable units:

### 3.5.1 Fixed-Size Chunking
- Chunk size: Configurable (e.g., 512 tokens)
- Overlap: 0-50 tokens between adjacent chunks
- Simple but may split logical sections

### 3.5.2 Structure-Aware/Recursive Chunking
- Chunk by headings (H1, H2, H3)
- Chunk by logical sections (introduction, body, conclusion)
- Preserve section context in each chunk

### 3.5.3 Semantic Chunking
- Use embeddings to identify thematic boundaries
- Chunk by topic changes rather than fixed sizes
- More accurate but computationally expensive

### 3.5.4 Table-Aware Chunking
- Detect and preserve table structure
- Extract header-row relationships
- Markdown-table format preservation

### 3.5.5 Parent-Child Retrieval
- **Parent**: Larger contextual unit (section, document)
- **Child**: Smaller searchable chunk
- Retrieval at child level, context at parent level

## 3.6 Telecom-Specific Metadata
### 3.6.1 Document Metadata Schema
```json
{
  "document_id": "CAT-FIBER-500",
  "title": "Fiber 500 Service",
  "source_type": "product_catalog",
  "domain": "fiber_broadband",
  "product": "fiber_500",
  "version": "2026-01",
  "effective_from": "2026-01-01",
  "language": "en"
}
```

### 3.6.2 Versioning Strategy
- Documents have `effective_from` dates
- Multiple versions can coexist
- Retrieval filters by `effective_from <= current_date`
- Deprecation and replacement tracking

### 3.6.3 Access Control Metadata
- `classification`: `public`, `internal`, `confidential`
- `tenant_isolation`: Optional tenant identifier
- `pii_flags`: Boolean array indicating PII presence

## 3.7 Ingestion Pipeline Flow
```
Document Source --> Loader --> Text Normalization --> Metadata Extraction --> Validation --> Chunking --> Embedding Generation --> Vector Store --> Idempotency Check
```

## 3.8 Idempotency & Incremental Ingestion
### 3.8.1 Hash-Based Deduplication
- Compute content hash (SHA-256) for each document
- Store hash in ingestion state
- Skip documents with existing hashes

### 3.8.2 Change Detection
- Compare `effective_from` dates
- Detect content modifications
- Update vector store with delta changes

### 3.8.3 Dead-Letter Queue
- Failed documents routed to DLQ
- Retry configuration (max attempts, backoff)
- Manual review interface for problematic documents

## 3.9 Exit Criteria - Stage 3
- Re-running ingestion does not create duplicates
- Document updates propagate correctly through the pipeline
- Metadata validation catches 100% of schema violations
- Chunking strategies produce consistent chunk counts for same documents