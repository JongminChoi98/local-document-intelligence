import json
from pathlib import Path

import chromadb
from chromadb.config import Settings

from embeddings.ollama import (
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
)


DB_PATH = (
    Path(__file__).resolve().parents[1]
    / "storage"
    / "chroma"
)

COLLECTION_NAME = "maintenance_bge_m3_v1"


def get_collection():
    client = chromadb.PersistentClient(
        path=str(DB_PATH),
        settings=Settings(anonymized_telemetry=False),
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
        configuration={
            "hnsw": {
                "space": "cosine",
            }
        },
    )


def upsert_document(data: dict):
    if data["embedding_model"] != EMBEDDING_MODEL:
        raise ValueError("Embedding model mismatch.")

    if len(data["embedding"]) != EMBEDDING_DIMENSION:
        raise ValueError("Embedding dimension mismatch.")

    source = data["source"]

    collection = get_collection()

    collection.upsert(
        ids=[data["document_id"]],
        embeddings=[data["embedding"]],
        documents=[data["text"]],
        metadatas=[{
            "embedding_model": data["embedding_model"],
            "source_file": source["file"],
            "source_format": source["format"],
            "source_sheet": source["sheet"],
            "source_cells": json.dumps(
                source["cells"],
                ensure_ascii=False,
            ),
        }],
    )

    return collection.count()
