"""
VERITAS AI - Evidence Retrieval Module (Optional Advanced Feature)
Performs local passage retrieval against a curated reference corpus of verified facts
and debunked claims without relying on external or paid cloud APIs.
"""

from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Local verified reference corpus with clear provenance and sources
LOCAL_REFERENCE_CORPUS = [
    {
        "id": "REF-001",
        "title": "Federal Reserve Monetary Policy Statement (Federal Reserve Board)",
        "source": "Federal Reserve Official Dispatches",
        "date": "2024-05-01",
        "claim_status": "Official Record",
        "passage": (
            "The Federal Open Market Committee decided to maintain the target range for the federal funds rate "
            "at 5.25 to 5.50 percent. The Committee does not expect it will be appropriate to reduce the target "
            "range until it has gained greater confidence that inflation is moving sustainably toward 2 percent."
        ),
    },
    {
        "id": "REF-002",
        "title": "Fact-Check: Dark Zenith Satellite Voting Pulse Claims (Snopes / PolitiFact)",
        "source": "Independent Fact-Checking Network Archive",
        "date": "2024-02-15",
        "claim_status": "Debunked Disinformation",
        "passage": (
            "Claims that an orbital military satellite named 'Dark Zenith' emitted electromagnetic pulses to "
            "manipulate electronic voting machines are completely fabricated. Voting tabulators operate on air-gapped, "
            "isolated systems with paper audit trails, and no such satellite or frequency transmission exists."
        ),
    },
    {
        "id": "REF-003",
        "title": "NASA Goddard Space Flight Center: Exoplanet Atmosphere Observations",
        "source": "NASA Science Mission Directorate",
        "date": "2023-11-22",
        "claim_status": "Verified Scientific Finding",
        "passage": (
            "NASA's James Webb Space Telescope observed sulfur dioxide, water vapor, and carbon dioxide in the "
            "atmosphere of exoplanet WASP-39 b using near-infrared spectrographs. The observation provides direct "
            "evidence of photochemistry driven by starlight on an exoplanet."
        ),
    },
    {
        "id": "REF-004",
        "title": "Fact-Check: Dandelion Extract Cures Cancer Overnight (Memorial Sloan Kettering / Reuters Fact Check)",
        "source": "Medical Fact Check Archive",
        "date": "2023-08-10",
        "claim_status": "Debunked Disinformation",
        "passage": (
            "Viral claims asserting that dandelion tea or root extract dissolves malignant cancer tumors in 24 hours "
            "are medically unfounded and dangerous. While laboratory in vitro cell studies have examined plant compounds, "
            "there is zero clinical trial evidence demonstrating efficacy in humans, and patients should never substitute "
            "unverified herbal infusions for standard oncology care."
        ),
    },
    {
        "id": "REF-005",
        "title": "World Economic Forum: Backyard Vegetable Gardening Policies",
        "source": "World Economic Forum Communications Office",
        "date": "2024-01-18",
        "claim_status": "Debunked Hoax",
        "passage": (
            "Social media posts claiming the World Economic Forum has mandated a global ban on private backyard "
            "vegetable gardens are false. The WEF has no regulatory authority over domestic agriculture, and no such "
            "policy proposal or decree has ever been published or proposed."
        ),
    },
    {
        "id": "REF-006",
        "title": "Global Electricity Review 2024 (Ember Energy Think-Tank)",
        "source": "Ember Energy Research",
        "date": "2024-04-12",
        "claim_status": "Verified Statistical Record",
        "passage": (
            "Renewable energy generated over 30 percent of global electricity for the first time in 2023, driven by "
            "rapid solar and wind capacity expansion in China and the European Union. Clean power growth is expected "
            "to usher in a new era of declining fossil fuel generation."
        ),
    },
]


class LocalEvidenceRetriever:
    """
    Retrieves relevant passages from the local reference corpus using cosine similarity
    over TF-IDF representations.
    """

    def __init__(self, corpus: Optional[List[Dict[str, Any]]] = None):
        self.corpus = corpus or LOCAL_REFERENCE_CORPUS
        self.passages = [doc["passage"] for doc in self.corpus]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.passages)

    def retrieve(self, query: str, top_k: int = 3, threshold: float = 0.08) -> List[Dict[str, Any]]:
        """
        Retrieves top-k relevant passages from the local verified collection.
        Returns matching passages with similarity scores and clear status badges.
        """
        if not query or not query.strip():
            return []

        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        ranked_indices = sims.argsort()[::-1]

        results = []
        for idx in ranked_indices:
            score = float(sims[idx])
            if score >= threshold and len(results) < top_k:
                item = self.corpus[idx].copy()
                item["similarity_score"] = round(score, 4)
                results.append(item)

        return results
