# System Architecture

Version: v0.1.0

## Document Ingestion Pipeline

Excel Upload
    -> Document Parser
    -> Rule-based Normalization
    -> Text Serialization
    -> BGE-M3 Embedding
    -> ChromaDB

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
- Exact document ID prioritization

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
| storage/processed/ | Raw extraction results |
| storage/normalized/ | Normalized records |
| storage/embeddings/ | Generated embedding files |
| storage/chroma/ | Vector database |
| storage/chat_history.db | Persistent chat history |
| storage/open-webui/ | Earlier Open WebUI PoC data |

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
