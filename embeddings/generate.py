import argparse
import json
from pathlib import Path

from embeddings.ollama import EMBEDDING_MODEL, embed_text
from embeddings.serializer import serialize_record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    record = json.loads(
        args.file.read_text(encoding="utf-8")
    )

    text = serialize_record(record)
    vector = embed_text(text)

    result = {
        "document_id": record["document_id"],
        "embedding_model": EMBEDDING_MODEL,
        "text": text,
        "embedding": vector,
        "source": record["source"],
    }

    output_dir = (
        Path(__file__).resolve().parents[1]
        / "storage"
        / "embeddings"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / args.file.name

    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Document ID: {result['document_id']}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Input characters: {len(text)}")
    print(f"Embedding dimension: {len(vector)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
