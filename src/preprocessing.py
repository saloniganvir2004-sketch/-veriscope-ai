"""
VERITAS AI - Text Preprocessing & Leakage Mitigation Module
Implements wire-service stripping, text normalization, linguistic stylometry metrics,
and TF-IDF vectorization.
"""

import re
import html
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

import config

logger = logging.getLogger("VeritasPreprocessing")


def strip_publisher_leakage(text: str) -> str:
    """
    Rigorously strips publisher names, wire-service datelines, and editorial signatures
    (e.g., 'WASHINGTON (Reuters) -', '(AP)', 'Reporting by John Doe; Editing by Jane Smith').

    This is critical in fake-news research to prevent TF-IDF models from achieving
    spurious 99%+ accuracy purely by memorizing 'reuters' or 'ap' publisher tokens.
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    sanitized = text

    # Remove leading city/dateline and wire service patterns
    # e.g., "WASHINGTON (Reuters) - The Federal Reserve..." -> "The Federal Reserve..."
    # e.g., "LONDON (AP) — British lawmakers..." -> "British lawmakers..."
    for pattern in config.WIRE_SERVICE_PATTERNS:
        sanitized = re.sub(pattern, " ", sanitized, flags=re.IGNORECASE)

    # Remove trailing editorial metadata commonly found in wire articles
    # e.g., "Reporting by..., editing by..."
    sanitized = re.sub(r"(Reporting by\s+[^;]+;\s*editing by\s+[^\n]+)", "", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"\(Editing by\s+[^\)]+\)", "", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"Additional reporting by\s+[^\n]+", "", sanitized, flags=re.IGNORECASE)

    return sanitized


def clean_text(text: str, remove_publisher_tags: bool = True) -> str:
    """
    Normalizes text while preserving stylometric features relevant for credibility assessment:
    - Strips URLs
    - Normalizes HTML entities
    - Cleans non-printable ASCII
    - Optionally removes wire-service signatures (anti-leakage)
    - Normalizes irregular whitespace
    """
    if not isinstance(text, str):
        return ""

    # Unescape HTML entities
    cleaned = html.unescape(text)

    # Remove URLs
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)

    # Remove publisher leakage if requested
    if remove_publisher_tags:
        cleaned = strip_publisher_leakage(cleaned)

    # Replace curly quotes and dashes with standard ASCII
    cleaned = cleaned.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    cleaned = cleaned.replace("—", "-").replace("–", "-")

    # Replace excessive repeated punctuation (e.g., '!!!!!' -> '!') while preserving presence
    cleaned = re.sub(r"!{2,}", "!", cleaned)
    cleaned = re.sub(r"\?{2,}", "?", cleaned)

    # Collapse multiple whitespaces and tabs
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def prepare_input_text(title: str, text: str, remove_publisher_tags: bool = True) -> str:
    """
    Combines headline title and body text into a coherent document for classification.
    """
    clean_title = clean_text(title or "", remove_publisher_tags=remove_publisher_tags)
    clean_body = clean_text(text or "", remove_publisher_tags=remove_publisher_tags)

    if clean_title and clean_body:
        return f"{clean_title}. {clean_body}"
    elif clean_title:
        return clean_title
    return clean_body


def extract_linguistic_features(text: str) -> Dict[str, Any]:
    """
    Extracts surface-level stylometric indicators often correlated with
    sensationalism, emotive manipulation, and clickbait in disinformation studies.
    """
    if not isinstance(text, str) or not text.strip():
        return {
            "char_count": 0,
            "word_count": 0,
            "caps_ratio": 0.0,
            "exclamation_count": 0,
            "question_count": 0,
            "avg_word_length": 0.0,
            "sensationalism_score": 0.0,
        }

    chars = len(text)
    words = text.split()
    word_count = len(words)

    # Uppercase letters count (excluding whitespace/punctuation)
    alpha_chars = [c for c in text if c.isalpha()]
    caps_count = sum(1 for c in alpha_chars if c.isupper())
    caps_ratio = (caps_count / len(alpha_chars)) if alpha_chars else 0.0

    exclamations = text.count("!")
    questions = text.count("?")

    avg_word_len = (sum(len(w) for w in words) / word_count) if word_count else 0.0

    # Heuristic stylometric index for UI insights (bounded 0.0 to 1.0)
    # Higher values correlate with clickbait/hyperbolic text
    sensationalism = min(1.0, (caps_ratio * 2.0) + (exclamations / max(1, word_count) * 20.0))

    return {
        "char_count": chars,
        "word_count": word_count,
        "caps_ratio": round(caps_ratio, 4),
        "exclamation_count": exclamations,
        "question_count": questions,
        "avg_word_length": round(avg_word_len, 2),
        "sensationalism_score": round(sensationalism, 4),
    }


def create_vectorizer(custom_config: Optional[dict] = None) -> TfidfVectorizer:
    """Instantiates a TfidfVectorizer with project configuration."""
    cfg = config.TFIDF_CONFIG.copy()
    if custom_config:
        cfg.update(custom_config)
    return TfidfVectorizer(**cfg)


def fit_and_save_vectorizer(texts: List[str], save_path: Path = config.MODELS_DIR / "tfidf_vectorizer.joblib", custom_config: Optional[dict] = None) -> TfidfVectorizer:
    """Fits TfidfVectorizer strictly on training texts and serializes to disk."""
    vec = create_vectorizer(custom_config)
    logger.info(f"Fitting TF-IDF vectorizer on {len(texts)} training texts...")
    vec.fit(texts)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(vec, save_path)
    logger.info(f"Fitted vectorizer saved to {save_path} (Vocab size: {len(vec.vocabulary_)})")
    return vec


def load_vectorizer(path: Path = config.MODELS_DIR / "tfidf_vectorizer.joblib") -> TfidfVectorizer:
    """Loads fitted TfidfVectorizer from disk."""
    if not path.exists():
        raise FileNotFoundError(f"Fitted vectorizer not found at {path}. Run training first.")
    return joblib.load(path)
