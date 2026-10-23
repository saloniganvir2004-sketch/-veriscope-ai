# VeriScope AI — Fake News Detection Using Explainable AI

> **Tagline:** *Intelligence Beyond the Headline.*

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Testing](https://img.shields.io/badge/Pytest-35%20Passed-emerald.svg)](tests/)
[![Architecture](https://img.shields.io/badge/Models-LR%20%7C%20MNB%20%7C%20Linear%20SVM-cyan.svg)](src/)
[![XAI Engines](https://img.shields.io/badge/Explainability-LIME%20%26%20SHAP-purple.svg)](src/)
[![OCR Engine](https://img.shields.io/badge/OCR-Tesseract%205.5-orange.svg)](src/ocr.py)

**VeriScope AI** is a research-grade, locally runnable Machine Learning and Explainable Artificial Intelligence (XAI) platform. The application classifies news articles supplied via **direct text entry or image screenshots** as *Likely Fake* or *Likely Real*, and opens the algorithmic "black box" by rendering simultaneous local explanations via **LIME** and **SHAP**.

Beyond basic classification, VeriScope AI systematically evaluates explanation quality, feature agreement, perturbation stability, and causal faithfulness, presented through a refined editorial intelligence user interface.

---

## MSc Project Team & Work Allocations

| Member # | Name | Enrolment No. | Assigned Responsibility |
|:---:|:---|:---|:---|
| **Member 1** | **Ayushman Kumar** | `A010175625019` | Dataset and NLP Preprocessing |
| **Member 2** | **Astha Thapa** | `A010175625014` | Machine-Learning Models and Tuning |
| **Member 3** | **Saloni Ganvir** | `A010175625017` | Explainable AI and Interpretation |
| **Member 4** | **Sarvesh** | `A010175625016` | Web Application and OCR Integration |
| **Member 5** | **Sri Rinith** | `A010175625018` | Evaluation, Testing and Integration |

---

## Key Features & Capabilities

1. **Dual Input Modalities (Strictly Two Separate Workflows):**
   - **Option 1 — Manual Text Entry:** Separate inputs for News Headline and News Context / Article Text with character/word counters, demonstration samples, required-field validation, and session-state preservation.
   - **Option 2 — Image OCR (Tesseract + Pillow):** Upload news screenshots or photos (PNG, JPG, JPEG, WEBP). Automatically performs EXIF orientation transpose, rotation correction (OSD), resolution normalization, high-contrast grayscale filtering, and edge sharpening. Extracted text is separated into candidate headline and context, editable before analysis.
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
6. **Automatic 3-Calendar-Month Retention Policy:**
   - Persistent SQLite audit history automatically purges records older than 3 calendar months (UTC), correctly accounting for leap years, varying month lengths, and month-end dates.
7. **Refined Editorial Intelligence UI/UX:**
   - Warm off-white reading surfaces (`#F8F9FA`), deep midnight ink typography (`#0F172A`), muted teal accents, restrained sage/coral status badges, and local vector illustrations.

---

## Local Setup & Quickstart (macOS)

### 1. Prerequisites
- **Python 3.12**
- **Tesseract OCR Engine:**
  If not already installed, install via Homebrew:
  ```bash
  brew install tesseract
  ```
  Verify installation:
  ```bash
  tesseract --version
  ```
  *(Detected automatically on macOS at `/opt/homebrew/bin/tesseract` or system PATH)*

### 2. Environment Activation & Dependencies
```bash
cd /Users/saloniganvir/Desktop/veritas-ai
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Automated Test Verification
Run the complete unit and integration test suite:
```bash
pytest
```
*All 35 automated tests validate OCR image extraction, leakage sanitization, inference, LIME, SHAP, SQLite retention, and Streamlit UI page workflows.*

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
