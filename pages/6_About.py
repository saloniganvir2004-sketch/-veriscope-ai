"""
VeriScope AI - Page 6: About & Project Team
Academic documentation, project team member allocations, research methodology,
mathematical formulations, epistemic limitations, and MSc Viva examination preparation.
"""

import streamlit as st

import config
from src.utils import load_custom_css, render_brand_header, render_epistemic_disclaimer

st.set_page_config(page_title="About & Team | VeriScope AI", page_icon="📖", layout="wide")
load_custom_css()

render_brand_header(
    title="Project Team & Academic Methodology",
    subtitle="Team member responsibilities, system architecture, mathematical formulations, and MSc viva defense documentation.",
)

# Navigation Tabs
tab_team, tab_overview, tab_xai, tab_leakage, tab_viva = st.tabs([
    "👥 Project Team & Responsibilities",
    "📐 Machine Learning Pipeline",
    "🔬 Explainable AI (LIME vs SHAP)",
    "🛡️ The Publisher Leakage Problem",
    "🎓 MSc Viva Defense Q&A",
])

# -----------------------------------------------------------------------------
# TAB 1: PROJECT TEAM & RESPONSIBILITIES
# -----------------------------------------------------------------------------
with tab_team:
    st.markdown("### MSc Project Team & Work Allocation")
    st.markdown(
        """
        <div style="background: #F1F5F9; border-left: 3px solid #0E7490; border-radius: 4px; padding: 12px 16px; margin-bottom: 24px; font-size: 0.9rem; color: #334155; line-height: 1.55;">
            <strong>Team Coordination & Governance:</strong>
            The task distributions below reflect proposed formal responsibilities across our five-member cohort.
            To achieve a unified system, members collaborate across adjacent modules.
            Assigned scope is distinguished from completed deliverables, with continuous integration maintained across code, models, and documentation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    team_members = [
        {
            "num": 1,
            "name": "Ayushman Kumar",
            "enrolment": "A010175625019",
            "role": "Dataset and NLP Preprocessing",
            "badge_color": "#0E7490",
            "tasks": [
                "Dataset inspection and loading.",
                "Data cleaning and missing-value handling.",
                "Duplicate detection and removal.",
                "Exploratory data analysis and class-distribution analysis.",
                "Label validation and dataset documentation.",
                "Text normalization and NLP preprocessing.",
                "Train/validation/test split preparation and leakage prevention.",
            ],
        },
        {
            "num": 2,
            "name": "Astha Thapa",
            "enrolment": "A010175625014",
            "role": "Machine-Learning Models and Tuning",
            "badge_color": "#334155",
            "tasks": [
                "TF-IDF feature extraction.",
                "Logistic Regression, Multinomial Naive Bayes and Linear SVM implementations where supported.",
                "Training and comparison of candidate models.",
                "Hyperparameter tuning using appropriate validation procedures.",
                "Model selection and saving the selected model and preprocessing pipeline.",
                "Reproducible inference configuration and model documentation.",
            ],
        },
        {
            "num": 3,
            "name": "Saloni Ganvir",
            "enrolment": "A010175625017",
            "role": "Explainable AI and Interpretation",
            "badge_color": "#15803D",
            "tasks": [
                "LIME and SHAP integration.",
                "Explanation visualizations.",
                "Feature-contribution interpretation.",
                "Case studies of representative predictions.",
                "Explanation stability and quality checks where feasible.",
                "Explainability-related testing and documentation.",
                "Clear communication of the model's limitations.",
            ],
        },
        {
            "num": 4,
            "name": "Sarvesh",
            "enrolment": "A010175625016",
            "role": "Web Application and OCR Integration",
            "badge_color": "#D97706",
            "tasks": [
                "Streamlit interface and navigation.",
                "Landing page and News Analyzer UI.",
                "Manual headline/context input.",
                "Image upload interface.",
                "Tesseract OCR integration and extracted-text editing.",
                "Integration with the trained classification pipeline.",
                "Result display, error handling and usability improvements.",
            ],
        },
        {
            "num": 5,
            "name": "Sri Rinith",
            "enrolment": "A010175625018",
            "role": "Evaluation, Testing and Integration",
            "badge_color": "#7C3AED",
            "tasks": [
                "Evaluation metrics: accuracy, precision, recall and F1 score.",
                "Confusion matrix and model comparison.",
                "Error analysis and representative failure cases.",
                "Unit and integration testing.",
                "End-to-end workflow verification.",
                "Git integration and change tracking.",
                "Report, documentation and presentation preparation.",
                "Regression testing after fixes.",
            ],
        },
    ]

    # Render Member Cards in a balanced layout
    for m in team_members:
        task_items_html = "".join([f"<li style='margin-bottom: 4px;'>{t}</li>" for t in m["tasks"]])
        st.markdown(
            f"""
            <div class="veritas-card" style="margin-bottom: 18px; border-left: 4px solid {m['badge_color']};">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; font-weight: 600;">
                            Member {m['num']}
                        </div>
                        <h4 style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin: 2px 0 6px 0;">
                            {m['name']}
                        </h4>
                        <div style="font-size: 0.88rem; color: #334155;">
                            <strong>Enrolment No.:</strong> <code style="background: #F1F5F9; color: #0E7490; padding: 2px 6px; border-radius: 4px; font-weight: 600;">{m['enrolment']}</code>
                        </div>
                    </div>
                    <div>
                        <span style="display: inline-block; background: {m['badge_color']}15; color: {m['badge_color']}; border: 1px solid {m['badge_color']}40; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                            {m['role']}
                        </span>
                    </div>
                </div>
                <div style="margin-top: 14px; border-top: 1px solid #E2E8F0; padding-top: 10px;">
                    <div style="font-size: 0.82rem; text-transform: uppercase; color: #64748B; font-weight: 600; margin-bottom: 6px;">
                        Assigned Responsibilities:
                    </div>
                    <ul style="font-size: 0.9rem; color: #334155; line-height: 1.55; margin: 0; padding-left: 20px;">
                        {task_items_html}
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------------------------------------------------------
# TAB 2: MACHINE LEARNING PIPELINE
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
           Models conditional word probability using Laplace smoothing ($\\alpha = 0.1$):
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
# TAB 3: EXPLAINABLE AI (LIME VS SHAP)
# -----------------------------------------------------------------------------
with tab_xai:
    st.markdown("### Primary Research Contribution: LIME vs SHAP Comparative Analysis")
    st.markdown(
        r"""
        #### 1. LIME (Local Interpretable Model-agnostic Explanations)
        LIME draws $M$ perturbed samples $z'$ around document $x$, weights them by proximity $\pi_x(z)$,
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
# TAB 4: THE PUBLISHER LEAKAGE PROBLEM
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
# TAB 5: MSC VIVA DEFENSE PREPARATION
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
            **Defense:** Uploaded news clippings and screenshots are decoded via Pillow, orientation-corrected using EXIF metadata
            and Tesseract OSD, converted to high-contrast grayscale, and filtered with edge sharpening. Tesseract extracts the textual contents,
            which are separated into candidate headline and context, and presented in an editable review window before feeding directly into the same leakage-sanitized
            TF-IDF inference and dual XAI attribution pipeline.
            """
        )

# Epistemic notice at bottom
st.write("")
render_epistemic_disclaimer()
