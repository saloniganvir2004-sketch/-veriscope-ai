"""
VeriScope AI - Page 2: News Analyzer Workspace
Analyzes news stories supplied via exactly two input workflows:
  Option 1: Manual text entry (separate headline and article context)
  Option 2: Local image upload with Tesseract OCR text extraction and review
Computes calibrated model predictions and renders dual LIME and SHAP explanations.
"""

import io
import streamlit as st
from PIL import Image

import config
from src.utils import (
    load_custom_css,
    render_brand_header,
    render_epistemic_disclaimer,
    build_horizontal_bar_chart,
    highlight_tokens_html,
)
from src.predict import predict_news, load_inference_pipeline
from src.preprocessing import prepare_input_text
from src.lime_explainer import VeritasLimeExplainer
from src.shap_explainer import VeritasShapExplainer
from src.database import save_analysis
from src.evidence_retriever import LocalEvidenceRetriever
from src.ocr import (
    extract_text_from_image,
    validate_image_bytes,
    is_tesseract_available,
    separate_headline_and_body,
)

st.set_page_config(page_title="News Analyzer | VeriScope AI", page_icon="📰", layout="wide")
load_custom_css()

render_brand_header(
    title="News Story Analyzer",
    subtitle="Submit a story manually or upload a screenshot to inspect its classification and understand which words influenced the result.",
)

# -----------------------------------------------------------------------------
# Demonstration Samples
# -----------------------------------------------------------------------------
SAMPLE_REAL = {
    "title": "Federal Reserve Holds Benchmark Interest Rates Steady Amid Inflation Data",
    "text": "The Federal Reserve concluded its monetary policy meeting, voting to leave its benchmark federal funds rate unchanged in the target range of 5.25 to 5.5 percent. Policymakers noted that while job gains have remained solid and unemployment has stayed low, inflation has eased over the past year but remains above the two percent target. Chairman Jerome Powell emphasized that officials require greater statistical confidence that price pressures are sustainably decelerating before initiating any rate reductions.",
}

SAMPLE_FAKE = {
    "title": "SHOCK CLAIM: Secret Deep State Satellite Transmits Brainwaves to Rig Election",
    "text": "BOMBSHELL report exposed by underground whistleblowers! A classified military orbital satellite code-named Dark Zenith is secretly transmitting high-frequency electromagnetic pulses to voting machines across fifty states! Unnamed sources reveal corrupt globalist puppet masters finalized their ultimate plot. Mainstream media fake news networks are in absolute panic and refusing to broadcast the truth! Leaked documents prove the election is already 100% rigged!",
}

# -----------------------------------------------------------------------------
# Session State Initialization (Ensures user inputs are preserved across reruns)
# -----------------------------------------------------------------------------
if "widget_manual_headline" not in st.session_state:
    st.session_state["widget_manual_headline"] = ""
if "widget_manual_body" not in st.session_state:
    st.session_state["widget_manual_body"] = ""
if "widget_ocr_head_val" not in st.session_state:
    st.session_state["widget_ocr_head_val"] = ""
if "widget_ocr_body_val" not in st.session_state:
    st.session_state["widget_ocr_body_val"] = ""
if "ocr_raw_text" not in st.session_state:
    st.session_state["ocr_raw_text"] = ""
if "active_analysis" not in st.session_state:
    st.session_state["active_analysis"] = None
if "record_saved" not in st.session_state:
    st.session_state["record_saved"] = False


