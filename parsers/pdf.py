import argparse
import json
from pathlib import Path

from pypdf import PdfReader


def parse_pdf(file_path: Path) -> dict:
    pages = []

    with file_path.open("rb") as file:
        reader = PdfReader(file)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text(
                extraction_mode="layout",
                layout_mode_space_vertically=False,
            ).strip()

            pages.append({
                "page": page_number,
                "text": text,
            })

    return {
        "source": file_path.name,
        "pages": pages,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    result = parse_pdf(args.file)

    output_dir = (
        Path(__file__).resolve().parents[1]
        / "storage"
        / "processed"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{args.file.name}.json"

    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Source: {result['source']}")
    print(f"Total pages: {len(result['pages'])}")

    for page in result["pages"]:
        print(f"Page {page['page']}: {len(page['text'])} characters")

        if not page["text"]:
            print("  Warning: No extractable text.")

    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
