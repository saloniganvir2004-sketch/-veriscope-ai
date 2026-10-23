"""
VeriScope AI - Main Portal & Application Entrypoint
Intelligence Beyond the Headline.
"""

import streamlit as st

import config
from src.utils import load_custom_css, render_brand_header, render_svg_asset
from src.database import get_history_stats

# Global Streamlit Configuration
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

# Main Portal Header
render_brand_header(
    title="Editorial Intelligence & Explainable AI",
    subtitle="An integrated machine learning platform to inspect news articles and understand AI classifications.",
)

# Landing Grid
col_hero, col_card = st.columns([1.3, 1])

with col_hero:
    st.markdown(
        f"""
        <div class="veritas-card" style="padding: 26px;">
            <h3 style="font-size: 1.4rem; font-weight: 700; color: #0F172A; margin: 0 0 10px 0;">
                Auditing News Deception with Transparent ML
            </h3>
            <p style="color: #475569; font-size: 0.96rem; line-height: 1.6; margin-bottom: 16px;">
                <strong>VeriScope AI</strong> enables journalists, researchers, and readers to analyze text stories
                and screenshot clippings. By coupling statistical machine learning with <strong>LIME</strong> and <strong>SHAP</strong>,
                it reveals exactly which phrases push predictions toward <em>Likely Fake</em> or <em>Likely Real</em>.
            </p>
            <div style="display: flex; gap: 12px; margin-top: 14px;">
                <div style="border-left: 2px solid {config.COLOR_THEME['primary']}; padding-left: 10px;">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: #64748B; font-weight: 600;">Text & OCR Input</div>
                    <div style="font-size: 0.9rem; color: #0F172A; font-weight: 500;">Paste articles or upload screenshots</div>
                </div>
                <div style="border-left: 2px solid {config.COLOR_THEME['real']}; padding-left: 10px;">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: #64748B; font-weight: 600;">Dual Explanations</div>
                    <div style="font-size: 0.9rem; color: #0F172A; font-weight: 500;">Side-by-side LIME and SHAP attributions</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_card:
    render_svg_asset(config.ASSETS_DIR / "hero_editorial.svg")

st.write("")
st.markdown("#### Explore Workspaces")

w_c1, w_c2, w_c3 = st.columns(3)

with w_c1:
    st.markdown(
        """
        <div class="veritas-card" style="height: 100%;">
            <div class="veritas-card-header">
                📰 News Analyzer
            </div>
            <p style="color: #64748B; font-size: 0.88rem; line-height: 1.5; margin-bottom: 16px;">
                Submit an article or upload a news clipping screenshot. Extract text via local OCR and generate real-time LIME & SHAP token attributions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open News Analyzer", use_container_width=True, key="btn_nav_an"):
        st.switch_page("pages/2_News_Analyzer.py")

with w_c2:
    st.markdown(
        """
        <div class="veritas-card" style="height: 100%;">
            <div class="veritas-card-header">
                🧪 Explainable AI Lab
            </div>
            <p style="color: #64748B; font-size: 0.88rem; line-height: 1.5; margin-bottom: 16px;">
                Examine LIME vs SHAP concordance, test perturbation stability, and evaluate feature faithfulness with token masking experiments.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open XAI Research Lab", use_container_width=True, key="btn_nav_xai"):
        st.switch_page("pages/3_Explainable_AI_Lab.py")

with w_c3:
    st.markdown(
        """
        <div class="veritas-card" style="height: 100%;">
            <div class="veritas-card-header">
                📈 Model Benchmarks
            </div>
            <p style="color: #64748B; font-size: 0.88rem; line-height: 1.5; margin-bottom: 16px;">
                Review held-out test evaluation benchmarks, confusion matrices, and Platt probability calibration across candidate models.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("View Model Performance", use_container_width=True, key="btn_nav_perf"):
        st.switch_page("pages/4_Model_Performance.py")