def run_pipeline_analysis(headline: str, body: str, source_type: str = "manual"):
    """Executes validated inference pipeline and dual LIME/SHAP explainers."""
    clean_h = (headline or "").strip()
    clean_b = (body or "").strip()

    with st.spinner("Analyzing linguistic patterns and generating LIME and SHAP explanations..."):
        try:
            pipeline = load_inference_pipeline()
            pred_res = predict_news(clean_h, clean_b, pipeline=pipeline, remove_publisher_tags=True)

            # Build unified text for XAI matching training format exactly
            unified_doc = prepare_input_text(clean_h, clean_b, remove_publisher_tags=True)

            lime_exp = VeritasLimeExplainer(pipeline)
            lime_res = lime_exp.explain(unified_doc)

            shap_exp = VeritasShapExplainer(pipeline)
            shap_res = shap_exp.explain(unified_doc)

            st.session_state["active_analysis"] = {
                "source_type": source_type,
                "headline": clean_h,
                "text": clean_b,
                "unified_doc": unified_doc,
                "prediction": pred_res,
                "lime": lime_res,
                "shap": shap_res,
            }
            st.session_state["record_saved"] = False
        except Exception as e:
            st.error(f"Inference pipeline error: {str(e)}")


# -----------------------------------------------------------------------------
# Two Clear Input Options: Tabs
# -----------------------------------------------------------------------------
tab_manual, tab_ocr = st.tabs([
    "📝 Option 1 — Enter News Manually",
    "📷 Option 2 — Upload News Image (OCR)",
])

# =============================================================================
# OPTION 1: MANUAL NEWS ENTRY
# =============================================================================
with tab_manual:
    st.markdown("##### Manual Story Submission")
    st.caption("Provide both the headline and the article context separately for classification.")

    # Demonstration loader and clear controls
    col_s1, col_s2, col_s3, _ = st.columns([1.3, 1.3, 1.2, 3.2])
    with col_s1:
        if st.button("Load Real Sample", key="btn_load_real", help="Load sample real news dispatch"):
            st.session_state["manual_headline"] = SAMPLE_REAL["title"]
            st.session_state["manual_body"] = SAMPLE_REAL["text"]
            st.session_state["widget_manual_headline"] = SAMPLE_REAL["title"]
            st.session_state["widget_manual_body"] = SAMPLE_REAL["text"]
            st.session_state["active_analysis"] = None
            st.session_state["record_saved"] = False
            st.rerun()

    with col_s2:
        if st.button("Load Fake Sample", key="btn_load_fake", help="Load sample disinformation claim"):
            st.session_state["manual_headline"] = SAMPLE_FAKE["title"]
            st.session_state["manual_body"] = SAMPLE_FAKE["text"]
            st.session_state["widget_manual_headline"] = SAMPLE_FAKE["title"]
            st.session_state["widget_manual_body"] = SAMPLE_FAKE["text"]
            st.session_state["active_analysis"] = None
            st.session_state["record_saved"] = False
            st.rerun()

    with col_s3:
        if st.button("Clear Input", key="btn_clear_manual", help="Reset manual inputs"):
            st.session_state["manual_headline"] = ""
            st.session_state["manual_body"] = ""
            st.session_state["widget_manual_headline"] = ""
            st.session_state["widget_manual_body"] = ""
            st.session_state["active_analysis"] = None
            st.session_state["record_saved"] = False
            st.rerun()

    # News Headline Field
    m_headline_input = st.text_input(
        "News Headline *",
        placeholder="Enter news headline (e.g., Central Bank Holds Benchmark Interest Rates Steady)...",
        key="widget_manual_headline",
    )

    # News Context / Article Text Field
    m_body_input = st.text_area(
        "News Context / Article Text *",
        placeholder="Paste full news story context or article paragraphs here...",
        height=200,
        key="widget_manual_body",
    )

    # Word and character counts
    m_char_count = len(m_headline_input) + len(m_body_input)
    m_word_count = len(f"{m_headline_input} {m_body_input}".split()) if m_char_count > 0 else 0

    col_meta, col_btn = st.columns([3, 1])
    with col_meta:
        st.caption(f"{m_word_count} words · {m_char_count} characters (Max {config.OCR_CONFIG['max_text_length']:,})")

    with col_btn:
        trigger_manual = st.button("Analyze News", type="primary", use_container_width=True, key="btn_manual_analyze")

    if trigger_manual:
        # Strict field validation
        has_h = bool(m_headline_input.strip())
        has_b = bool(m_body_input.strip())

        if not has_h and not has_b:
            st.error("Please enter both a News Headline and News Context / Article Text before analyzing.")
        elif not has_h:
            st.error("News Headline is required. Please provide a headline for the article.")
        elif not has_b:
            st.error("News Context / Article Text is required. Please provide the article body.")
        elif m_word_count < 5:
            st.warning("The submitted text is very short (under 5 words). Short snippets may yield low-confidence predictions.")
            run_pipeline_analysis(m_headline_input, m_body_input, source_type="manual")
        elif m_char_count > config.OCR_CONFIG["max_text_length"]:
            st.warning(f"Submitted text exceeds {config.OCR_CONFIG['max_text_length']:,} characters. It will be truncated safely.")
            run_pipeline_analysis(m_headline_input, m_body_input[:config.OCR_CONFIG["max_text_length"]], source_type="manual")
        else:
            run_pipeline_analysis(m_headline_input, m_body_input, source_type="manual")

