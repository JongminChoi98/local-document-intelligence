from vector_store.chroma import get_collection


def list_documents() -> list[dict]:
    collection = get_collection()

    result = collection.get(
        include=["metadatas"],
    )

    documents = []

    for document_id, metadata in zip(
        result["ids"],
        result["metadatas"],
    ):
        documents.append({
            "document_id": document_id,
            "filename": metadata["source_file"],
            "sheet": metadata["source_sheet"],
            "format": metadata["source_format"],
        })

    return sorted(
        documents,
        key=lambda item: item["document_id"],
    )


def delete_document(document_id: str) -> int:
    if not document_id.strip():
        raise ValueError("Document ID must not be empty.")

    collection = get_collection()

    collection.delete(ids=[document_id])

    return collection.count()
