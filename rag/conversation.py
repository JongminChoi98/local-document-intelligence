from time import perf_counter

from llm.ollama import generate_answer
from llm.settings import GenerationSettings
from rag.pipeline import ask


MAX_HISTORY_MESSAGES = 6
MAX_MESSAGE_LENGTH = 1200

REWRITE_PROMPT = """
당신은 차량 A/S 정비 기록 검색을 위한 질문 재구성 시스템입니다.

이전 대화와 현재 질문을 참고하여 현재 질문을
독립적으로 이해할 수 있는 검색 질문으로 변환하세요.

규칙:
1. 질문에 답변하지 마세요.
2. 재구성된 질문만 출력하세요.
3. 이전 대화에서 필요한 차량명, 고객명, 문서번호를 보완하세요.
4. 새로운 사실을 임의로 추가하지 마세요.
5. 현재 질문이 독립적이라면 그대로 반환하세요.
6. 이전 답변은 문맥 파악에만 사용하세요.
   이전 AI 답변을 검증된 정비 사실로 간주하지 마세요.
7. 사용자의 원래 질문 의도와 질문 범위를 유지하세요.
8. 추정, 의심, 가능성 및 미확인 표현을 확정된 사실로 변경하지 마세요.
9. 차량명, 문서번호, 부품명 및 기술 용어를 임의로 변형하지 마세요.
10. 현재 질문에 없는 원인이나 인과관계를 추가하지 마세요.
11. 한국어로 작성하세요.

재구성 예시:

이전 질문: 테스트 차량 2호의 고장 원인은 뭐야?
이전 답변: 접촉저항 증가로 추정됩니다.
현재 질문: 그러면 어떤 부품을 사용했어?

올바른 재구성:
테스트 차량 2호의 정비에 사용된 부품은 무엇인가?

잘못된 재구성:
접촉저항 증가로 고장 난 테스트 차량 2호에 사용된 부품은 무엇인가?

이전 대화의 추정 원인을 확정된 사실로 바꾸거나
현재 질문에 불필요하게 포함하지 마세요.
""".strip()


def rewrite_question(
    question: str,
    history: list[dict],
    settings: GenerationSettings = GenerationSettings(),
) -> str:
    if not history:
        return question

    history_lines = []

    for message in history[-MAX_HISTORY_MESSAGES:]:
        role = message["role"]

        if role == "user":
            content = message["content"]

        elif role == "assistant":
            content = message["result"]["answer"]

        else:
            continue

        history_lines.append(
            f"{role}: {content[:MAX_MESSAGE_LENGTH]}"
        )

    if not history_lines:
        return question

    history_text = "\n".join(history_lines)

    messages = [
        {
            "role": "system",
            "content": REWRITE_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"이전 대화:\n{history_text}\n\n"
                f"현재 질문:\n{question}"
            ),
        },
    ]

    result = generate_answer(messages, settings)

    return result["answer"].strip()


def ask_conversation(
    question: str,
    history: list[dict],
    top_k: int = 3,
    settings: GenerationSettings = GenerationSettings(),
) -> dict:
    started = perf_counter()

    rewritten = rewrite_question(question, history, settings)
    rewrite_seconds = perf_counter() - started

    result = ask(rewritten, top_k=top_k, settings=settings)

    result["question"] = question
    result["rewritten_question"] = rewritten
    result["rewrite_seconds"] = rewrite_seconds
    result["total_seconds"] = perf_counter() - started

    return result
