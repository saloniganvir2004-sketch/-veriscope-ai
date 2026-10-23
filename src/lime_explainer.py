"""
VERITAS AI - LIME Explainer Module
Provides local interpretable model-agnostic explanations (LIME) for news articles.
Identifies influential words pushing predictions toward Likely Real or Likely Fake.
"""

import logging
from typing import Dict, Any, List, Optional
import numpy as np
from lime.lime_text import LimeTextExplainer

import config
from src.predict import load_inference_pipeline
from src.preprocessing import clean_text

logger = logging.getLogger("VeritasLime")


class VeritasLimeExplainer:
    """
    Encapsulates LIME text explanation logic with robust error handling,
    directional attribution separation, and structured visualization payload generation.
    """

    def __init__(self, pipeline: Optional[Dict[str, Any]] = None):
        if pipeline is None:
            pipeline = load_inference_pipeline()
        self.pipeline = pipeline
        self.vectorizer = pipeline["vectorizer"]
        self.classifier = pipeline["classifier"]
        self.class_names = pipeline.get("class_names", config.LABEL_CLASSES)

        self.explainer = LimeTextExplainer(
            class_names=self.class_names,
            split_expression=r"\W+",
            bow=False,
            random_state=config.LIME_CONFIG["random_state"],
        )

    def _predict_probabilities(self, texts: List[str]) -> np.ndarray:
        """Prediction function required by LIME returning an (N, 2) probability array."""
        cleaned_texts = [clean_text(t, remove_publisher_tags=True) for t in texts]
        X = self.vectorizer.transform(cleaned_texts)

        if hasattr(self.classifier, "predict_proba"):
            return self.classifier.predict_proba(X)
        elif hasattr(self.classifier, "decision_function"):
            scores = self.classifier.decision_function(X)
            p_fake = 1.0 / (1.0 + np.exp(-scores))
            return np.vstack([1.0 - p_fake, p_fake]).T
        else:
            preds = self.classifier.predict(X)
            probs = np.zeros((len(preds), 2))
            for i, p in enumerate(preds):
                probs[i, p] = 1.0
            return probs

    def explain(
        self,
        text: str,
        num_features: int = config.LIME_CONFIG["num_features"],
        num_samples: int = config.LIME_CONFIG["num_samples"],
    ) -> Dict[str, Any]:
        """
        Generates local explanation for input text.
        Returns:
            - word_attributions: full sorted list of (word, weight)
            - fake_contributing_words: words pushing toward Likely Fake (positive weights)
            - real_contributing_words: words pushing toward Likely Real (negative weights)
            - top_features: combined top influential words
            - explanation_score: LIME local model fidelity score (R^2)
        """
        cleaned = clean_text(text, remove_publisher_tags=True)
        tokens = cleaned.split()

        # Handle edge cases: empty or single-token inputs
        if len(tokens) < 2:
            return {
                "method": "LIME",
                "available": False,
                "message": "Text is too short to construct a valid perturbation neighborhood.",
                "top_features": [],
                "fake_contributing": [],
                "real_contributing": [],
                "intercept": 0.0,
                "local_fidelity_r2": 0.0,
            }

        try:
            exp = self.explainer.explain_instance(
                cleaned,
                self._predict_probabilities,
                num_features=num_features,
                num_samples=num_samples,
                labels=[config.LABEL_FAKE],  # Focus on class 1 (Likely Fake) direction
            )

            # In LIME, with labels=[1], positive weight pushes toward Fake, negative pushes toward Real
            raw_list = exp.as_list(label=config.LABEL_FAKE)

            top_features = []
            fake_contributing = []
            real_contributing = []

            for word, weight in raw_list:
                item = {
                    "feature": word,
                    "weight": round(float(weight), 4),
                    "pushes_toward": "Likely Fake" if weight > 0 else "Likely Real",
                    "magnitude": round(abs(float(weight)), 4),
                }
                top_features.append(item)
                if weight > 0:
                    fake_contributing.append(item)
                else:
                    real_contributing.append(item)

            # Sort by absolute magnitude
            top_features.sort(key=lambda x: x["magnitude"], reverse=True)
            fake_contributing.sort(key=lambda x: x["weight"], reverse=True)
            real_contributing.sort(key=lambda x: abs(x["weight"]), reverse=True)

            if isinstance(exp.intercept, dict):
                intercept = float(exp.intercept.get(config.LABEL_FAKE, 0.0))
            elif isinstance(exp.intercept, (list, np.ndarray)):
                intercept = float(exp.intercept[config.LABEL_FAKE]) if len(exp.intercept) > config.LABEL_FAKE else 0.0
            else:
                intercept = float(exp.intercept)

            if isinstance(exp.score, dict):
                score = float(exp.score.get(config.LABEL_FAKE, 0.0))
            elif isinstance(exp.score, (list, np.ndarray)):
                score = float(exp.score[config.LABEL_FAKE]) if len(exp.score) > config.LABEL_FAKE else 0.0
            else:
                score = float(exp.score)

            return {
                "method": "LIME",
                "available": True,
                "top_features": top_features,
                "fake_contributing": fake_contributing,
                "real_contributing": real_contributing,
                "intercept": round(intercept, 4),
                "local_fidelity_r2": round(score, 4),
            }

        except Exception as e:
            logger.error(f"LIME explanation generation failed: {e}")
            return {
                "method": "LIME",
                "available": False,
                "message": f"Explanation failed: {str(e)}",
                "top_features": [],
                "fake_contributing": [],
                "real_contributing": [],
                "intercept": 0.0,
                "local_fidelity_r2": 0.0,
            }
