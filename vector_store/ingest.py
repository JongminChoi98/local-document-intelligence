import argparse
import json
from pathlib import Path

from vector_store.chroma import (
    DB_PATH,
    COLLECTION_NAME,
    upsert_document,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", type=Path, nargs="+")
    args = parser.parse_args()

    for file_path in args.files:
        data = json.loads(
            file_path.read_text(encoding="utf-8")
        )

        count = upsert_document(data)

        print(f"Document ID: {data['document_id']}")
        print(f"Embedding dimension: {len(data['embedding'])}")
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Total documents: {count}")

    print(f"Database path: {DB_PATH}")


if __name__ == "__main__":
    main()
