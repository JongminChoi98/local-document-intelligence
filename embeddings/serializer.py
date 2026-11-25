FIELD_LABELS = {
    "document_id": "문서번호",
    "created_date": "작성일자",
    "received_date": "접수일자",
    "service_date": "처리일자",
    "customer": "고객명",
    "location": "장소",
    "vehicle": "조치 차량",
    "department": "처리 부서",
    "service_duration": "작업 소요시간",
    "symptom_category": "이상증상 분류",
    "cause_category": "주요원인 분류",
    "action_category": "조치내용 분류",
    "part_category": "소요부품 분류",
    "reported_symptom": "고객 접수 내용",
    "observed_symptom": "현장 확인 내용",
    "cause": "발생 원인",
    "repair_action": "조치 내용",
    "service_parts": "조치 부품",
    "prevention": "재발 방지 및 수평 전개 사항",
}


def serialize_record(record: dict) -> str:
    lines = ["차량 A/S 정비 일지"]

    for field, label in FIELD_LABELS.items():
        value = record.get(field)

        if value is None:
            continue

        text = str(value).strip()

        if text:
            lines.append(f"{label}: {text}")

    return "\n\n".join(lines)
