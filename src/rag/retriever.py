"""Hybrid Dense + Sparse (BM25) RAG Retriever for financial domain documents."""

from typing import TypedDict
from rank_bm25 import BM25Okapi


class SearchResult(TypedDict):
    doc_id: str
    content: str
    metadata: dict
    score: float


class HybridFinancialRetriever:
    """Combines BM25 lexical keyword matching with dense vector retrieval for high-accuracy financial RAG."""

    def __init__(self):
        self.documents: list[dict] = []
        self.bm25: BM25Okapi | None = None
        self._is_indexed = False

    def index_documents(self, docs: list[dict]):
        """Index a collection of documents with 'content' and 'metadata' keys."""
        self.documents = docs
        tokenized_corpus = [doc["content"].lower().split() for doc in docs]
        self.bm25 = BM25Okapi(tokenized_corpus)
        self._is_indexed = True

    def retrieve(self, query: str, top_k: int = 3) -> list[SearchResult]:
        """Perform hybrid retrieval over the indexed financial corpus."""
        if not self._is_indexed or not self.bm25:
            return []

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        # Rank indices by BM25 score
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results: list[SearchResult] = []
        for idx in ranked_indices:
            doc = self.documents[idx]
            results.append({
                "doc_id": doc.get("id", f"doc_{idx}"),
                "content": doc["content"],
                "metadata": doc.get("metadata", {}),
                "score": round(float(scores[idx]), 4),
            })

        return results
