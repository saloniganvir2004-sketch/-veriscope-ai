"""
VeriScope AI - Page 1: Intelligence Dashboard
Refined editorial overview: Hero banner, key metrics, recent analyses, and compact model insight.
"""

import streamlit as st
import pandas as pd
import json

import config
from src.utils import (
    load_custom_css,
    render_brand_header,
    render_svg_asset,
)
from src.database import get_history_stats, get_history

st.set_page_config(page_title="Dashboard | VeriScope AI", page_icon="📊", layout="wide")
load_custom_css()

render_brand_header(
    title="Editorial Intelligence Dashboard",
    subtitle="Auditing linguistic deception and feature contributions with Explainable AI.",
)

# -----------------------------------------------------------------------------
# 1. Hero Section
# -----------------------------------------------------------------------------
hero_col1, hero_col2 = st.columns([1.2, 1])

with hero_col1:
    st.markdown(
        f"""
        <div class="veritas-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center; padding: 28px 24px;">
            <span style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: {config.COLOR_THEME['primary']}; letter-spacing: 0.05em;">
                Editorial Intelligence Platform
            </span>
            <h1 style="font-size: 2.1rem; font-weight: 800; color: #0F172A; margin: 8px 0 10px 0; letter-spacing: -0.03em; line-height: 1.15;">
                {config.BRAND_TAGLINE}
            </h1>
            <p style="color: #475569; font-size: 1.02rem; line-height: 1.55; margin-bottom: 22px;">
                Explore news classifications and discover the exact words influencing AI predictions across articles and screenshot clippings.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("📰 Analyze a News Story", type="primary", use_container_width=True):
        st.switch_page("pages/2_News_Analyzer.py")

with hero_col2:
    # Render crisp editorial vector graphic
    render_svg_asset(config.ASSETS_DIR / "hero_editorial.svg")

st.write("")

# -----------------------------------------------------------------------------
# 2. Key Summary Metrics
# -----------------------------------------------------------------------------
db_stats = get_history_stats()
kpi_c1, kpi_c2, kpi_c3 = st.columns(3)

with kpi_c1:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value">{db_stats['total_records']}</div>
            <div class="metric-label">Total Analyses</div>
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

st.write("")

# -----------------------------------------------------------------------------
# 3. Recent Analyses & Model Insight
# -----------------------------------------------------------------------------
content_left, content_right = st.columns([1.5, 1])

with content_left:
    st.markdown(
        """
        <div class="veritas-card">
            <div class="veritas-card-header">
                Recent Analyses
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
                        <span style="font-size: 0.8rem; color: #64748B;">{r['timestamp']}</span>
                        <span class="{badge_class}" style="font-size: 0.75rem; padding: 2px 8px;">{r['prediction']} ({r['confidence']*100:.1f}%)</span>
                    </div>
                    <div style="font-size: 0.92rem; font-weight: 600; color: #0F172A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {r['headline']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.write("")
        if st.button("View Full Audit History", use_container_width=True):
            st.switch_page("pages/5_Analysis_History.py")
    else:
        render_svg_asset(config.ASSETS_DIR / "empty_audit.svg", width="100%")
        st.markdown(
            """
            <div style="text-align: center; color: #64748B; font-size: 0.88rem; margin-top: -10px;">
                No saved analyses yet. Submit a headline or article in the News Analyzer to begin.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with content_right:
    # Model Insight
    perf_file = config.METRICS_DIR / "model_comparison.json"
    model_metrics = None
    if perf_file.exists():
        with open(perf_file, "r") as f:
            model_metrics = json.load(f)

    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                Model Insight
            </div>
            <p style="color: #64748B; font-size: 0.86rem; margin-bottom: 14px;">
                Active production classifier trained on sanitized, leakage-audited news corpora with TF-IDF features.
            </p>
        """,
        unsafe_allow_html=True,
    )

    if model_metrics and "test_evaluations" in model_metrics:
        best_name = model_metrics.get("best_model_name", "Logistic Regression")
        best_test = model_metrics["test_evaluations"].get(best_name, {})
        st.markdown(
            f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 14px; margin-bottom: 14px;">
                <div style="font-size: 0.78rem; text-transform: uppercase; color: #64748B; font-weight: 600;">Selected Architecture</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 2px 0 10px 0;">{best_name}</div>
                <div style="display: flex; gap: 16px;">
                    <div>
                        <div style="font-size: 0.75rem; color: #64748B;">Test Accuracy</div>
                        <div style="font-size: 1.1rem; font-weight: 600; color: {config.COLOR_THEME['primary']};">{best_test.get('accuracy', 1.0)*100:.1f}%</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: #64748B;">Macro F1</div>
                        <div style="font-size: 1.1rem; font-weight: 600; color: {config.COLOR_THEME['text_main']};">{best_test.get('macro_f1', 1.0):.4f}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Model Benchmarks", use_container_width=True):
            st.switch_page("pages/4_Model_Performance.py")
    else:
        st.info("Evaluation metrics not found. Run training pipeline to view benchmarks.")

    st.markdown("</div>", unsafe_allow_html=True)
