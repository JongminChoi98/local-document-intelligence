# System Architecture

Version: v0.1.0

Scope: Current main branch, including stabilization changes.
The original MVP remains available under the v0.1.0 tag.

## Document Ingestion Pipeline

Excel Upload
    -> Document Parser
    -> Rule-based Normalization
    -> Text Serialization
    -> BGE-M3 Embedding
    -> Save Original Excel
    -> ChromaDB

Failed ingestion performs compensating file cleanup.
Files referenced by the database are retained.
Files are also retained when database state cannot be verified.
This is not a fully atomic transaction.

## Question Answering Pipeline

User Question
    -> Conversation History
    -> Query Rewriting
    -> Query Embedding
    -> Hybrid Retrieval
    -> Context Construction
    -> Local LLM
    -> Answer and Retrieved Sources

## Hybrid Retrieval

The retrieval module combines:

- Dense vector similarity search
- Keyword matching
- Reciprocal Rank Fusion
- Exact document ID filtering
- Minimum cosine similarity: 0.52
- Maximum gap from the best similarity: 0.06

Explicit matching document IDs bypass semantic thresholds.
Missing IDs in the supported KAS and TEST-AS formats
prevent unrelated records from being substituted.

The thresholds were calibrated using a small synthetic dataset.
Their generalization to production data remains unverified.

When retrieval returns no documents,
answer generation is skipped.

## Query Rewrite Recovery

- The first question bypasses query rewriting.
- Failed rewriting can fall back to the original question
  when it contains a supported explicit document ID.
- Otherwise, the application requests clarification.
- Empty and truncated rewrite responses are treated as failures.

Answer generation prompts instruct the model to preserve
source uncertainty and technical terminology.
This does not guarantee factual accuracy.

The current implementation targets small local datasets.

## Project Modules

| Module | Responsibility |
|---|---|
| app.py | Streamlit user interface |
| chat_store.py | Persistent chat management |
| parsers/ | Excel and PDF extraction |
| preprocessors/ | Maintenance record normalization |
| embeddings/ | Text serialization and embedding |
| vector_store/ | ChromaDB and document management |
| retrieval/ | Dense and hybrid retrieval |
| llm/ | Ollama generation and model settings |
| rag/ | RAG and conversational pipelines |
| ingestion/ | Automated document ingestion |
| config/ | Runtime configuration |
| docs/ | Project documentation |
| scripts/ | Environment startup scripts |
| storage/ | Local runtime data |

## Runtime Storage

| Path | Purpose |
|---|---|
| storage/input/ | Original documents |
| storage/input/uploads/ | Uploaded documents |
| storage/processed/ | Standalone CLI extraction output |
| storage/normalized/ | Standalone CLI normalization output |
| storage/embeddings/ | Standalone CLI embedding output |
| storage/chroma/ | Vector database |
| storage/chat_history.db | Persistent chat history |
| storage/open-webui/ | Earlier Open WebUI PoC data |

Web ingestion processes extraction, normalization,
serialization, and embedding in memory.

The original upload is stored under
storage/input/uploads/<uuid>/<filename>.

The resulting text, vector, and source metadata
are stored in ChromaDB.

Removing a document from retrieval does not delete its original file.

## Runtime Boundaries

- Ollama: 127.0.0.1:11434
- Streamlit: 127.0.0.1:8501
- Open WebUI (optional): 127.0.0.1:8080

The custom application does not require Open WebUI.

## Design Decisions

- Reuse local models through Ollama.
- Keep embedding and generation models independent.
- Separate document processing from retrieval and generation.
- Store chat history separately from the knowledge database.
- Preserve original source references.
- Keep runtime and company data outside Git.
- Defer generalized document preprocessing.

## Deployment Scope

Single-user local prototype.

Production deployment requires authentication,
authorization, security validation, backup procedures,
and quantitative evaluation.
