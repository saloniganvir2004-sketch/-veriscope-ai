# VeriScope AI — Dataset Methodology & Empirical Benchmark Summary
*Academic Presentation Companion Guide (MSc Data Science / Machine Learning)*

---

## Dataset Overview

## 1. Dual-Tier Dataset Architecture

VeriScope AI employs a two-tier evaluation methodology: an extensive real-world empirical corpus (**ISOT Fake News Dataset**) for production evaluation, while preserving a controlled synthetic suite (**`benchmark_fake_news.csv`**) for rapid continuous regression testing.

| Metric / Dimension | Tier 1: Public Empirical Benchmark (ISOT) | Tier 2: Synthetic Regression Benchmark |
| :--- | :--- | :--- |
| **Dataset Provenance** | University of Victoria ISOT Lab (H. Ahmed et al.) | Curated Internal Verification Suite |
| **Storage Location** | `data/external/isot/True.csv`, `Fake.csv` | `data/raw/benchmark_fake_news.csv` |
| **Total Raw Records** | 44,898 records | 400 records |
| **Valid Non-Empty Records** | 44,267 records (631 empty dropped) | 400 records |
| **Unique Base Articles** | 38,583 unique canonical bodies | 16 discrete canonical documents |
| **Duplicate Body Count** | 5,600 duplicate copies quarantined | 384 duplicate dispatch copies |
| **Class Distribution** | 21,416 Likely Real / 22,851 Likely Fake | 200 Likely Real / 200 Likely Fake |
| **Zero-Leakage Partitions** | **Train: 30,869** \| **Val: 6,629** \| **Test: 6,685** | **Train: 300** \| **Val: 50** \| **Test: 50** |
| **Usage Role** | Primary Production Evaluation & viva proof | Development & Regression Testing |

---

## 2. Inclusion & Exclusion Criteria

### Inclusion Criteria
- **Likely Real Articles:** Factual reporting adhering to journalistic objectivity from verified wire services and international institutions (e.g., Reuters, Federal Reserve, NASA, WHO, European Parliament).
- **Likely Fake Articles:** Documented viral falsehoods, pseudoscientific medical claims, and conspiratorial narratives debunked by nonpartisan fact-checking organizations (PolitiFact, Snopes, Wikipedia).
- **Substantive Content:** Articles with at least 50 words of descriptive narrative body text to allow stylometric and n-gram lexical analysis.

### Exclusion Criteria
- **Empty / Media-Only Records:** 631 records containing no readable narrative text (e.g., placeholder video embeds or image-only tweets) were identified and pruned.
- **Pure Opinion / Editorial Columns:** Non-factual political commentary lacking verifiable assertions.
- **Micro-Claims:** Short social media snippets (< 25 words).

---

## 3. Preprocessing & Wire-Service Leakage Sanitization

### The Publisher Header Memorization Problem
In public fake-news benchmarks (such as ISOT or Kaggle datasets), classifiers frequently achieve spurious $99\%+$ accuracy simply by memorizing publisher datelines:
- Real articles in ISOT begin with wire tags: `"WASHINGTON (Reuters) -"` or `"SEATTLE/WASHINGTON (Reuters) -"`.
- Without sanitization, TF-IDF weights for `"reuters"` or `"ap"` dominate the decision boundary, leaving the model ineffective on articles published without wire headers.

### VeriScope AI Anti-Leakage Protocol
1. **Regex Dateline Stripping:** Extended regex systematically removes wire-service patterns, city datelines, and trailing editorial signatures:
   ```regex
   ^\s*([A-Za-z0-9\s/,\.]{2,40})?\s*\(\s*(Reuters|AP|Associated Press|Bloomberg|AFP)\s*\)\s*[-–—:]?\s*
   ```
2. **Text Normalization:** Lowercasing, HTML entity unescaping, URL removal, and punctuation regularization.
3. **Strict TF-IDF Fit Boundary:** The TF-IDF vocabulary ($5,000$ features, sublinear scaling) is **strictly fitted on the training split only (30,869 texts)**. The validation and test sets are transformed using the frozen training vocabulary.

