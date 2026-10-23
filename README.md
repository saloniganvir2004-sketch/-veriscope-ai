# VeriScope AI — Fake News Detection Using Explainable AI

> **Tagline:** *Intelligence Beyond the Headline.*

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Testing](https://img.shields.io/badge/Pytest-23%20Passed-emerald.svg)](tests/)
[![Architecture](https://img.shields.io/badge/Models-LR%20%7C%20MNB%20%7C%20Linear%20SVM-cyan.svg)](src/)
[![XAI Engines](https://img.shields.io/badge/Explainability-LIME%20%26%20SHAP-purple.svg)](src/)
[![OCR Engine](https://img.shields.io/badge/OCR-Tesseract%205.5-orange.svg)](src/ocr.py)

**VeriScope AI** is a research-grade, locally runnable Machine Learning and Explainable Artificial Intelligence (XAI) platform. The application classifies news articles supplied as **direct text or image screenshots** as *Likely Fake* or *Likely Real*, and opens the algorithmic "black box" by rendering simultaneous local explanations via **LIME** and **SHAP**.

Beyond basic classification, VeriScope AI systematically evaluates explanation quality, feature agreement, perturbation stability, and causal faithfulness, presented through a refined editorial intelligence user interface.

---

## Key Features & Capabilities

1. **Dual Input Modalities (Text & Screenshot OCR):**
   - **Direct Text Input:** Headline and full article body with word/character counters, demonstration samples, and input preservation.
   - **Image OCR (Tesseract + PIL):** Upload news screenshots or photos (JPG, PNG, WEBP). Automatically performs EXIF orientation transpose, resolution normalization, high-contrast grayscale filtering, and edge sharpening. Extracted text is presented in an editable window for review before classification.
2. **Dual Explainable AI Engines:**
   - **LIME:** Local surrogate ridge regression fitted over Monte Carlo text perturbations.
   - **SHAP:** Game-theoretic Shapley feature attributions computed in $<100\text{ ms}$ via optimized linear log-odds decomposition.
3. **Systematic XAI Research Suite:**
   - **Top-$k$ Jaccard Agreement:** Measures feature overlap between LIME and SHAP across benchmark dispatches.
   - **Directional Sign Concordance:** Evaluates whether both explainers agree on the sign of influence (100% agreement on shared tokens).
   - **Perturbation Stability:** Tests explanation resilience under typographical noise.
   - **Token Masking Faithfulness:** Confirms that removing top highlighted words causes a dramatic confidence drop compared to masking random words.
4. **Data Leakage Mitigation:**
   - Automatically sanitizes publisher headers, wire-service signatures (e.g., `(Reuters)`, `(AP)`, `WASHINGTON —`), and editorial metadata to prevent models from learning spurious publisher artifacts.
5. **Calibrated Machine Learning Pipeline:**
   - Evaluates **Logistic Regression**, **Multinomial Naive Bayes**, and **Linear Support Vector Machine**.
   - Applies **Platt Scaling** (`CalibratedClassifierCV`) to Linear SVM to produce mathematically bounded confidence probabilities rather than raw uncalibrated geometric margins.
6. **Contextual Evidence Retrieval (Local Reference Corpus):**
   - Offline cosine similarity passage retrieval matching submitted claims against verified reference dispatches and fact-check archives.
7. **Persistent SQLite Audit Database:**
   - Audits past investigations with real-time KPI counters, keyword search, class filtering, and CSV export.
8. **Refined Editorial Intelligence UI/UX:**
   - Warm off-white reading surfaces (`#F8F9FA`), deep midnight ink typography (`#0F172A`), muted teal accents, restrained sage/coral status badges, and local vector illustrations.

---

## Project Structure

```
veritas-ai/
├── app.py                      # Main entrypoint & editorial portal
├── config.py                   # Central configuration & parameters
├── requirements.txt            # Pinned dependencies for Python 3.12
├── pytest.ini                  # Pytest configuration
├── README.md                   # Complete documentation & replication guide
├── .gitignore                  # Git exclusions
├── assets/
│   ├── hero_editorial.svg      # Vector illustration for dashboard hero
│   └── empty_audit.svg         # Clean line-art illustration for empty states
├── pages/
│   ├── 1_Dashboard.py          # Hero, key KPIs & recent audit log
│   ├── 2_News_Analyzer.py      # Dual input workspace (Text & Image OCR), LIME/SHAP
│   ├── 3_Explainable_AI_Lab.py # Side-by-side XAI comparison & stability tests
│   ├── 4_Model_Performance.py  # Model comparison, calibration & confusion matrices
│   ├── 5_Analysis_History.py   # SQLite-backed persistent audit log & CSV export
│   └── 6_About.py              # Methodology, mathematical formulas & MSc Viva preparation
├── src/
│   ├── ocr.py                  # Image decoding, preprocessing & Tesseract OCR
│   ├── data_loader.py          # Dataset acquisition, validation & splitting
│   ├── preprocessing.py        # Leakage removal, text normalization & TF-IDF
│   ├── train.py                # Multi-model training, calibration & artifact export
│   ├── evaluate.py             # Evaluation metrics & confusion matrix generators
│   ├── predict.py              # Unified inference engine with confidence scoring
│   ├── lime_explainer.py       # Independent LIME module
│   ├── shap_explainer.py       # Independent SHAP LinearExplainer module
│   ├── explanation_evaluation.py # XAI research suite (Jaccard, stability, fidelity)
│   ├── evidence_retriever.py   # Local offline reference passage retriever
│   ├── database.py             # SQLite CRUD operations
│   └── utils.py                # Editorial CSS, Plotly charts & token highlighter
├── data/
│   ├── raw/                    # Raw source CSVs
│   └── processed/              # Stratified train, val, test splits
├── artifacts/
│   ├── models/                 # Fitted pipeline (best_pipeline.joblib) & candidates
│   ├── metrics/                # model_comparison.json, confusion_matrices.json
│   ├── xai_experiments/        # Precomputed empirical research study results
│   └── veritas_history.db      # SQLite persistent storage
├── tests/
│   ├── test_ocr.py             # OCR decoding & synthetic image tests
│   ├── test_preprocessing.py   # Preprocessing & leakage tests
│   ├── test_prediction.py      # Inference & confidence bounds tests
│   ├── test_explanations.py    # LIME/SHAP structure & agreement tests
│   ├── test_evidence.py        # Local evidence retrieval tests
│   └── test_database.py        # SQLite storage & deletion tests
└── reports/
    └── model_evaluation_report.md # Academic evaluation report
```

---

## Local Setup & Quickstart (macOS)

### 1. Prerequisites
- **Python 3.12**
- **Tesseract OCR Engine:**
  If not already installed, install via Homebrew:
  ```bash
  brew install tesseract
  ```
  *(Already installed on macOS at `/opt/homebrew/bin/tesseract`)*

### 2. Environment Activation & Dependencies
```bash
cd /Users/saloniganvir/.gemini/antigravity/scratch/veritas-ai
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Automated Test Verification
Run the complete unit and integration test suite:
```bash
pytest
```
*All 23 automated tests validate OCR image extraction, leakage sanitization, inference, LIME, SHAP, and SQLite persistence.*

### 4. Launching the Web Application
Start the Streamlit application:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## Research Disclaimer

> **Research Notice & Epistemic Boundaries:**  
> *VeriScope AI predicts whether news resembles patterns in its training data. Predictions and feature explanations are not definitive evidence of factual truth. Verify important claims using reliable sources.*
