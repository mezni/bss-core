# Domain Model - telco-rag-rs

## 2.1 Core Concepts

### 2.1.1 Knowledge Domain
The telecommunications domain encompasses product information, policies, troubleshooting procedures, and customer service knowledge. Knowledge is organized into the following categories:

- **Product Information**: Service plans, pricing, features, technical specifications
- **Policy Documents**: Billing policies, roaming rules, data caps, terms of service
- **Troubleshooting**: Connectivity issues, equipment configuration, service restoration
- **FAQs**: Common customer questions and answers
- **Technical Documentation**: Equipment manuals, configuration guides, API documentation

### 2.1.2 Document Types
| Document Type | Format | Example |
|--------------|--------|---------|
| Product catalog | Markdown/JSON | Fiber 500 service description |
| Policy documents | Markdown/PDF | Roaming policy v2026 |
| Troubleshooting guides | Markdown | Fiber LOS diagnosis |
| FAQs | Markdown | Billing question answers |
| Technical manuals | Markdown/HTML | ONT installation guide |
| Service procedures | Markdown | Outage handling procedure |

### 2.1.3 User Personas
- **Customer Support Agent**: Needs quick, accurate answers with citations to assist customers
- **End Customer**: Self-service answers about their own service
- **Technical Specialist**: Deep technical details about equipment and configuration

## 2.2 Knowledge Source Modeling

### 2.2.1 Document Metadata Schema
Each document must have the following metadata:

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
  "tags": ["fiber", "broadband", "500mbps"]
}
```

### 2.2.2 Document Chunking
Documents are split into searchable chunks using strategies:
- **Fixed-size**: Uniform chunk size (e.g., 512 tokens)
- **Structure-aware**: Chunk by headings, sections, or logical breaks
- **Semantic**: Chunk by thematic boundaries
- **Table-aware**: Preserve table structure when chunking

### 2.2.3 Versioning Strategy
Documents have `effective_from` dates. When retrieving:
- Filter by `effective_from <= current_date`
- Support for multiple concurrent versions
- Deprecation and replacement tracking

## 2.3 Question Categories
Telecom questions fall into these categories:

| Category | Example Questions |
|----------|------------------|
| Product features | "What is the upload speed of Fiber 500?" |
| Billing questions | "How does roaming charges work?" |
| Troubleshooting | "My fiber light is red, what does it mean?" |
| Policy explanation | "What is the data cap for my plan?" |
| Service procedures | "How do I migrate from mobile to fiber?" |
| Unanswerable | "What is my exact account balance?" (requires PII) |

## 2.4 Exit Criteria
You can explain:
- When RAG is appropriate vs. traditional search vs. fine-tuning
- What data the system needs (document sources, formats, metadata)
- How to measure whether answers are trustworthy (groundedness, citation correctness)
- When to escalate vs. abstain