"""
VeriScope AI - Page 2: News Analyzer Workspace
Analyzes news stories supplied via direct text or image screenshots (OCR),
computes calibrated model predictions, and renders dual LIME and SHAP explanations.
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
from src.lime_explainer import VeritasLimeExplainer
from src.shap_explainer import VeritasShapExplainer
from src.database import save_analysis
from src.evidence_retriever import LocalEvidenceRetriever
from src.ocr import extract_text_from_image, validate_image_bytes

st.set_page_config(page_title="News Analyzer | VeriScope AI", page_icon="📰", layout="wide")
load_custom_css()

render_brand_header(
    title="Analyze a News Story",
    subtitle="Paste an article or upload a screenshot to examine its classification and understand which words influenced the result.",
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
# Session State Initialization (Ensures user inputs are never silently discarded)
# -----------------------------------------------------------------------------
if "text_headline" not in st.session_state:
    st.session_state["text_headline"] = ""
if "text_body" not in st.session_state:
    st.session_state["text_body"] = ""
if "ocr_extracted_text" not in st.session_state:
    st.session_state["ocr_extracted_text"] = ""
if "ocr_headline" not in st.session_state:
    st.session_state["ocr_headline"] = ""
if "active_analysis" not in st.session_state:
    st.session_state["active_analysis"] = None
if "record_saved" not in st.session_state:
    st.session_state["record_saved"] = False

# -----------------------------------------------------------------------------
# Two Input Modes: Paste Text & Upload Image
# -----------------------------------------------------------------------------
tab_text, tab_image = st.tabs(["📝 Paste Text", "📷 Upload Image (OCR)"])

# -----------------------------------------------------------------------------
# TAB 1: TEXT INPUT WORKSPACE
# -----------------------------------------------------------------------------
with tab_text:
    st.markdown("##### Story Input")

    # Sample loader and clear buttons
    col_d1, col_d2, col_d3, _ = st.columns([1.3, 1.3, 1.2, 3.2])
    with col_d1:
        if st.button("Load Real Sample", help="Demonstration real news dispatch"):
            st.session_state["text_headline"] = SAMPLE_REAL["title"]
            st.session_state["text_body"] = SAMPLE_REAL["text"]
            st.session_state["active_analysis"] = None
            st.session_state["record_saved"] = False
            st.rerun()

    with col_d2:
        if st.button("Load Fake Sample", help="Demonstration disinformation claim"):
            st.session_state["text_headline"] = SAMPLE_FAKE["title"]
            st.session_state["text_body"] = SAMPLE_FAKE["text"]
            st.session_state["active_analysis"] = None
            st.session_state["record_saved"] = False
            st.rerun()

    with col_d3:
        if st.button("Clear Input", help="Reset all fields"):
            st.session_state["text_headline"] = ""
            st.session_state["text_body"] = ""
            st.session_state["active_analysis"] = None
            st.session_state["record_saved"] = False
            st.rerun()

    headline_val = st.text_input(
        "Headline or Claim Title",
        value=st.session_state["text_headline"],
        placeholder="Enter headline (e.g. Central Bank Holds Interest Rates Steady)...",
        key="widget_headline_input",
    )
    # Synchronize state
    st.session_state["text_headline"] = headline_val

    body_val = st.text_area(
        "Article Body or Context",
        value=st.session_state["text_body"],
        placeholder="Paste full news story or social media post text here...",
        height=180,
        key="widget_body_input",
    )
    st.session_state["text_body"] = body_val

    # Character and word counters
    total_chars = len(headline_val) + len(body_val)
    total_words = len(f"{headline_val} {body_val}".split()) if total_chars > 0 else 0

    col_meta, col_btn = st.columns([3, 1])
    with col_meta:
        st.caption(f"{total_words} words · {total_chars} characters (max {config.OCR_CONFIG['max_text_length']:,})")

    with col_btn:
        trigger_text_analysis = st.button("Analyze News Story", type="primary", use_container_width=True)

    if trigger_text_analysis:
        if not headline_val.strip() and not body_val.strip():
            st.error("Please enter a headline or article text before analyzing.")
        elif total_words < 5:
            st.warning("The submitted text is very short (under 5 words). Short snippets may yield low-confidence predictions.")
            run_anyway = True
        elif total_chars > config.OCR_CONFIG["max_text_length"]:
            st.warning(f"Submitted text exceeds {config.OCR_CONFIG['max_text_length']:,} characters. It will be truncated safely.")
            body_val = body_val[:config.OCR_CONFIG["max_text_length"]]
            run_anyway = True
        else:
            run_anyway = True

        if headline_val.strip() or body_val.strip():
            with st.spinner("Analyzing linguistic patterns and generating LIME and SHAP explanations..."):
                try:
                    pipeline = load_inference_pipeline()
                    pred_res = predict_news(headline_val, body_val, pipeline=pipeline)
                    full_text = f"{headline_val}. {body_val}" if headline_val else body_val

                    lime_exp = VeritasLimeExplainer(pipeline)
                    lime_res = lime_exp.explain(full_text)

                    shap_exp = VeritasShapExplainer(pipeline)
                    shap_res = shap_exp.explain(full_text)

                    st.session_state["active_analysis"] = {
                        "source_type": "text",
                        "headline": headline_val,
                        "text": body_val,
                        "prediction": pred_res,
                        "lime": lime_res,
                        "shap": shap_res,
                    }
                    st.session_state["record_saved"] = False
                except Exception as e:
                    st.error(f"Inference error: {str(e)}")

# -----------------------------------------------------------------------------
# TAB 2: IMAGE UPLOAD & OCR WORKSPACE
# -----------------------------------------------------------------------------
with tab_image:
    st.markdown("##### Upload a News Screenshot or Photo")
    st.markdown(
        "<p style='color: #64748B; font-size: 0.88rem; margin-top: -6px;'>"
        "Upload a news screenshot, clipping, or headline photograph. Text will be extracted locally via Tesseract OCR for your review before analysis."
        "</p>",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=config.OCR_CONFIG["allowed_extensions"],
        help="Supported formats: JPG, JPEG, PNG, WEBP (Max 10MB)",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        is_valid, validation_err = validate_image_bytes(file_bytes, uploaded_file.name)

        if not is_valid:
            st.error(validation_err)
        else:
            col_img_prev, col_ocr_res = st.columns([1, 1])

            with col_img_prev:
                try:
                    image_obj = Image.open(io.BytesIO(file_bytes))
                    w, h = image_obj.size
                    st.image(image_obj, caption=f"Uploaded Image: {uploaded_file.name} ({w}×{h} px)", use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to display image: {e}")

                if st.button("🔍 Extract Text via OCR", type="primary", use_container_width=True):
                    with st.spinner("Processing image and performing Optical Character Recognition..."):
                        ocr_result = extract_text_from_image(file_bytes, uploaded_file.name)
                        if ocr_result["success"]:
                            st.session_state["ocr_extracted_text"] = ocr_result["text"]
                            # Infer first line as potential headline if short
                            lines = [l.strip() for l in ocr_result["text"].splitlines() if l.strip()]
                            if lines and len(lines[0]) < 120 and len(lines) > 1:
                                st.session_state["ocr_headline"] = lines[0]
                                st.session_state["ocr_extracted_text"] = "\n".join(lines[1:])
                            st.success(f"Successfully extracted {ocr_result['word_count']} words.")
                        else:
                            st.error(ocr_result.get("error", "No readable text detected."))

            with col_ocr_res:
                st.markdown("###### Review & Edit Extracted Text")
                ocr_head_val = st.text_input(
                    "Extracted Headline (Editable)",
                    value=st.session_state["ocr_headline"],
                    placeholder="Headline extracted from image...",
                    key="widget_ocr_head",
                )
                st.session_state["ocr_headline"] = ocr_head_val

                ocr_body_val = st.text_area(
                    "Extracted Article Body (Editable)",
                    value=st.session_state["ocr_extracted_text"],
                    placeholder="Article text extracted via OCR will appear here for verification...",
                    height=200,
                    key="widget_ocr_body",
                )
                st.session_state["ocr_extracted_text"] = ocr_body_val

                ocr_words = len(f"{ocr_head_val} {ocr_body_val}".split()) if (ocr_head_val or ocr_body_val) else 0
                st.caption(f"{ocr_words} words extracted")

                if st.button("Analyze Extracted Story", type="primary", use_container_width=True):
                    if not ocr_head_val.strip() and not ocr_body_val.strip():
                        st.error("No text available for analysis. Please extract text from an image or enter text manually.")
                    else:
                        with st.spinner("Analyzing extracted text and computing explanations..."):
                            try:
                                pipeline = load_inference_pipeline()
                                pred_res = predict_news(ocr_head_val, ocr_body_val, pipeline=pipeline)
                                full_text = f"{ocr_head_val}. {ocr_body_val}" if ocr_head_val else ocr_body_val

                                lime_exp = VeritasLimeExplainer(pipeline)
                                lime_res = lime_exp.explain(full_text)

                                shap_exp = VeritasShapExplainer(pipeline)
                                shap_res = shap_exp.explain(full_text)

                                st.session_state["active_analysis"] = {
                                    "source_type": "image",
                                    "headline": ocr_head_val,
                                    "text": ocr_body_val,
                                    "prediction": pred_res,
                                    "lime": lime_res,
                                    "shap": shap_res,
                                }
                                st.session_state["record_saved"] = False
                            except Exception as e:
                                st.error(f"Inference error: {str(e)}")

# -----------------------------------------------------------------------------
# UNIFIED ANALYSIS FINDINGS VIEW
# -----------------------------------------------------------------------------
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
    st.markdown("### Analysis Findings")

    # Classification Banner Card
    st.markdown(
        f"""
        <div class="veritas-card" style="border-left: 4px solid {accent_bar};">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div>
                    <span style="font-size: 0.82rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Model Assessment</span>
                    <div style="margin-top: 4px;">
                        <span class="{badge_style}">{pred['prediction']}</span>
                    </div>
                </div>
                <div>
                    <span style="font-size: 0.82rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Classification Confidence</span>
                    <div style="font-size: 1.85rem; font-weight: 700; color: {score_color}; line-height: 1.2;">
                        {pred['confidence']*100:.1f}%
                    </div>
                </div>
                <div>
                    <span style="font-size: 0.82rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Model Architecture</span>
                    <div style="font-size: 1.05rem; font-weight: 600; color: #0F172A; margin-top: 4px;">
                        {pred['model_name']}
                    </div>
                </div>
            </div>
            <div style="margin-top: 14px; border-top: 1px solid #E2E8F0; padding-top: 10px; display: flex; gap: 20px; font-size: 0.85rem; color: #64748B;">
                <span>Probability Breakdown:</span>
                <span style="color: {config.COLOR_THEME['real']}; font-weight: 500;">Likely Real: {pred['probabilities']['Likely Real']*100:.1f}%</span>
                <span style="color: {config.COLOR_THEME['fake']}; font-weight: 500;">Likely Fake: {pred['probabilities']['Likely Fake']*100:.1f}%</span>
            </div>
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
                Words contributing toward <strong style="color: {config.COLOR_THEME['fake']};">Likely Fake</strong> are highlighted in coral;
                words contributing toward <strong style="color: {config.COLOR_THEME['real']};">Likely Real</strong> are highlighted in sage green.
            </p>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 16px; border-radius: 6px; font-size: 0.95rem; line-height: 1.8; color: #1E293B;">
                {highlight_tokens_html(f"{res['headline']}. {res['text']}" if res['headline'] else res['text'], shap.get('top_features', []))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Side-by-side LIME and SHAP
    st.markdown("##### Explainable AI Attributions")
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
                Retrieves semantically aligned passages from our local, verified journalistic and fact-check archive.
                <br><em>Note: Text similarity provides context; it does not constitute definitive proof of truth.</em>
            </p>
            """,
            unsafe_allow_html=True,
        )
        retriever = LocalEvidenceRetriever()
        retrieved_passages = retriever.retrieve(f"{res['headline']} {res['text']}", top_k=2)

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
        st.caption("Store this record in the local SQLite database for historical compliance and audit logging.")
    with save_col2:
        if not st.session_state["record_saved"]:
            if st.button("Save Analysis to History", use_container_width=True):
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
            st.button("✓ Record Saved", disabled=True, use_container_width=True)

    # Epistemic notice at bottom of results
    st.write("")
    render_epistemic_disclaimer()