---

## 4. Group-Based Stratified Splitting: Eliminating Optimistic Bias

### The Leakage Problem Identified
Many fake news articles in real-world collections were syndicated, re-posted, or re-published with slight headline tweaks.
- In ISOT, there are **5,600 duplicate copies of article bodies**.
- A naive row-level `train_test_split` scatters duplicate copies of the same article across Train, Validation, and Test sets.
- Evaluating a model on duplicate bodies seen during training causes severe optimistic bias.

### The Group-Aware Solution
VeriScope AI implements `leakage_safe_group_split`:
1. Normalized article bodies are hashed using SHA-256 (`body_hash`).
2. Label consistency is verified across identical bodies (0 conflicts detected).
3. Splitting operates strictly at the **group level**: all copies of any article body are assigned to the exact same partition.
4. **Zero-Leakage Invariant:**
   $$\text{Train}_{\text{hashes}} \cap \text{Val}_{\text{hashes}} = \emptyset, \quad \text{Train}_{\text{hashes}} \cap \text{Test}_{\text{hashes}} = \emptyset, \quad \text{Val}_{\text{hashes}} \cap \text{Test}_{\text{hashes}} = \emptyset$$

---

## 5. Model Architecture & Empirical Benchmark Results

Evaluated on the held-out test partition ($N=6,685$ unseen articles with zero duplicate leakage):

| Architecture | Test Accuracy | Macro F1 | Macro Precision | Macro Recall | Correct / Errors | Production Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **★ Linear SVM (Calibrated)** | **98.31%** | **0.9831** | **0.9829** | **0.9835** | **6,572 / 113** | **★ Selected Primary** |
| **Logistic Regression** | **98.37%** | **0.9837** | **0.9835** | **0.9840** | **6,576 / 109** | Production Candidate |
| **Multinomial Naive Bayes** | **94.45%** | **0.9444** | **0.9443** | **0.9445** | **6,314 / 371** | Candidate Architecture |

### Side-by-Side Confusion Matrices ($N=6,685$)

```
Linear SVM (Calibrated):        Logistic Regression:           Multinomial Naive Bayes:
       Pred Real  Pred Fake            Pred Real  Pred Fake           Pred Real  Pred Fake
True Real   [ 3185       19 ]   True Real   [ 3179       25 ]   True Real   [ 3029      175 ]
True Fake   [   94     3387 ]   True Fake   [   84     3397 ]   True Fake   [  196     3285 ]
(TN=3185, FP=19, FN=94, TP=3387) (TN=3179, FP=25, FN=84, TP=3397) (TN=3029, FP=175, FN=196, TP=3285)
```

### Architectural Insights for MSc Presentation
- **Linear Models vs. Naive Bayes:** Calibrated Linear SVM and Logistic Regression achieve superior performance ($>98.3\%$) because $L_2$ regularization handles the high-dimensional sparse TF-IDF space without independence assumptions.
- **Naive Bayes Behavior:** Multinomial Naive Bayes assumes conditional feature independence. On complex disinformation narratives with correlated linguistic markers, it achieves a respectable $94.45\%$ accuracy, but makes more false-positive and false-negative errors ($371$ errors vs $113$ for SVM).
- **Probability Calibration:** Platt sigmoid scaling (`CalibratedClassifierCV(method='sigmoid', cv=3)`) provides valid posterior probabilities ($0.0$ to $1.0$) for the SVM without test leakage.

---

## 6. Real-World Limitations & Generalization Scope

1. **Temporal Deception Drift:** Disinformation patterns evolve over time. Surface stylometric models must be paired with dynamic retrieval (VeriScope's Contextual Bandit) and neural semantic verification (DeBERTa-v3 NLI).
2. **Domain Specificity:** The ISOT dataset predominantly covers political and world news from 2015–2017. Emerging topics require ongoing retraining.
3. **Reproducibility:** Seed 42 and deterministic group hash allocation ensure complete experimental reproducibility.
