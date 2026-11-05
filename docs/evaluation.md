# RAG Evaluation and Quality Engineering - telco-rag-rs

## 7.1 Retrieval Metrics

### 7.1.1 Recall@K
- Definition: Percentage of relevant documents among top K retrieved
- Formula: `|Relevant ∩ Retrieved@K| / |Relevant|`
- Telecom use case: Recall@10, Recall@20 for question answering

### 7.1.2 Precision@K
- Definition: Percentage of retrieved documents that are relevant
- Formula: `|Relevant ∩ Retrieved@K| / K`

### 7.1.3 Mean Reciprocal Rank (MRR)
- Definition: Average of reciprocal ranks of first relevant document across queries
- Formula: `mean(1/rank_of_first_relevant)` across all queries
- Rewards getting the first relevant document early

### 7.1.4 NDCG (Normalized Discounted Cumulative Gain)
- **Graded relevance**: Relevance scores (0=irrelevant, 1=relevant, 2=highly relevant, etc.)
- **Discount factor**: Position-dependent, `1/log2(position+1)`
- **CG**: Cumulative Gain at position K
- **IDCG**: Ideal DCG (best possible ranking)
- **NDCG**: CG/IDCG, normalized to [0, 1]

### 7.1.5 Retrieval Error Analysis
- **False negatives**: Relevant documents not retrieved
- **False positives**: Irrelevant documents retrieved
- **Position analysis**: Where relevant documents appear in results
- **Per-category analysis**: Recall/precision by domain, product, question type

## 7.2 Generation Metrics

### 7.2.1 Faithfulness / Groundedness
- Definition: Percentage of answer claims supported by retrieved evidence
- Measurement: LLM-as-judge evaluating each claim against sources
- Formula: `|supported_claims| / |total_claims|`

### 7.2.2 Answer Relevance
- Definition: How well the answer addresses the user question
- Measurement: Human or LLM evaluation of answer-query alignment
- Scale: 1-5 or binary relevant/non-relevant

### 7.2.3 Context Relevance
- Definition: How relevant the retrieved context is to the question
- Measurement: Percentage of context units directly answering the question

### 7.2.4 Citation Correctness
- Definition: Each citation accurately references the claimed source
- Measurement: Automatic verification of document_id/chunk_id pairs
- Critical for trust and auditability

### 7.2.5 Completeness
- Definition: Whether all aspects of the question are addressed
- Measurement: Checklist-based or LLM-as-judge evaluation

### 7.2.6 Correct Abstention Rate
- Definition: Percentage of unanswerable questions where system correctly abstains
- Formula: `|correct_abstentions| / |unanswerable_questions|`
- Critical for avoiding hallucinations

## 7.3 Evaluation Methods

### 7.3.1 Golden Datasets
- **Structure**: Questions + expected answers + expected sources + unanswerable flags
- **Size**: Minimum 100 questions for Stage 7, growing over time
- **Coverage**: Products, billing, troubleshooting, policies, unanswerable
- **Maintenance**: Continuous expansion with new scenarios

### 7.3.2 Deterministic Metrics
- Calculated directly from retrieval/generation outputs
- Recall@K, Precision@K, MRR, NDCG
- Groundedness score, citation correctness
- Run on fixed dataset, track regression

### 7.3.3 LLM-as-a-Judge
- **Calibrated rubrics**: Specific criteria for each metric
- **Few-shot prompts**: Examples of good/bad evaluations
- **Multiple judges**: Average scores to reduce bias
- **Example rubric for groundedness**:
  - 1: Answer completely hallucinated, no support
  - 2: Some claims unsupported, partial grounding
  - 3: Mostly grounded, minor unsupported claims
  - 4: Fully grounded, all claims supported

### 7.3.4 Human Review
- **Sample-based**: Human evaluators assess random subset
- **Full human eval**: Complete dataset assessment (costly)
- **Expert reviewers**: Telecom domain experts for accuracy
- **Crowdsourced**: For large volumes, controlled platform

### 7.3.5 Regression Testing
- Every major change (prompt, embedding, chunking, retrieval) tested against baseline
- Automated metric comparison before/after changes
- Guard rails to prevent quality degradation

### 7.3.6 Adversarial Test Cases
- **Adversarial questions**: Designed to trigger failures
- **Edge cases**: Missing information, ambiguous queries
- **Distractor documents**: Irrelevant but similar content
- **Language variations**: Synonyms, terminology differences

## 7.4 Evaluation Dataset Structure - Telecom Example

| Question | Category | Expected Answer | Expected Sources | Unanswerable |
|----------|----------|----------------|-----------------|--------------|
| What is the upload speed of Fiber 500? | Product features | "Fiber 500 provides up to 100 Mbps upload speed." | CAT-FIBER-500, chunk-03 | No |
| How does roaming work? | Policies | "Roaming charges apply when using service abroad." | CAT-POLICY-ROAMING, chunk-01 | No |
| What is my exact account balance? | Personal data | (abstain) | - | Yes |
| How do I fix red light on fiber? | Troubleshooting | "Check ONT connections, restart equipment." | CAT-TROUBLESHOOTING, chunk-05 | No |

## 7.5 Exit Criteria - Stage 7
- Golden dataset with ≥100 questions created (products, billing, troubleshooting, policies, unanswerable)
- Every major prompt/embedding/chunking/retrieval change tested against baseline metrics
- Faithfulness/groundedness, answer relevance, citation correctness measured and tracked
- Correct abstention rate measured on unanswerable questions
- Regression testing pipeline established
- Adversarial test cases documented and passing