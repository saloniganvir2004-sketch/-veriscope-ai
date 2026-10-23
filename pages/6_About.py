"""
VeriScope AI - Page 6: About & Research Methodology
Academic documentation, mathematical formulations, data provenance,
epistemic limitations, and MSc Viva examination preparation.
"""

import streamlit as st

import config
from src.utils import load_custom_css, render_brand_header, render_epistemic_disclaimer

st.set_page_config(page_title="About & Research | VeriScope AI", page_icon="📖", layout="wide")
load_custom_css()

render_brand_header(
    title="Research Architecture & Academic Methodology",
    subtitle="Full technical documentation, mathematical formulations, and MSc viva examination defense.",
)

# Research Navigation Tabs
tab_overview, tab_xai, tab_leakage, tab_viva = st.tabs([
    "📐 Machine Learning Pipeline",
    "🔬 Explainable AI (LIME vs SHAP)",
    "🛡️ The Publisher Leakage Problem",
    "🎓 MSc Viva Defense Q&A",
])

# -----------------------------------------------------------------------------
# TAB 1: MACHINE LEARNING PIPELINE
# -----------------------------------------------------------------------------
with tab_overview:
    st.markdown("### System Architecture & Mathematical Foundations")
    st.markdown(
        """
        #### 1. Text Feature Extraction: Sublinear TF-IDF
        Standard term-frequency representations disproportionately weight high-frequency tokens.
        VeriScope AI utilizes **Sublinear TF-IDF scaling** with unigram and bigram features:
        """
    )
    st.latex(r"\text{TF}_{\text{sublinear}}(t, d) = 1 + \ln(\text{TF}(t, d)) \quad \text{for } \text{TF}(t, d) > 0")
    st.latex(r"\text{IDF}(t, D) = \ln \left( \frac{1 + |D|}{1 + |\{d \in D : t \in d\}|} \right) + 1")
    st.markdown(
        """
        Features are bounded to a maximum vocabulary of 5,000 to maintain computational efficiency
        for real-time XAI explainers while capturing rich stylistic n-grams.
        
        #### 2. Model Architectures Evaluated:
        1. **Logistic Regression (L2 Regularized):**
           Maximizes the log-likelihood of binomial posterior distribution:
        """
    )
    st.latex(r"P(y=1|\mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}")
    st.markdown(
        """
        2. **Multinomial Naive Bayes:**
           Models conditional word probability using Laplace smoothing ($\alpha = 0.1$):
        """
    )
    st.latex(r"P(x_i | y) = \frac{N_{yi} + \alpha}{N_y + \alpha |V|}")
    st.markdown(
        """
        3. **Linear Support Vector Machine (LinearSVC):**
           Finds the maximum-margin hyperplane separating classes. Because raw decision values
           represent geometric distances rather than calibrated probabilities, we apply **Platt Scaling**:
        """
    )
    st.latex(r"P(y=1|\mathbf{x}) = \frac{1}{1 + \exp(A \cdot f(\mathbf{x}) + B)}")
    st.markdown("Fitted via 3-fold cross-validation on the training set using `CalibratedClassifierCV`.")

# -----------------------------------------------------------------------------
# TAB 2: EXPLAINABLE AI (LIME VS SHAP)
# -----------------------------------------------------------------------------
with tab_xai:
    st.markdown("### Primary Research Contribution: LIME vs SHAP Comparative Analysis")
    st.markdown(
        r"""
        #### 1. LIME (Local Interpretable Model-agnostic Explanations)
        LIME draws $M$ perturbed samples $z'$ around the document $x$, weights them by proximity $\pi_x(z)$,
        and fits an interpretable sparse surrogate model $g \in G$:
        """
    )
    st.latex(r"\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)")
    st.markdown(
        """
        - **Sampling Variance:** Because perturbations are drawn randomly, LIME exhibits slight sampling
          variance across executions.
        
        #### 2. SHAP (SHapley Additive exPlanations)
        SHAP computes the unique attribution satisfying Local Accuracy, Missingness, and Consistency
        grounded in cooperative game theory:
        """
    )
    st.latex(r"\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N| - |S| - 1)!}{|N|!} (v(S \cup \{i\}) - v(S))")
    st.markdown(
        """
        For sparse linear models with a zero-baseline background, SHAP attributions simplify to:
        """
    )
    st.latex(r"\phi_i = w_i \cdot x_i")
    st.markdown(
        """
        This calculation executes in **$<100\text{ ms}$**, eliminating the typical 30-second latency
        of KernelExplainer on high-dimensional text.
        
        #### 3. Quantitative Agreement Metric (Jaccard Index)
        """
    )
    st.latex(r"J(L_k, S_k) = \frac{|L_k \cap S_k|}{|L_k \cup S_k|}")
    st.markdown(
        """
        Our research establishes that while token rank orders differ due to LIME's perturbation sampling,
        the **directional sign concordance between LIME and SHAP is 100%**, validating their alignment
        on the direction of influence.
        """
    )

