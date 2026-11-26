import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from parsers.excel import parse_excel
from preprocessors.maintenance import normalize_excel
from embeddings.serializer import serialize_record
from embeddings.ollama import EMBEDDING_MODEL, embed_text
from vector_store.chroma import get_collection, upsert_document


INPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "storage"
    / "input"
)

MAX_FILE_SIZE = 20 * 1024 * 1024

logger = logging.getLogger(__name__)


def cleanup_failed_upload(
    saved_path: Path,
    relative_path: Path,
    document_id: str,
    upsert_started: bool,
) -> None:
    if upsert_started:
        try:
            result = get_collection().get(
                ids=[document_id],
                include=["metadatas"],
            )

            if result["ids"]:
                source_file = result["metadatas"][0]["source_file"]

                if not isinstance(source_file, str) or not source_file:
                    raise ValueError("Invalid source metadata.")

                if source_file == relative_path.as_posix():
                    logger.warning(
                        "Upload retained: database references the file."
                    )
                    return

        except Exception:
            logger.warning(
                "Upload retained: database state could not be verified."
            )
            return

    try:
        saved_path.unlink(missing_ok=True)
        saved_path.parent.rmdir()

    except OSError:
        logger.warning(
            "Failed to clean up incomplete upload.",
            exc_info=True,
        )


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

        saved_path.parent.mkdir(parents=True, exist_ok=False)
        upsert_started = False

        try:
            saved_path.write_bytes(content)

            record["source"]["file"] = relative_path.as_posix()

            data = {
                "document_id": record["document_id"],
                "embedding_model": EMBEDDING_MODEL,
                "text": text,
                "embedding": vector,
                "source": record["source"],
            }

            upsert_started = True
            count = upsert_document(data)

        except Exception:
            cleanup_failed_upload(
                saved_path,
                relative_path,
                record["document_id"],
                upsert_started,
            )
            raise

    return {
        "document_id": record["document_id"],
        "filename": filename,
        "embedding_dimension": len(vector),
        "total_documents": count,
    }
