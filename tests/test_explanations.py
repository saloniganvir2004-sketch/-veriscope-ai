"""
Unit tests for Explainable AI (LIME and SHAP) modules.
"""

import pytest
from src.predict import load_inference_pipeline
from src.lime_explainer import VeritasLimeExplainer
from src.shap_explainer import VeritasShapExplainer
from src.explanation_evaluation import compute_top_k_agreement, evaluate_feature_fidelity


def test_lime_explainer_structure():
    pipeline = load_inference_pipeline()
    explainer = VeritasLimeExplainer(pipeline)
    text = "Federal Reserve holds benchmark interest rates steady as inflation decelerates."
    exp = explainer.explain(text, num_features=5, num_samples=100)

    assert exp["method"] == "LIME"
    assert exp["available"] is True
    assert len(exp["top_features"]) > 0
    assert "fake_contributing" in exp
    assert "real_contributing" in exp
    for item in exp["top_features"]:
        assert "feature" in item
        assert "weight" in item
        assert item["pushes_toward"] in ["Likely Real", "Likely Fake"]


def test_shap_explainer_structure():
    pipeline = load_inference_pipeline()
    explainer = VeritasShapExplainer(pipeline)
    text = "BOMBSHELL report reveals secret globalist conspiracy and shocking alien coverup!"
    exp = explainer.explain(text, top_k=5)

    assert exp["method"] == "SHAP"
    assert exp["available"] is True
    assert len(exp["top_features"]) > 0
    for item in exp["top_features"]:
        assert "feature" in item
        assert "weight" in item
        assert item["pushes_toward"] in ["Likely Real", "Likely Fake"]


def test_short_text_handling():
    pipeline = load_inference_pipeline()
    lime_exp = VeritasLimeExplainer(pipeline)
    shap_exp = VeritasShapExplainer(pipeline)

    l_res = lime_exp.explain("Hello")
    assert l_res["available"] is False

    s_res = shap_exp.explain("Hi")
    assert s_res["available"] is False


def test_agreement_computation():
    lime_feats = [
        {"feature": "rate", "weight": -0.4, "pushes_toward": "Likely Real"},
        {"feature": "reserve", "weight": -0.3, "pushes_toward": "Likely Real"},
        {"feature": "inflation", "weight": -0.2, "pushes_toward": "Likely Real"},
    ]
    shap_feats = [
        {"feature": "rate", "weight": -0.5, "pushes_toward": "Likely Real"},
        {"feature": "reserve", "weight": -0.3, "pushes_toward": "Likely Real"},
        {"feature": "bank", "weight": -0.1, "pushes_toward": "Likely Real"},
    ]

    agreement = compute_top_k_agreement(lime_feats, shap_feats, k=3)
    assert agreement["k"] == 3
    assert agreement["overlap_count"] == 2
    assert "rate" in agreement["overlap_words"]
    assert "reserve" in agreement["overlap_words"]
    assert agreement["directional_concordance"] == 1.0
