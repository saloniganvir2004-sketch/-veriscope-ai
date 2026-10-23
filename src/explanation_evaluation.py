"""
VERITAS AI - Explainable AI Research & Evaluation Suite
Conducts systematic empirical comparisons between LIME and SHAP explanations:
1. Top-k Feature Agreement (Jaccard Index & Directional Sign Alignment)
2. Perturbation-Based Explanation Stability
3. Feature Faithfulness & Fidelity via Token Masking Tests
4. Comparative Case Studies (True Positives vs Borderline/Misclassified Cases)
"""

import json
import random
import logging
from typing import Dict, Any, List, Set, Tuple
import numpy as np

import config
from src.predict import predict_news, load_inference_pipeline
from src.lime_explainer import VeritasLimeExplainer
from src.shap_explainer import VeritasShapExplainer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("VeritasXaiEval")


def compute_top_k_agreement(
    lime_features: List[Dict[str, Any]],
    shap_features: List[Dict[str, Any]],
    k: int = 5,
) -> Dict[str, Any]:
    """
    Computes quantitative agreement between LIME and SHAP top-k feature attributions:
    - Jaccard similarity: |L_k ∩ S_k| / |L_k ∪ S_k|
    - Overlap count: |L_k ∩ S_k|
    - Directional sign concordance: % of shared features that push in the same direction
    """
    top_lime = lime_features[:k]
    top_shap = shap_features[:k]

    words_lime = {item["feature"].lower() for item in top_lime}
    words_shap = {item["feature"].lower() for item in top_shap}

    intersection = words_lime.intersection(words_shap)
    union = words_lime.union(words_shap)

    jaccard = len(intersection) / len(union) if union else 0.0

    # Check directional agreement on intersecting words
    lime_dirs = {item["feature"].lower(): item["pushes_toward"] for item in top_lime}
    shap_dirs = {item["feature"].lower(): item["pushes_toward"] for item in top_shap}

    directional_matches = sum(1 for w in intersection if lime_dirs.get(w) == shap_dirs.get(w))
    directional_concordance = (directional_matches / len(intersection)) if intersection else 0.0

    return {
        "k": k,
        "jaccard_similarity": round(float(jaccard), 4),
        "overlap_count": len(intersection),
        "overlap_words": sorted(list(intersection)),
        "union_count": len(union),
        "directional_concordance": round(float(directional_concordance), 4),
    }


def perturb_text(text: str, noise_rate: float = 0.08, seed: int = 42) -> str:
    """
    Applies controlled character/token perturbations to evaluate explanation stability:
    Injects mild typographical noise without destroying semantic structure.
    """
    rng = random.Random(seed)
    words = text.split()
    if len(words) <= 3:
        return text

    num_words_to_perturb = max(1, int(len(words) * noise_rate))
    indices = rng.sample(range(len(words)), min(num_words_to_perturb, len(words)))

    perturbed_words = list(words)
    for idx in indices:
        w = perturbed_words[idx]
        if len(w) > 4:
            # Swap two adjacent inner characters
            char_list = list(w)
            swap_pos = rng.randint(1, len(char_list) - 2)
            char_list[swap_pos], char_list[swap_pos + 1] = char_list[swap_pos + 1], char_list[swap_pos]
            perturbed_words[idx] = "".join(char_list)

    return " ".join(perturbed_words)


