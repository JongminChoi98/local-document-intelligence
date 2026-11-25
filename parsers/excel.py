import argparse
import json
from pathlib import Path

from openpyxl import load_workbook


def parse_excel(file_path: Path, sheet_name: str) -> dict:
    workbook = load_workbook(
        file_path,
        read_only=True,
        data_only=True,
        keep_links=False,
    )

    try:
        if sheet_name not in workbook.sheetnames:
            raise ValueError(
                f"Sheet not found: {sheet_name}. "
                f"Available sheets: {workbook.sheetnames}"
            )

        sheet = workbook[sheet_name]
        rows = []

        for row in sheet.iter_rows():
            cells = {}

            for cell in row:
                value = cell.value

                if value is None:
                    continue

                if isinstance(value, str):
                    value = value.strip()

                    if not value:
                        continue

                cells[cell.coordinate] = value

            if cells:
                rows.append(cells)

        return {
            "source": file_path.name,
            "sheet": sheet_name,
            "rows": rows,
        }

    finally:
        workbook.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--sheet", default="AS일지_2026")
    args = parser.parse_args()

    result = parse_excel(args.file, args.sheet)

    output_dir = (
        Path(__file__).resolve().parents[1]
        / "storage"
        / "processed"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{args.file.stem}.json"

    output_path.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    print(f"Source: {result['source']}")
    print(f"Sheet: {result['sheet']}")
    print(f"Extracted rows: {len(result['rows'])}")
    print(f"Extracted cells: {sum(len(row) for row in result['rows'])}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
