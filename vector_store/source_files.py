from pathlib import Path


INPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "storage"
    / "input"
).resolve()


def get_source_file(source_file: str) -> Path:
    relative_path = Path(source_file)

    if relative_path.is_absolute():
        raise ValueError("Absolute paths are not allowed.")

    path = (INPUT_DIR / relative_path).resolve()

    if not path.is_relative_to(INPUT_DIR):
        raise ValueError("Invalid source file path.")

    if path.suffix.lower() != ".xlsx":
        raise ValueError("Unsupported file format.")

    if not path.is_file():
        raise FileNotFoundError("Source file not found.")

    return path