def evaluate_explanation_stability(
    text: str,
    explainer_type: str = "LIME",
    k: int = 5,
    noise_rate: float = 0.08,
    trials: int = 3,
) -> Dict[str, Any]:
    """
    Evaluates how stable an explainer's top-k features are under input perturbations.
    Computes average Jaccard overlap between the base explanation and perturbed explanations.
    """
    pipeline = load_inference_pipeline()
    if explainer_type == "LIME":
        explainer = VeritasLimeExplainer(pipeline)
    else:
        explainer = VeritasShapExplainer(pipeline)

    base_exp = explainer.explain(text)
    base_features = [f["feature"].lower() for f in base_exp.get("top_features", [])[:k]]

    if not base_features:
        return {"stability_score": 0.0, "message": "Baseline explanation produced no features."}

    overlap_scores = []
    trial_details = []

    for trial_idx in range(trials):
        perturbed = perturb_text(text, noise_rate=noise_rate, seed=config.RANDOM_SEED + trial_idx)
        perturbed_exp = explainer.explain(perturbed)
        perturbed_features = [f["feature"].lower() for f in perturbed_exp.get("top_features", [])[:k]]

        set_base = set(base_features)
        set_pert = set(perturbed_features)

        union = set_base.union(set_pert)
        inter = set_base.intersection(set_pert)
        jaccard = len(inter) / len(union) if union else 0.0
        overlap_scores.append(jaccard)

        trial_details.append({
            "trial": trial_idx + 1,
            "perturbed_overlap": round(jaccard, 4),
            "common_words": list(inter),
        })

    avg_stability = float(np.mean(overlap_scores)) if overlap_scores else 0.0

    return {
        "explainer": explainer_type,
        "k": k,
        "average_stability_jaccard": round(avg_stability, 4),
        "trials": trial_details,
    }


def evaluate_feature_fidelity(
    text: str,
    top_features: List[Dict[str, Any]],
    k: int = 5,
) -> Dict[str, Any]:
    """
    Explanation Faithfulness / Fidelity test:
    Measures the drop in model classification confidence when top-k explained words
    are masked vs. when random words are masked.
    A faithful explanation will show a significantly higher confidence drop when
    its highlighted words are masked.
    """
    pipeline = load_inference_pipeline()
    base_pred = predict_news(headline="", body=text, pipeline=pipeline)
    pred_class_idx = base_pred["predicted_class_idx"]
    base_confidence = base_pred["confidence"]

    # Extract top-k words
    target_words = [f["feature"].lower() for f in top_features[:k]]
    tokens = text.split()

    # 1. Mask top-k words
    masked_tokens_top_k = [
        "[MASK]" if t.lower().strip(".,!?:;\"'") in target_words else t
        for t in tokens
    ]
    masked_text_top_k = " ".join(masked_tokens_top_k)
    pred_after_top_mask = predict_news(headline="", body=masked_text_top_k, pipeline=pipeline)
    top_k_confidence = pred_after_top_mask["confidence"]
    top_k_drop = base_confidence - top_k_confidence

    # 2. Mask random k words
    rng = random.Random(config.RANDOM_SEED)
    non_target_indices = [
        i for i, t in enumerate(tokens)
        if t.lower().strip(".,!?:;\"'") not in target_words and len(t) > 2
    ]
    sample_size = min(k, len(non_target_indices))
    random_indices = set(rng.sample(non_target_indices, sample_size)) if non_target_indices else set()

    masked_tokens_random = [
        "[MASK]" if i in random_indices else t
        for i, t in enumerate(tokens)
    ]
    masked_text_random = " ".join(masked_tokens_random)
    pred_after_random_mask = predict_news(headline="", body=masked_text_random, pipeline=pipeline)
    random_k_confidence = pred_after_random_mask["confidence"]
    random_drop = base_confidence - random_k_confidence

    # Relative fidelity impact
    fidelity_advantage = top_k_drop - random_drop

    return {
        "base_confidence": round(base_confidence, 4),
        "confidence_after_top_k_mask": round(top_k_confidence, 4),
        "top_k_drop": round(top_k_drop, 4),
        "confidence_after_random_mask": round(random_k_confidence, 4),
        "random_drop": round(random_drop, 4),
        "fidelity_advantage": round(fidelity_advantage, 4),
        "interpretation": (
            "High fidelity: model reliance on explained words confirmed."
            if fidelity_advantage > 0.05
            else "Moderate/Low fidelity: masked words alone did not disproportionately shift confidence."
        ),
    }


