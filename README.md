# Local Document Intelligence

A local RAG application for vehicle A/S maintenance records,
built with Python, Ollama, ChromaDB, SQLite, and Streamlit.

## Project Status

Version: v0.1.0
Status: MVP / Local Prototype

## Developer Documentation

Start here if you are new to this project.

| Step | Document | Description |
|---|---|---|
| 1 | [Developer Overview](docs/developer-overview.md) | Project objectives, AI technologies, and design decisions |
| 2 | [Developer Setup Guide](docs/developer-setup.md) | Environment installation, repository setup, execution, and smoke tests |
| 3 | [Codex QA Prompt](qa/CODEX_QA_PROMPT.md) | Independent integration testing and defect reporting |

### Technical References

- [System Architecture](docs/architecture.md)
- [Development Roadmap](docs/roadmap.md)

### Run QA with Codex

Open this repository in Codex and provide the following instruction:

> Read qa/CODEX_QA_PROMPT.md and execute the integration QA
> procedure. Use synthetic test data and preserve the existing
> application source code and user data.

### Historical Development Records

The following documents describe the initial proof of concept.
They are not required to run the current application.

- [Local LLM Validation](docs/archive/local-llm-validation.md)
- [Open WebUI Setup](docs/archive/open-webui-setup.md)
- [Initial RAG PoC Validation](docs/archive/rag-poc-validation.md)

The original MVP source remains available under the v0.1.0 tag.
Developer documentation added after that tag is maintained on main.

## Features

- Local LLM inference using Ollama
- Excel and PDF text extraction
- Rule-based maintenance record normalization
- BGE-M3 document embeddings
- Persistent ChromaDB vector storage
- Semantic and hybrid search with RRF
- Document-grounded question answering
- Conversational RAG with query rewriting
- Single and batch Excel document uploads
- Document listing and removal from retrieval
- Original Excel document downloads
- Persistent chat history using SQLite
- Configurable LLM and inference settings

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.12.16 |
| Package Manager | uv |
| LLM Runtime | Ollama |
| Default LLM | Qwen3.5 4B Q4_K_M |
| Embedding | BGE-M3 (1024 dimensions) |
| Vector Database | ChromaDB |
| Chat Database | SQLite |
| Excel Parser | openpyxl |
| PDF Parser | pypdf |
| Web Interface | Streamlit |
| Retrieval | Dense Search, Keyword Search, RRF |
| Development OS | Ubuntu on WSL2 |

## Installation

Prerequisites:

- Git
- uv
- Ollama running locally

Clone the repository:

    git clone https://github.com/JongminChoi98/local-document-intelligence.git
    cd local-document-intelligence

Install Python and project dependencies:

    uv python install 3.12.16
    uv sync --locked

Download the required Ollama models:

    ollama pull qwen3.5:4b-q4_K_M
    ollama pull bge-m3:567m

Confirm that Ollama is running:

    ollama list

## Run the Application

    uv run python -m streamlit run app.py

Open the application at:

http://127.0.0.1:8501

## Usage

1. Start the application.
2. Upload supported A/S Excel records.
3. Register documents using the sidebar.
4. Ask questions about maintenance records.
5. Review answers and retrieved sources.
6. Download original documents when necessary.

## Default Inference Settings

| Parameter | Value |
|---|---|
| Thinking | Disabled |
| Context Window | 16384 |
| Temperature | 0.1 |
| Max Output Tokens | 1024 |
| Retrieval Top-K | 3 |
| Embedding Model | bge-m3:567m |

## Current Limitations

- Excel normalization supports a specific maintenance template.
- Inconsistent document layouts may fail during registration.
- PDF extraction is implemented but not integrated into retrieval.
- OCR and image analysis are not implemented.
- Retrieval quality has not been quantitatively evaluated.
- Alternative LLM configurations remain unverified.
- Multi-user authentication and authorization are not implemented.
- Full offline operation has not been verified.

## Data Security

The application is configured for local operation.

Original documents, generated embeddings, vector databases,
chat history, and runtime data are excluded from Git.

Do not commit confidential company documents or credentials.

This prototype is not yet approved for production deployment.
