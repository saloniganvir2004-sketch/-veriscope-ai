"""
Unit tests for text preprocessing, leakage sanitization, and stylometric feature extraction.
"""

import pytest
from src.preprocessing import (
    strip_publisher_leakage,
    clean_text,
    prepare_input_text,
    extract_linguistic_features,
)


def test_strip_publisher_leakage_reuters():
    text = "WASHINGTON (Reuters) - The Federal Reserve decided to pause interest rate hikes on Wednesday."
    cleaned = strip_publisher_leakage(text)
    assert "Reuters" not in cleaned
    assert "WASHINGTON" not in cleaned
    assert "Federal Reserve" in cleaned


def test_strip_publisher_leakage_ap():
    text = "LONDON (AP) — British parliament voted to approve the budget."
    cleaned = strip_publisher_leakage(text)
    assert "AP" not in cleaned
    assert "British parliament" in cleaned


def test_strip_publisher_leakage_editorial_trailing():
    text = "A full market rally occurred. Reporting by John Smith; editing by Jane Doe."
    cleaned = strip_publisher_leakage(text)
    assert "Reporting by" not in cleaned
    assert "editing by" not in cleaned
    assert "A full market rally occurred." in cleaned


def test_clean_text_urls_and_html():
    raw = "Breaking news at https://example.com/test! Doctors &amp; scientists confirm findings."
    cleaned = clean_text(raw)
    assert "https://" not in cleaned
    assert "&amp;" not in cleaned
    assert "&" in cleaned
    assert "Doctors & scientists" in cleaned


def test_prepare_input_text():
    title = "Market Update"
    body = "Tech shares rebounded strongly on Friday."
    combined = prepare_input_text(title, body)
    assert combined == "Market Update. Tech shares rebounded strongly on Friday."


def test_extract_linguistic_features_sensational():
    text = "SHOCKING BOMBSHELL!!! CAN YOU BELIEVE THIS CONSPIRACY?!"
    stats = extract_linguistic_features(text)
    assert stats["exclamation_count"] >= 3
    assert stats["question_count"] >= 1
    assert stats["caps_ratio"] > 0.5
    assert stats["sensationalism_score"] > 0.5


def test_extract_linguistic_features_empty():
    stats = extract_linguistic_features("")
    assert stats["char_count"] == 0
    assert stats["word_count"] == 0
    assert stats["caps_ratio"] == 0.0