# =============================================================================
# OPTION 2: IMAGE UPLOAD & TESSERACT OCR
# =============================================================================
with tab_ocr:
    st.markdown("##### Upload a News Image / Screenshot")
    st.caption("Upload a screenshot or photo containing a headline and article text. Text is extracted locally using Tesseract OCR for your review before analysis.")

    # Check Tesseract Availability
    tess_avail, tess_info = is_tesseract_available()
    if not tess_avail:
        st.error(
            "⚠️ **Tesseract OCR is not installed or not accessible.**\n\n"
            "To enable image text extraction on macOS, install Tesseract via Homebrew:\n\n"
            "```bash\n"
            "brew install tesseract\n"
            "```\n\n"
            "Verify installation in your terminal:\n"
            "```bash\n"
            "tesseract --version\n"
            "```\n\n"
            "*You can still use Option 1 (Manual Text Entry) while Tesseract is being installed.*"
        )

    uploaded_image = st.file_uploader(
        "Choose an image file (PNG, JPG, JPEG, WEBP)",
        type=config.OCR_CONFIG["allowed_extensions"],
        help=f"Supported formats: PNG, JPG, JPEG, WEBP. Maximum file size: {config.OCR_CONFIG['max_file_size_mb']}MB.",
        key="ocr_image_uploader",
    )

    if uploaded_image is not None:
        file_bytes = uploaded_image.getvalue()
        is_valid_img, img_err = validate_image_bytes(file_bytes, uploaded_image.name)

        if not is_valid_img:
            st.error(img_err)
        else:
            col_img_left, col_ocr_right = st.columns([1, 1.2])

            with col_img_left:
                try:
                    pil_img = Image.open(io.BytesIO(file_bytes))
                    w, h = pil_img.size
                    st.image(
                        pil_img,
                        caption=f"Uploaded: {uploaded_image.name} ({w}×{h}px · {len(file_bytes)/1024:.1f} KB)",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Could not render image preview: {e}")

                if st.button("🔍 Extract Text via Tesseract OCR", type="primary", use_container_width=True, disabled=not tess_avail):
                    with st.spinner("Executing local Tesseract OCR & image preprocessing..."):
                        ocr_res = extract_text_from_image(file_bytes, uploaded_image.name)
                        if ocr_res["success"]:
                            st.session_state["ocr_headline"] = ocr_res["headline"]
                            st.session_state["ocr_body"] = ocr_res["body"]
                            st.session_state["widget_ocr_head_val"] = ocr_res["headline"]
                            st.session_state["widget_ocr_body_val"] = ocr_res["body"]
                            st.session_state["ocr_raw_text"] = ocr_res["text"]
                            st.success(f"Extracted {ocr_res['word_count']} words successfully! Review and edit the fields below before analyzing.")
                        else:
                            st.error(ocr_res.get("error", "No readable text detected."))

            with col_ocr_right:
                st.markdown("###### Review & Edit Extracted Content")
                st.caption("Verify and correct the extracted headline and article body before submitting for classification.")

                ocr_h_val = st.text_input(
                    "Extracted News Headline (Editable) *",
                    placeholder="Extracted headline will appear here for review...",
                    key="widget_ocr_head_val",
                )

                ocr_b_val = st.text_area(
                    "Extracted Article Context / Text (Editable) *",
                    placeholder="Extracted article body will appear here for verification...",
                    height=200,
                    key="widget_ocr_body_val",
                )

                # Separation helper
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    if st.button("Merge All into Article Context", help="Put headline text into article body"):
                        merged = f"{st.session_state['ocr_headline']}\n\n{st.session_state['ocr_body']}".strip()
                        st.session_state["ocr_body"] = merged
                        st.session_state["ocr_headline"] = ""
                        st.session_state["widget_ocr_body_val"] = merged
                        st.session_state["widget_ocr_head_val"] = ""
                        st.rerun()
                with col_h2:
                    if st.button("Clear Extracted Text", help="Reset OCR fields"):
                        st.session_state["ocr_headline"] = ""
                        st.session_state["ocr_body"] = ""
                        st.session_state["widget_ocr_head_val"] = ""
                        st.session_state["widget_ocr_body_val"] = ""
                        st.session_state["active_analysis"] = None
                        st.rerun()

                ocr_tot_words = len(f"{ocr_h_val} {ocr_b_val}".split()) if (ocr_h_val or ocr_b_val) else 0
                st.caption(f"{ocr_tot_words} words ready for analysis")

                if st.button("Analyze News Story", type="primary", use_container_width=True, key="btn_ocr_analyze"):
                    has_oh = bool(ocr_h_val.strip())
                    has_ob = bool(ocr_b_val.strip())

                    if not has_oh and not has_ob:
                        st.error("No text available for analysis. Please extract text from an image or enter text manually.")
                    elif not has_oh:
                        st.error("News Headline is required. Please enter or confirm the headline before analyzing.")
                    elif not has_ob:
                        st.error("News Context / Article Text is required. Please provide the article body.")
                    elif ocr_tot_words < 5:
                        st.warning("Extracted text is very short (under 5 words). Short snippets may yield low-confidence predictions.")
                        run_pipeline_analysis(ocr_h_val, ocr_b_val, source_type="ocr_image")
                    else:
                        run_pipeline_analysis(ocr_h_val, ocr_b_val, source_type="ocr_image")

# =============================================================================
# UNIFIED CLASSIFICATION RESULTS & EXPLAINABILITY VIEW
# =============================================================================
if st.session_state["active_analysis"]:
    res = st.session_state["active_analysis"]
    pred = res["prediction"]
    lime = res["lime"]
    shap = res["shap"]

    is_fake = pred["prediction"] == "Likely Fake"
    badge_style = "badge-fake" if is_fake else "badge-real"
    score_color = config.COLOR_THEME["fake"] if is_fake else config.COLOR_THEME["real"]
    accent_bar = config.COLOR_THEME["fake"] if is_fake else config.COLOR_THEME["real"]

    st.write("")
    st.markdown("---")
    st.markdown("### Analysis Findings & Explanations")

    # Submitted Story Overview Card
    st.markdown(
        f"""
        <div class="veritas-card" style="border-left: 4px solid {accent_bar};">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: #64748B; font-weight: 600; letter-spacing: 0.04em;">
                Submitted News Headline
            </div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin: 4px 0 10px 0;">
                {res['headline']}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-top: 14px; border-top: 1px solid #E2E8F0; padding-top: 14px;">
                <div>
                    <span style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Classification Assessment</span>
                    <div style="margin-top: 4px;">
                        <span class="{badge_style}">{pred['prediction']}</span>
                    </div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Calibrated Model Confidence</span>
                    <div style="font-size: 1.85rem; font-weight: 700; color: {score_color}; line-height: 1.2;">
                        {pred['confidence']*100:.1f}%
                    </div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Active Model</span>
                    <div style="font-size: 1.05rem; font-weight: 600; color: #0F172A; margin-top: 4px;">
                        {pred['model_name']}
                    </div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Input Source</span>
                    <div style="font-size: 0.95rem; font-weight: 500; color: #334155; margin-top: 4px;">
                        {'Direct Manual Input' if res['source_type'] == 'manual' else 'Extracted Image OCR'}
                    </div>
                </div>
            </div>
            <div style="margin-top: 12px; font-size: 0.84rem; color: #64748B;">
                Probability Distribution:
                <strong style="color: {config.COLOR_THEME['real']}; margin-left: 6px;">Likely Real: {pred['probabilities']['Likely Real']*100:.1f}%</strong> |
                <strong style="color: {config.COLOR_THEME['fake']}; margin-left: 6px;">Likely Fake: {pred['probabilities']['Likely Fake']*100:.1f}%</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Article Context (Collapsible if long)
    if res["text"]:
        if len(res["text"]) > 350:
            with st.expander("📖 View Submitted Article Context (Full Text)"):
                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 14px; font-size: 0.92rem; line-height: 1.6; color: #334155;">
                        {res['text']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                f"""
                <div class="veritas-card" style="padding: 16px 20px;">
                    <div style="font-size: 0.8rem; text-transform: uppercase; color: #64748B; font-weight: 600; margin-bottom: 6px;">
                        Article Context
                    </div>
                    <p style="color: #334155; font-size: 0.92rem; line-height: 1.6; margin: 0;">
                        {res['text']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Stylometric Profile
    stats = pred.get("linguistic_stats", {})
    st_c1, st_c2, st_c3, st_c4 = st.columns(4)
    with st_c1:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-value">{stats.get('caps_ratio', 0.0)*100:.1f}%</div>
                <div class="metric-label">Uppercase Letter Ratio</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st_c2:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-value">{stats.get('exclamation_count', 0)}</div>
                <div class="metric-label">Exclamation Marks</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st_c3:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-value">{stats.get('avg_word_length', 0.0)}</div>
                <div class="metric-label">Avg Word Length</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st_c4:
        sens_color = config.COLOR_THEME["fake"] if stats.get("sensationalism_score", 0) > 0.4 else config.COLOR_THEME["primary"]
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-value" style="color: {sens_color};">{stats.get('sensationalism_score', 0.0)*100:.1f}%</div>
                <div class="metric-label">Sensationalism Index</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Document Attributed Token Highlights
    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                Attributed Token Highlights
            </div>
            <p style="color: #64748B; font-size: 0.85rem; margin-bottom: 12px;">
                Words contributing toward <strong style="color: {config.COLOR_THEME['fake']};">Likely Fake</strong> are highlighted in soft coral;
                words contributing toward <strong style="color: {config.COLOR_THEME['real']};">Likely Real</strong> are highlighted in soft sage green.
            </p>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 16px; border-radius: 6px; font-size: 0.95rem; line-height: 1.8; color: #1E293B;">
                {highlight_tokens_html(res['unified_doc'], shap.get('top_features', []))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Side-by-side LIME and SHAP Explainers
    st.markdown("##### Explainable AI Token Attributions")
    xai_col1, xai_col2 = st.columns(2)

    with xai_col1:
        st.markdown(
            f"""
            <div class="veritas-card" style="height: 100%;">
                <div class="veritas-card-header" style="color: {config.COLOR_THEME['primary']};">
                    LIME Local Explanation
                </div>
                <p style="color: #64748B; font-size: 0.84rem;">
                    Local surrogate ridge regression fitted over {config.LIME_CONFIG['num_samples']} perturbed document variations.
                </p>
            """,
            unsafe_allow_html=True,
        )
        if lime.get("available"):
            fig_lime = build_horizontal_bar_chart(lime["top_features"][:8], title="Top LIME Attributions")
            st.plotly_chart(fig_lime, use_container_width=True)
            st.caption(f"Local Model Fidelity (R²): {lime.get('local_fidelity_r2', 0.0):.3f}")
        else:
            st.info(lime.get("message", "LIME explanation unavailable."))
        st.markdown("</div>", unsafe_allow_html=True)

    with xai_col2:
        st.markdown(
            f"""
            <div class="veritas-card" style="height: 100%;">
                <div class="veritas-card-header" style="color: {config.COLOR_THEME['secondary']};">
                    SHAP Feature Attribution
                </div>
                <p style="color: #64748B; font-size: 0.84rem;">
                    Exact game-theoretic Shapley contributions mapping vocabulary tokens to model log-odds.
                </p>
            """,
            unsafe_allow_html=True,
        )
        if shap.get("available"):
            fig_shap = build_horizontal_bar_chart(shap["top_features"][:8], title="Top SHAP Attributions")
            st.plotly_chart(fig_shap, use_container_width=True)
            st.caption(f"Shapley Expected Base Value: {shap.get('base_value', 0.0):.3f}")
        else:
            st.info(shap.get("message", "SHAP explanation unavailable."))
        st.markdown("</div>", unsafe_allow_html=True)

    # Optional Contextual Evidence Retrieval
    with st.expander("📚 Contextual Evidence Retrieval (Local Reference Corpus)"):
        st.markdown(
            """
            <p style="color: #64748B; font-size: 0.85rem; margin-bottom: 12px;">
                Retrieves semantically aligned passages from our local journalistic and fact-check archive.
                <br><em>Note: Semantic text similarity provides context; it does not constitute definitive proof of truth.</em>
            </p>
            """,
            unsafe_allow_html=True,
        )
        retriever = LocalEvidenceRetriever()
        retrieved_passages = retriever.retrieve(res["unified_doc"], top_k=2)

        if retrieved_passages:
            for p in retrieved_passages:
                status_color = config.COLOR_THEME["real"] if ("Verified" in p["claim_status"] or "Official" in p["claim_status"]) else config.COLOR_THEME["fake"]
                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <span style="font-size: 0.88rem; font-weight: 600; color: #0F172A;">{p['title']}</span>
                            <span style="font-size: 0.75rem; background: #FFFFFF; color: {status_color}; padding: 2px 8px; border-radius: 4px; border: 1px solid {status_color};">
                                {p['claim_status']}
                            </span>
                        </div>
                        <p style="color: #334155; font-size: 0.86rem; margin: 4px 0; line-height: 1.5;">{p['passage']}</p>
                        <div style="font-size: 0.75rem; color: #64748B;">
                            Source: {p['source']} · Date: {p['date']} · Cosine Match: {p['similarity_score']:.3f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No matching reference passages found above the similarity threshold.")

    # Save to Database Section
    st.write("")
    save_col1, save_col2 = st.columns([3, 1])
    with save_col1:
        st.caption("Store this record in the local SQLite database for compliance auditing (auto-retained for 3 calendar months).")
    with save_col2:
        if not st.session_state["record_saved"]:
            if st.button("Save Analysis to History", use_container_width=True, key="btn_save_analysis"):
                top_feats = shap.get("top_features", [])[:5]
                save_analysis(
                    headline=res["headline"],
                    text=res["text"],
                    prediction=pred["prediction"],
                    confidence=pred["confidence"],
                    model_name=pred["model_name"],
                    top_features=top_feats,
                    linguistic_stats=stats,
                )
                st.session_state["record_saved"] = True
                st.success("Analysis saved to local SQLite history!")
                st.rerun()
        else:
            st.button("✓ Record Saved", disabled=True, use_container_width=True, key="btn_saved_disabled")

    # Epistemic notice at bottom of results
    st.write("")
    render_epistemic_disclaimer()
