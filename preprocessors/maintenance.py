import argparse
import json
from pathlib import Path


FIELD_MAP = {
    "document_id": "M1",
    "created_date": "M4",
    "received_date": "D6",
    "service_date": "K6",
    "customer": "D8",
    "location": "D9",
    "vehicle": "D10",
    "department": "K9",
    "service_duration": "I12",
    "symptom_category": "D12",
    "cause_category": "D13",
    "action_category": "D14",
    "part_category": "D15",
    "reported_symptom": "D16",
    "observed_symptom": "D17",
    "cause": "D18",
    "repair_action": "D19",
    "service_parts": "D20",
    "prevention": "D21",
}

EXPECTED_LABELS = {
    "K1": "문서번호",
    "A8": "고객명",
    "A10": "조치 차량",
    "A16": "고객 접수 내용",
    "A17": "현장 확인 내용",
    "A18": "발생 원인",
    "A19": "조치 내용",
    "A20": "조치 부품",
}


def normalize_excel(data: dict) -> dict:
    if data.get("sheet") != "AS일지_2026":
        raise ValueError("Unsupported maintenance sheet.")

    cells = {
        address: value
        for row in data["rows"]
        for address, value in row.items()
    }

    for address, expected in EXPECTED_LABELS.items():
        if cells.get(address) != expected:
            raise ValueError(
                f"Unexpected template layout at {address}"
            )

    record = {
        field: cells.get(address)
        for field, address in FIELD_MAP.items()
    }

    if not record["document_id"]:
        raise ValueError("Missing document ID.")

    record["source"] = {
        "file": data["source"],
        "format": "xlsx",
        "sheet": data["sheet"],
        "cells": FIELD_MAP.copy(),
    }

    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    data = json.loads(
        args.file.read_text(encoding="utf-8")
    )

    record = normalize_excel(data)

    output_dir = (
        Path(__file__).resolve().parents[1]
        / "storage"
        / "normalized"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / args.file.name

    output_path.write_text(
        json.dumps(
            record,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    filled = sum(
        record[field] is not None
        for field in FIELD_MAP
    )

    print(f"Normalized fields: {filled}/{len(FIELD_MAP)}")
    print(f"Document ID: {record['document_id']}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
