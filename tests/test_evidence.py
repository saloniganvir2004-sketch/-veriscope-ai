"""
Unit tests for Local Evidence Retriever module.
"""

from src.evidence_retriever import LocalEvidenceRetriever


def test_evidence_retriever_query():
    retriever = LocalEvidenceRetriever()
    query = "Federal Reserve holds interest rates steady amid inflation"
    results = retriever.retrieve(query, top_k=2)

    assert len(results) > 0
    top_hit = results[0]
    assert "title" in top_hit
    assert "source" in top_hit
    assert "claim_status" in top_hit
    assert "passage" in top_hit
    assert top_hit["similarity_score"] > 0.0


def test_evidence_retriever_empty_query():
    retriever = LocalEvidenceRetriever()
    assert retriever.retrieve("") == []
    assert retriever.retrieve("   ") == []
