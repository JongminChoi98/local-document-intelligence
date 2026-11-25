import argparse
import re
import unicodedata

from retrieval.search import search_documents
from vector_store.chroma import get_collection


RRF_K = 60

STOP_WORDS = {
    "알려줘", "설명해", "찾아줘",
    "정리해", "비교해", "무엇인가",
    "뭐야", "해주세요", "문서",
}


def normalize(text: str) -> str:
    return unicodedata.normalize(
        "NFKC", text
    ).casefold()


def tokenize(text: str) -> set[str]:
    tokens = re.findall(
        r"[a-z0-9]+(?:-[a-z0-9]+)*|[가-힣]+",
        normalize(text),
    )

    return {
        token
        for token in tokens
        if len(token) >= 2
        and token not in STOP_WORDS
    }


def keyword_score(query: str, text: str) -> int:
    tokens = tokenize(query)
    content = normalize(text)

    return sum(
        token in content
        for token in tokens
    )


def exact_id_match(query: str, document_id: str) -> bool:
    pattern = (
        r"(?<![a-z0-9-])"
        + re.escape(normalize(document_id))
        + r"(?![a-z0-9-])"
    )

    return bool(re.search(pattern, normalize(query)))


def search_hybrid(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    if not query.strip():
        raise ValueError("Query must not be empty.")

    if top_k < 1:
        raise ValueError("Invalid top_k.")

    count = get_collection().count()

    if count == 0:
        return []

    documents = search_documents(
        query,
        top_k=count,
    )

    for rank, document in enumerate(documents, start=1):
        document["dense_rank"] = rank
        document["keyword_score"] = keyword_score(
            query,
            document["text"],
        )

        document["exact_id_match"] = exact_id_match(
            query,
            document["document_id"],
        )

    keyword_scores = sorted(
        {
            doc["keyword_score"]
            for doc in documents
            if doc["keyword_score"] > 0
        },
        reverse=True,
    )

    keyword_ranks = {
        score: rank
        for rank, score in enumerate(
            keyword_scores, start=1
        )
    }

    for document in documents:
        score = 1 / (
            RRF_K + document["dense_rank"]
        )

        keyword_rank = keyword_ranks.get(
            document["keyword_score"]
        )

        if keyword_rank is not None:
            score += 1 / (RRF_K + keyword_rank)

        document["keyword_rank"] = keyword_rank
        document["hybrid_score"] = score

    documents.sort(
        key=lambda doc: (
            doc["exact_id_match"],
            doc["hybrid_score"],
            doc["similarity"],
        ),
        reverse=True,
    )

    return documents[:top_k]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    results = search_hybrid(args.query, args.top_k)

    for rank, document in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print(f"Document: {document['document_id']}")
        print(f"Dense rank: {document['dense_rank']}")
        print(f"Similarity: {document['similarity']:.4f}")
        print(f"Keyword score: {document['keyword_score']}")
        print(f"Keyword rank: {document['keyword_rank']}")
        print(f"Hybrid score: {document['hybrid_score']:.6f}")
        print(f"Exact ID match: {document['exact_id_match']}")


if __name__ == "__main__":
    main()
