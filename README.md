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

Initial project setup.

## Data Privacy

Confidential documents, credentials, model weights,
and generated document indexes must not be committed
to this repository.

## Setup Guides

- [Ollama Environment Setup](docs/ollama-setup.md)

## Configuration

- [Ollama systemd Override](config/ollama/override.conf)

## Validation

- [Local LLM Validation](docs/local-llm-validation.md)
