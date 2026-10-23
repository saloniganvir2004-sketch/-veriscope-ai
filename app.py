"""
VeriScope AI - Main Portal & Application Entrypoint
Intelligence Beyond the Headline.
Editorial Intelligence & Explainable AI for News Credibility Analysis.
"""

import streamlit as st

import config
from src.utils import load_custom_css, render_svg_asset, render_epistemic_disclaimer
from src.database import get_history_stats

# Global Streamlit Page Configuration
st.set_page_config(
    page_title=f"{config.BRAND_NAME} · {config.BRAND_TAGLINE}",
    page_icon="🗞️",
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
        if st.button("📰 Analyze News Story", type="primary", use_container_width=True, key="hero_cta_analyze"):
            st.switch_page("pages/2_News_Analyzer.py")
    with col_btn_xai:
        if st.button("🧪 Explore XAI Lab", use_container_width=True, key="hero_cta_xai"):
            st.switch_page("pages/3_Explainable_AI_Lab.py")

with hero_col2:
    render_svg_asset(config.ASSETS_DIR / "hero_editorial.svg")

st.write("")
st.markdown("---")

# =============================================================================
# 2. HOW IT WORKS (FOUR-STEP WORKFLOW)
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
# 3. CORE CAPABILITIES
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
# 4. VISUAL PROOF OF WORKFLOW
# =============================================================================
st.markdown("### Visual Proof of the Workflow")
st.caption("A genuine demonstration showing how VeriScope AI combines predictions, stylometry, and token attributions.")

proof_c1, proof_c2 = st.columns([1.2, 1])

with proof_c1:
    st.markdown(
        f"""
        <div class="veritas-card" style="border-left: 4px solid {config.COLOR_THEME['real']};">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: #64748B; font-weight: 600;">
                Live Analysis Example · Economic Dispatch
            </div>
            <h4 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 4px 0 8px 0;">
                Federal Reserve Holds Benchmark Interest Rates Steady Amid Inflation Data
            </h4>
            <div style="display: flex; gap: 16px; margin: 12px 0; font-size: 0.88rem;">
                <span class="badge-real">Likely Real</span>
                <span style="color: {config.COLOR_THEME['real']}; font-weight: 700; font-size: 1.1rem;">96.8% Confidence</span>
                <span style="color: #64748B; font-weight: 500;">Architecture: Logistic Regression</span>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 6px; font-size: 0.88rem; line-height: 1.6; color: #334155; margin-top: 10px;">
                The <span class="token-real">Federal Reserve</span> concluded its monetary policy meeting, voting to leave its
                benchmark federal funds <span class="token-real">rate unchanged</span>. Policymakers noted that while job gains have
                remained solid and unemployment low, <span class="token-real">inflation</span> has eased over the past year.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with proof_c2:
    db_stats = get_history_stats()
    st.markdown(
        f"""
        <div class="veritas-card" style="height: 100%;">
            <div class="veritas-card-header">
                System Audit Status
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 8px;">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.9rem;">
                    <span style="color: #64748B;">Active Best Model:</span>
                    <strong style="color: #0F172A;">Logistic Regression (TF-IDF)</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.9rem;">
                    <span style="color: #64748B;">Total Audited Stories in DB:</span>
                    <strong style="color: #0F172A;">{db_stats['total_records']}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.9rem;">
                    <span style="color: #64748B;">OCR Engine:</span>
                    <strong style="color: #0E7490;">Tesseract Local Engine</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span style="color: #64748B;">History Retention:</span>
                    <strong style="color: #15803D;">3 Calendar Months (UTC)</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =============================================================================
# 5. CALL TO ACTION SECTION
# =============================================================================
st.markdown(
    f"""
    <div style="background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px; padding: 28px 24px; text-align: center; margin: 16px 0 24px 0;">
        <h3 style="font-size: 1.45rem; font-weight: 700; color: #0F172A; margin: 0 0 8px 0;">
            Ready to inspect a news story?
        </h3>
        <p style="color: #475569; font-size: 0.98rem; max-width: 620px; margin: 0 auto 18px auto; line-height: 1.5;">
            Navigate to the News Analyzer to enter an article or upload a clipping screenshot,
            generate calibrated predictions, and examine side-by-side LIME and SHAP attributions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

cta_col1, cta_col2, cta_col3 = st.columns([1.5, 2, 1.5])
with cta_col2:
    if st.button("🚀 Launch News Analyzer Workspace", type="primary", use_container_width=True, key="bottom_cta_analyze"):
        st.switch_page("pages/2_News_Analyzer.py")

# Bottom Epistemic Disclaimer
st.write("")
render_epistemic_disclaimer()
