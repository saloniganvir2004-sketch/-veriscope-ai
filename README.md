# VeriScope AI — Fake News Detection Using Explainable AI & Natural Language Inference

> **Tagline:** *Intelligence Beyond the Headline.*

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Testing](https://img.shields.io/badge/Pytest-47%20Passed-emerald.svg)](tests/)
[![Architecture](https://img.shields.io/badge/Models-LR%20%7C%20MNB%20%7C%20Linear%20SVM-cyan.svg)](src/)
[![NLI Engine](https://img.shields.io/badge/NLI-Cross--Encoder%20DeBERTa--v3-indigo.svg)](src/nli_verifier.py)
[![RL Engine](https://img.shields.io/badge/Contextual%20Bandit-Upper%20Confidence%20Bound-amber.svg)](src/evidence_bandit.py)
[![XAI Engines](https://img.shields.io/badge/Explainability-LIME%20%26%20SHAP-purple.svg)](src/)
[![OCR Engine](https://img.shields.io/badge/OCR-Tesseract%205.5-orange.svg)](src/ocr.py)

**VeriScope AI** is an advanced, locally runnable Machine Learning, Natural Language Inference (NLI), and Explainable Artificial Intelligence (XAI) platform. The application classifies news articles supplied via **direct text entry or image screenshots** as *Likely Fake* or *Likely Real*, verifies factual claims against an audited reference knowledge base using cross-encoder inference, and opens the algorithmic "black box" by rendering simultaneous local explanations via **LIME** and **SHAP**.

Beyond basic classification, VeriScope AI systematically evaluates explanation quality, feature agreement, perturbation stability, and causal faithfulness, presented through a refined editorial intelligence user interface.

---

## Everyday Use & Quick Launch (No Terminal Commands Required)

### 1. Launching VeriScope AI
- **One-Click Launch:** Double-click [`Start VeriScope.command`](Start%20VeriScope.command) in the project folder.
- **What happens automatically:**
  1. Checks for the local virtual environment and Python 3.12 interpreter.
  2. Inspects port `8502`. If an instance is already active and healthy, it reuses it without launching duplicate background processes.
  3. If not yet running, starts the Streamlit server in the background and writes logs to `logs/server.log`.
  4. Automatically opens `http://localhost:8502` in your default web browser.

### 2. Stopping VeriScope AI
- **One-Click Shutdown:** Double-click [`Stop VeriScope.command`](Stop%20VeriScope.command).
- Cleanly terminates the background Streamlit process using its recorded PID, releases port `8502`, and cleans up lock files.

### 3. Restarting VeriScope AI
- Double-click [`Stop VeriScope.command`](Stop%20VeriScope.command), followed by [`Start VeriScope.command`](Start%20VeriScope.command).

---

## MSc Project Team & Work Allocations

| Member # | Name | Enrolment No. | Assigned Responsibility |
|:---:|:---|:---|:---|
| **Member 1** | **Ayushman Kumar** | `A010175625019` | Dataset, Reference Corpus, and NLP Preprocessing |
| **Member 2** | **Astha Thapa** | `A010175625014` | Machine-Learning Classification Models and Hyperparameter Tuning |
| **Member 3** | **Saloni Ganvir** | `A010175625017` | Explainable AI (LIME & SHAP), NLI Cross-Encoder Verification |
| **Member 4** | **Sarvesh** | `A010175625016` | Web Application Architecture, Editorial UI, and OCR Integration |
| **Member 5** | **Sri Rinith** | `A010175625018` | Model Evaluation, Reinforcement Learning Bandit, Testing & Integration |

---

## Academic Subject Integration

| Academic Domain | Practical Implementation in VeriScope AI | Source Reference |
|:---|:---|:---|
| **Pattern Recognition & OCR** | Tesseract 5.5 OCR engine with orientation detection (OSD), contrast normalization, adaptive thresholding, and headline/body heuristic segmentation. | [`src/ocr.py`](src/ocr.py) |
| **Natural Language Processing (NLP)** | Publisher leakage mitigation, TF-IDF n-gram vectorization, and pre-trained Transformer / ONNX cross-encoder Natural Language Inference (`cross-encoder/nli-deberta-v3-base`). | [`src/preprocessing.py`](src/preprocessing.py), [`src/nli_verifier.py`](src/nli_verifier.py) |
| **Business Intelligence & Analytics** | Interactive executive dashboard, time-series analysis velocity tracking, distribution charts, and SQLite audit database with 3-calendar-month UTC retention policy. | [`app.py`](app.py), [`src/database.py`](src/database.py), [`pages/4_Analysis_History.py`](pages/4_Analysis_History.py) |
| **Reinforcement Learning** | Contextual Multi-Armed Bandit (Upper Confidence Bound - UCB1 / $\varepsilon$-greedy) that adaptively chooses between retrieval strategies using an objective, non-circular quality reward. | [`src/evidence_bandit.py`](src/evidence_bandit.py) |
| **Ethics & Social Responsibility** | Epistemic modesty disclosures, zero fabricated confidence, transparent provenance tiering, data privacy compliance, and explainable AI audit trails. | [`pages/5_About.py`](pages/5_About.py), [`pages/2_Explainable_AI_Lab.py`](pages/2_Explainable_AI_Lab.py) |

---

## Key Features & Capabilities

1. **Dual Input Modalities (Strictly Two Separate Workflows):**
   - **Option 1 — Manual Text Entry:** Separate inputs for News Headline and News Context / Article Text with character/word counters, demonstration samples, required-field validation, and session-state preservation.
   - **Option 2 — Image OCR (Tesseract + Pillow):** Upload news screenshots or photos (PNG, JPG, JPEG, WEBP). Automatically performs EXIF orientation transpose, rotation correction (OSD), resolution normalization, high-contrast grayscale filtering, and edge sharpening. Extracted text is separated into candidate headline and context, editable before analysis.

2. **Genuine Natural Language Inference (NLI) Verification:**
   - Evaluates retrieved evidence passages (premises) against the user's headline (hypothesis) using cross-encoder architectures (`cross-encoder/nli-deberta-v3-base` / `small` or ONNX runtime).
   - Generates genuine probabilities for **Entailment**, **Contradiction**, and **Neutral**.
   - Aggregates multi-passage verdicts conservatively: returns `Supported by Available Evidence`, `Contradicted by Available Evidence`, or `Insufficient Evidence`. Automatically detects and flags **conflicting evidence** when both high-entailment and high-contradiction passages are present.
   - Strictly honest fallback: when weights are not present offline, it reports `Insufficient Evidence` with diagnostic details without fabricating synthetic confidence scores.

3. **Objective Reinforcement Learning Bandit:**
   - Multi-armed contextual bandit adaptively selects retrieval parameters (balanced vs dense coverage).
   - Non-circular reward function evaluating objective retrieval properties:
     $$R = 0.50 \cdot S_{\text{rel}} + 0.30 \cdot E_{\text{cov}} + 0.20 \cdot M_{\text{nli}}$$
     where $S_{\text{rel}}$ is cosine similarity, $E_{\text{cov}}$ is named entity overlap, and $M_{\text{nli}} = |P(\text{entailment}) - P(\text{contradiction})|$ is the NLI decisiveness margin.

4. **Dual Explainable AI Engines:**
   - **LIME:** Local surrogate ridge regression fitted over Monte Carlo text perturbations.
   - **SHAP:** Game-theoretic Shapley feature attributions computed in $<100\text{ ms}$ via optimized linear log-odds decomposition.

5. **Systematic XAI Research Suite:**
   - **Top-$k$ Jaccard Agreement:** Measures feature overlap between LIME and SHAP across benchmark dispatches.
   - **Directional Sign Concordance:** Evaluates whether both explainers agree on the sign of influence (100% agreement on shared tokens).
   - **Perturbation Stability:** Tests explanation resilience under typographical noise.
   - **Token Masking Faithfulness:** Confirms that removing top highlighted words causes a dramatic confidence drop compared to masking random words.

6. **Data Leakage Mitigation:**
   - Automatically sanitizes publisher headers, wire-service signatures (e.g., `(Reuters)`, `(AP)`, `WASHINGTON —`), and editorial metadata to prevent models from learning spurious publisher artifacts.

7. **Calibrated Machine Learning Pipeline:**
   - Evaluates **Logistic Regression**, **Multinomial Naive Bayes**, and **Linear Support Vector Machine**.
   - Applies **Platt Scaling** (`CalibratedClassifierCV`) to Linear SVM to produce mathematically bounded confidence probabilities rather than raw uncalibrated geometric margins.

8. **Automatic 3-Calendar-Month Retention Policy:**
   - Persistent SQLite audit history automatically purges records older than 3 calendar months (UTC), correctly accounting for leap years, varying month lengths, and month-end dates.

9. **Refined Editorial Intelligence UI/UX:**
   - Bright editorial design system featuring warm ivory surfaces (`#FBFBFD`), deep midnight ink typography (`#0B1528`), rich cobalt blue primary actions (`#1D4ED8`), restrained verification badges, and local vector illustrations. Zero raw SVG/HTML code, zero fake stats, zero viva questions.

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
./venv/bin/python -m pytest -v
```
*All 47 automated tests validate NLI conflict detection, fallback handling, deduplication, RL bandit rewards, OCR image extraction, leakage sanitization, inference, LIME, SHAP, SQLite retention, and Streamlit UI page workflows.*

### 4. Launching the Web Application
```bash
# Option A: One-Click GUI Launcher
./Start\ VeriScope.command

# Option B: Manual Terminal Execution
./venv/bin/python -m streamlit run app.py --server.port 8502
```
Open your browser at `http://localhost:8502`.

---

## Research Disclaimer

> **Research Notice & Epistemic Boundaries:**
> *VeriScope AI predicts whether news resembles patterns in its training data. Predictions and feature explanations are not definitive evidence of factual truth. Verify important claims using reliable sources.*
