"""
VeriScope AI - Page 5: Analysis History Audit Log
Local SQLite persistent storage for auditing user-submitted analyses,
filtering by class, inspecting token contributions, and exporting records.
Enforces an automatic 3-calendar-month retention policy using UTC timestamps.
"""

import streamlit as st
import pandas as pd
import json

import config
from src.utils import load_custom_css, render_brand_header, render_svg_asset
from src.database import (
    get_history,
    delete_analysis,
    clear_history,
    get_history_stats,
    delete_expired_history,
    get_retention_info,
)

st.set_page_config(page_title="Audit History | VeriScope AI", page_icon="🗄️", layout="wide")
load_custom_css()

render_brand_header(
    title="Analysis Audit History & Records",
    subtitle="Query, filter, inspect, and export persistent records stored locally in SQLite.",
)

# Retention Policy Notice Bar
ret_info = get_retention_info(months=3)
st.markdown(
    f"""
    <div style="background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 6px; padding: 10px 16px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div style="font-size: 0.86rem; color: #334155;">
            <strong>Retention Policy:</strong> Records are retained for <strong>3 calendar months</strong> (UTC) and automatically purged on startup and save. Current cutoff: <code style="color: #0E7490;">{ret_info['cutoff_timestamp']}</code>.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Controls Row: Search & Filters
c_search, c_filter, c_limit = st.columns([2, 1, 1])

with c_search:
    search_q = st.text_input("🔍 Search by Headline or Content Snippet:", placeholder="e.g. Federal Reserve, election...")

with c_filter:
    class_filter = st.selectbox("Filter by Class:", ["All", "Likely Real", "Likely Fake"])

with c_limit:
    record_limit = st.selectbox("Records to Show:", [10, 25, 50, 100], index=1)

# Fetch Records
selected_class = None if class_filter == "All" else class_filter
records = get_history(
    search_query=search_q,
    label_filter=selected_class,
    limit=record_limit,
)

# Top Action Row
db_stats = get_history_stats()
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 14px 0 16px 0;">
        <span style="color: #64748B; font-size: 0.88rem;">
            Showing <strong>{len(records)}</strong> of <strong>{db_stats['total_records']}</strong> total stored analyses.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Display Records
if records:
    for r in records:
        is_fake = r["prediction"] == "Likely Fake"
        badge_class = "badge-fake" if is_fake else "badge-real"
        card_border = config.COLOR_THEME["fake"] if is_fake else config.COLOR_THEME["real"]

        with st.expander(f"[{r['timestamp']} UTC] {r['headline']} — {r['prediction']} ({r['confidence']*100:.1f}%)"):
            st.markdown(
                f"""
                <div style="border-left: 3px solid {card_border}; padding-left: 12px; margin-bottom: 12px;">
                    <span class="{badge_class}" style="font-size: 0.85rem; padding: 3px 10px;">{r['prediction']}</span>
                    <span style="margin-left: 12px; color: #64748B; font-size: 0.85rem;">Model: <strong>{r['model_name']}</strong></span>
                    <span style="margin-left: 12px; color: #64748B; font-size: 0.85rem;">Confidence: <strong>{r['confidence']*100:.1f}%</strong></span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("**Article Snippet:**")
            st.markdown(f"> *{r['snippet']}*")

            # Top Features
            if r["top_features"]:
                st.markdown("**Top Explanatory Features Recorded:**")
                feat_tags = []
                for f in r["top_features"][:6]:
                    f_name = f.get("feature", "")
                    f_weight = f.get("weight", 0.0)
                    color = config.COLOR_THEME["fake"] if f_weight > 0 else config.COLOR_THEME["real"]
                    feat_tags.append(
                        f"<span style='background: #F8FAFC; border: 1px solid {color}; padding: 3px 8px; border-radius: 4px; font-size: 0.82rem; color: #0F172A; margin-right: 6px;'>"
                        f"<strong>{f_name}</strong> ({f_weight:+.3f})"
                        f"</span>"
                    )
                st.markdown("".join(feat_tags), unsafe_allow_html=True)

            # Linguistic stats
            if r.get("linguistic_stats"):
                st.write("")
                st.caption(
                    f"Linguistic Profile: Caps Ratio: {r['linguistic_stats'].get('caps_ratio', 0)*100:.1f}% | "
                    f"Exclamations: {r['linguistic_stats'].get('exclamation_count', 0)} | "
                    f"Sensationalism Index: {r['linguistic_stats'].get('sensationalism_score', 0)*100:.1f}%"
                )

            # Action: Delete individual entry
            st.write("")
            if st.button(f"Delete Record #{r['id']}", key=f"del_{r['id']}"):
                delete_analysis(r["id"])
                st.success(f"Record #{r['id']} deleted.")
                st.rerun()

    # Export & Bulk Actions
    st.write("")
    st.markdown("---")
    act_col1, act_col2, act_col3 = st.columns([1.5, 1.2, 1.3])

    with act_col1:
        # Export to CSV
        export_df = pd.DataFrame(records)[["id", "timestamp", "headline", "snippet", "prediction", "confidence", "model_name"]]
        csv_data = export_df.to_csv(index=False)
        st.download_button(
            label="📥 Export Current Results to CSV",
            data=csv_data,
            file_name="veriscope_ai_analysis_audit.csv",
            mime="text/csv",
        )

    with act_col2:
        if st.button("🧹 Run 3-Month Retention Cleanup"):
            purged = delete_expired_history(months=3)
            if purged > 0:
                st.success(f"Purged {purged} record(s) older than 3 calendar months.")
            else:
                st.info("No expired records found (all records are within 3 calendar months).")
            st.rerun()

    with act_col3:
        confirm_clear = st.checkbox("Confirm Purge All History", key="chk_purge")
        if confirm_clear:
            if st.button("🚨 Clear Entire History", type="secondary"):
                cleared_count = clear_history()
                st.warning(f"Cleared {cleared_count} records from database.")
                st.rerun()

else:
    st.markdown('<div class="veritas-card" style="text-align: center; padding: 30px 20px;">', unsafe_allow_html=True)
    render_svg_asset(config.ASSETS_DIR / "empty_audit.svg", width="100%")
    st.markdown(
        """
        <h4 style="color: #0F172A; margin: 12px 0 4px 0;">No Analysis Records Found</h4>
        <p style="color: #64748B; font-size: 0.88rem; margin-bottom: 16px;">
            No saved analyses match your search criteria or the database is currently empty.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to News Analyzer"):
        st.switch_page("pages/2_News_Analyzer.py")
