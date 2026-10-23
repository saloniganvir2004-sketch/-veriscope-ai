"""
VERITAS AI - Unified Inference Engine
Handles text validation, feature transformation, probability estimation,
and classification scoring across supported models.
"""

import logging
from typing import Dict, Any, Optional
import numpy as np
import joblib

import config
from src.preprocessing import prepare_input_text, extract_linguistic_features

logger = logging.getLogger("VeritasPredict")


_CACHED_PIPELINE = None


def load_inference_pipeline(model_path=config.MODELS_DIR / "best_pipeline.joblib") -> Dict[str, Any]:
    """Loads and caches the best fitted pipeline."""
    global _CACHED_PIPELINE
    if _CACHED_PIPELINE is not None:
        return _CACHED_PIPELINE

    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained pipeline artifact not found at {model_path}. "
            "Please run 'python -m src.train' to train models first."
        )

    pipeline = joblib.load(model_path)
    _CACHED_PIPELINE = pipeline
    return pipeline


def predict_news(
    headline: str,
    body: str,
    pipeline: Optional[Dict[str, Any]] = None,
    remove_publisher_tags: bool = True,
) -> Dict[str, Any]:
    """
    Performs inference on a news article headline and body:
    1. Validates text integrity
    2. Sanitizes input (anti-leakage)
    3. Transforms via fitted TF-IDF
    4. Computes calibrated class probabilities
    5. Returns structured prediction with confidence and stylometry metrics
    """
    clean_headline = (headline or "").strip()
    clean_body = (body or "").strip()

    if not clean_headline and not clean_body:
        raise ValueError("Article headline or text body must not be empty.")

    if pipeline is None:
        pipeline = load_inference_pipeline()

    vectorizer = pipeline["vectorizer"]
    classifier = pipeline["classifier"]
    model_name = pipeline.get("model_name", "Classifier")

    # Combine & sanitize text
    combined_text = prepare_input_text(clean_headline, clean_body, remove_publisher_tags=remove_publisher_tags)
    if not combined_text.strip():
        raise ValueError("Submitted text contains no alphanumeric content after sanitization.")

    # Transform
    X_tfidf = vectorizer.transform([combined_text])

    # Probability estimation
    if hasattr(classifier, "predict_proba"):
        probabilities = classifier.predict_proba(X_tfidf)[0]
    elif hasattr(classifier, "decision_function"):
        # For raw linear classifiers lacking calibration, apply Platt-style logistic sigmoid
        raw_score = float(classifier.decision_function(X_tfidf)[0])
        prob_fake = 1.0 / (1.0 + np.exp(-raw_score))
        probabilities = np.array([1.0 - prob_fake, prob_fake])
    else:
        # Fallback to hard prediction
        hard_pred = classifier.predict(X_tfidf)[0]
        probabilities = np.array([1.0, 0.0]) if hard_pred == 0 else np.array([0.0, 1.0])

    prob_real = float(probabilities[config.LABEL_REAL])
    prob_fake = float(probabilities[config.LABEL_FAKE])

    pred_idx = int(np.argmax(probabilities))
    prediction_label = config.LABEL_NAMES.get(pred_idx, "Unknown")
    confidence_score = float(probabilities[pred_idx])

    # Extract stylometric linguistic markers
    linguistic_stats = extract_linguistic_features(f"{clean_headline} {clean_body}")

    return {
        "headline": clean_headline,
        "combined_text": combined_text,
        "prediction": prediction_label,
        "predicted_class_idx": pred_idx,
        "confidence": round(confidence_score, 4),
        "probabilities": {
            "Likely Real": round(prob_real, 4),
            "Likely Fake": round(prob_fake, 4),
        },
        "model_name": model_name,
        "linguistic_stats": linguistic_stats,
        "disclaimer": config.DISCLAIMER_TEXT,
    }
