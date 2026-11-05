# Requirements Specification - telco-rag-rs

## 1.1 Business Problem
Telecommunications customers need reliable, accurate answers to queries about products, policies, billing, and technical issues. Traditional keyword search fails because:
- Product codes and technical identifiers don't match natural language questions
- Important details are scattered across multiple documents (catalogs, manuals, policies)
- Customers require grounded answers with citations, not hallucinated information

## 1.2 Target Users
- **Customer support agents** - Need quick access to accurate product and policy information
- **End customers** - Self-service answers to common questions about their services
- **Technical staff** - Troubleshooting connectivity and configuration issues

## 1.3 Knowledge Sources
| Source Type | Example Content |
|-------------|-----------------|
| Product catalog | Fiber 500, Mobile Unlimited, TV packages |
| Policy documents | Return policy, roaming policy, data caps |
| Troubleshooting guides | Fiber LOS red light, router configuration |
| FAQs | Billing questions, service plan changes |
| Technical manuals | ONT setup, SIM installation, router firmware |
| Service procedures | Activation, outage handling, escalation |

## 1.4 System Requirements
### Functional Requirements
- [ ] Answer questions about fiber, mobile, internet, and TV products
- [ ] Explain billing, roaming, data usage, and service policies
- [ ] Troubleshoot connectivity and service issues
- [ ] Retrieve accurate information from product catalogs, technical manuals, FAQs, and support procedures
- [ ] Provide grounded answers with citations and source references
- [ ] Escalate questions when evidence is missing or confidence is insufficient

### Non-Functional Requirements
- [ ] Answers must be grounded in retrieved evidence (no hallucination)
- [ ] Citations must include document_id and chunk_id
- [ ] System must abstain when retrieval confidence is insufficient
- [ ] Ingestion must be idempotent (re-running does not create duplicates)
- [ ] Retrieval must support metadata filtering (domain, product, version, language)

### Constraints
- Rust backend only
- PostgreSQL + pgvector for initial vector storage
- Must support incremental ingestion
- Must handle document versioning (effective_from dates)

## 1.5 Success Metrics
- **Recall@K**: Percentage of relevant documents retrieved in top K results
- **Groundedness**: Percentage of answers fully supported by retrieved citations
- **Citation correctness**: Percentage of citations that accurately reference source documents
- **Abstention rate**: Percentage of questions where system correctly identifies unanswerable questions

## 1.6 Assumptions & Open Questions
- LLM provider costs and latency characteristics
- Initial document corpus size and format diversity
- Required latency for customer-facing queries
- Security and tenant isolation requirements