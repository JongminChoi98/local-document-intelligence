# RAG Proof of Concept Validation

## 1. Objective

Validate a local RAG system for vehicle A/S maintenance
records and understand the core RAG architecture.

Validation date: 2026-11-25

## 2. Technical Configuration

| Component | Configuration |
|---|---|
| LLM Runtime | Ollama 0.40.17 |
| LLM | qwen3.5:4b-q4_K_M |
| Embedding Model | bge-m3:567m |
| Embedding Dimension | 1024 |
| Embedding Precision | F16 |
| Vector Database | ChromaDB |
| Interface | Open WebUI 0.13.4 |
| GPU | NVIDIA RTX 4060 Laptop 8GB |
| Ollama Default Context | 8192 |
| LLM Context | 16384 |
| Embedding Context | 8192 |
| Chunk Size | 1024 characters |
| Chunk Overlap | 100 characters |
| Document Format | XLSX |
| Retrieval Strategy | Traditional RAG |

## 3. Open WebUI Configuration

Document settings:

- Embedding Engine: Ollama
- Embedding Model: bge-m3:567m
- Embedding API: http://127.0.0.1:11434
- Embedding Batch Size: 1
- Chunk Size: 1024
- Chunk Overlap: 100

LLM settings:

- num_ctx: 16384
- File Context: Enabled
- Builtin Tools: Disabled
- Citations: Enabled
- Thinking: Default

These settings are managed through the Admin UI.

## 4. Validation Results

| Test | Result |
|---|---|
| Local LLM inference | PASS |
| Embedding API | PASS |
| GPU acceleration | PASS |
| Simultaneous model loading | PASS |
| Cosine similarity calculation | PASS |
| Semantic search | PASS |
| ChromaDB integration | PASS |
| Excel document ingestion | PASS |
| Document-based question answering | PASS |
| Source citation display | PASS |
| Retrieval accuracy | Needs improvement |
| Document parsing quality | Needs improvement |
| Response latency | Needs improvement |
| Full offline operation | Not verified |

## 5. Observed Limitations

- Excel auxiliary sheets introduce irrelevant content.
- Empty cells produce NaN values in extracted text.
- Generic chunking may separate related maintenance fields.
- Relevant customer information was inconsistently retrieved.
- Agentic RAG caused repeated context length errors.
- Increasing the context length alone did not resolve
  all errors.
- Traditional RAG generated answers without the observed
  context error in the final tests.
- Thinking-enabled responses showed excessive latency.
- Citation display does not guarantee factual accuracy.

## 6. Conclusion

The initial RAG proof of concept is successful.

The system demonstrates local document retrieval
and document-grounded answer generation.

Production readiness and answer reliability have
not yet been established.

## 7. Next Development Phase

Implement a custom Python-based RAG pipeline:

1. Project initialization
2. A/S Excel document parser
3. PDF document parser
4. Data preprocessing and normalization
5. Embedding module
6. Vector storage and retrieval
7. RAG answer generation
8. Evaluation and optimization

Existing Ollama models will be reused.

## 8. Data Security

Original company documents, personal information,
runtime databases, and generated embeddings must
not be committed to Git.

Full offline operation remains to be verified.
