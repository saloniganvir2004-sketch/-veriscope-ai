"""
Unit tests for Local Evidence Retriever and RL Contextual Bandit modules.
"""

from src.evidence_retriever import LocalEvidenceRetriever
from src.evidence_bandit import EvidenceRetrievalBandit, compute_retrieval_reward


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


def test_verify_claim_supported():
    """Tests claim verification against official Federal Reserve interest rate records with NLI entailment."""
    retriever = LocalEvidenceRetriever()

    # Configure NLI verifier to return entailment for this pair
    def mock_sup(premise, hypothesis):
        return {
            "available": True,
            "probabilities": {"entailment": 0.94, "contradiction": 0.02, "neutral": 0.04},
            "stance": "SUPPORTS",
            "confidence": 0.94,
            "margin": 0.92,
            "premise": premise,
            "hypothesis": hypothesis,
            "model_name": "cross-encoder/nli-deberta-v3-base",
        }
    retriever.nli_verifier.set_mock_inference(mock_sup)

    headline = "Federal Reserve Holds Benchmark Interest Rates Steady Amid Inflation Data"
    body = "The Federal Reserve concluded its monetary policy meeting, voting to leave benchmark federal funds rate unchanged."
    res = retriever.verify_claim(headline, body)

    assert res["outcome"] == "Supported by Available Evidence"
    assert res["badge_style"] == "badge-real"
    assert len(res["sources"]) > 0
    assert "Federal Reserve" in res["reasoning"]
    assert res["strategy_used"] in ["entity_focused", "semantic_hybrid", "keyphrase_ngram"]
    assert res["nli_available"] is True


def test_verify_claim_contradicted():
    """Tests claim verification against documented fact-check debunking Antarctic bio-labs hoax with NLI contradiction."""
    retriever = LocalEvidenceRetriever()

    # Configure NLI verifier to return contradiction for this pair
    def mock_contra(premise, hypothesis):
        return {
            "available": True,
            "probabilities": {"entailment": 0.03, "contradiction": 0.92, "neutral": 0.05},
            "stance": "CONTRADICTS",
            "confidence": 0.92,
            "margin": 0.89,
            "premise": premise,
            "hypothesis": hypothesis,
            "model_name": "cross-encoder/nli-deberta-v3-base",
        }
    retriever.nli_verifier.set_mock_inference(mock_contra)

    headline = "Secret Deep State Military Bio-Labs Discovered Under Antarctic Ice Sheet"
    body = "Underground military bio-laboratories exposed by whistleblowers in Antarctica operating in secrecy."
    res = retriever.verify_claim(headline, body)

    assert res["outcome"] == "Contradicted by Available Evidence"
    assert res["badge_style"] == "badge-fake"
    assert len(res["sources"]) > 0
    assert "contradict" in res["reasoning"].lower()
    assert res["nli_available"] is True


def test_verify_claim_insufficient_evidence():
    """Tests claim verification for novel or uncorroborated story returning Insufficient Evidence."""
    retriever = LocalEvidenceRetriever()
    retriever.nli_verifier.set_mock_inference(None)
    headline = "Local Village Garden Club Hosts Annual Pumpkin Exhibition"
    body = "Community residents gathered to admire record-setting giant pumpkins grown in community allotments."
    res = retriever.verify_claim(headline, body)

    assert res["outcome"] == "Insufficient Evidence"
    assert res["badge_style"] == "badge-insufficient"
    assert "cannot be confirmed" in res["reasoning"].lower() or "no sufficiently corroborated" in res["reasoning"].lower()


def test_nli_verifier_conflict_detection():
    """Tests that conflicting evidence across retrieved sources triggers explicit conflict detection."""
    retriever = LocalEvidenceRetriever()
    call_count = 0

    def mock_conflict(premise, hypothesis):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "available": True,
                "probabilities": {"entailment": 0.85, "contradiction": 0.05, "neutral": 0.10},
                "stance": "SUPPORTS",
                "confidence": 0.85,
                "margin": 0.80,
                "premise": premise,
                "hypothesis": hypothesis,
            }
        else:
            return {
                "available": True,
                "probabilities": {"entailment": 0.05, "contradiction": 0.88, "neutral": 0.07},
                "stance": "CONTRADICTS",
                "confidence": 0.88,
                "margin": 0.83,
                "premise": premise,
                "hypothesis": hypothesis,
            }

    retriever.nli_verifier.set_mock_inference(mock_conflict)
    headline = "Federal Reserve Holds Benchmark Interest Rates Steady"
    body = "The Federal Reserve concluded its monetary policy meeting, voting to maintain target rates."
    res = retriever.verify_claim(headline, body, top_k=2)

    assert res["conflict_detected"] is True
    assert res["outcome"] == "Insufficient Evidence"
    assert "conflicting evidence detected" in res["reasoning"].lower()


def test_nli_verifier_support_only():
    """Tests aggregation when multiple passages independently support the claim."""
    from src.nli_verifier import NLIVerifier
    verifier = NLIVerifier()
    verifier.set_mock_inference(lambda premise, hypothesis: {
        "available": True,
        "probabilities": {"entailment": 0.88, "contradiction": 0.04, "neutral": 0.08},
        "stance": "SUPPORTS",
        "confidence": 0.88,
        "margin": 0.84,
        "premise": premise,
        "hypothesis": hypothesis,
    })
    passages = [
        {"id": "SRC-1", "passage": "First corroborating report", "publisher": "Reuters"},
        {"id": "SRC-2", "passage": "Second corroborating dispatch", "publisher": "Associated Press"},
    ]
    res = verifier.verify_claim_against_passages("A verified event happened", passages)
    assert res["conflict_detected"] is False
    assert res["support_count"] == 2
    assert res["contradict_count"] == 0
    assert res["final_verdict"] == "Supported by Available Evidence"
    assert res["overall_confidence"] >= 0.80


