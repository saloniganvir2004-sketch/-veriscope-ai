"""
Unit tests for model inference, confidence scoring, probability bounds, and validation.
"""

import pytest
from src.predict import predict_news, load_inference_pipeline
from src.preprocessing import prepare_input_text


def test_predict_real_news_sample():
    pipeline = load_inference_pipeline()
    headline = "Federal Reserve Holds Benchmark Interest Rates Steady"
    body = "The Federal Open Market Committee noted that inflation has eased over the past year."
    res = predict_news(headline, body, pipeline=pipeline)

    assert "prediction" in res
    assert res["prediction"] in ["Likely Real", "Likely Fake"]
    assert 0.0 <= res["confidence"] <= 1.0
    assert 0.0 <= res["probabilities"]["Likely Real"] <= 1.0
    assert 0.0 <= res["probabilities"]["Likely Fake"] <= 1.0
    assert abs(res["probabilities"]["Likely Real"] + res["probabilities"]["Likely Fake"] - 1.0) < 1e-3
    assert "linguistic_stats" in res
    assert "disclaimer" in res


def test_predict_fake_news_sample():
    pipeline = load_inference_pipeline()
    headline = "BOMBSHELL: Secret Alien Mothership Uncovered Under Ice Sheet"
    body = "Globalist puppet masters and corrupt elite cabals are panicking over leaked military documents!"
    res = predict_news(headline, body, pipeline=pipeline)

    assert res["prediction"] == "Likely Fake"
    assert res["confidence"] >= 0.5


def test_predict_headline_only_and_body_only():
    pipeline = load_inference_pipeline()
    # Headline only
    res_h = predict_news("Federal Reserve Holds Benchmark Rates Steady", "", pipeline=pipeline)
    assert res_h["prediction"] in ["Likely Real", "Likely Fake"]
    assert 0.0 <= res_h["confidence"] <= 1.0

    # Body only
    res_b = predict_news("", "The Federal Reserve concluded its monetary policy meeting today.", pipeline=pipeline)
    assert res_b["prediction"] in ["Likely Real", "Likely Fake"]
    assert 0.0 <= res_b["confidence"] <= 1.0


def test_prepare_input_text_contract():
    """Ensures input combination contract strictly matches training formatting."""
    combined = prepare_input_text("Test Headline", "Test article body text.")
    assert combined == "Test Headline. Test article body text."

    # Wire leakage removal in combination
    leaked = prepare_input_text("Headline", "WASHINGTON (Reuters) - The Senate voted today.")
    assert "Reuters" not in leaked
    assert "Senate voted today." in leaked


def test_predict_empty_text_raises_error():
    pipeline = load_inference_pipeline()
    with pytest.raises(ValueError):
        predict_news("", "", pipeline=pipeline)

    with pytest.raises(ValueError):
        predict_news("   ", "   ", pipeline=pipeline)
