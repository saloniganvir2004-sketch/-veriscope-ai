"""
VeriScope AI - Editorial Intelligence Dashboard & Application Portal
Intelligence Beyond the Headline.
Editorial Intelligence & Explainable AI for News Credibility Analysis.
"""

import json
import streamlit as st
import plotly.graph_objects as go

import config
from src.utils import load_custom_css, render_svg_asset, render_epistemic_disclaimer
from src.database import get_history_stats, get_history, get_activity_by_date

# Global Streamlit Page Configuration
st.set_page_config(
    page_title=f"{config.BRAND_NAME} · {config.BRAND_TAGLINE}",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Editorial Intelligence Theme
load_custom_css()

# Sidebar Navigation Branding
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 10px 0 16px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">
                VeriScope <span style="color: {config.COLOR_THEME['primary']};">AI</span>
            </div>
            <div style="font-size: 0.82rem; color: #64748B; font-weight: 500; margin-top: 2px;">
                {config.BRAND_TAGLINE}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Editorial Workspaces")

# =============================================================================
# 1. HERO SECTION
# =============================================================================
hero_col1, hero_col2 = st.columns([1.25, 1], gap="large")

with hero_col1:
    st.markdown(
        f"""
        <div style="padding-top: 8px;">
            <div style="display: inline-block; background: {config.COLOR_THEME['primary']}15; color: {config.COLOR_THEME['primary']}; border: 1px solid {config.COLOR_THEME['primary']}30; padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                Editorial Intelligence Platform
            </div>
            <h1 style="font-size: 2.5rem; font-weight: 800; color: #0F172A; letter-spacing: -0.03em; line-height: 1.15; margin: 0 0 10px 0;">
                {config.BRAND_NAME}
            </h1>
            <div style="font-size: 1.25rem; font-weight: 600; color: {config.COLOR_THEME['primary']}; margin-bottom: 14px; font-family: 'Newsreader', Georgia, serif; font-style: italic;">
                “{config.BRAND_TAGLINE}”
            </div>
            <p style="color: #475569; font-size: 1.05rem; line-height: 1.6; margin-bottom: 22px;">
                An MSc research platform combining statistical natural language processing,
                local <strong>Tesseract OCR</strong> image extraction, and dual <strong>LIME & SHAP</strong>
                explainability to audit linguistic deception and explain every classification transparently.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_btn_hero, col_btn_xai = st.columns([1.3, 1])
    with col_btn_hero:
        if st.button("📰 Analyze News Story", type="primary", width="stretch", key="hero_cta_analyze"):
            st.switch_page("pages/1_News_Analyzer.py")
    with col_btn_xai:
        if st.button("🧪 Explore XAI Lab", width="stretch", key="hero_cta_xai"):
            st.switch_page("pages/2_Explainable_AI_Lab.py")

with hero_col2:
    render_svg_asset(config.ASSETS_DIR / "hero_editorial.svg")

st.write("")

# =============================================================================
# 2. AUDIT KPI METRICS
# =============================================================================
db_stats = get_history_stats()
kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)

with kpi_c1:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value">{db_stats['total_records']}</div>
            <div class="metric-label">Total Audited Stories</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_c2:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value" style="color: {config.COLOR_THEME['fake']};">{db_stats['fake_count']}</div>
            <div class="metric-label">Likely Fake Predictions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_c3:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value" style="color: {config.COLOR_THEME['real']};">{db_stats['real_count']}</div>
            <div class="metric-label">Likely Real Predictions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_c4:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #0E7490;">3 Months</div>
            <div class="metric-label">UTC Audit Retention</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =============================================================================
# 3. RECENT ANALYSES & AUDIT ANALYTICS
# =============================================================================
dash_left, dash_right = st.columns([1.4, 1.1])

with dash_left:
    st.markdown(
        """
        <div class="veritas-card">
            <div class="veritas-card-header">
                Recent Audit Records
            </div>
        """,
        unsafe_allow_html=True,
    )

    recent_records = get_history(limit=5)
    if recent_records:
        for r in recent_records:
            badge_class = "badge-fake" if r["prediction"] == "Likely Fake" else "badge-real"
            st.markdown(
                f"""
                <div style="border-bottom: 1px solid #E2E8F0; padding: 12px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size: 0.8rem; color: #64748B;">{r['timestamp']} UTC</span>
                        <span class="{badge_class}" style="font-size: 0.75rem; padding: 2px 8px;">{r['prediction']} ({r['confidence']*100:.1f}%)</span>
                    </div>
                    <div style="font-size: 0.92rem; font-weight: 600; color: #0B1528; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {r['headline']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.write("")
        if st.button("View Full Audit History", width="stretch", key="dash_btn_history"):
            st.switch_page("pages/4_Analysis_History.py")
    else:
        render_svg_asset(config.ASSETS_DIR / "empty_audit.svg", width="100%")
        st.markdown(
            """
            <div style="text-align: center; color: #64748B; font-size: 0.88rem; margin-top: -6px;">
                No saved analyses yet. Submit a headline or article in the News Analyzer to begin.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with dash_right:
    st.markdown(
        """
        <div class="veritas-card">
            <div class="veritas-card-header">
                Audit Distribution & Production Model
            </div>
        """,
        unsafe_allow_html=True,
    )

    if db_stats["total_records"] > 0:
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Likely Real", "Likely Fake"],
            values=[db_stats["real_count"], db_stats["fake_count"]],
            hole=0.55,
            marker=dict(colors=[config.COLOR_THEME["real"], config.COLOR_THEME["fake"]]),
            textinfo="percent+label",
            textposition="inside",
        )])
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=180,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_donut, width="stretch")
    else:
        st.markdown(
            """
            <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 6px; padding: 18px; text-align: center; margin-bottom: 14px;">
                <div style="font-size: 0.85rem; color: #64748B;">Audit Analytics</div>
                <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 2px;">Real-time verdict breakdown activates when analyses are stored.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    perf_file = config.METRICS_DIR / "model_comparison.json"
    model_metrics = None
    if perf_file.exists():
        with open(perf_file, "r") as f:
            model_metrics = json.load(f)

    if model_metrics and "test_evaluations" in model_metrics:
        best_name = model_metrics.get("best_model_name", "Logistic Regression")
        best_test = model_metrics["test_evaluations"].get(best_name, {})
        st.markdown(
            f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px 14px; margin-top: 8px;">
                <div style="font-size: 0.76rem; text-transform: uppercase; color: #64748B; font-weight: 600;">Active Model Architecture</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #0B1528; margin: 2px 0 6px 0;">{best_name}</div>
                <div style="display: flex; gap: 16px;">
                    <div>
                        <div style="font-size: 0.72rem; color: #64748B;">Test Accuracy</div>
                        <div style="font-size: 1.0rem; font-weight: 700; color: {config.COLOR_THEME['primary']};">{best_test.get('accuracy', 1.0)*100:.1f}%</div>
                    </div>
                    <div>
                        <div style="font-size: 0.72rem; color: #64748B;">Macro F1</div>
                        <div style="font-size: 1.0rem; font-weight: 700; color: {config.COLOR_THEME['text_main']};">{best_test.get('macro_f1', 1.0):.4f}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Explore Model Benchmarks", width="stretch", key="dash_btn_benchmarks"):
            st.switch_page("pages/3_Model_Performance.py")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.markdown("---")

# =============================================================================
# 4. HOW IT WORKS (FOUR-STEP WORKFLOW)
# =============================================================================
st.markdown("### How It Works")
st.caption("A transparent, four-stage verification workflow from raw submission to token-level explainability.")

step_c1, step_c2, step_c3, step_c4 = st.columns(4)

with step_c1:
    st.markdown(
        f"""
        <div class="veritas-card" style="height: 100%; border-top: 3px solid {config.COLOR_THEME['primary']};">
            <div style="font-size: 0.8rem; font-weight: 700; color: {config.COLOR_THEME['primary']}; text-transform: uppercase;">Step 01</div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin: 6px 0 8px 0;">Story Submission</h4>
            <p style="color: #64748B; font-size: 0.88rem; line-height: 1.5; margin: 0;">
                Input a news headline and context manually, or upload a clipping screenshot (PNG, JPG, WEBP).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step_c2:
    st.markdown(
        f"""
        <div class="veritas-card" style="height: 100%; border-top: 3px solid {config.COLOR_THEME['secondary']};">
            <div style="font-size: 0.8rem; font-weight: 700; color: {config.COLOR_THEME['secondary']}; text-transform: uppercase;">Step 02</div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin: 6px 0 8px 0;">OCR & Preprocessing</h4>
            <p style="color: #64748B; font-size: 0.88rem; line-height: 1.5; margin: 0;">
                Tesseract extracts image text locally. Regex pipelines strip publisher leakage to prevent false memorization.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step_c3:
    st.markdown(
        f"""
        <div class="veritas-card" style="height: 100%; border-top: 3px solid #D97706;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #D97706; text-transform: uppercase;">Step 03</div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin: 6px 0 8px 0;">Model Classification</h4>
            <p style="color: #64748B; font-size: 0.88rem; line-height: 1.5; margin: 0;">
                Sublinear TF-IDF features feed calibrated Logistic Regression, SVM, and Naive Bayes architectures.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step_c4:
    st.markdown(
        f"""
        <div class="veritas-card" style="height: 100%; border-top: 3px solid {config.COLOR_THEME['real']};">
            <div style="font-size: 0.8rem; font-weight: 700; color: {config.COLOR_THEME['real']}; text-transform: uppercase;">Step 04</div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin: 6px 0 8px 0;">Explainable AI</h4>
            <p style="color: #64748B; font-size: 0.88rem; line-height: 1.5; margin: 0;">
                LIME perturbations and exact SHAP Shapley values reveal exactly which tokens influenced the prediction.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =============================================================================
# 5. CORE CAPABILITIES
# =============================================================================
st.markdown("### Core Capabilities")
st.caption("Engineered for university demonstration, academic rigor, and practical newsroom auditing.")

cap_c1, cap_c2 = st.columns(2)

with cap_c1:
    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                📰 Dual-Method News Classification
            </div>
            <p style="color: #475569; font-size: 0.92rem; line-height: 1.6; margin-bottom: 12px;">
                Accepts entered headlines and article context, or extracts text directly from news screenshots using
                <strong>local Tesseract OCR</strong>. Employs leakage-sanitized feature extraction to ensure genuine stylometric evaluation.
            </p>
            <div style="font-size: 0.84rem; color: #64748B;">
                ✓ Separate Headline & Context Validation &nbsp;·&nbsp; ✓ Preprocessing Safeguards &nbsp;·&nbsp; ✓ Calibrated Confidence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                🔬 Dual Explainable AI Lab (LIME & SHAP)
            </div>
            <p style="color: #475569; font-size: 0.92rem; line-height: 1.6; margin-bottom: 12px;">
                Inspect side-by-side attributions from LIME local ridge surrogates and SHAP cooperative game-theoretic Shapley values.
                Test perturbation stability under input typos and verify causal fidelity with token masking tests.
            </p>
            <div style="font-size: 0.84rem; color: #64748B;">
                ✓ Top-k Jaccard Concordance &nbsp;·&nbsp; ✓ Perturbation Stability &nbsp;·&nbsp; ✓ Causal Token Masking
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with cap_c2:
    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                📷 Robust Local Image OCR (Pillow & Tesseract)
            </div>
            <p style="color: #475569; font-size: 0.92rem; line-height: 1.6; margin-bottom: 12px;">
                Automatically transposes EXIF orientation, flattens transparent PNGs, resizes small text with Lanczos interpolation,
                and enhances contrast. Allows full in-browser editing of extracted headlines and context before classification.
            </p>
            <div style="font-size: 0.84rem; color: #64748B;">
                ✓ Local Processing (Zero Paid APIs) &nbsp;·&nbsp; ✓ Rotation Correction &nbsp;·&nbsp; ✓ Editable Review Window
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                📈 Rigorous Model Benchmarking & History
            </div>
            <p style="color: #475569; font-size: 0.92rem; line-height: 1.6; margin-bottom: 12px;">
                Compares held-out test evaluation across candidate architectures (Logistic Regression, Multinomial Naive Bayes, Linear SVM).
                Maintains a local SQLite audit database with an automatic 3-calendar-month retention policy.
            </p>
            <div style="font-size: 0.84rem; color: #64748B;">
                ✓ Stratified 70/15/15 Splits &nbsp;·&nbsp; ✓ Confusion Matrices &nbsp;·&nbsp; ✓ 3-Month UTC Retention
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =============================================================================
# 6. VISUAL PROOF OF THE WORKFLOW & EPISTEMIC FOUNDATIONS
# =============================================================================
st.markdown("### Visual Proof of the Workflow & Epistemic Foundations")
st.caption("VeriScope AI strictly separates statistical stylometric classification from neural evidence verification.")

proof_c1, proof_c2 = st.columns([1.25, 1])

with proof_c1:
    if recent_records:
        latest = recent_records[0]
        badge_style = "badge-fake" if latest["prediction"] == "Likely Fake" else "badge-real"
        accent_color = config.COLOR_THEME["fake"] if latest["prediction"] == "Likely Fake" else config.COLOR_THEME["real"]
        st.markdown(
            f"""
            <div class="veritas-card" style="border-left: 4px solid {accent_color};">
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #64748B; font-weight: 600;">
                    Latest Audited Dispatch · Recorded from SQLite
                </div>
                <h4 style="font-size: 1.15rem; font-weight: 700; color: #0B1528; margin: 4px 0 8px 0;">
                    {latest['headline']}
                </h4>
                <div style="display: flex; gap: 16px; margin: 10px 0; font-size: 0.88rem; align-items: center;">
                    <span class="{badge_style}">{latest['prediction']}</span>
                    <span style="color: {accent_color}; font-weight: 700; font-size: 1.05rem;">{latest['confidence']*100:.1f}% Confidence</span>
                    <span style="color: #64748B; font-weight: 500;">Model: {latest['model_name']}</span>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 6px; font-size: 0.88rem; line-height: 1.6; color: #334155; margin-top: 10px;">
                    {latest['snippet']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="veritas-card" style="border-left: 4px solid {config.COLOR_THEME['primary']};">
                <div style="font-size: 0.8rem; text-transform: uppercase; color: {config.COLOR_THEME['primary']}; font-weight: 600;">
                    Core Verification Pipeline Overview
                </div>
                <h4 style="font-size: 1.15rem; font-weight: 700; color: #0B1528; margin: 4px 0 8px 0;">
                    How VeriScope AI Audits Dispatches
                </h4>
                <div style="font-size: 0.90rem; color: #334155; line-height: 1.6;">
                    <p style="margin-bottom: 8px;">
                        <strong>1. ML Stylometry:</strong> Calibrated classifier evaluates linguistic deception signals (sensationalism index, punctuation density, emotional hedges).
                    </p>
                    <p style="margin-bottom: 8px;">
                        <strong>2. Cross-Encoder NLI:</strong> Neural inference checks whether verified archives entail or contradict the claim.
                    </p>
                    <p style="margin-bottom: 0;">
                        <strong>3. Explainability (XAI):</strong> LIME and SHAP identify the specific tokens driving the prediction.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with proof_c2:
    st.markdown(
        f"""
        <div class="veritas-card" style="height: 100%;">
            <div class="veritas-card-header">
                System Audit Status
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 8px;">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.88rem;">
                    <span style="color: #64748B;">Active Best Model:</span>
                    <strong style="color: #0B1528;">Logistic Regression (TF-IDF)</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.88rem;">
                    <span style="color: #64748B;">Total Audited Stories in DB:</span>
                    <strong style="color: #0B1528;">{db_stats['total_records']}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.88rem;">
                    <span style="color: #64748B;">OCR Engine:</span>
                    <strong style="color: {config.COLOR_THEME['primary']};">Tesseract 5.5 (Local)</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.88rem;">
                    <span style="color: #64748B;">History Retention:</span>
                    <strong style="color: {config.COLOR_THEME['real']};">3 Calendar Months (UTC)</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =============================================================================
# 7. CALL TO ACTION SECTION
# =============================================================================
st.markdown(
    f"""
    <div style="background: {config.COLOR_THEME['primary_light']}; border: 1px solid rgba(29, 78, 216, 0.20); border-radius: 10px; padding: 28px 24px; text-align: center; margin: 16px 0 24px 0;">
        <h3 style="font-size: 1.45rem; font-weight: 700; color: #0B1528; margin: 0 0 8px 0;">
            Ready to inspect a news story?
        </h3>
        <p style="color: #334155; font-size: 0.98rem; max-width: 620px; margin: 0 auto 18px auto; line-height: 1.55;">
            Navigate to the News Analyzer to enter an article or upload a clipping screenshot,
            generate calibrated predictions, examine side-by-side LIME and SHAP attributions,
            and corroborate against external fact-checked evidence.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

cta_col1, cta_col2, cta_col3 = st.columns([1.5, 2, 1.5])
with cta_col2:
    if st.button("🚀 Launch News Analyzer Workspace", type="primary", width="stretch", key="bottom_cta_analyze"):
        st.switch_page("pages/1_News_Analyzer.py")

# Bottom Epistemic Disclaimer
st.write("")
render_epistemic_disclaimer()
