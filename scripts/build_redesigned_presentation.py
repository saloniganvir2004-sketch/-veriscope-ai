"""
VeriScope AI - Master Presentation Redesign Generator
Produces: VeriScope_AI_Redesigned.pptx
Adheres strictly to Amity Integrated Project Presentation Format:
  1. Title
  2. Introduction
  3. Abstract
  4. Project Introduction — bullet points
  5. Software and Hardware Requirements
  6. Implementation
  7. Actual Output Screenshots
  8. Conclusion
  9. Future Scope
  10. References
Total Slides: 20
Theme: Futuristic, cinematic AI aesthetic (Midnight Navy, Deep Black, Electric Cyan, Teal, Violet).
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------------------------
BG_DARK = RGBColor(6, 11, 20)           # Midnight Navy / Deep Black
CARD_BG = RGBColor(13, 21, 38)          # Elevated Container Fill
CARD_BG_ALT = RGBColor(17, 28, 51)      # Alternate Elevated Card
BORDER_CYAN = RGBColor(14, 116, 144)    # Glowing Cyan Border
BORDER_SUBTLE = RGBColor(30, 45, 74)    # Subtle Container Border
BORDER_VIOLET = RGBColor(109, 40, 217)  # Violet Accent Border

CYAN = RGBColor(0, 242, 254)            # Electric Cyan Accent
SKY = RGBColor(56, 189, 248)            # Light Sky Cyan
TEAL = RGBColor(20, 184, 166)           # Vibrant Teal
VIOLET = RGBColor(168, 85, 247)         # Subtle Glowing Violet
WHITE = RGBColor(255, 255, 255)         # Crisp White
ICE = RGBColor(226, 232, 240)           # Ice Blue Body Text
SLATE = RGBColor(148, 163, 184)         # Slate Secondary Text
MUTED = RGBColor(100, 116, 139)         # Muted Label Text
GREEN = RGBColor(34, 197, 94)           # Success / Verified Green
GOLD = RGBColor(245, 158, 11)           # Warning / Highlight Gold

FONT_NAME = "Arial"

# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def add_base_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    return slide

def add_header(slide, section_tag, title_text, subtitle_text=None):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.32))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = section_tag.upper()
    p_c.font.name = FONT_NAME
    p_c.font.size = Pt(9.5)
    p_c.font.bold = True
    p_c.font.color.rgb = CYAN

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.70), Inches(11.733), Inches(0.50))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_NAME
    p_t.font.size = Pt(19)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.18), Inches(11.733), Inches(0.32))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle_text
        p_s.font.name = FONT_NAME
        p_s.font.size = Pt(10.5)
        p_s.font.color.rgb = SLATE

    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.52), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_SUBTLE
    line.line.fill.background()

def add_card(slide, left, top, width, height, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE, border_width=1):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_rgb
    if border_rgb:
        card.line.color.rgb = border_rgb
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_metric_badge(slide, left, top, width, height, value_text, label_text, sub_text=None, accent_color=CYAN):
    add_card(slide, left, top, width, height, bg_rgb=CARD_BG_ALT, border_rgb=accent_color, border_width=1.2)
    tx = slide.shapes.add_textbox(left + Inches(0.12), top + Inches(0.10), width - Inches(0.24), height - Inches(0.20))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p_val = tf.paragraphs[0]
    p_val.text = value_text
    p_val.font.name = FONT_NAME
    p_val.font.size = Pt(20)
    p_val.font.bold = True
    p_val.font.color.rgb = accent_color
    p_val.alignment = PP_ALIGN.CENTER

    p_lbl = tf.add_paragraph()
    p_lbl.text = label_text
    p_lbl.font.name = FONT_NAME
    p_lbl.font.size = Pt(9.5)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = WHITE
    p_lbl.alignment = PP_ALIGN.CENTER

    if sub_text:
        p_sub = tf.add_paragraph()
        p_sub.text = sub_text
        p_sub.font.name = FONT_NAME
        p_sub.font.size = Pt(8.0)
        p_sub.font.color.rgb = SLATE
        p_sub.alignment = PP_ALIGN.CENTER

def add_table(slide, left, top, width, height, headers, rows_data, col_widths=None):
    num_rows = len(rows_data) + 1
    num_cols = len(headers)
    tbl_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    tbl = tbl_shape.table

    if col_widths:
        for idx, w in enumerate(col_widths):
            tbl.columns[idx].width = Inches(w)

    for c_idx, title in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG_ALT
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = title
        p.font.name = FONT_NAME
        p.font.size = Pt(9.0)
        p.font.bold = True
        p.font.color.rgb = CYAN
        p.alignment = PP_ALIGN.CENTER

    for r_idx, row in enumerate(rows_data):
        row_bg = CARD_BG if r_idx % 2 == 0 else RGBColor(10, 17, 31)
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = FONT_NAME
            p.font.size = Pt(8.5)
            p.font.color.rgb = WHITE if c_idx == 0 else ICE
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER

    return tbl_shape

# ---------------------------------------------------------------------------
# SLIDE BUILDERS
# ---------------------------------------------------------------------------

def build_slide_01_title(prs):
    slide = add_base_slide(prs)

    # Decorative glow rings (subtle layered shapes)
    ring1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.0), Inches(-1.5), Inches(5.5), Inches(5.5))
    ring1.fill.solid()
    ring1.fill.fore_color.rgb = RGBColor(14, 25, 48)
    ring1.line.color.rgb = BORDER_CYAN
    ring1.line.width = Pt(1.5)

    ring2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.8), Inches(-0.7), Inches(3.9), Inches(3.9))
    ring2.fill.solid()
    ring2.fill.fore_color.rgb = RGBColor(10, 19, 36)
    ring2.line.color.rgb = BORDER_VIOLET
    ring2.line.width = Pt(1.0)

    # Top Pill Badge
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(4.5), Inches(0.38))
    pill.fill.solid()
    pill.fill.fore_color.rgb = CARD_BG_ALT
    pill.line.color.rgb = BORDER_CYAN
    pill.line.width = Pt(1.0)
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "INTEGRATED CAPSTONE PROJECT REPORT  •  2026"
    p_pill.font.name = FONT_NAME
    p_pill.font.size = Pt(8.5)
    p_pill.font.bold = True
    p_pill.font.color.rgb = CYAN
    p_pill.alignment = PP_ALIGN.CENTER

    # Project Title
    tx_title = slide.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.0), Inches(1.4))
    tf_t = tx_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0

    p1 = tf_t.paragraphs[0]
    p1.text = "VERISCOPE AI"
    p1.font.name = FONT_NAME
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf_t.add_paragraph()
    p2.text = "Fake News Detection Using Explainable AI"
    p2.font.name = FONT_NAME
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = CYAN

    p3 = tf_t.add_paragraph()
    p3.text = "Intelligence Beyond the Headline"
    p3.font.name = FONT_NAME
    p3.font.size = Pt(13)
    p3.font.italic = True
    p3.font.color.rgb = SLATE

    # Subtitle Card / Academic Program
    card_prog = add_card(slide, Inches(1.0), Inches(3.3), Inches(11.333), Inches(1.0), bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)
    tx_prog = slide.shapes.add_textbox(Inches(1.2), Inches(3.4), Inches(10.9), Inches(0.8))
    tf_p = tx_prog.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0

    p_deg = tf_p.paragraphs[0]
    p_deg.text = "Master of Science in Artificial Intelligence and Data Analytics  (Semester IV)"
    p_deg.font.name = FONT_NAME
    p_deg.font.size = Pt(13)
    p_deg.font.bold = True
    p_deg.font.color.rgb = WHITE

    p_inst = tf_p.add_paragraph()
    p_inst.text = "Amity Institute of Information Technology  |  Amity University, Noida  |  Academic Year 2025–2026"
    p_inst.font.name = FONT_NAME
    p_inst.font.size = Pt(10.5)
    p_inst.font.color.rgb = SKY

    # Team Members Ribbon on Title Slide
    card_team = add_card(slide, Inches(1.0), Inches(4.5), Inches(11.333), Inches(2.2), bg_rgb=CARD_BG_ALT, border_rgb=BORDER_CYAN, border_width=1.2)
    tx_team = slide.shapes.add_textbox(Inches(1.2), Inches(4.6), Inches(10.9), Inches(2.0))
    tf_tm = tx_team.text_frame
    tf_tm.word_wrap = True
    tf_tm.margin_left = tf_tm.margin_right = tf_tm.margin_top = tf_tm.margin_bottom = 0

    p_th = tf_tm.paragraphs[0]
    p_th.text = "PROJECT RESEARCH COHORT (ALL 5 MEMBERS)"
    p_th.font.name = FONT_NAME
    p_th.font.size = Pt(9.5)
    p_th.font.bold = True
    p_th.font.color.rgb = CYAN

    members_line1 = [
        "1. Ayushman Kumar (A010175625019) — NLP Preprocessing & Reference Corpus [PRESENTER]",
        "2. Astha Thapa (A010175625014) — ML Classification & Hyperparameters [PRESENTER]",
        "3. Saloni Ganvir (A010175625017) — Explainable AI (LIME/SHAP) & NLI [PRESENTER]"
    ]
    members_line2 = [
        "4. Sri Rinith (A010175625018) — Model Evaluation & RL Bandit [PRESENTER]",
        "5. Sarvesh (A010175625016) — Editorial UI, Web App & OCR [TEAM MEMBER — Non-Speaking Role]"
    ]
    for m in members_line1 + members_line2:
        p = tf_tm.add_paragraph()
        p.text = f"•  {m}"
        p.font.name = FONT_NAME
        p.font.size = Pt(9.5)
        p.font.color.rgb = ICE if "PRESENTER" in m else SLATE

def build_slide_02_team(prs):
    slide = add_base_slide(prs)
    add_header(slide, "01 • PROJECT RESEARCH TEAM", "Team Members, Specializations & Technical Responsibilities",
               "MSc AI & Data Analytics Cohort — Complete Technical Ownership Across All Engineering Modules")

    members = [
        {
            "name": "Ayushman Kumar", "roll": "A010175625019",
            "role": "NLP Preprocessing & Corpus",
            "status": "PRESENTER", "status_col": CYAN,
            "tasks": [
                "Sourced & audited 44,898 ISOT articles",
                "Regex wire-tag eradication ('(Reuters)')",
                "Sublinear TF-IDF (5,000 max features)",
                "Stratified holdout group validation"
            ]
        },
        {
            "name": "Astha Thapa", "roll": "A010175625014",
            "role": "ML Classification & Tuning",
            "status": "PRESENTER", "status_col": CYAN,
            "tasks": [
                "Logistic Regression L-BFGS optimization",
                "Multinomial Naive Bayes (Laplace α=1.0)",
                "Linear SVM soft-margin classification",
                "3-fold Platt probability calibration"
            ]
        },
        {
            "name": "Saloni Ganvir", "roll": "A010175625017",
            "role": "Explainable AI & NLI",
            "status": "PRESENTER", "status_col": CYAN,
            "tasks": [
                "LIME local surrogate perturbations (N=500)",
                "SHAP closed-form linear Shapley values",
                "DeBERTa-v3 cross-encoder NLI pipeline",
                "Apple Silicon MPS Metal acceleration"
            ]
        },
        {
            "name": "Sri Rinith", "roll": "A010175625018",
            "role": "Evaluation & RL Bandit",
            "status": "PRESENTER", "status_col": CYAN,
            "tasks": [
                "UCB1 multi-armed bandit evidence loop",
                "Empirical benchmarking (N=6,685 test set)",
                "XAI faithfulness & token masking tests",
                "Automated pytest suite (60/60 passing)"
            ]
        },
        {
            "name": "Sarvesh", "roll": "A010175625016",
            "role": "Editorial UI & OCR Engine",
            "status": "TEAM MEMBER", "status_col": MUTED,
            "tasks": [
                "Streamlit 6-view responsive interface",
                "Tesseract 5.5 OCR screenshot ingestion",
                "SQLite audit persistence (WAL mode)",
                "90-day automated record retention"
            ]
        }
    ]

    card_width = Inches(2.2)
    card_height = Inches(5.3)
    start_left = Inches(0.8)
    gap = Inches(0.18)

    for idx, m in enumerate(members):
        left = start_left + idx * (card_width + gap)
        top = Inches(1.75)
        border_col = BORDER_CYAN if m["status"] == "PRESENTER" else BORDER_SUBTLE
        add_card(slide, left, top, card_width, card_height, bg_rgb=CARD_BG, border_rgb=border_col, border_width=1.2)

        tx = slide.shapes.add_textbox(left + Inches(0.12), top + Inches(0.15), card_width - Inches(0.24), card_height - Inches(0.3))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_stat = tf.paragraphs[0]
        p_stat.text = m["status"]
        p_stat.font.name = FONT_NAME
        p_stat.font.size = Pt(8.0)
        p_stat.font.bold = True
        p_stat.font.color.rgb = m["status_col"]

        p_name = tf.add_paragraph()
        p_name.text = m["name"]
        p_name.font.name = FONT_NAME
        p_name.font.size = Pt(12)
        p_name.font.bold = True
        p_name.font.color.rgb = WHITE

        p_roll = tf.add_paragraph()
        p_roll.text = m["roll"]
        p_roll.font.name = FONT_NAME
        p_roll.font.size = Pt(8.5)
        p_roll.font.color.rgb = SKY

        p_role = tf.add_paragraph()
        p_role.text = m["role"]
        p_role.font.name = FONT_NAME
        p_role.font.size = Pt(9.0)
        p_role.font.bold = True
        p_role.font.color.rgb = VIOLET

        tf.add_paragraph().text = "" # spacer

        p_hdr = tf.add_paragraph()
        p_hdr.text = "CORE RESPONSIBILITIES:"
        p_hdr.font.name = FONT_NAME
        p_hdr.font.size = Pt(7.5)
        p_hdr.font.bold = True
        p_hdr.font.color.rgb = MUTED

        for t in m["tasks"]:
            p_t = tf.add_paragraph()
            p_t.text = f"• {t}"
            p_t.font.name = FONT_NAME
            p_t.font.size = Pt(8.0)
            p_t.font.color.rgb = ICE

def build_slide_03_intro(prs):
    slide = add_base_slide(prs)
    add_header(slide, "02 • INTRODUCTION OF THE PROJECT", "The Disinformation Crisis & The AI Black-Box Dilemma",
               "Why Statistical Classifiers Require Explainability and Evidence Grounding")

    # 3 Column Cards
    col_w = Inches(3.7)
    col_h = Inches(4.0)
    top = Inches(1.8)

    cards = [
        {
            "tag": "CHALLENGE 01", "tag_col": CYAN,
            "title": "Information Velocity & Scale",
            "points": [
                "Disinformation propagates 6x faster than verified reporting across modern social media graphs.",
                "Manual editorial fact-checking requires hours per story, creating severe response latency.",
                "Automated computational triaging is urgent to flag deceptive narratives at web scale."
            ]
        },
        {
            "tag": "CHALLENGE 02", "tag_col": GOLD,
            "title": "The AI Black-Box Hazard",
            "points": [
                "Standard deep models output opaque numbers (e.g., '92% Fake') without actionable human rationale.",
                "Journalists, legal scholars, and citizens cannot trust decisions without verifiable justification.",
                "Opaque predictions produce either false confidence or complete algorithmic skepticism."
            ]
        },
        {
            "tag": "CHALLENGE 03", "tag_col": VIOLET,
            "title": "Stylometry vs. Factual Truth",
            "points": [
                "Writing style is NOT identical to ground truth: polished lies use neutral, academic syntax.",
                "Conversely, authentic citizen reporting during crises often uses urgent, emotional language.",
                "Statistical text classification must be grounded in external natural language evidence."
            ]
        }
    ]

    for idx, c in enumerate(cards):
        left = Inches(0.8) + idx * (col_w + Inches(0.3))
        add_card(slide, left, top, col_w, col_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = c["tag"]
        p_tag.font.name = FONT_NAME
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = c["tag_col"]

        p_t = tf.add_paragraph()
        p_t.text = c["title"]
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        tf.add_paragraph().text = ""

        for pt in c["points"]:
            p = tf.add_paragraph()
            p.text = f"•  {pt}"
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.color.rgb = ICE

    # Bottom Philosophy Banner
    bot_card = add_card(slide, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.95), bg_rgb=CARD_BG_ALT, border_rgb=BORDER_CYAN, border_width=1.2)
    tx_b = slide.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.333), Inches(0.8))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

    p_b1 = tf_b.paragraphs[0]
    p_b1.text = "THE VERISCOPE AI VERIFICATION TRIAD"
    p_b1.font.name = FONT_NAME
    p_b1.font.size = Pt(9.0)
    p_b1.font.bold = True
    p_b1.font.color.rgb = CYAN

    p_b2 = tf_b.add_paragraph()
    p_b2.text = "1. Calibrated Machine Learning (Stylometry)  →  2. Dual XAI Interpretability (LIME & SHAP)  →  3. Neural NLI Grounding (DeBERTa-v3)"
    p_b2.font.name = FONT_NAME
    p_b2.font.size = Pt(11)
    p_b2.font.bold = True
    p_b2.font.color.rgb = WHITE

def build_slide_04_abstract(prs):
    slide = add_base_slide(prs)
    add_header(slide, "03 • ABSTRACT", "Executive Academic Abstract & System Synthesis",
               "An Explainable, Multimodal Verification Architecture Grounded in Empirical Evidence")

    # Left Narrative Card
    left_w = Inches(7.2)
    left_h = Inches(5.2)
    add_card(slide, Inches(0.8), Inches(1.8), left_w, left_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

    tx_l = slide.shapes.add_textbox(Inches(1.05), Inches(2.0), left_w - Inches(0.5), left_h - Inches(0.4))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_ah = tf_l.paragraphs[0]
    p_ah.text = "RESEARCH ABSTRACT"
    p_ah.font.name = FONT_NAME
    p_ah.font.size = Pt(9.0)
    p_ah.font.bold = True
    p_ah.font.color.rgb = CYAN

    paragraphs = [
        "VeriScope AI addresses the proliferation of synthetic and deceptive news by providing an end-to-end, transparent, and evidence-grounded verification framework. While standard NLP classifiers rely on uncalibrated black-box predictions, VeriScope AI unifies statistical machine learning with local and additive explainability and cross-encoder neural language inference.",
        "To resolve systemic publisher dateline leakage in prior benchmarks, we integrated the 44,267-article ISOT dataset, purged wire tags (e.g., 'Reuters'), and developed a group-aware stratified splitting engine that guarantees 0.0% cross-partition leakage across 38,583 unique body clusters.",
        "On the held-out test set (N = 6,685), our calibrated Linear SVM achieved 98.31% Accuracy and 0.9831 Macro F1 (Logistic Regression: 98.37% Accuracy / 0.9837 Macro F1). Predictions are decomposed via LIME and SHAP with 100% directional sign concordance, while a DeBERTa-v3 cross-encoder validates claims against external evidence.",
        "Designed as an assistive editorial co-pilot, VeriScope AI operates with strict epistemic modesty: statistical style indicates deceptive language cues, but true verification requires external evidence corroboration."
    ]
    for p in paragraphs:
        p_elem = tf_l.add_paragraph()
        p_elem.text = p
        p_elem.font.name = FONT_NAME
        p_elem.font.size = Pt(9.0)
        p_elem.font.color.rgb = ICE

    # Right 4 Feature Cards
    r_left = Inches(8.3)
    r_w = Inches(4.233)
    r_h = Inches(1.2)
    features = [
        ("MULTIMODAL INPUT", "Tesseract 5.5 OCR + Text", "Processes raw text, headlines, and screenshot clippings.", CYAN),
        ("ZERO DATA LEAKAGE", "ISOT Group Partitioning", "Eliminates duplicate body leakage across 38,583 clusters.", TEAL),
        ("DUAL EXPLAINABILITY", "LIME + Exact Linear SHAP", "Transparent token-level attributions with 100% sign agreement.", VIOLET),
        ("EVIDENCE GROUNDING", "DeBERTa-v3 NLI + UCB1", "Zero-shot cross-encoder verification with adaptive bandit search.", SKY)
    ]
    for idx, (tag, title, desc, col) in enumerate(features):
        top = Inches(1.8) + idx * (r_h + Inches(0.13))
        add_card(slide, r_left, top, r_w, r_h, bg_rgb=CARD_BG_ALT, border_rgb=col, border_width=1.0)
        tx_f = slide.shapes.add_textbox(r_left + Inches(0.15), top + Inches(0.12), r_w - Inches(0.3), r_h - Inches(0.24))
        tf_f = tx_f.text_frame
        tf_f.word_wrap = True
        tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0

        p1 = tf_f.paragraphs[0]
        p1.text = tag
        p1.font.name = FONT_NAME
        p1.font.size = Pt(8.0)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf_f.add_paragraph()
        p2.text = title
        p2.font.name = FONT_NAME
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = WHITE

        p3 = tf_f.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_NAME
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = SLATE

def build_slide_05_problem_statement(prs):
    slide = add_base_slide(prs)
    add_header(slide, "04 • PROJECT INTRODUCTION (POINTS)", "Problem Statement: Epistemological & Technical Vulnerabilities",
               "Key Deficiencies in Traditional Fake News Classifiers Addressed by VeriScope AI")

    problems = [
        {
            "num": "01", "col": CYAN,
            "title": "Publisher Dateline Leakage in Datasets",
            "desc": "Traditional benchmark datasets contain wire-service dateline headers such as 'WASHINGTON (Reuters) -'. Machine learning classifiers trained on uncurated corpora learn to associate Reuters tags with genuine news and their absence with fake news, achieving 99% accuracy through publisher memorization rather than learning genuine deception stylometry."
        },
        {
            "num": "02", "col": GOLD,
            "title": "Black-Box Opacity & Overconfident Margins",
            "desc": "Standard neural and ensemble models output uncalibrated, monolithic confidence scores without explaining which phrases drove the verdict. Decision-makers cannot tell whether a classification was triggered by a genuine factual falsehood, sensational adjectives, or irrelevant stopword noise."
        },
        {
            "num": "03", "col": VIOLET,
            "title": "The Epistemic Disconnect: Style vs. Ground Truth",
            "desc": "Stylometric NLP analyzes linguistic distributions (hyperbolic phrasing, punctuation, sentiment). It cannot verify whether a real-world event took place. A sophisticated disinformation agent can write a fabricated narrative in flawless journalistic prose, completely bypassing stylometric filters."
        }
    ]

    card_w = Inches(11.733)
    card_h = Inches(1.55)
    start_top = Inches(1.8)

    for idx, p in enumerate(problems):
        top = start_top + idx * (card_h + Inches(0.2))
        add_card(slide, Inches(0.8), top, card_w, card_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

        # Number Callout on Left
        num_box = slide.shapes.add_textbox(Inches(1.0), top + Inches(0.2), Inches(0.8), Inches(1.0))
        tf_n = num_box.text_frame
        tf_n.word_wrap = True
        tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
        p_num = tf_n.paragraphs[0]
        p_num.text = p["num"]
        p_num.font.name = FONT_NAME
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = p["col"]

        # Content on Right
        c_box = slide.shapes.add_textbox(Inches(1.9), top + Inches(0.18), card_w - Inches(1.3), card_h - Inches(0.35))
        tf_c = c_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

        p_t = tf_c.paragraphs[0]
        p_t.text = p["title"]
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_c.add_paragraph()
        p_d.text = p["desc"]
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = ICE

def build_slide_06_objectives(prs):
    slide = add_base_slide(prs)
    add_header(slide, "04 • PROJECT INTRODUCTION (POINTS)", "Project Objectives & Engineering Milestones",
               "Key Concrete Technical Goals Achieved in the VeriScope AI Implementation")

    objectives = [
        ("1. Multimodal Text & Vision Ingestion", "Enable seamless editorial input via direct text entry, URL pasting, and Tesseract 5.5 OCR screenshot analysis with adaptive contrast correction.", CYAN),
        ("2. Leakage-Free Dataset Hygiene", "Integrate the 44,267-article ISOT corpus, purge wire-service dateline headers, and engineer group-aware splitting ensuring 0% cross-split duplication.", TEAL),
        ("3. Calibrated Multi-Model Classification", "Train and benchmark Logistic Regression, Multinomial Naive Bayes, and Linear SVM with 3-fold Platt scaling for true bounded posterior probabilities.", SKY),
        ("4. Dual Explainable AI (XAI) Engine", "Implement simultaneous LIME (local surrogate perturbations) and SHAP (exact closed-form linear Shapley values) to visualize token-level influence.", VIOLET),
        ("5. Cross-Encoder NLI Evidence Grounding", "Integrate a 435M-parameter DeBERTa-v3 cross-encoder to verify claims against external evidence with Entailment, Contradiction, and Neutral scoring.", CYAN),
        ("6. Enterprise Auditability & Persistence", "Develop an embedded SQLite audit trail with WAL concurrency, tamper-evident history, and automated 90-day retention pruning.", GREEN)
    ]

    card_w = Inches(5.7)
    card_h = Inches(1.55)

    for idx, (title, desc, col) in enumerate(objectives):
        row = idx // 2
        c_idx = idx % 2
        left = Inches(0.8) + c_idx * (card_w + Inches(0.333))
        top = Inches(1.8) + row * (card_h + Inches(0.2))

        add_card(slide, left, top, card_w, card_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.35))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = ICE

def build_slide_07_workflow(prs):
    slide = add_base_slide(prs)
    add_header(slide, "04 • PROJECT INTRODUCTION (POINTS)", "End-to-End Workflow & Target User Personas",
               "Operational Pipeline Execution & Key Stakeholder Beneficiaries")

    # Workflow Steps
    steps = [
        ("01", "INGESTION", "Text Entry or OCR Screenshot"),
        ("02", "PREPROCESS", "Wire-Tag Regex & Tokenizer"),
        ("03", "FEATURES", "Sublinear TF-IDF (5,000 Dim)"),
        ("04", "CLASSIFY", "Platt-Calibrated Linear SVM"),
        ("05", "EXPLAIN", "Dual LIME & SHAP Weights"),
        ("06", "GROUNDING", "DeBERTa-v3 NLI + SQLite Log")
    ]
    step_w = Inches(1.8)
    step_h = Inches(1.8)
    start_l = Inches(0.8)
    gap = Inches(0.18)

    for idx, (num, title, desc) in enumerate(steps):
        left = start_l + idx * (step_w + gap)
        top = Inches(1.8)
        border_col = BORDER_CYAN if idx in [0, 3, 4] else BORDER_SUBTLE
        add_card(slide, left, top, step_w, step_h, bg_rgb=CARD_BG_ALT, border_rgb=border_col)

        tx = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.15), step_w - Inches(0.2), step_h - Inches(0.3))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.name = FONT_NAME
        p_num.font.size = Pt(14)
        p_num.font.bold = True
        p_num.font.color.rgb = CYAN

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.0)
        p_d.font.color.rgb = SLATE

    # Target User Personas
    personas = [
        ("FACT-CHECKERS & NEWSROOMS", "Rapid editorial triage of viral social claims with token-level justification and external evidence references.", CYAN),
        ("ACADEMIC AI RESEARCHERS", "Empirical benchmarking of XAI explanation fidelity (Top-k Jaccard, sign concordance, token masking tests).", TEAL),
        ("MEDIA LITERACY EDUCATORS", "Teaching students and citizens how algorithmic models assess text and where statistical AI fails.", VIOLET),
        ("GENERAL NEWS CONSUMERS", "A transparent second-opinion companion that demystifies headlines without claiming absolute truth.", SKY)
    ]

    p_w = Inches(2.8)
    p_h = Inches(2.8)
    p_top = Inches(3.9)
    p_gap = Inches(0.17)

    for idx, (title, desc, col) in enumerate(personas):
        left = Inches(0.8) + idx * (p_w + p_gap)
        add_card(slide, left, p_top, p_w, p_h, bg_rgb=CARD_BG, border_rgb=col, border_width=1.0)

        tx = slide.shapes.add_textbox(left + Inches(0.15), p_top + Inches(0.2), p_w - Inches(0.3), p_h - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        tf.add_paragraph().text = ""

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(9.0)
        p_d.font.color.rgb = ICE

def build_slide_08_requirements(prs):
    slide = add_base_slide(prs)
    add_header(slide, "05 • SOFTWARE & HARDWARE REQUIREMENTS", "Technical Environment & Specification Stack",
               "Production-Ready Architecture Built Exclusively on Free, Open-Source Tools")

    # Left: Software Stack
    sw_headers = ["Software Component", "Version", "Role in Architecture"]
    sw_data = [
        ["Python Runtime", "3.12.15", "Core execution environment & typing"],
        ["scikit-learn", "1.6.1+", "Classification, TF-IDF & Platt scaling"],
        ["LIME", "0.2.0.1", "Local linear surrogate perturbations"],
        ["SHAP", "0.46.0+", "Closed-form linear Shapley attributions"],
        ["PyTorch / Transformers", "2.5.1+ / 4.48+", "DeBERTa-v3 cross-encoder NLI model"],
        ["Tesseract OCR", "5.5.0+", "Multimodal news screenshot text extraction"],
        ["Streamlit", "1.40.0+", "Reactive 6-view web user interface"],
        ["SQLite 3", "3.45+", "Audit persistence & 90-day retention log"],
        ["Pytest Test Harness", "9.1.1+", "Automated testing (60 unit/integration tests)"]
    ]
    add_table(slide, Inches(0.8), Inches(1.8), Inches(6.5), Inches(5.1), sw_headers, sw_data, col_widths=[1.8, 1.1, 3.6])

    # Right: Hardware Specs Card
    r_left = Inches(7.6)
    r_w = Inches(4.933)
    r_h = Inches(5.1)
    add_card(slide, r_left, Inches(1.8), r_w, r_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

    tx_r = slide.shapes.add_textbox(r_left + Inches(0.25), Inches(2.0), r_w - Inches(0.5), r_h - Inches(0.4))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "HARDWARE SPECIFICATIONS"
    p_rh.font.name = FONT_NAME
    p_rh.font.size = Pt(10.5)
    p_rh.font.bold = True
    p_rh.font.color.rgb = CYAN

    hw_items = [
        ("Verified Development Machine:", [
            "Apple Silicon M-Series SoC (ARM64 unified architecture)",
            "16 GB Unified Memory (LPDDR5)",
            "macOS Sonoma / Darwin 24.3.0 Unix subsystem",
            "Apple Metal Performance Shaders (MPS) for PyTorch"
        ]),
        ("Target Demo & Viva Minimum Specs:", [
            "Standard x86_64 or ARM64 64-bit CPU (Quad-core+)",
            "8 GB – 16 GB RAM (Zero dedicated GPU requirement)",
            "2.5 GB Free Disk Space (Includes model cache)",
            "Standard 1080p display for web workspace presentation"
        ]),
        ("Economic Self-Sufficiency:", [
            "Zero cloud API fees (No OpenAI or cloud subscription costs)",
            "Permissive open-source licenses (MIT, Apache 2.0, BSD-3)"
        ])
    ]

    for section_title, bullets in hw_items:
        p_sec = tf_r.add_paragraph()
        p_sec.text = f"\n{section_title}"
        p_sec.font.name = FONT_NAME
        p_sec.font.size = Pt(9.5)
        p_sec.font.bold = True
        p_sec.font.color.rgb = WHITE

        for b in bullets:
            p_b = tf_r.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.name = FONT_NAME
            p_b.font.size = Pt(8.5)
            p_b.font.color.rgb = ICE

def build_slide_09_architecture(prs):
    slide = add_base_slide(prs)
    add_header(slide, "06 • IMPLEMENTATION — SYSTEM ARCHITECTURE", "Multi-Tiered Modular System Architecture",
               "Decoupled Architectural Pipeline from Ingestion to Explainability & Evidence Verification")

    tiers = [
        ("TIER 1: MULTIMODAL INGESTION LAYER", "Streamlit 6-view web UI • Direct editorial text entry • Tesseract 5.5 OCR screenshot parser with Otsu binarization and deskewing.", CYAN),
        ("TIER 2: SANITIZATION & FEATURE EXTRACTION", "Regex wire-tag eradication (strips '(Reuters)', '(AP)') • Canonical MD5 body clustering • Sublinear TF-IDF vectorization (5,000 features).", TEAL),
        ("TIER 3: STATISTICAL ML & CALIBRATION", "Logistic Regression (log-odds) • Multinomial Naive Bayes (Laplace smoothing) • Platt-calibrated Linear SVM (3-fold cross-validated sigmoid scaling).", SKY),
        ("TIER 4: DUAL EXPLAINABLE AI & NEURAL NLI", "LIME local surrogate perturbations • SHAP exact closed-form linear Shapley values • DeBERTa-v3 cross-encoder NLI verification.", VIOLET),
        ("TIER 5: ACTIVE LEARNING & AUDIT STORE", "Contextual UCB1 multi-armed bandit (adaptive evidence search) • SQLite embedded database with WAL concurrency and 90-day retention pruning.", GREEN)
    ]

    card_w = Inches(11.733)
    card_h = Inches(0.95)
    start_top = Inches(1.8)

    for idx, (title, desc, col) in enumerate(tiers):
        top = start_top + idx * (card_h + Inches(0.12))
        add_card(slide, Inches(0.8), top, card_w, card_h, bg_rgb=CARD_BG, border_rgb=col, border_width=1.0)

        tx = slide.shapes.add_textbox(Inches(1.0), top + Inches(0.1), card_w - Inches(0.4), card_h - Inches(0.2))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = ICE

def build_slide_10_dataset(prs):
    slide = add_base_slide(prs)
    add_header(slide, "06 • IMPLEMENTATION — DATASET CURATION", "Dataset Hygiene & Zero-Leakage Group Partitioning",
               "Sourcing the Public ISOT Corpus and Eradicating Duplicate-Body Cross-Split Leakage")

    # Left: ISOT Dataset Split Summary Table
    tbl_headers = ["Partition", "Records", "Unique Groups", "Likely Fake", "Likely Real", "Ratio"]
    tbl_data = [
        ["Training Set", "30,869", "27,008", "15,860", "15,009", "69.75%"],
        ["Validation Set", "6,629", "5,787", "3,426", "3,203", "14.98%"],
        ["Held-Out Test Set", "6,685", "5,788", "3,481", "3,204", "15.10%"],
        ["Co-Assigned Duplicates", "5,600", "0 (Quarantined)", "2,842", "2,758", "Zero Leakage"],
        ["Total Evaluated Corpus", "44,258", "38,583", "22,767", "21,416", "100.00%"]
    ]
    add_table(slide, Inches(0.8), Inches(1.8), Inches(6.8), Inches(3.2), tbl_headers, tbl_data, col_widths=[1.5, 1.0, 1.3, 1.0, 1.0, 1.0])

    # Right: Anti-Leakage Methodology Card
    r_left = Inches(7.9)
    r_w = Inches(4.633)
    r_h = Inches(5.1)
    add_card(slide, r_left, Inches(1.8), r_w, r_h, bg_rgb=CARD_BG, border_rgb=BORDER_CYAN, border_width=1.2)

    tx_r = slide.shapes.add_textbox(r_left + Inches(0.2), Inches(2.0), r_w - Inches(0.4), r_h - Inches(0.4))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "ANTI-LEAKAGE ENGINEERING"
    p_rh.font.name = FONT_NAME
    p_rh.font.size = Pt(11)
    p_rh.font.bold = True
    p_rh.font.color.rgb = CYAN

    points = [
        ("The Duplicate Leakage Flaw:", "In standard news datasets, identical stories are republished across multiple outlets. Random splitting assigns copies of the same text to both train and test, inflating accuracy artificially."),
        ("Canonical MD5 Grouping:", "We compute MD5(normalize_whitespace(lower(body))). All duplicate copies of an article are co-assigned to the EXACT same partition via group_aware_stratified_split."),
        ("Zero Cross-Split Contamination:", "Cryptographic audit confirms: Intersection(Train_Hashes, Test_Hashes) == 0 (0.0% leakage across 38,583 clusters)."),
        ("Synthetic Benchmark Quarantined:", "The legacy synthetic benchmark (400 rows, 16 unique bodies) is strictly reserved as an offline regression suite.")
    ]
    for title, desc in points:
        p_t = tf_r.add_paragraph()
        p_t.text = f"\n{title}"
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_r.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = ICE

    # Bottom Callout Box under table
    add_metric_badge(slide, Inches(0.8), Inches(5.2), Inches(6.8), Inches(1.7), "0.0% LEAKAGE",
                     "Mathematically Audited Across 38,583 Unique Body Clusters",
                     "Wire-Service Header Removal Regex Eradicates Publisher Tag Memorization Shortcuts", accent_color=GREEN)

def build_slide_11_classification(prs):
    slide = add_base_slide(prs)
    add_header(slide, "06 • IMPLEMENTATION — CLASSIFIER BENCHMARKING", "Statistical Machine Learning & Platt Probability Calibration",
               "Evaluating Diverse Classifiers & Transforming Raw Margins into Calibrated Posteriors")

    models = [
        {
            "name": "Logistic Regression",
            "tag": "BASELINE BENCHMARK", "col": SKY,
            "math": "P(y = 1 | x) = σ(wᵀx + b)",
            "details": [
                "L2-regularized binary cross-entropy minimization.",
                "L-BFGS optimization algorithm (C = 1.0).",
                "Direct continuous log-odds interpretability.",
                "Fast, highly stable convex convergence."
            ]
        },
        {
            "name": "Multinomial Naive Bayes",
            "tag": "PROBABILISTIC CLASSIFIER", "col": TEAL,
            "math": "θ_yi = (N_yi + α) / (N_y + α·n)",
            "details": [
                "Bayes' theorem under conditional independence.",
                "Laplace smoothing (α = 1.0) prevents zero-probability tokens.",
                "Lightweight inference (<5 ms per document).",
                "Strong generative baseline for text classification."
            ]
        },
        {
            "name": "Linear SVM (Calibrated) ★",
            "tag": "PRIMARY PRODUCTION MODEL", "col": CYAN,
            "math": "P(y = 1 | f) = 1 / (1 + exp(A·f + B))",
            "details": [
                "Soft-margin hyperplane maximizing geometric separation.",
                "3-fold cross-validated Platt scaling (sigmoid calibration).",
                "Transforms uncalibrated margins into true posterior probabilities.",
                "Selected based on highest validation Macro F1 (0.9855)."
            ]
        }
    ]

    c_w = Inches(3.7)
    c_h = Inches(5.2)

    for idx, m in enumerate(models):
        left = Inches(0.8) + idx * (c_w + Inches(0.3))
        top = Inches(1.8)
        border_col = CYAN if "★" in m["name"] else BORDER_SUBTLE
        add_card(slide, left, top, c_w, c_h, bg_rgb=CARD_BG, border_rgb=border_col, border_width=1.2 if "★" in m["name"] else 1.0)

        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = m["tag"]
        p_tag.font.name = FONT_NAME
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = m["col"]

        p_name = tf.add_paragraph()
        p_name.text = m["name"]
        p_name.font.name = FONT_NAME
        p_name.font.size = Pt(13)
        p_name.font.bold = True
        p_name.font.color.rgb = WHITE

        p_math = tf.add_paragraph()
        p_math.text = f"\n{m['math']}\n"
        p_math.font.name = "Courier New"
        p_math.font.size = Pt(9.5)
        p_math.font.bold = True
        p_math.font.color.rgb = SKY

        for d in m["details"]:
            p = tf.add_paragraph()
            p.text = f"• {d}"
            p.font.name = FONT_NAME
            p.font.size = Pt(8.5)
            p.font.color.rgb = ICE

def build_slide_12_xai(prs):
    slide = add_base_slide(prs)
    add_header(slide, "06 • IMPLEMENTATION — EXPLAINABLE AI (XAI)", "Dual Explainability Engine: LIME & SHAP",
               "Local Surrogate Perturbations vs. Cooperative Game-Theoretic Shapley Attributions")

    # Left: LIME Card
    w = Inches(5.7)
    h = Inches(4.0)
    top = Inches(1.8)

    add_card(slide, Inches(0.8), top, w, h, bg_rgb=CARD_BG, border_rgb=BORDER_CYAN)
    tx_lime = slide.shapes.add_textbox(Inches(1.0), top + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
    tf_l = tx_lime.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_lh = tf_l.paragraphs[0]
    p_lh.text = "LIME (LOCAL INTERPRETABLE MODEL-AGNOSTIC EXPLANATIONS)"
    p_lh.font.name = FONT_NAME
    p_lh.font.size = Pt(9.5)
    p_lh.font.bold = True
    p_lh.font.color.rgb = CYAN

    lime_points = [
        "Formulation: Trains a local sparse linear surrogate model g on perturbed instances z' around original input x.",
        "Perturbation Sampling: Uniformly samples N = 500 word-presence vectors z' in {0, 1}^d.",
        "Distance Weighting: Weights perturbed samples via exponential cosine distance kernel: π_x(z) = exp(-D(x, z)² / σ²).",
        "Outcome: Extracts top deceptive tokens (pushing toward Likely Fake) and credibility tokens (pushing toward Likely Real)."
    ]
    for pt in lime_points:
        p = tf_l.add_paragraph()
        p.text = f"•  {pt}"
        p.font.name = FONT_NAME
        p.font.size = Pt(9.0)
        p.font.color.rgb = ICE

    # Right: SHAP Card
    add_card(slide, Inches(6.833), top, w, h, bg_rgb=CARD_BG, border_rgb=BORDER_VIOLET)
    tx_shap = slide.shapes.add_textbox(Inches(7.033), top + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
    tf_s = tx_shap.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0

    p_sh = tf_s.paragraphs[0]
    p_sh.text = "SHAP (SHAPLEY ADDITIVE EXPLANATIONS)"
    p_sh.font.name = FONT_NAME
    p_sh.font.size = Pt(9.5)
    p_sh.font.bold = True
    p_sh.font.color.rgb = VIOLET

    shap_points = [
        "Formulation: Grounded in cooperative game theory, calculating the exact marginal contribution of each token.",
        "Axiomatic Rigor: Satisfies Efficiency, Symmetry, Dummy (Null Effect), and Additivity.",
        "Linear Optimization: For calibrated Linear SVM, reduces to closed-form: φ_i = w_i · (x_i - E[x_i]), computing in <100 ms.",
        "Outcome: Decomposes prediction into base value + additive token log-odds shifts."
    ]
    for pt in shap_points:
        p = tf_s.add_paragraph()
        p.text = f"•  {pt}"
        p.font.name = FONT_NAME
        p.font.size = Pt(9.0)
        p.font.color.rgb = ICE

    # Bottom Essential Disclaimer Banner
    add_card(slide, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.95), bg_rgb=CARD_BG_ALT, border_rgb=GOLD, border_width=1.2)
    tx_disc = slide.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.333), Inches(0.8))
    tf_d = tx_disc.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0

    p_dh = tf_d.paragraphs[0]
    p_dh.text = "CRITICAL EPISTEMIC PRINCIPLE: XAI EXPLAINS PREDICTIONS, NOT REALITY"
    p_dh.font.name = FONT_NAME
    p_dh.font.size = Pt(9.0)
    p_dh.font.bold = True
    p_dh.font.color.rgb = GOLD

    p_db = tf_d.add_paragraph()
    p_db.text = "LIME and SHAP explain which lexical features triggered the model's classification. They do NOT independently verify whether an event occurred in the real world. External factual truth requires empirical evidence verification."
    p_db.font.name = FONT_NAME
    p_db.font.size = Pt(9.0)
    p_db.font.color.rgb = WHITE

def build_slide_13_nli_bandit(prs):
    slide = add_base_slide(prs)
    add_header(slide, "06 • IMPLEMENTATION — EVIDENCE & NLI", "Cross-Encoder NLI Verification & Contextual UCB1 Bandit",
               "Grounding Claims in Real-World Evidence via Pretrained DeBERTa-v3 & Adaptive Search")

    # Left: DeBERTa-v3 Cross-Encoder
    w = Inches(5.7)
    h = Inches(5.1)
    top = Inches(1.8)

    add_card(slide, Inches(0.8), top, w, h, bg_rgb=CARD_BG, border_rgb=BORDER_CYAN)
    tx_nli = slide.shapes.add_textbox(Inches(1.0), top + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
    tf_n = tx_nli.text_frame
    tf_n.word_wrap = True
    tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0

    p_nh = tf_n.paragraphs[0]
    p_nh.text = "NEURAL NATURAL LANGUAGE INFERENCE (NLI)"
    p_nh.font.name = FONT_NAME
    p_nh.font.size = Pt(10.5)
    p_nh.font.bold = True
    p_nh.font.color.rgb = CYAN

    nli_points = [
        ("Pretrained Model Architecture:", "cross-encoder/nli-deberta-v3-base (435M parameters)."),
        ("Disentangled Attention:", "Decouples content representations from relative token positions, achieving superior cross-sequence reasoning over standard BERT."),
        ("Premise-Hypothesis Encoding:", "Full bidirectional cross-attention over [CLS] Premise [SEP] Hypothesis [SEP], scoring claim veracity against retrieved news evidence."),
        ("Tri-Class Softmax Distribution:", "Entailment (Claim corroborated) | Contradiction (Claim refuted) | Neutral (Insufficient evidence)."),
        ("Hardware Acceleration:", "Native PyTorch Metal Performance Shaders (MPS) on Apple Silicon achieves 45–65 ms inference latency.")
    ]
    for title, desc in nli_points:
        p_t = tf_n.add_paragraph()
        p_t.text = f"\n{title}"
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(9.0)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_n.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = ICE

    # Right: UCB1 Bandit Evidence Retrieval
    add_card(slide, Inches(6.833), top, w, h, bg_rgb=CARD_BG, border_rgb=BORDER_VIOLET)
    tx_b = slide.shapes.add_textbox(Inches(7.033), top + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

    p_bh = tf_b.paragraphs[0]
    p_bh.text = "CONTEXTUAL UCB1 MULTI-ARMED BANDIT"
    p_bh.font.name = FONT_NAME
    p_bh.font.size = Pt(10.5)
    p_bh.font.bold = True
    p_bh.font.color.rgb = VIOLET

    bandit_points = [
        ("Exploration vs. Exploitation:", "Different claims demand different search strategies (named actors vs. semantic concepts vs. exact quotes)."),
        ("Arm 0 — Entity-Centric Querying:", "spaCy NER extraction focused on specific political and institutional actors."),
        ("Arm 1 — Semantic Hybrid Search:", "Combines BM25 lexical keyword matching with dense embedding cosine similarity."),
        ("Arm 2 — Keyphrase N-gram Salience:", "Targets highest-scoring TF-IDF n-grams (length 2–4)."),
        ("Upper Confidence Bound Action Rule:", "Score_i(t) = Q̄_i + c · √(2·ln(t) / N_i(t)) with c = 0.5."),
        ("Reinforcement Reward Function:", "R_t = 0.5·max(P_ent, P_con) + 0.3·Authority + 0.2·Diversity.")
    ]
    for title, desc in bandit_points:
        p_t = tf_b.add_paragraph()
        p_t.text = f"\n{title}"
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(9.0)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_b.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = ICE

def build_slide_14_screenshots_dashboard(prs):
    slide = add_base_slide(prs)
    add_header(slide, "07 • ACTUAL OUTPUT SCREENSHOTS", "Executive System Dashboard & Telemetry",
               "Real-Time Verification KPIs, Throughput Monitoring & Subsystem Readiness")

    # Left: Styled Container for Actual Screenshot
    frame_w = Inches(7.5)
    frame_h = Inches(5.1)
    frame_left = Inches(0.8)
    frame_top = Inches(1.8)
    add_card(slide, frame_left, frame_top, frame_w, frame_h, bg_rgb=RGBColor(8, 14, 25), border_rgb=BORDER_CYAN, border_width=1.5)

    tx_ph = slide.shapes.add_textbox(frame_left + Inches(0.5), frame_top + Inches(1.8), frame_w - Inches(1.0), Inches(1.5))
    tf_ph = tx_ph.text_frame
    tf_ph.word_wrap = True
    p1 = tf_ph.paragraphs[0]
    p1.text = "ACTUAL APPLICATION SCREENSHOT"
    p1.font.name = FONT_NAME
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = CYAN
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf_ph.add_paragraph()
    p2.text = "Executive Monitoring & Real-Time KPI Dashboard"
    p2.font.name = FONT_NAME
    p2.font.size = Pt(10)
    p2.font.color.rgb = WHITE
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_ph.add_paragraph()
    p3.text = "[Drop Dashboard Screenshot Here / Streamlit View 1]"
    p3.font.name = FONT_NAME
    p3.font.size = Pt(8.5)
    p3.font.italic = True
    p3.font.color.rgb = SLATE
    p3.alignment = PP_ALIGN.CENTER

    # Right: Feature Annotations
    ann_w = Inches(4.0)
    ann_left = Inches(8.533)
    add_card(slide, ann_left, frame_top, ann_w, frame_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

    tx_ann = slide.shapes.add_textbox(ann_left + Inches(0.2), frame_top + Inches(0.2), ann_w - Inches(0.4), frame_h - Inches(0.4))
    tf_a = tx_ann.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0

    p_ah = tf_a.paragraphs[0]
    p_ah.text = "DASHBOARD CAPABILITIES"
    p_ah.font.name = FONT_NAME
    p_ah.font.size = Pt(10.5)
    p_ah.font.bold = True
    p_ah.font.color.rgb = CYAN

    items = [
        ("Real-Time KPI Cards:", "Instant visualization of total dispatches audited, likely fake count, and mean model confidence across editorial sessions."),
        ("Verification Activity Velocity:", "Interactive time-series charts displaying verification request throughput and prediction class distribution."),
        ("Subsystem Health Badges:", "Live status indicators verifying that the Scikit-learn models, Tesseract OCR engine, and SQLite audit DB are operational."),
        ("Active Model Diagnostic:", "Indicates active model architecture (Linear SVM ★ vs. Logistic Regression vs. Naive Bayes).")
    ]
    for title, desc in items:
        p_t = tf_a.add_paragraph()
        p_t.text = f"\n{title}"
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(9.0)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_a.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.0)
        p_d.font.color.rgb = ICE

def build_slide_15_screenshots_analyzer(prs):
    slide = add_base_slide(prs)
    add_header(slide, "07 • ACTUAL OUTPUT SCREENSHOTS", "News Analyzer & Calibrated Prediction Interface",
               "Interactive Text Triage, Real-Time Wire Sanitization Alerts & Calibrated Probabilities")

    frame_w = Inches(7.5)
    frame_h = Inches(5.1)
    frame_left = Inches(0.8)
    frame_top = Inches(1.8)
    add_card(slide, frame_left, frame_top, frame_w, frame_h, bg_rgb=RGBColor(8, 14, 25), border_rgb=BORDER_CYAN, border_width=1.5)

    tx_ph = slide.shapes.add_textbox(frame_left + Inches(0.5), frame_top + Inches(1.8), frame_w - Inches(1.0), Inches(1.5))
    tf_ph = tx_ph.text_frame
    tf_ph.word_wrap = True
    p1 = tf_ph.paragraphs[0]
    p1.text = "ACTUAL APPLICATION SCREENSHOT"
    p1.font.name = FONT_NAME
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = CYAN
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf_ph.add_paragraph()
    p2.text = "News Analyzer Workspace & Prediction Results"
    p2.font.name = FONT_NAME
    p2.font.size = Pt(10)
    p2.font.color.rgb = WHITE
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_ph.add_paragraph()
    p3.text = "[Drop News Analyzer Screenshot Here / Streamlit View 2]"
    p3.font.name = FONT_NAME
    p3.font.size = Pt(8.5)
    p3.font.italic = True
    p3.font.color.rgb = SLATE
    p3.alignment = PP_ALIGN.CENTER

    ann_w = Inches(4.0)
    ann_left = Inches(8.533)
    add_card(slide, ann_left, frame_top, ann_w, frame_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

    tx_ann = slide.shapes.add_textbox(ann_left + Inches(0.2), frame_top + Inches(0.2), ann_w - Inches(0.4), frame_h - Inches(0.4))
    tf_a = tx_ann.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0

    p_ah = tf_a.paragraphs[0]
    p_ah.text = "ANALYZER CAPABILITIES"
    p_ah.font.name = FONT_NAME
    p_ah.font.size = Pt(10.5)
    p_ah.font.bold = True
    p_ah.font.color.rgb = CYAN

    items = [
        ("Dual Ingestion Text Area:", "Separate input fields for Article Headline and Article Body with real-time character counters and pre-loaded sample news buttons."),
        ("Wire-Tag Sanitizer Notification:", "Displays real-time alert when wire service datelines (e.g. 'Reuters', 'AP') are detected and stripped to prevent shortcut bias."),
        ("Calibrated Probability Gauge:", "Outputs clear 'Likely Real' or 'Likely Fake' badge with Platt-calibrated confidence score percentage."),
        ("Epistemic Modesty Warning:", "Prominently displays disclaimer that classification reflects linguistic stylometry rather than verified ontology.")
    ]
    for title, desc in items:
        p_t = tf_a.add_paragraph()
        p_t.text = f"\n{title}"
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(9.0)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_a.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.0)
        p_d.font.color.rgb = ICE

def build_slide_16_screenshots_ocr_xai(prs):
    slide = add_base_slide(prs)
    add_header(slide, "07 • ACTUAL OUTPUT SCREENSHOTS", "Multimodal OCR & Dual Explainability Visualizer",
               "Tesseract Vision Ingestion, LIME vs. SHAP Attributions & NLI Evidence Corroboration")

    frame_w = Inches(7.5)
    frame_h = Inches(5.1)
    frame_left = Inches(0.8)
    frame_top = Inches(1.8)
    add_card(slide, frame_left, frame_top, frame_w, frame_h, bg_rgb=RGBColor(8, 14, 25), border_rgb=BORDER_VIOLET, border_width=1.5)

    tx_ph = slide.shapes.add_textbox(frame_left + Inches(0.5), frame_top + Inches(1.8), frame_w - Inches(1.0), Inches(1.5))
    tf_ph = tx_ph.text_frame
    tf_ph.word_wrap = True
    p1 = tf_ph.paragraphs[0]
    p1.text = "ACTUAL APPLICATION SCREENSHOT"
    p1.font.name = FONT_NAME
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = VIOLET
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf_ph.add_paragraph()
    p2.text = "OCR Ingestion & Dual XAI Feature Attribution Lab"
    p2.font.name = FONT_NAME
    p2.font.size = Pt(10)
    p2.font.color.rgb = WHITE
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_ph.add_paragraph()
    p3.text = "[Drop OCR / Dual XAI Screenshot Here / Streamlit View 3]"
    p3.font.name = FONT_NAME
    p3.font.size = Pt(8.5)
    p3.font.italic = True
    p3.font.color.rgb = SLATE
    p3.alignment = PP_ALIGN.CENTER

    ann_w = Inches(4.0)
    ann_left = Inches(8.533)
    add_card(slide, ann_left, frame_top, ann_w, frame_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

    tx_ann = slide.shapes.add_textbox(ann_left + Inches(0.2), frame_top + Inches(0.2), ann_w - Inches(0.4), frame_h - Inches(0.4))
    tf_a = tx_ann.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0

    p_ah = tf_a.paragraphs[0]
    p_ah.text = "OCR & XAI CAPABILITIES"
    p_ah.font.name = FONT_NAME
    p_ah.font.size = Pt(10.5)
    p_ah.font.bold = True
    p_ah.font.color.rgb = VIOLET

    items = [
        ("Tesseract OCR Processing:", "Drag-and-drop ingestion of PNG, JPG, and WEBP news screenshots with automatic orientation correction and thresholding."),
        ("LIME Token Contributions:", "Interactive horizontal bar chart highlighting words driving the classification toward 'Fake' (red) or 'Real' (green)."),
        ("SHAP Log-Odds Force Plot:", "Displays exact closed-form linear Shapley attributions showing additive shifts relative to the expected base value."),
        ("NLI Evidence Corroboration:", "Shows premise-hypothesis entailment vs. contradiction probabilities against external knowledge corpora.")
    ]
    for title, desc in items:
        p_t = tf_a.add_paragraph()
        p_t.text = f"\n{title}"
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(9.0)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_a.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.0)
        p_d.font.color.rgb = ICE

def build_slide_17_results(prs):
    slide = add_base_slide(prs)
    add_header(slide, "07 • RESULTS & EVALUATION", "Empirical Evaluation & Verified Benchmark Metrics",
               "Rigorous Performance Verification on the External ISOT Held-Out Test Set (N = 6,685)")

    # Top Table: Model Comparison on Test Set
    tbl_headers = ["Model Architecture", "Test Accuracy", "Macro F1", "Macro Precision", "Macro Recall", "Correct", "Errors", "Val F1"]
    tbl_data = [
        ["Linear SVM (Calibrated) ★", "98.31%", "0.9831", "0.9829", "0.9835", "6,572", "113", "0.9855"],
        ["Logistic Regression", "98.37%", "0.9837", "0.9835", "0.9840", "6,576", "109", "0.9834"],
        ["Multinomial Naive Bayes", "94.45%", "0.9444", "0.9443", "0.9445", "6,314", "371", "0.9455"]
    ]
    add_table(slide, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.0), tbl_headers, tbl_data,
              col_widths=[2.8, 1.2, 1.2, 1.3, 1.3, 1.2, 1.2, 1.533])

    # Bottom 4 Metric Badges
    b_w = Inches(2.75)
    b_h = Inches(2.7)
    gap = Inches(0.244)
    b_top = Inches(4.2)

    badges = [
        ("100.0%", "SIGN CONCORDANCE", "Directional agreement between LIME & SHAP on shared salient tokens across all tested instances.", CYAN),
        ("35–50%", "FAITHFULNESS DROP", "Points lost when top-5 XAI tokens are masked (vs <2% for random masking), proving causal attribution.", VIOLET),
        ("50.00%", "SYNTHETIC BASELINE", "Neutral accuracy on synthetic benchmark (N=50), verifying ZERO shortcut memorization of templates.", GOLD),
        ("60 / 60", "PASSING TESTS", "100% test pass rate across data loading, models, LIME/SHAP, NLI, OCR, and Streamlit pages in 12.36s.", GREEN)
    ]
    for idx, (val, lbl, sub, col) in enumerate(badges):
        left = Inches(0.8) + idx * (b_w + gap)
        add_metric_badge(slide, left, b_top, b_w, b_h, val, lbl, sub, accent_color=col)

def build_slide_18_conclusion(prs):
    slide = add_base_slide(prs)
    add_header(slide, "08 • CONCLUSION", "Project Contributions & Epistemic Governance",
               "Transforming Opaque Black-Box AI into Transparent, Verifiable, and Accountable Intelligence")

    conclusions = [
        {
            "tag": "CONTRIBUTION 01", "col": CYAN,
            "title": "The AI Black Box Opened",
            "points": [
                "Integrated simultaneous LIME and SHAP feature attributions directly tied to calibrated margins.",
                "100% directional sign concordance provides consistent token-level explanations.",
                "Replaced blind algorithmic scores with human-interpretable rationale for news triage."
            ]
        },
        {
            "tag": "CONTRIBUTION 02", "col": TEAL,
            "title": "Dataset Leakage Eradicated",
            "points": [
                "Replaced inadequate synthetic benchmarks with the 44,267-article ISOT corpus.",
                "Engineered group-aware MD5 body clustering guaranteeing zero cross-split duplication.",
                "Purged wire-service headers, ensuring models learn authentic linguistic deception."
            ]
        },
        {
            "tag": "CONTRIBUTION 03", "col": VIOLET,
            "title": "Epistemic Modesty by Design",
            "points": [
                "Positioned strictly as an editorial assistive co-pilot rather than an infallible truth arbiter.",
                "Explicitly distinguishes stylometric probability from external factual verification.",
                "Integrates DeBERTa-v3 cross-encoder NLI to ground claims in empirical evidence."
            ]
        }
    ]

    c_w = Inches(3.7)
    c_h = Inches(4.0)
    top = Inches(1.8)

    for idx, c in enumerate(conclusions):
        left = Inches(0.8) + idx * (c_w + Inches(0.3))
        add_card(slide, left, top, c_w, c_h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)

        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = c["tag"]
        p_tag.font.name = FONT_NAME
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = c["col"]

        p_t = tf.add_paragraph()
        p_t.text = c["title"]
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        tf.add_paragraph().text = ""

        for pt in c["points"]:
            p = tf.add_paragraph()
            p.text = f"•  {pt}"
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.color.rgb = ICE

    # Bottom Tagline Card
    add_card(slide, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.95), bg_rgb=CARD_BG_ALT, border_rgb=BORDER_CYAN, border_width=1.2)
    tx_b = slide.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.333), Inches(0.7))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

    p_b1 = tf_b.paragraphs[0]
    p_b1.text = "CORE PROJECT PHILOSOPHY: INTELLIGENCE BEYOND THE HEADLINE"
    p_b1.font.name = FONT_NAME
    p_b1.font.size = Pt(9.5)
    p_b1.font.bold = True
    p_b1.font.color.rgb = CYAN

    p_b2 = tf_b.add_paragraph()
    p_b2.text = "\"Artificial Intelligence in journalism should explain, corroborate, and assist — never dictate truth in silence.\""
    p_b2.font.name = FONT_NAME
    p_b2.font.size = Pt(11)
    p_b2.font.italic = True
    p_b2.font.color.rgb = WHITE

def build_slide_19_future_scope(prs):
    slide = add_base_slide(prs)
    add_header(slide, "09 • FUTURE SCOPE", "Current Limitations & Strategic Development Roadmap",
               "Honest Epistemic Boundaries and Next-Generation Architectural Extensions")

    # Left: Current Limitations Card
    w = Inches(5.7)
    h = Inches(5.1)
    top = Inches(1.8)

    add_card(slide, Inches(0.8), top, w, h, bg_rgb=CARD_BG, border_rgb=GOLD, border_width=1.0)
    tx_l = slide.shapes.add_textbox(Inches(1.0), top + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    p_lh = tf_l.paragraphs[0]
    p_lh.text = "CURRENT TECHNICAL LIMITATIONS"
    p_lh.font.name = FONT_NAME
    p_lh.font.size = Pt(11)
    p_lh.font.bold = True
    p_lh.font.color.rgb = GOLD

    lims = [
        ("Stylometry Boundary:", "Cannot verify unprecedented or novel factual events without corresponding reference evidence in the knowledge base."),
        ("English Language Constraint:", "The current TF-IDF vocabulary and DeBERTa cross-encoder are optimized exclusively for English prose."),
        ("OCR Compression Sensitivity:", "Tesseract OCR accuracy degrades when encountering heavily compressed or blurry social media screenshots."),
        ("Temporal Concept Drift:", "Political and cultural vocabularies evolve over time, requiring periodic retraining on emerging news corpora.")
    ]
    for title, desc in lims:
        p_t = tf_l.add_paragraph()
        p_t.text = f"\n{title}"
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_l.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = ICE

    # Right: Future Scope Roadmap Card
    add_card(slide, Inches(6.833), top, w, h, bg_rgb=CARD_BG, border_rgb=BORDER_CYAN, border_width=1.0)
    tx_r = slide.shapes.add_textbox(Inches(7.033), top + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "STRATEGIC FUTURE ROADMAP"
    p_rh.font.name = FONT_NAME
    p_rh.font.size = Pt(11)
    p_rh.font.bold = True
    p_rh.font.color.rgb = CYAN

    future = [
        ("Phase 1: Multilingual & Multimodal Vision:", "Integrate mDeBERTa and XLM-RoBERTa for regional languages alongside CLIP vision-language transformers for deepfake image analysis."),
        ("Phase 2: Live Autonomous Web & KG RAG:", "Connect evidence retrieval to live Knowledge Graphs (Wikidata, DBpedia) and real-time syndication feeds via Google Fact Check Tools API."),
        ("Phase 3: Conformal Prediction Bounds:", "Implement conformal prediction to generate mathematically guaranteed coverage intervals rather than point estimates."),
        ("Phase 4: Atomic Claim Decomposition:", "Deploy Open Information Extraction (OpenIE) to segment complex articles into atomic tuples (Subject, Predicate, Object) verified independently.")
    ]
    for title, desc in future:
        p_t = tf_r.add_paragraph()
        p_t.text = f"\n{title}"
        p_t.font.name = FONT_NAME
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        p_d = tf_r.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_NAME
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = ICE

def build_slide_20_references(prs):
    slide = add_base_slide(prs)
    add_header(slide, "10 • REFERENCES", "Authoritative References & Technological Foundations",
               "Peer-Reviewed Academic Literature, Model Foundations & Open-Source Frameworks")

    # Column 1: Academic Research
    w = Inches(5.7)
    h = Inches(5.1)
    top = Inches(1.8)

    add_card(slide, Inches(0.8), top, w, h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)
    tx_1 = slide.shapes.add_textbox(Inches(1.0), top + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
    tf_1 = tx_1.text_frame
    tf_1.word_wrap = True
    tf_1.margin_left = tf_1.margin_right = tf_1.margin_top = tf_1.margin_bottom = 0

    p_1h = tf_1.paragraphs[0]
    p_1h.text = "PEER-REVIEWED RESEARCH LITERATURE"
    p_1h.font.name = FONT_NAME
    p_1h.font.size = Pt(10)
    p_1h.font.bold = True
    p_1h.font.color.rgb = CYAN

    refs_research = [
        "Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). 'Why Should I Trust You?': Explaining the Predictions of Any Classifier. ACM SIGKDD (KDD '16), pp. 1135–1144. (LIME Foundation)",
        "Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. Advances in Neural Information Processing Systems (NeurIPS 30), pp. 4765–4774. (SHAP)",
        "He, P., Gao, J., & Chen, W. (2021). DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding. arXiv:2111.09543. (NLI Backbone)",
        "Ahmed, H., Traore, I., & Saad, S. (2018). Detecting opinion spams and fake news using text classification. Security and Privacy, 1(1), e9. (ISOT Corpus Provenance)",
        "Platt, J. (1999). Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods. Advances in Large Margin Classifiers, pp. 61–74."
    ]
    for r in refs_research:
        p = tf_1.add_paragraph()
        p.text = f"\n• {r}"
        p.font.name = FONT_NAME
        p.font.size = Pt(8.0)
        p.font.color.rgb = ICE

    # Column 2: Algorithmic & Software Foundations
    add_card(slide, Inches(6.833), top, w, h, bg_rgb=CARD_BG, border_rgb=BORDER_SUBTLE)
    tx_2 = slide.shapes.add_textbox(Inches(7.033), top + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
    tf_2 = tx_2.text_frame
    tf_2.word_wrap = True
    tf_2.margin_left = tf_2.margin_right = tf_2.margin_top = tf_2.margin_bottom = 0

    p_2h = tf_2.paragraphs[0]
    p_2h.text = "ALGORITHMIC & SOFTWARE FOUNDATIONS"
    p_2h.font.name = FONT_NAME
    p_2h.font.size = Pt(10)
    p_2h.font.bold = True
    p_2h.font.color.rgb = VIOLET

    refs_tech = [
        "Auer, P., Cesa-Bianchi, N., & Fischer, P. (2002). Finite-time Analysis of the Multiarmed Bandit Problem. Machine Learning, 47(2–3), pp. 235–256. (UCB1 Bandit Algorithm)",
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research (JMLR), 12, pp. 2825–2830. (Classifier Pipelines & Platt Scaling)",
        "Smith, R. (2007). An Overview of the Tesseract OCR Engine. Ninth International Conference on Document Analysis and Recognition (ICDAR 2007), IEEE, pp. 629–633.",
        "Devlin, J., et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL-HLT 2019, pp. 4171–4186.",
        "Streamlit Inc. (2024). Streamlit: The Fastest Way to Build Data Applications. https://streamlit.io."
    ]
    for r in refs_tech:
        p = tf_2.add_paragraph()
        p.text = f"\n• {r}"
        p.font.name = FONT_NAME
        p.font.size = Pt(8.0)
        p.font.color.rgb = ICE

# ---------------------------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------------------------
def generate_all_slides():
    prs = create_presentation()
    print("Building Slide 01: Title...")
    build_slide_01_title(prs)
    print("Building Slide 02: Team...")
    build_slide_02_team(prs)
    print("Building Slide 03: Introduction...")
    build_slide_03_intro(prs)
    print("Building Slide 04: Abstract...")
    build_slide_04_abstract(prs)
    print("Building Slide 05: Problem Statement...")
    build_slide_05_problem_statement(prs)
    print("Building Slide 06: Objectives...")
    build_slide_06_objectives(prs)
    print("Building Slide 07: Workflow & Users...")
    build_slide_07_workflow(prs)
    print("Building Slide 08: Requirements...")
    build_slide_08_requirements(prs)
    print("Building Slide 09: System Architecture...")
    build_slide_09_architecture(prs)
    print("Building Slide 10: Dataset Curation...")
    build_slide_10_dataset(prs)
    print("Building Slide 11: Classification...")
    build_slide_11_classification(prs)
    print("Building Slide 12: Dual XAI (LIME & SHAP)...")
    build_slide_12_xai(prs)
    print("Building Slide 13: Neural NLI & Bandit...")
    build_slide_13_nli_bandit(prs)
    print("Building Slide 14: Screenshots - Dashboard...")
    build_slide_14_screenshots_dashboard(prs)
    print("Building Slide 15: Screenshots - News Analyzer...")
    build_slide_15_screenshots_analyzer(prs)
    print("Building Slide 16: Screenshots - OCR & XAI...")
    build_slide_16_screenshots_ocr_xai(prs)
    print("Building Slide 17: Results & Evaluation...")
    build_slide_17_results(prs)
    print("Building Slide 18: Conclusion...")
    build_slide_18_conclusion(prs)
    print("Building Slide 19: Future Scope...")
    build_slide_19_future_scope(prs)
    print("Building Slide 20: References...")
    build_slide_20_references(prs)

    output_path = "VeriScope_AI_Redesigned.pptx"
    prs.save(output_path)
    print(f"Successfully created presentation: {output_path} with {len(prs.slides)} slides!")

if __name__ == "__main__":
    generate_all_slides()
