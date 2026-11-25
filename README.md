# Local Document Intelligence

A local document intelligence system powered by
Ollama and Retrieval-Augmented Generation (RAG).

## Overview

This project explores the implementation of a local
document retrieval and question-answering system
using open-source language models.

## Objectives

- Run large language models locally.
- Understand embeddings and vector search.
- Implement a RAG pipeline.
- Provide document-based question answering.
- Verify retrieval accuracy and source citations.
- Keep document processing within the local environment.

## Technology Stack

| Component | Technology |
|---|---|
| Development Environment | WSL2 Ubuntu |
| Programming Language | Python |
| LLM Runtime | Ollama |
| Initial LLM | Qwen3.5 4B |
| User Interface (PoC) | Open WebUI |
| Embedding Model | TBD |
| Vector Store | TBD |
| Version Control | Git / GitHub |

## Project Status

Local LLM and Open WebUI integration validated. RAG development is pending.

## Data Privacy

Confidential documents, credentials, model weights,
and generated document indexes must not be committed
to this repository.

## Setup Guides

- [Ollama Environment Setup](docs/ollama-setup.md)
- [Open WebUI Environment Setup](docs/open-webui-setup.md)

## Configuration

- [Ollama systemd Override](config/ollama/override.conf)
- [Open WebUI Environment Template](config/open-webui/.env.example)

## Validation

- [Local LLM Validation](docs/local-llm-validation.md)

## Quick Start

Ensure the Ollama service is running:

    systemctl is-active ollama

Start Open WebUI:

    ./scripts/start-open-webui.sh

Open http://localhost:8080 in a browser.

See the setup guides for installation prerequisites.

## RAG Proof of Concept

The initial local RAG proof of concept has been completed
using Ollama, Qwen3.5, BGE-M3, ChromaDB, and Open WebUI.

- [RAG PoC Validation](docs/rag-poc-validation.md)

The next phase focuses on implementing a custom
Python-based RAG pipeline for A/S maintenance records.
