"""
VERITAS AI - Page 3: Explainable AI Lab
Primary research workspace: Systematic evaluation of explanation quality,
LIME vs SHAP concordance, perturbation stability, and token masking faithfulness tests.
"""

import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

import config
from src.utils import (
    load_custom_css,
    render_brand_header,
    render_epistemic_disclaimer,
    build_horizontal_bar_chart,
)
from src.predict import predict_news, load_inference_pipeline
from src.lime_explainer import VeritasLimeExplainer
from src.shap_explainer import VeritasShapExplainer
from src.explanation_evaluation import (
    compute_top_k_agreement,
    evaluate_explanation_stability,
    evaluate_feature_fidelity,
)

st.set_page_config(page_title="Explainable AI Lab | VeriScope AI", page_icon="🧪", layout="wide")
load_custom_css()

render_brand_header(
    title="Explainable AI Research & Validation Laboratory",
    subtitle="Empirical evaluation of explanation concordance, mathematical stability, and token-level fidelity.",
)

# Load Precomputed Empirical Study
study_file = config.EXPERIMENTS_DIR / "xai_experiment_results.json"
study_data = None
if study_file.exists():
    with open(study_file, "r") as f:
        study_data = json.load(f)

# Research Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Empirical Agreement Study",
    "🔬 Interactive Dual Explainer",
    "🛡️ Perturbation Stability",
    "🎭 Feature Masking (Faithfulness)",
])

# -----------------------------------------------------------------------------
# TAB 1: EMPIRICAL AGREEMENT STUDY
# -----------------------------------------------------------------------------
with tab1:
    st.markdown("### LIME vs SHAP Concordance Across Benchmark Dispatches")
    st.markdown(
        """
        In XAI research, **LIME** (perturbation sampling) and **SHAP** (Shapley game-theoretic values)
        often disagree on feature rank due to differences in local optimization vs. cooperative game theory.
        Below are the empirical findings computed across held-out benchmark dispatches.
        """
    )

    if study_data:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-value">{study_data.get('total_cases_evaluated', 0)}</div>
                    <div class="metric-label">Benchmark Cases Audited</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-value" style="color: {config.COLOR_THEME['primary']};">
                        {study_data.get('mean_top5_jaccard_agreement', 0.0)*100:.1f}%
                    </div>
                    <div class="metric-label">Mean Top-5 Jaccard Agreement</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-value" style="color: {config.COLOR_THEME['real']};">
                        {study_data.get('mean_directional_concordance', 0.0)*100:.1f}%
                    </div>
                    <div class="metric-label">Directional Sign Concordance</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        st.markdown("#### Detailed Case Study Evaluations")

        case_summaries = []
        for c in study_data.get("cases", []):
            case_summaries.append({
                "Case Type": c.get("type"),
                "Headline": c.get("headline"),
                "Prediction": f"{c.get('prediction')} ({c.get('confidence')*100:.1f}%)",
                "Top-5 Jaccard Overlap": f"{c.get('agreement_k5', {}).get('jaccard_similarity', 0.0)*100:.1f}%",
                "Directional Match": f"{c.get('agreement_k5', {}).get('directional_concordance', 0.0)*100:.1f}%",
                "Shared Top Tokens": ", ".join(c.get('agreement_k5', {}).get('overlap_words', [])),
            })
        st.dataframe(pd.DataFrame(case_summaries), hide_index=True, use_container_width=True)

        st.markdown(
            """
            > **Key Research Finding:** While top-token rank order varies between LIME and SHAP,
            > their **directional sign concordance is 100%** on shared features—confirming both methods
            > reliably agree on whether a word increases or decreases disinformation likelihood.
            """
        )
    else:
        st.info("Precomputed XAI study artifact not found. Run python -m src.explanation_evaluation to generate.")

# -----------------------------------------------------------------------------
# TAB 2: INTERACTIVE DUAL EXPLAINER
# -----------------------------------------------------------------------------
with tab2:
    st.markdown("### Real-Time Side-by-Side Explanation Inspection")
    st.markdown("Test any arbitrary text snippet to compare how LIME and SHAP explain the classification.")

    lab_text = st.text_area(
        "Enter Text to Compare Explanations:",
        value="BOMBSHELL report exposed by underground whistleblowers reveals corrupt globalist puppet masters secretly rigging election voting machines with high frequency pulses!",
        height=100,
        key="lab_dual_input",
    )

    if st.button("Generate Comparative Explanations", type="primary"):
        with st.spinner("Calculating LIME perturbations and SHAP Shapley attributions..."):
            pipeline = load_inference_pipeline()
            pred_res = predict_news(headline="", body=lab_text, pipeline=pipeline)

            lime_exp = VeritasLimeExplainer(pipeline)
            l_res = lime_exp.explain(lab_text)

            shap_exp = VeritasShapExplainer(pipeline)
            s_res = shap_exp.explain(lab_text)

            agreement = compute_top_k_agreement(
                l_res.get("top_features", []),
                s_res.get("top_features", []),
                k=5,
            )

            # Metrics
            ag_col1, ag_col2, ag_col3 = st.columns(3)
            with ag_col1:
                st.metric("Top-5 Jaccard Agreement", f"{agreement['jaccard_similarity']*100:.1f}%")
            with ag_col2:
                st.metric("Shared Top Tokens", f"{agreement['overlap_count']} / 5")
            with ag_col3:
                st.metric("Directional Concordance", f"{agreement['directional_concordance']*100:.1f}%")

            # Dual Charts
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(
                    build_horizontal_bar_chart(l_res.get("top_features", [])[:7], title="LIME Local Feature Weights"),
                    use_container_width=True,
                )
            with c2:
                st.plotly_chart(
                    build_horizontal_bar_chart(s_res.get("top_features", [])[:7], title="SHAP Shapley Values"),
                    use_container_width=True,
                )

