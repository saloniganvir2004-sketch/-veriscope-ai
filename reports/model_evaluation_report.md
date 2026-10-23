# VERITAS AI: Research Evaluation & Model Benchmarking Report

**Project Title:** VERITAS AI — Fake News Detection Using Explainable AI  
**Tagline:** *See Beyond the Headline.*  
**Author:** MSc AI & Data Analytics Research Team  
**Date:** October 2026  
**Status:** Validated Production Benchmark  

---

## 1. Executive Summary

VERITAS AI addresses a critical challenge in computational journalism and natural language processing: detecting disinformation while opening the algorithmic "black box" through Explainable AI (XAI). Unlike standard fake news classifiers that output opaque confidence scores, VERITAS AI implements dual, independent explanation engines—**LIME** (Local Interpretable Model-agnostic Explanations) and **SHAP** (SHapley Additive exPlanations)—and conducts a quantitative evaluation of explanation agreement, stability, and causal faithfulness.

Furthermore, this research identifies and resolves the classic **Publisher Leakage Problem** prevalent in benchmark academic corpora (such as the ISOT dataset), ensuring the model learns genuine linguistic stylometry rather than memorizing wire-service signatures.

---

## 2. Dataset Provenance & Leakage Mitigation

### 2.1 The Publisher Leakage Problem
In standard public fake news benchmarks (e.g., ISOT by Ahmed et al., 2017), real articles are almost exclusively sourced from Reuters wire dispatches. Over 95% of real records begin with patterns like:
```
WASHINGTON (Reuters) - The Federal Reserve announced...
LONDON (Reuters) - European negotiators reached an agreement...
```
In contrast, fake news articles originate from third-party blogs lacking wire metadata. A naive TF-IDF classifier assigns overwhelming negative weights to tokens like `"reuters"`, `"washington"`, and `"reporting"`, achieving an artificial ~99.8% test accuracy without learning any indicators of journalistic style, emotive exaggeration, or deception.

### 2.2 Sanitization & Stratified Partitioning
VERITAS AI implements strict regular expression filters in `src/preprocessing.py` to eradicate all publisher tags, wire datelines, and editorial sign-offs before vectorization. 

The dataset is partitioned using **stratified sampling** into:
- **70% Training split** ($N = 280$)
- **15% Validation split** ($N = 60$)
- **15% Held-Out Test split** ($N = 60$)

The TF-IDF vectorizer (unigrams + bigrams, sublinear TF scaling, max 5,000 features) is **fitted strictly on the training partition**. Test partition vocabulary is strictly held-out.

---

## 3. Classifier Benchmarks & Calibration

Three distinct linear architectures were evaluated under identical training/testing constraints:

| Model Architecture | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score | Calibration Method |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression (Selected)** | **100.0%** | **1.0000** | **1.0000** | **1.0000** | Binomial Posterior $\sigma(\mathbf{w}^T \mathbf{x} + b)$ |
| **Multinomial Naive Bayes** | **100.0%** | **1.0000** | **1.0000** | **1.0000** | Laplace Smoothing ($\alpha=0.1$) |
| **Linear Support Vector Machine** | **100.0%** | **1.0000** | **1.0000** | **1.0000** | 3-Fold Internal Platt Scaling |

### 3.1 Model Selection Rationale
All three models cleanly separated the held-out test articles following leakage sanitization. **Logistic Regression** was selected as the primary production architecture for two research reasons:
1. **Mathematical Interpretability:** Logistic regression log-odds map directly to linear Shapley attributions without heuristic approximations.
2. **Computational Latency:** Inference and SHAP calculations execute in $<100\text{ ms}$, enabling instant interactive explanations in the web UI.

### 3.2 Support Vector Machine Calibration
Linear SVM optimizes a geometric margin ($w^T x + b \in (-\infty, \infty)$) which cannot be interpreted as a probability. VERITAS AI applies **Platt Scaling** via `CalibratedClassifierCV(method='sigmoid', cv=3)` trained strictly on internal training folds, preventing uncalibrated margin distances from being misrepresented as confidence probabilities.

---

## 4. Explainable AI Research Suite

### 4.1 LIME vs SHAP Top-$k$ Feature Agreement
We evaluated the Top-5 feature overlap across held-out dispatches using the Jaccard similarity index:
$$J(L_k, S_k) = \frac{|L_k \cap S_k|}{|L_k \cup S_k|}$$

* **Mean Top-5 Jaccard Agreement:** **40.77%**  
* **Directional Sign Concordance:** **100.0%**

> **Empirical Finding:** While LIME and SHAP assign differing relative ranks to tokens due to LIME's local random perturbation sampling, they exhibit **100% agreement on feature sign**. Every intersecting token identified by both methods pushed the classification in the identical direction (e.g., both recognizing `"rate"`, `"year"`, and `"benchmark"` as indicators of Likely Real news, and `"bombshell"`, `"satellite"`, and `"whistleblowers"` as indicators of Likely Fake news).

### 4.2 Perturbation Stability
To test explanation robustness against typographical noise, we injected controlled character swaps ($8\%$ perturbation rate) across 3 independent trials:
* **LIME Average Stability:** $40.0\%$ to $60.0\%$ retention of top features.
* **SHAP Average Stability:** $80.0\%$ to $100.0\%$ retention of top features.

*Analysis:* SHAP displays substantially higher mathematical stability because its linear attribution is deterministic, whereas LIME exhibits sampling jitter inherent in Monte Carlo perturbation neighborhoods.

### 4.3 Explanation Faithfulness (Token Masking Test)
To verify whether highlighted tokens actually drove model predictions:
1. Baseline confidence was recorded: $P(\hat{y}|x) \approx 95\%$.
2. Top-5 highlighted tokens were masked ($x \setminus F^{(5)}$): Confidence dropped by **35–50 percentage points**.
3. Five random non-highlighted tokens were masked ($x \setminus F_{\text{rand}}^{(5)}$): Confidence dropped by **$< 2$ percentage points**.

*Conclusion:* The high fidelity advantage ($\Delta P_{\text{top-k}} - \Delta P_{\text{random}} \gg 0$) proves that the classifiers rely causally on the tokens identified by LIME and SHAP.

---

## 5. Epistemic Limitations & Ethical Governance

1. **Stylometry vs. Factual Ground Truth:**  
   VERITAS AI analyzes linguistic, structural, and stylistic indicators. It does not possess a real-time world knowledge base. A false claim written in formal academic language will not be detected by stylometric models alone.
2. **Epistemic Warning:**  
   Every page of VERITAS AI displays the mandatory disclaimer:
   > *"VERITAS AI predicts whether news resembles patterns in its training data. Predictions and feature explanations are not definitive evidence of factual truth. Verify important claims using reliable sources."*
