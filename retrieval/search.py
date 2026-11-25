import argparse
import json

from embeddings.ollama import embed_text
from vector_store.chroma import get_collection


def search_documents(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    if not query.strip():
        raise ValueError("Query must not be empty.")

    if top_k < 1:
        raise ValueError("top_k must be greater than zero.")

    collection = get_collection()
    count = collection.count()

    if count == 0:
        return []

    query_vector = embed_text(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(top_k, count),
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = []

    for index, document_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][index]
        metadata = results["metadatas"][0][index]

        documents.append({
            "document_id": document_id,
            "text": results["documents"][0][index],
            "distance": distance,
            "similarity": 1.0 - distance,
            "source": {
                "file": metadata["source_file"],
                "format": metadata["source_format"],
                "sheet": metadata["source_sheet"],
                "cells": json.loads(metadata["source_cells"]),
            },
        })

    return documents


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    results = search_documents(args.query, args.top_k)

    print(f"Query: {args.query}")
    print(f"Retrieved documents: {len(results)}")

    for rank, result in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print(f"Document ID: {result['document_id']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Source: {result['source']['file']}")


if __name__ == "__main__":
    main()
