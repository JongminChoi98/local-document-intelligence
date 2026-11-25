import json
from urllib.request import Request, urlopen


OLLAMA_URL = "http://127.0.0.1:11434"
EMBEDDING_MODEL = "bge-m3:567m"
EMBEDDING_DIMENSION = 1024


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts or any(not text.strip() for text in texts):
        raise ValueError("Embedding input must not be empty.")

    payload = {
        "model": EMBEDDING_MODEL,
        "input": texts,
        "truncate": False,
    }

    request = Request(
        f"{OLLAMA_URL}/api/embed",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        result = json.load(response)

    vectors = result["embeddings"]

    if len(vectors) != len(texts):
        raise ValueError("Embedding count mismatch.")

    for vector in vectors:
        if len(vector) != EMBEDDING_DIMENSION:
            raise ValueError("Embedding dimension mismatch.")

    return vectors


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]
