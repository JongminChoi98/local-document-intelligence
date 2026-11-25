from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from parsers.excel import parse_excel
from preprocessors.maintenance import normalize_excel
from embeddings.serializer import serialize_record
from embeddings.ollama import EMBEDDING_MODEL, embed_text
from vector_store.chroma import upsert_document


INPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "storage"
    / "input"
)

MAX_FILE_SIZE = 20 * 1024 * 1024


def ingest_excel(filename: str, content: bytes) -> dict:
    filename = Path(filename.replace("\\", "/")).name

    if Path(filename).suffix.lower() != ".xlsx":
        raise ValueError("Only XLSX files are supported.")

    if not content or len(content) > MAX_FILE_SIZE:
        raise ValueError("Invalid file size.")

    upload_dir = INPUT_DIR / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory(dir=upload_dir) as temp_dir:
        temp_path = Path(temp_dir) / filename
        temp_path.write_bytes(content)

        raw = parse_excel(temp_path, "AS일지_2026")
        record = normalize_excel(raw)
        text = serialize_record(record)
        vector = embed_text(text)

        relative_path = Path("uploads") / uuid4().hex / filename
        saved_path = INPUT_DIR / relative_path

        saved_path.parent.mkdir(parents=True, exist_ok=True)
        saved_path.write_bytes(content)

        record["source"]["file"] = relative_path.as_posix()

        data = {
            "document_id": record["document_id"],
            "embedding_model": EMBEDDING_MODEL,
            "text": text,
            "embedding": vector,
            "source": record["source"],
        }

        count = upsert_document(data)

    return {
        "document_id": record["document_id"],
        "filename": filename,
        "embedding_dimension": len(vector),
        "total_documents": count,
    }
