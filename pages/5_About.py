"""
VeriScope AI - Page 5: About & Project Team
Academic documentation, project team member allocations, research methodology,
mathematical formulations, epistemic limitations, and academic research documentation.
"""

import streamlit as st

import config
from src.utils import load_custom_css, render_brand_header, render_epistemic_disclaimer

st.set_page_config(page_title="About & Team | VeriScope AI", page_icon="📖", layout="wide")
load_custom_css()

render_brand_header(
    title="Project Team & Academic Methodology",
    subtitle="Team member responsibilities, system architecture, mathematical formulations, and research methodology.",
)

# Navigation Tabs
tab_team, tab_subjects, tab_overview, tab_xai, tab_leakage, tab_ethics = st.tabs([
    "👥 Project Team & Responsibilities",
    "🎓 Five Academic Subjects Integration",
    "📐 Machine Learning & NLI Pipeline",
    "🔬 Explainable AI (LIME vs SHAP)",
    "🛡️ The Publisher Leakage Problem",
    "⚠️ Responsible Use & Limitations",
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
# TAB 2: FIVE ACADEMIC SUBJECTS INTEGRATION
# -----------------------------------------------------------------------------
with tab_subjects:
    st.markdown("### Integration Across Five Academic Curriculum Subjects")
    st.markdown(
        """
        VeriScope AI deliberately integrates theoretical concepts and practical algorithms from
        five distinct core computer science and data science curriculum subjects.
        """
    )

    academic_domains = [
        {
            "subject": "1. Pattern Recognition & Image Processing",
            "icon": "📷",
            "color": config.COLOR_THEME["primary"],
            "code_ref": "src/ocr.py",
            "summary": "Local Tesseract 5.5 OCR engine with EXIF orientation detection (OSD), contrast normalization, adaptive thresholding, and headline/body heuristic layout segmentation.",
            "components": [
                "EXIF transpose & rotation correction under orientation ambiguity",
                "Lanczos-filtered resolution scaling & high-contrast grayscale normalization",
                "Heuristic separation of prominent header blocks from body paragraphs",
                "Robust byte validation and in-memory error handling for malformed uploads",
            ],
        },
        {
            "subject": "2. Natural Language Processing (NLP)",
            "icon": "📝",
            "color": config.COLOR_THEME["secondary"],
            "code_ref": "src/preprocessing.py, src/nli_verifier.py",
            "summary": "Publisher leakage neutralization, sublinear TF-IDF n-gram vectorization, and pre-trained Cross-Encoder Natural Language Inference (cross-encoder/nli-deberta-v3-base / ONNX).",
            "components": [
                "Automated regex-based stripping of wire service headers ((Reuters), (AP), datelines)",
                "Sublinear TF-IDF vectorization with unigram and bigram representation (5,000 max features)",
                "Neural cross-encoder inference evaluating premise vs claim hypothesis",
                "Conservative multi-passage aggregation with automated conflict detection",
            ],
        },
        {
            "subject": "3. Business Intelligence & Analytics",
            "icon": "📊",
            "color": config.COLOR_THEME["accent_teal"],
            "code_ref": "app.py, src/database.py, pages/4_Analysis_History.py",
            "summary": "Executive intelligence portal, real-time KPI metrics, verification velocity monitoring, and an auditable SQLite storage layer enforcing a 3-calendar-month UTC retention policy.",
            "components": [
                "Interactive executive dashboard with verdict breakdowns and auditing velocities",
                "Persistent SQLite audit logging with SHA-256 deduplication and snippet storage",
                "Calendar-accurate 3-month retention policy handling leap years and month-end dates",
                "Exportable audit logs supporting compliance review and retrospective quality control",
            ],
        },
        {
            "subject": "4. Reinforcement Learning",
            "icon": "🎯",
            "color": config.COLOR_THEME["uncertain"],
            "code_ref": "src/evidence_bandit.py",
            "summary": "Contextual Multi-Armed Bandit (Upper Confidence Bound - UCB1) adaptively routing retrieval queries using an objective, non-circular quality reward.",
            "components": [
                "Three discrete retrieval arms: entity_focused, semantic_hybrid, and keyphrase_ngram",
                "UCB1 action-selection balancing exploration of uncertain formulations with exploitation",
                "Non-circular reward: R = 0.50 * Sim + 0.30 * EntityCov + 0.20 * NLI_Margin",
                "State persistence in JSON artifacts enabling continuous learning across sessions",
            ],
        },
        {
            "subject": "5. Professional Ethics & Social Responsibility",
            "icon": "⚖️",
            "color": config.COLOR_THEME["real"],
            "code_ref": "pages/5_About.py, src/utils.py",
            "summary": "Epistemic modesty disclosures, zero fabricated confidence, transparent provenance tiering, data privacy compliance, and dual-explainer algorithmic accountability.",
            "components": [
                "Explicit epistemic boundaries: models predict dataset resemblance, not absolute truth",
                "Zero fabricated metrics or illustrative numbers presented as real outputs",
                "Dual XAI accountability: LIME and SHAP verify feature contributions without black boxes",
                "Privacy-preserving retention: stored snippets truncate long personal texts",
            ],
        },
    ]

    for subj in academic_domains:
        items_html = "".join([f"<li style='margin-bottom: 3px;'>{c}</li>" for c in subj["components"]])
        st.markdown(
            f"""
            <div class="veritas-card" style="border-left: 4px solid {subj['color']}; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div style="font-size: 1.15rem; font-weight: 700; color: #0B1528;">
                        {subj['icon']} {subj['subject']}
                    </div>
                    <code style="background: #F1F5F9; color: {subj['color']}; padding: 3px 8px; border-radius: 4px; font-size: 0.82rem;">{subj['code_ref']}</code>
                </div>
                <p style="color: #334155; font-size: 0.92rem; line-height: 1.55; margin: 4px 0 10px 0;">
                    {subj['summary']}
                </p>
                <div style="font-size: 0.82rem; text-transform: uppercase; color: #64748B; font-weight: 600; margin-bottom: 4px;">
                    Key Functional Implementations:
                </div>
                <ul style="font-size: 0.88rem; color: #475569; line-height: 1.5; margin: 0; padding-left: 20px;">
                    {items_html}
                </ul>
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
# TAB 6: RESPONSIBLE USE & LIMITATIONS
# -----------------------------------------------------------------------------
with tab_ethics:
    st.markdown("### Ethical Boundaries, Transparency & Operational Limitations")
    st.markdown(
        f"""
        <div class="veritas-card" style="border-left: 4px solid {config.COLOR_THEME['uncertain']}; margin-bottom: 20px;">
            <h4 style="font-size: 1.15rem; font-weight: 700; color: #0B1528; margin: 0 0 8px 0;">
                Core Epistemic Principles
            </h4>
            <div style="font-size: 0.92rem; color: #334155; line-height: 1.6;">
                <p>
                    <strong>1. Classification Confidence is Not Proof of Truth:</strong>
                    Machine learning classifiers evaluate whether submitted text shares stylistic, lexical, and structural
                    patterns with historical disinformation records. High model confidence indicates strong pattern resemblance,
                    never absolute ontological truth.
                </p>
                <p>
                    <strong>2. Local Reference Boundaries:</strong>
                    The evidence verification subsystem queries our curated, locally auditable reference archive of 16 multi-domain
                    records. A verdict of <em>Insufficient Evidence</em> indicates absence of corroborating passages within this
                    local archive, not that an external claim is false.
                </p>
                <p>
                    <strong>3. Conflict Transparency:</strong>
                    When retrieved records yield contradictory stances, the platform does not choose an arbitrary verdict.
                    It explicitly flags conflicting evidence to preserve neutrality and user agency.
                </p>
                <p style="margin-bottom: 0;">
                    <strong>4. Privacy Compliance & Data Minimization:</strong>
                    Submitted articles are never sent to external commercial APIs. Database retention is strictly capped at
                    3 calendar months (UTC), storing only truncated snippets rather than full proprietary texts.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        #### Operational Limitations:
        - **Evolving Misinformation Campaigns:** Deceptive narrative patterns shift rapidly. A model trained on static corpora may struggle with novel rhetorical devices.
        - **OCR Quality Dependencies:** Tesseract text extraction accuracy depends heavily on input image resolution, font rendering, and contrast. Reviewing extracted text before analysis is mandatory.
        - **Absence of Real-Time Web Scraping:** VeriScope AI intentionally operates strictly offline without unauthorized live scraping or paid API tokens to ensure reproducible academic grading.
        """
    )

# Epistemic notice at bottom
st.write("")
render_epistemic_disclaimer()