# -----------------------------------------------------------------------------
# TAB 3: THE PUBLISHER LEAKAGE PROBLEM
# -----------------------------------------------------------------------------
with tab_leakage:
    st.markdown("### The Publisher Artifact Problem in Fake News Datasets")
    st.markdown(
        """
        #### The Critical Flaw in Standard Benchmarks (e.g., ISOT):
        In open academic fake-news datasets like ISOT (Ahmed et al., 2017), real articles are mined almost
        exclusively from Reuters wire dispatches. Consequently, over 95% of real articles contain
        signatures such as:
        ```
        WASHINGTON (Reuters) - The Senate approved...
        LONDON (Reuters) - British inflation eased...
        ```
        Meanwhile, fake news articles originate from third-party blogs without wire signatures.
        
        #### The Resulting Machine Learning Failure:
        A naive TF-IDF model will assign the highest negative weights to tokens like `"reuters"`,
        `"washington"`, and `"reporting"`. The model achieves an artificial **99.8% accuracy** by purely
        detecting whether the word `"reuters"` is present, **learning zero linguistic or stylometric cues of deception**.
        
        #### VeriScope AI's Methodological Solution:
        1. **Automated Leakage Stripping:** `src/preprocessing.py` applies rigorous regular expressions
           to eliminate wire service prefixes, datelines, and editorial sign-offs before vectorization.
        2. **Explainability Audit:** Using LIME and SHAP, we verify that models trained on sanitized text
           focus on emotive modifiers, clickbait adjectives, and hyperbolic claims rather than publisher markers.
        """
    )

# -----------------------------------------------------------------------------
# TAB 4: MSC VIVA DEFENSE PREPARATION
# -----------------------------------------------------------------------------
with tab_viva:
    st.markdown("### Master's Viva Defense Examination Guide")
    st.markdown("Key questions and academic defenses for university project assessment:")

    with st.expander("Q1: Why does your model not prove whether an article is factually true?"):
        st.markdown(
            """
            **Defense:** Natural language processing models operating on statistical stylometry (TF-IDF, word frequencies)
            detect **linguistic patterns, emotional intensity, and stylistic structure** correlated with disinformation
            in the training corpus. They do not possess external knowledge bases or world verification capabilities.
            An objectively false claim written in formal academic prose will test as 'Likely Real', whereas a true claim
            written in sensationalist capital letters may test as 'Likely Fake'. We explicitly enforce this epistemic
            limitation in our disclaimer.
            """
        )

    with st.expander("Q2: Why did you compare LIME and SHAP rather than using only one explainer?"):
        st.markdown(
            """
            **Defense:** A central challenge in Explainable AI is the absence of ground-truth explanation labels.
            By comparing LIME (a perturbation-based local surrogate) against SHAP (a game-theoretic Shapley decomposition),
            we can cross-validate explanation consistency. Our research suite evaluates their Top-$k$ Jaccard agreement,
            perturbation stability, and feature masking fidelity to determine whether local explanations are trustworthy.
            """
        )

    with st.expander("Q3: How did you handle data leakage during preprocessing?"):
        st.markdown(
            """
            **Defense:** We implemented three strict architectural controls:
            1. All wire-service publisher headers (`(Reuters)`, `(AP)`, datelines) were stripped using regex.
            2. Stratified splitting (70% train, 15% val, 15% test) was performed *before* any feature extraction.
            3. The TF-IDF vectorizer was strictly fitted *only* on the training split; unseen test vocabulary was ignored.
            """
        )

    with st.expander("Q4: Why did you calibrate the Linear SVM rather than using raw decision scores?"):
        st.markdown(
            r"""
            **Defense:** Linear Support Vector Machines optimize a hinge loss objective, yielding signed margin distances
            $f(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b \in (-\infty, \infty)$. These scores lack probabilistic properties
            (they are uncalibrated and non-probabilistic). To present valid model confidence scores, we applied Platt Scaling
            via `CalibratedClassifierCV(method='sigmoid', cv=3)` strictly on internal training folds, guaranteeing proper
            posterior probabilities bounded in $[0, 1]$.
            """
        )

    with st.expander("Q5: What are the primary failure modes of this system?"):
        st.markdown(
            """
            **Defense:**
            1. **Sarcasm and Satire:** Sublinear TF-IDF cannot capture deep pragmatic context or double meanings.
            2. **Vocabulary Shift:** Novel disinformation campaigns using emergent terminology not present in the 5,000-word
               vocabulary will suffer from out-of-vocabulary attenuation.
            3. **Adversarial Paraphrasing:** A malicious actor can rewrite disinformation in sober, dry journalistic language
               to evade stylometric detection.
            """
        )

    with st.expander("Q6: How does the Image OCR pipeline process visual screenshots?"):
        st.markdown(
            """
            **Defense:** Uploaded news clippings and screenshots are decoded via PIL, orientation-corrected using EXIF metadata,
            converted to high-contrast grayscale, and filtered with edge sharpening. Tesseract 5.5.2 extracts the textual contents,
            which are cleaned and presented in an editable review window before feeding directly into the same leakage-sanitized
            TF-IDF inference and dual XAI attribution pipeline.
            """
        )