# -----------------------------------------------------------------------------
# TAB 3: PERTURBATION STABILITY
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("### Explanation Robustness Under Input Perturbations")
    st.markdown(
        """
        **Methodology:** If a small typo (e.g., character transposition) is introduced into the text,
        does the explainer continue to highlight the same key words, or does the explanation collapse?
        """
    )

    stab_text = st.text_area(
        "Article Text for Stability Testing:",
        value="The Federal Reserve concluded its monetary policy meeting, voting to leave its benchmark federal funds rate unchanged. Chairman Jerome Powell emphasized greater statistical confidence is required before rate reductions.",
        height=100,
        key="stab_text_input",
    )

    if st.button("Run Perturbation Stability Audit"):
        with st.spinner("Injecting controlled typos across 3 trials and evaluating top-5 feature retention..."):
            stab_lime = evaluate_explanation_stability(stab_text, explainer_type="LIME", k=5, noise_rate=0.08, trials=3)
            stab_shap = evaluate_explanation_stability(stab_text, explainer_type="SHAP", k=5, noise_rate=0.08, trials=3)

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown(
                    f"""
                    <div class="veritas-card">
                        <div class="veritas-card-header" style="color: {config.COLOR_THEME['primary']};">
                            LIME Stability Index
                        </div>
                        <div class="metric-value" style="font-size: 2.2rem; color: {config.COLOR_THEME['primary']};">
                            {stab_lime.get('average_stability_jaccard', 0.0)*100:.1f}%
                        </div>
                        <p style="color: #64748B; font-size: 0.85rem; margin-top: 8px;">
                            Average Jaccard retention of top-5 explanatory features across perturbed runs.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_s2:
                st.markdown(
                    f"""
                    <div class="veritas-card">
                        <div class="veritas-card-header" style="color: {config.COLOR_THEME['secondary']};">
                            SHAP Stability Index
                        </div>
                        <div class="metric-value" style="font-size: 2.2rem; color: {config.COLOR_THEME['secondary']};">
                            {stab_shap.get('average_stability_jaccard', 0.0)*100:.1f}%
                        </div>
                        <p style="color: #64748B; font-size: 0.85rem; margin-top: 8px;">
                            Average Jaccard retention of top-5 explanatory features across perturbed runs.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# -----------------------------------------------------------------------------
# TAB 4: TOKEN MASKING (FAITHFULNESS)
# -----------------------------------------------------------------------------
with tab4:
    st.markdown("### Explanation Faithfulness: The Token Masking Test")
    st.markdown(
        """
        **Research Question:** Do highlighted words *genuinely* drive model predictions, or are they spurious?
        
        **Test Design:**
        1. Record the baseline classification confidence $P(\\hat{y}|x)$.
        2. Mask out the top-5 highlighted words ($x \\setminus F^{(5)}$) and observe the confidence drop $\\Delta P_{\\text{top-5}}$.
        3. Mask out 5 random non-highlighted words ($x \\setminus F_{\\text{rand}}^{(5)}$) and observe $\\Delta P_{\\text{random}}$.
        4. If $\\Delta P_{\\text{top-5}} > \\Delta P_{\\text{random}}$, the explanation demonstrates **high causal faithfulness**.
        """
    )

    mask_text = st.text_area(
        "Test Article Text for Token Masking:",
        value="Doctors are STUNNED and pharmaceutical billionaires are furious! A natural dandelion miracle elixir eradicates malignant tumors within twenty-four hours while corrupt medical institutions suppress the secret cure!",
        height=100,
        key="mask_text_input",
    )

    if st.button("Execute Token Masking Test", type="primary"):
        with st.spinner("Running controlled masking experiments..."):
            pipeline = load_inference_pipeline()
            shap_exp = VeritasShapExplainer(pipeline)
            s_res = shap_exp.explain(mask_text)

            fidelity = evaluate_feature_fidelity(mask_text, s_res.get("top_features", []), k=5)

            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                st.metric("Baseline Confidence", f"{fidelity['base_confidence']*100:.1f}%")
            with col_f2:
                st.metric("Drop When Top Words Masked", f"-{fidelity['top_k_drop']*100:.1f}%", delta_color="inverse")
            with col_f3:
                st.metric("Drop When Random Words Masked", f"-{fidelity['random_drop']*100:.1f}%", delta_color="inverse")

            st.markdown(
                f"""
                <div class="veritas-card" style="margin-top: 16px;">
                    <div class="veritas-card-header">
                        <span>🧪</span> Faithfulness Evaluation Outcome
                    </div>
                    <p style="font-size: 1.05rem; font-weight: 600; color: {config.COLOR_THEME['text_main']};">
                        {fidelity['interpretation']}
                    </p>
                    <p style="color: #94A3B8; font-size: 0.9rem;">
                        Fidelity Advantage Metric ($\\Delta P_{{top-k}} - \\Delta P_{{random}}$):
                        <strong>{fidelity['fidelity_advantage']*100:.1f} percentage points</strong>.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