def run_comprehensive_xai_study():
    """
    Executes a precomputed empirical study comparing LIME and SHAP across
    representative Real and Fake news test cases.
    Saves results to artifacts/xai_experiments/xai_experiment_results.json.
    """
    logger.info("Executing comprehensive LIME vs SHAP comparative study...")
    pipeline = load_inference_pipeline()
    lime_exp = VeritasLimeExplainer(pipeline)
    shap_exp = VeritasShapExplainer(pipeline)

    test_cases = [
        {
            "id": "case_1_real",
            "type": "Clear Real",
            "headline": "Federal Reserve Holds Benchmark Interest Rates Steady",
            "body": "The Federal Open Market Committee noted that while job gains have remained solid and unemployment has stayed low, inflation has eased over the past year. Chairman Jerome Powell emphasized that policymakers require greater statistical confidence before initiating rate reductions.",
        },
        {
            "id": "case_2_fake",
            "type": "Clear Disinformation",
            "headline": "BOMBSHELL: Secret Satellite Transmits Brainwaves to Rig Election",
            "body": "A classified military satellite code-named Dark Zenith is secretly transmitting high-frequency electromagnetic pulses to voting machines! Unnamed sources reveal corrupt globalist puppet masters finalized their plot. Mainstream media fake news networks are in panic!",
        },
        {
            "id": "case_3_health_fake",
            "type": "Medical Disinformation",
            "headline": "Miracle Herbal Extract Dissolves Cancer Tumors Overnight",
            "body": "Doctors are STUNNED and pharmaceutical billionaires are furious! A groundbreaking natural dandelion miracle elixir eradicates malignant tumors within twenty-four hours. Corrupt medical agencies are arresting holistic doctors to suppress the secret cure!",
        },
        {
            "id": "case_4_science_real",
            "type": "Scientific News",
            "headline": "James Webb Space Telescope Observes Atmospheric Composition of Exoplanet",
            "body": "An international consortium of astrophysicists detected water vapor, carbon dioxide, and sulfur dioxide in an extrasolar planetary atmosphere using high-resolution infrared spectrographs. The findings establish a reliable benchmark for planetary chemistry.",
        },
    ]

    study_results = []

    for case in test_cases:
        full_text = f"{case['headline']}. {case['body']}"
        pred = predict_news(case["headline"], case["body"], pipeline=pipeline)

        l_res = lime_exp.explain(full_text)
        s_res = shap_exp.explain(full_text)

        agreement_k5 = compute_top_k_agreement(l_res.get("top_features", []), s_res.get("top_features", []), k=5)
        agreement_k10 = compute_top_k_agreement(l_res.get("top_features", []), s_res.get("top_features", []), k=10)

        fidelity_lime = evaluate_feature_fidelity(full_text, l_res.get("top_features", []), k=5)
        fidelity_shap = evaluate_feature_fidelity(full_text, s_res.get("top_features", []), k=5)

        stability_lime = evaluate_explanation_stability(full_text, explainer_type="LIME", k=5)
        stability_shap = evaluate_explanation_stability(full_text, explainer_type="SHAP", k=5)

        study_results.append({
            "case_id": case["id"],
            "type": case["type"],
            "headline": case["headline"],
            "prediction": pred["prediction"],
            "confidence": pred["confidence"],
            "lime_top_features": l_res.get("top_features", [])[:5],
            "shap_top_features": s_res.get("top_features", [])[:5],
            "agreement_k5": agreement_k5,
            "agreement_k10": agreement_k10,
            "fidelity": {
                "LIME": fidelity_lime,
                "SHAP": fidelity_shap,
            },
            "stability": {
                "LIME": stability_lime,
                "SHAP": stability_shap,
            },
        })

    # Summary statistics
    avg_jaccard_k5 = np.mean([c["agreement_k5"]["jaccard_similarity"] for c in study_results])
    avg_concordance = np.mean([c["agreement_k5"]["directional_concordance"] for c in study_results])

    overall_summary = {
        "total_cases_evaluated": len(study_results),
        "mean_top5_jaccard_agreement": round(float(avg_jaccard_k5), 4),
        "mean_directional_concordance": round(float(avg_concordance), 4),
        "cases": study_results,
    }

    out_file = config.EXPERIMENTS_DIR / "xai_experiment_results.json"
    with open(out_file, "w") as f:
        json.dump(overall_summary, f, indent=2)

    logger.info(f"XAI comparative study completed and saved to {out_file}")
    return overall_summary


if __name__ == "__main__":
    run_comprehensive_xai_study()
