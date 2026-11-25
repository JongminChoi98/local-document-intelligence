import argparse
from llm.settings import GenerationSettings
import json
from urllib.request import Request, urlopen


OLLAMA_URL = "http://127.0.0.1:11434"
LLM_MODEL = "qwen3.5:4b-q4_K_M"


def generate_answer(
    messages: list[dict],
    settings: GenerationSettings = GenerationSettings(),
) -> dict:
    if not messages:
        raise ValueError("Messages must not be empty.")

    payload = {
        "model": settings.model,
        "messages": messages,
        "stream": False,
        "options": {
            "num_ctx": settings.num_ctx,
            "temperature": settings.temperature,
            "num_predict": settings.num_predict,
        },
    }

    if settings.think is not None:
        payload["think"] = settings.think

    request = Request(
        f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        result = json.load(response)

    answer = result["message"]["content"].strip()

    if not answer:
        raise ValueError("LLM returned an empty answer.")

    return {
        "model": result["model"],
        "answer": answer,
        "done_reason": result.get("done_reason"),
        "prompt_tokens": result.get("prompt_eval_count", 0),
        "completion_tokens": result.get("eval_count", 0),
        "total_seconds": result.get("total_duration", 0) / 1e9,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    args = parser.parse_args()

    messages = [
        {
            "role": "system",
            "content": "한국어로 간결하고 정확하게 답변하세요.",
        },
        {
            "role": "user",
            "content": args.question,
        },
    ]

    result = generate_answer(messages)

    print(f"Model: {result['model']}")
    print(f"Prompt tokens: {result['prompt_tokens']}")
    print(f"Completion tokens: {result['completion_tokens']}")
    print(f"Duration: {result['total_seconds']:.2f}s")
    print(f"Done reason: {result['done_reason']}")
    print(f"\nAnswer:\n{result['answer']}")


if __name__ == "__main__":
    main()