def test_nli_verifier_contradiction_only():
    """Tests aggregation when multiple passages independently refute the claim."""
    from src.nli_verifier import NLIVerifier
    verifier = NLIVerifier()
    verifier.set_mock_inference(lambda premise, hypothesis: {
        "available": True,
        "probabilities": {"entailment": 0.03, "contradiction": 0.92, "neutral": 0.05},
        "stance": "CONTRADICTS",
        "confidence": 0.92,
        "margin": 0.89,
        "premise": premise,
        "hypothesis": hypothesis,
    })
    passages = [
        {"id": "SRC-A", "passage": "Fact check refuting statement 1", "publisher": "PolitiFact"},
        {"id": "SRC-B", "passage": "Fact check refuting statement 2", "publisher": "Snopes"},
    ]
    res = verifier.verify_claim_against_passages("A fabricated conspiracy claim", passages)
    assert res["conflict_detected"] is False
    assert res["support_count"] == 0
    assert res["contradict_count"] == 2
    assert res["final_verdict"] == "Contradicted by Available Evidence"
    assert res["overall_confidence"] >= 0.90


def test_nli_verifier_neutral_only():
    """Tests that neutral evidence does not count as support or contradiction and does not trigger conflict."""
    from src.nli_verifier import NLIVerifier
    verifier = NLIVerifier()
    verifier.set_mock_inference(lambda premise, hypothesis: {
        "available": True,
        "probabilities": {"entailment": 0.20, "contradiction": 0.15, "neutral": 0.65},
        "stance": "NEUTRAL",
        "confidence": 0.65,
        "margin": 0.05,
        "premise": premise,
        "hypothesis": hypothesis,
    })
    passages = [
        {"id": "SRC-N1", "passage": "Unrelated background passage", "publisher": "Archive 1"},
        {"id": "SRC-N2", "passage": "Ambiguous commentary", "publisher": "Archive 2"},
    ]
    res = verifier.verify_claim_against_passages("Unverified claim", passages)
    assert res["conflict_detected"] is False
    assert res["support_count"] == 0
    assert res["contradict_count"] == 0
    assert res["neutral_count"] == 2
    assert res["final_verdict"] == "Insufficient Evidence"


def test_nli_verifier_duplicate_passages_deduplication():
    """Tests that duplicate passages (same ID or identical text) are deduplicated and not counted twice."""
    from src.nli_verifier import NLIVerifier
    verifier = NLIVerifier()
    call_count = 0
    def mock_counter(premise, hypothesis):
        nonlocal call_count
        call_count += 1
        return {
            "available": True,
            "probabilities": {"entailment": 0.85, "contradiction": 0.05, "neutral": 0.10},
            "stance": "SUPPORTS",
            "confidence": 0.85,
            "margin": 0.80,
            "premise": premise,
            "hypothesis": hypothesis,
        }
    verifier.set_mock_inference(mock_counter)
    # 3 passages with duplicate ID and identical text
    passages = [
        {"id": "REF-DUP-1", "passage": "Identical passage body text", "publisher": "Wire Service"},
        {"id": "REF-DUP-1", "passage": "Identical passage body text", "publisher": "Wire Service Duplicate"},
        {"id": "REF-DUP-2", "passage": "Identical passage body text", "publisher": "Mirror Service"},
    ]
    res = verifier.verify_claim_against_passages("Claim about duplicate wire", passages)
    assert len(res["passage_evaluations"]) == 1
    assert call_count == 1
    assert res["support_count"] == 1


def test_nli_verifier_fallback_when_model_unavailable():
    """Tests that when NLI model is unavailable, the system safely and honestly returns Insufficient Evidence."""
    from src.nli_verifier import NLIVerifier
    verifier = NLIVerifier()
    verifier.is_loaded = False
    verifier.load_error = "Model weights not downloaded in test environment"

    res = verifier.verify_claim_against_passages(
        claim="Some scientific claim",
        passages=[{"id": "P1", "passage": "Some reference passage text", "publisher": "Test Bureau"}],
    )
    assert res["nli_available"] is False
    assert res["final_verdict"] == "Insufficient Evidence"
    assert "could not be executed" in res["reasoning"].lower()


def test_rl_bandit_selection_and_update():
    """Tests the UCB1 Multi-Armed Bandit strategy selection, reward computation, and value estimation."""
    bandit = EvidenceRetrievalBandit()
    context = {"entity_count": 3, "word_count": 50, "sensationalism_score": 0.2}
    strategy, ucb_scores = bandit.select_strategy(context)

    assert strategy in bandit.strategies
    assert len(ucb_scores) == 3

    reward = compute_retrieval_reward(top_similarity=0.35, source_count=2, entity_coverage=1.0, nli_margin=0.8)
    assert 0.5 <= reward <= 1.0

    old_pulls = bandit.counts[strategy]
    bandit.update(strategy, reward)
    assert bandit.counts[strategy] == old_pulls + 1

    stats = bandit.get_summary_statistics()
    assert "total_decisions" in stats
    assert "strategy_pulls" in stats
    assert "estimated_values" in stats
    assert "best_current_strategy" in stats
