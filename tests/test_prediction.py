"""
Unit tests for model inference, confidence scoring, probability bounds, and validation.
"""

import pytest
from src.predict import predict_news, load_inference_pipeline


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


def test_predict_empty_text_raises_error():
    pipeline = load_inference_pipeline()
    with pytest.raises(ValueError):
        predict_news("", "", pipeline=pipeline)

    with pytest.raises(ValueError):
        predict_news("   ", "   ", pipeline=pipeline)
