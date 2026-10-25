#!/usr/bin/env python3
"""
VeriScope AI — Redesigned Academic Presentation Generator
Generates VeriScope_AI_Redesigned_Presentation.pptx with:
- Ultra-readable typography for classroom projectors (Titles: 34-40pt, Headings: 26-30pt, Body: 22-26pt, Labels: 18-20pt)
- Strictly 3-5 concise, single-line bullets per slide
- Clean, wide, empty rectangular screenshot placeholders with subtle borders and discreet labels
- Modern research-oriented AI theme: Midnight Navy (#0B1120) & Crisp Off-White (#F8FAFC)
- 16:9 Widescreen format with full editability
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Design System & Color Tokens (Research Lab / Digital Trust Theme)
# -----------------------------------------------------------------------------
C_NAVY_DARK    = RGBColor(11, 17, 32)     # #0B1120 - Deep Midnight Navy (Selected Dark Slides)
C_NAVY_CARD    = RGBColor(19, 29, 53)     # #131D35 - Dark Surface Container
C_NAVY_BORDER  = RGBColor(37, 51, 88)     # #253358 - Subtle Dark Border

C_CANVAS_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC - Crisp Light Canvas
C_WHITE_CARD   = RGBColor(255, 255, 255)  # #FFFFFF - Pure White Surface
C_LIGHT_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 - Clean Light Border
C_PLACEHOLDER_BG = RGBColor(241, 245, 249) # #F1F5F9 - Neutral Empty Placeholder

C_CYAN_ACCENT  = RGBColor(6, 182, 212)    # #06B6D4 - Electric Cyan Highlight
C_INDIGO_ACCENT= RGBColor(67, 56, 202)    # #4338CA - Rich Royal Indigo
C_VIOLET_ACCENT= RGBColor(124, 58, 237)   # #7C3AED - Restrained Electric Violet
C_TEAL_ACCENT  = RGBColor(13, 148, 136)   # #0D9488 - Crisp Mint Teal
C_AMBER_ACCENT = RGBColor(217, 119, 6)    # #D97706 - Restrained Amber

C_TEXT_DARK    = RGBColor(15, 23, 42)     # #0F172A - Deep Charcoal (High Contrast)
C_TEXT_SLATE   = RGBColor(71, 85, 105)    # #475569 - Secondary Muted Text
C_TEXT_LIGHT   = RGBColor(248, 250, 252)  # #F8FAFC - Pure White on Dark
C_TEXT_MUTED_L = RGBColor(148, 163, 184)  # #94A3B8 - Slate on Dark

FONT_NAME = "Arial"

SLIDE_WIDTH  = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def create_deck():
    """Creates a 16:9 widescreen presentation."""
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    return prs


def add_background(slide, color):
    """Adds a clean solid full-bleed background."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg


def add_header(slide, section_tag, title_text, dark_mode=False):
    """
    Standardized, high-visibility header.
    Section Tag: 18-20 pt bold uppercase
    Title: 34-38 pt bold
    """
    # Eyebrow / Section Label
    tb_eye = slide.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.5), Inches(0.4))
    tf_eye = tb_eye.text_frame
    tf_eye.word_wrap = True
    tf_eye.margin_left = tf_eye.margin_top = tf_eye.margin_right = tf_eye.margin_bottom = 0
    p_eye = tf_eye.paragraphs[0]
    p_eye.text = section_tag.upper()
    p_eye.font.name = FONT_NAME
    p_eye.font.size = Pt(18)
    p_eye.font.bold = True
    p_eye.font.color.rgb = C_CYAN_ACCENT if dark_mode else C_INDIGO_ACCENT

    # Main Title (Large for classroom projection)
    tb_title = slide.shapes.add_textbox(Inches(0.9), Inches(0.85), Inches(11.5), Inches(0.7))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_NAME
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = C_TEXT_LIGHT if dark_mode else C_TEXT_DARK


def add_card(slide, left, top, width, height, bg_color=C_WHITE_CARD, border_color=C_LIGHT_BORDER, border_width=1):
    """Draws a refined rectangular container."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape


def add_empty_screenshot_placeholder(slide, left, top, width, height, label_text, dark_mode=False):
    """
    Creates a clean, wide, EMPTY rectangular screenshot placeholder
    with a subtle thin border and a discreet 18-20 pt label.
    """
    bg = C_NAVY_CARD if dark_mode else C_PLACEHOLDER_BG
    border = C_CYAN_ACCENT if dark_mode else C_INDIGO_ACCENT

    # The container shape
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = bg
    box.line.color.rgb = border
    box.line.width = Pt(1.5)

    # Discreet center label
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + (height / 2) - Inches(0.4), width - Inches(0.4), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = f"[{label_text}]"
    p.font.name = FONT_NAME
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT if dark_mode else C_INDIGO_ACCENT

    p_sub = tf.add_paragraph()
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "Empty Area Reserved for Actual Screenshot"
    p_sub.font.name = FONT_NAME
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = C_TEXT_MUTED_L if dark_mode else C_TEXT_SLATE
    p_sub.space_before = Pt(4)

    return box


# =============================================================================
# SLIDE 1: TITLE SLIDE (Dark Theme — Premium Research Lab Cover)
# =============================================================================
def build_slide_01_title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_NAVY_DARK)

    # Minimal accent line
    acc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.8), Inches(1.2), Inches(0.08))
    acc.fill.solid()
    acc.fill.fore_color.rgb = C_CYAN_ACCENT
    acc.line.fill.background()

    # Product Name
    tb_prod = slide.shapes.add_textbox(Inches(0.9), Inches(1.05), Inches(11.5), Inches(0.6))
    tf_p = tb_prod.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
    pp = tf_p.paragraphs[0]
    pp.text = "VeriScope AI"
    pp.font.name = FONT_NAME
    pp.font.size = Pt(40)
    pp.font.bold = True
    pp.font.color.rgb = C_CYAN_ACCENT

    # Project Title
    tb_title = slide.shapes.add_textbox(Inches(0.9), Inches(1.75), Inches(11.5), Inches(1.1))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    pt = tf_t.paragraphs[0]
    pt.text = "Fake News Detection Using Explainable AI"
    pt.font.name = FONT_NAME
    pt.font.size = Pt(38)
    pt.font.bold = True
    pt.font.color.rgb = C_TEXT_LIGHT

    # Subtitle / Tagline & Institution
    tb_sub = slide.shapes.add_textbox(Inches(0.9), Inches(2.9), Inches(11.5), Inches(0.6))
    tf_s = tb_sub.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    ps = tf_s.paragraphs[0]
    ps.text = "MSc Artificial Intelligence & Data Analytics  |  Amity University, Noida"
    ps.font.name = FONT_NAME
    ps.font.size = Pt(22)
    ps.font.bold = True
    ps.font.color.rgb = C_TEXT_MUTED_L

    # Team Members Section (5 Clean Cards, Large 20-22pt Text)
    tb_th = slide.shapes.add_textbox(Inches(0.9), Inches(3.8), Inches(11.5), Inches(0.4))
    tf_th = tb_th.text_frame
    tf_th.margin_left = tf_th.margin_top = tf_th.margin_right = tf_th.margin_bottom = 0
    pth = tf_th.paragraphs[0]
    pth.text = "PROJECT RESEARCH TEAM"
    pth.font.name = FONT_NAME
    pth.font.size = Pt(18)
    pth.font.bold = True
    pth.font.color.rgb = C_CYAN_ACCENT

    team = [
        ("Ayushman Kumar", "A010175625019", "NLP Preprocessing"),
        ("Astha Thapa", "A010175625014", "ML Classification"),
        ("Saloni Ganvir", "A010175625017", "Explainable AI & NLI"),
        ("Sarvesh", "A010175625016", "Editorial UI & OCR"),
        ("Sri Rinith", "A010175625018", "Evaluation & Testing"),
    ]

    card_w = Inches(2.18)
    card_h = Inches(2.3)
    gap = Inches(0.15)
    start_x = Inches(0.9)
    y_pos = Inches(4.35)

    for i, (name, enrol, role) in enumerate(team):
        cx = start_x + i * (card_w + gap)
        add_card(slide, cx, y_pos, card_w, card_h, bg_color=C_NAVY_CARD, border_color=C_NAVY_BORDER, border_width=1.5)

        tb = slide.shapes.add_textbox(cx + Inches(0.15), y_pos + Inches(0.2), card_w - Inches(0.3), card_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = name
        p1.font.name = FONT_NAME
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_LIGHT

        p2 = tf.add_paragraph()
        p2.text = enrol
        p2.font.name = FONT_NAME
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = C_CYAN_ACCENT
        p2.space_before = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = role
        p3.font.name = FONT_NAME
        p3.font.size = Pt(18)
        p3.font.color.rgb = C_TEXT_MUTED_L
        p3.space_before = Pt(8)


# =============================================================================
# SLIDE 2: INTRODUCTION OF THE PROJECT (Light Theme — High Contrast)
# =============================================================================
def build_slide_02_intro(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 02 • Introduction of the Project", "The Disinformation Challenge & AI Black Box")

    # 3 High-Impact, Single-Line Classroom Bullets (24 pt)
    tb_bullets = slide.shapes.add_textbox(Inches(0.9), Inches(1.85), Inches(11.53), Inches(2.2))
    tf = tb_bullets.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    bullets = [
        ("Information Velocity", "Unverified claims propagate rapidly, making manual editorial verification impossible at scale."),
        ("The Black-Box Dilemma", "Standard AI classifiers output opaque binary scores without actionable human-interpretable reasoning."),
        ("Prediction is Not Proof", "Stylometric mimicry easily fools models; genuine verification demands external factual evidence."),
    ]

    for i, (title, desc) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}: "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_INDIGO_ACCENT

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.color.rgb = C_TEXT_DARK

        if i > 0:
            p.space_before = Pt(14)

    # Solution Callout Card (Bottom, 24 pt)
    sol_card = add_card(slide, Inches(0.9), Inches(4.5), Inches(11.53), Inches(2.2),
                        bg_color=C_WHITE_CARD, border_color=C_INDIGO_ACCENT, border_width=2)
    tb_sol = slide.shapes.add_textbox(Inches(1.2), Inches(4.75), Inches(10.9), Inches(1.7))
    tf_sol = tb_sol.text_frame
    tf_sol.word_wrap = True
    tf_sol.margin_left = tf_sol.margin_top = tf_sol.margin_right = tf_sol.margin_bottom = 0

    p_sh = tf_sol.paragraphs[0]
    p_sh.text = "The VeriScope AI Verification Triad:"
    p_sh.font.name = FONT_NAME
    p_sh.font.size = Pt(26)
    p_sh.font.bold = True
    p_sh.font.color.rgb = C_INDIGO_ACCENT

    p_sb = tf_sol.add_paragraph()
    p_sb.text = "1. Calibrated Machine Learning  →  2. Dual XAI Interpretability  →  3. Neural Evidence Corroboration"
    p_sb.font.name = FONT_NAME
    p_sb.font.size = Pt(22)
    p_sb.font.bold = True
    p_sb.font.color.rgb = C_TEXT_DARK
    p_sb.space_before = Pt(8)

    p_sc = tf_sol.add_paragraph()
    p_sc.text = "Empowers human editors with transparent, evidence-grounded intelligence rather than blind algorithmic trust."
    p_sc.font.name = FONT_NAME
    p_sc.font.size = Pt(20)
    p_sc.font.color.rgb = C_TEXT_SLATE
    p_sc.space_before = Pt(8)


# =============================================================================
# SLIDE 3: ABSTRACT (Light Theme — 4 Concise Core Deliverables)
# =============================================================================
def build_slide_03_abstract(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 03 • Abstract", "Executive Academic Abstract")

    # 4 Clean Cards Representing the Entire Research Abstract (22-26 pt)
    cards = [
        ("The Core Problem", "Mitigating online disinformation while eliminating opaque black-box AI predictions.", C_INDIGO_ACCENT),
        ("Multimodal Pipeline", "Direct text entry and Tesseract 5.5 OCR extraction with wire-leakage sanitization.", C_VIOLET_ACCENT),
        ("Dual Explainability", "Simultaneous LIME and SHAP token attributions with 100% directional sign agreement.", C_CYAN_ACCENT),
        ("Factual Grounding", "Cross-encoder DeBERTa-v3 NLI verification guided by an objective UCB1 bandit.", C_TEAL_ACCENT),
    ]

    card_w = Inches(5.6)
    card_h = Inches(2.2)
    start_x1 = Inches(0.9)
    start_x2 = Inches(6.83)
    top_y1 = Inches(1.85)
    top_y2 = Inches(4.35)

    coords = [(start_x1, top_y1), (start_x2, top_y1), (start_x1, top_y2), (start_x2, top_y2)]

    for (title, desc, color), (cx, cy) in zip(cards, coords):
        add_card(slide, cx, cy, card_w, card_h, bg_color=C_WHITE_CARD, border_color=C_LIGHT_BORDER, border_width=1.5)

        # Color indicator line
        ind = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx + Inches(0.3), cy + Inches(0.25), Inches(0.8), Inches(0.08))
        ind.fill.solid()
        ind.fill.fore_color.rgb = color
        ind.line.fill.background()

        tb = slide.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.45), card_w - Inches(0.6), card_h - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_NAME
        p1.font.size = Pt(26)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_NAME
        p2.font.size = Pt(22)
        p2.font.color.rgb = C_TEXT_DARK
        p2.space_before = Pt(6)


# =============================================================================
# SLIDE 4: INTRODUCTION IN POINTS — PROBLEM & OBJECTIVES (Light Theme)
# =============================================================================
def build_slide_04_intro_points_p1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 04 • Introduction of the Project in Points", "Problem Statement & Project Objectives")

    col_w = Inches(5.6)
    left_x = Inches(0.9)
    right_x = Inches(6.83)
    top_y = Inches(1.85)
    height = Inches(4.8)

    # Left: Problem Statement Card
    add_card(slide, left_x, top_y, col_w, height, bg_color=C_WHITE_CARD, border_color=C_LIGHT_BORDER)
    tb_left = slide.shapes.add_textbox(left_x + Inches(0.4), top_y + Inches(0.4), col_w - Inches(0.8), height - Inches(0.8))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    p_lh = tf_l.paragraphs[0]
    p_lh.text = "Problem Statement"
    p_lh.font.name = FONT_NAME
    p_lh.font.size = Pt(28)
    p_lh.font.bold = True
    p_lh.font.color.rgb = C_INDIGO_ACCENT

    probs = [
        "Publisher Leakage: Standard datasets allow models to memorize wire-service datelines rather than deceptive stylometry.",
        "Opaque Decisions: Complex models output raw confidence numbers with zero feature attribution.",
        "Lack of Factual Evidence: Text style alone cannot establish whether a real-world event occurred.",
    ]
    for p_txt in probs:
        p = tf_l.add_paragraph()
        p.text = f"•  {p_txt}"
        p.font.name = FONT_NAME
        p.font.size = Pt(22)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(14)

    # Right: Objectives Card
    add_card(slide, right_x, top_y, col_w, height, bg_color=C_WHITE_CARD, border_color=C_LIGHT_BORDER)
    tb_right = slide.shapes.add_textbox(right_x + Inches(0.4), top_y + Inches(0.4), col_w - Inches(0.8), height - Inches(0.8))
    tf_r = tb_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "Project Objectives"
    p_rh.font.name = FONT_NAME
    p_rh.font.size = Pt(28)
    p_rh.font.bold = True
    p_rh.font.color.rgb = C_TEAL_ACCENT

    objs = [
        "Dual Modality: Enable seamless analysis via manual text entry and OCR image uploads.",
        "Leakage-Free Learning: Eradicate wire datelines to train genuine stylometric classifiers.",
        "Explainable AI: Provide simultaneous LIME and SHAP token attributions.",
        "Evidence Corroboration: Ground claims with cross-encoder NLI and 3-month audit history.",
    ]
    for o_txt in objs:
        p = tf_r.add_paragraph()
        p.text = f"✓  {o_txt}"
        p.font.name = FONT_NAME
        p.font.size = Pt(22)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(12)


# =============================================================================
# SLIDE 5: INTRODUCTION IN POINTS — WORKFLOW & USERS (Dark Theme)
# =============================================================================
def build_slide_05_intro_points_p2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_NAVY_DARK)
    add_header(slide, "Section 04 • Introduction of the Project in Points", "End-to-End Workflow & Intended Users", dark_mode=True)

    # Top: Large Visible Flow Diagram (22-26 pt)
    tb_flow_h = slide.shapes.add_textbox(Inches(0.9), Inches(1.8), Inches(11.53), Inches(0.4))
    tf_fh = tb_flow_h.text_frame
    tf_fh.margin_left = tf_fh.margin_top = tf_fh.margin_right = tf_fh.margin_bottom = 0
    pfh = tf_fh.paragraphs[0]
    pfh.text = "SIMPLIFIED SYSTEM WORKFLOW"
    pfh.font.name = FONT_NAME
    pfh.font.size = Pt(20)
    pfh.font.bold = True
    pfh.font.color.rgb = C_CYAN_ACCENT

    # 4 Workflow Steps (Horizontal Flow, 24 pt bold)
    steps = [
        ("1. Input", "Text or OCR Image"),
        ("2. Cleanse", "Regex Leakage Filter"),
        ("3. Classify", "Calibrated ML Models"),
        ("4. Explain", "LIME, SHAP & NLI"),
    ]

    sw = Inches(2.7)
    sh = Inches(1.6)
    gap = Inches(0.24)
    sx = Inches(0.9)
    sy = Inches(2.25)

    for i, (num_title, sub_desc) in enumerate(steps):
        bx = sx + i * (sw + gap)
        add_card(slide, bx, sy, sw, sh, bg_color=C_NAVY_CARD, border_color=C_CYAN_ACCENT, border_width=1.5)

        tb = slide.shapes.add_textbox(bx + Inches(0.15), sy + Inches(0.25), sw - Inches(0.3), sh - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = num_title
        p1.font.name = FONT_NAME
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = C_CYAN_ACCENT

        p2 = tf.add_paragraph()
        p2.text = sub_desc
        p2.font.name = FONT_NAME
        p2.font.size = Pt(20)
        p2.font.color.rgb = C_TEXT_LIGHT
        p2.space_before = Pt(6)

    # Bottom: 3 Key Target User Groups (24 pt)
    tb_usr_h = slide.shapes.add_textbox(Inches(0.9), Inches(4.25), Inches(11.53), Inches(0.4))
    tf_uh = tb_usr_h.text_frame
    tf_uh.margin_left = tf_uh.margin_top = tf_uh.margin_right = tf_uh.margin_bottom = 0
    puh = tf_uh.paragraphs[0]
    puh.text = "INTENDED USER PERSONAS"
    puh.font.name = FONT_NAME
    puh.font.size = Pt(20)
    puh.font.bold = True
    puh.font.color.rgb = C_CYAN_ACCENT

    tb_users = slide.shapes.add_textbox(Inches(0.9), Inches(4.75), Inches(11.53), Inches(2.0))
    tf_u = tb_users.text_frame
    tf_u.word_wrap = True
    tf_u.margin_left = tf_u.margin_top = tf_u.margin_right = tf_u.margin_bottom = 0

    users = [
        ("Fact-Checkers & Journalists", "Rapid triage of viral claims with transparent token-level justification."),
        ("Media Literacy Educators", "Teaching students how algorithmic models assess news and where AI fails."),
        ("General Readers", "Assisting news evaluation without presenting AI predictions as infallible truth."),
    ]
    for i, (utitle, udesc) in enumerate(users):
        p = tf_u.paragraphs[0] if i == 0 else tf_u.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {utitle}: "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_CYAN_ACCENT
        r2 = p.add_run()
        r2.text = udesc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.color.rgb = C_TEXT_LIGHT
        if i > 0:
            p.space_before = Pt(12)


# =============================================================================
# SLIDE 6: SOFTWARE & HARDWARE CONFIGURATION (Light Theme — High Readability)
# =============================================================================
def build_slide_06_tech_config(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 05 • Required Configuration", "Software & Hardware Configuration")

    col_w = Inches(5.6)
    left_x = Inches(0.9)
    right_x = Inches(6.83)
    top_y = Inches(1.85)
    height = Inches(4.8)

    # Left: Software Stack
    add_card(slide, left_x, top_y, col_w, height, bg_color=C_WHITE_CARD, border_color=C_LIGHT_BORDER)
    tb_sw = slide.shapes.add_textbox(left_x + Inches(0.4), top_y + Inches(0.4), col_w - Inches(0.8), height - Inches(0.8))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True
    tf_sw.margin_left = tf_sw.margin_top = tf_sw.margin_right = tf_sw.margin_bottom = 0

    psw_h = tf_sw.paragraphs[0]
    psw_h.text = "Implemented Software Stack"
    psw_h.font.name = FONT_NAME
    psw_h.font.size = Pt(28)
    psw_h.font.bold = True
    psw_h.font.color.rgb = C_INDIGO_ACCENT

    sw_items = [
        "Python 3.12 (Modern runtime)",
        "scikit-learn 1.4+ (Classifiers & Platt scaling)",
        "LIME 0.2 & SHAP 0.44 (Dual XAI)",
        "Tesseract 5.5 & Pillow (OCR engine)",
        "Transformers & ONNX (DeBERTa-v3 NLI)",
        "Streamlit 1.33 & SQLite (UI & audit log)",
    ]
    for sw in sw_items:
        p = tf_sw.add_paragraph()
        p.text = f"•  {sw}"
        p.font.name = FONT_NAME
        p.font.size = Pt(22)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # Right: Hardware Profile
    add_card(slide, right_x, top_y, col_w, height, bg_color=C_WHITE_CARD, border_color=C_LIGHT_BORDER)
    tb_hw = slide.shapes.add_textbox(right_x + Inches(0.4), top_y + Inches(0.4), col_w - Inches(0.8), height - Inches(0.8))
    tf_hw = tb_hw.text_frame
    tf_hw.word_wrap = True
    tf_hw.margin_left = tf_hw.margin_top = tf_hw.margin_right = tf_hw.margin_bottom = 0

    phw_h = tf_hw.paragraphs[0]
    phw_h.text = "Hardware Configuration"
    phw_h.font.name = FONT_NAME
    phw_h.font.size = Pt(28)
    phw_h.font.bold = True
    phw_h.font.color.rgb = C_VIOLET_ACCENT

    hw_items = [
        "Verified Development Environment:",
        "  - Apple Silicon ARM64 (M-Series SoC)",
        "  - 16 GB Unified Memory (RAM)",
        "  - macOS Sonoma / Sequoia (Unix)",
        "Suggested Viva & Demo Specs:",
        "  - Quad-Core 64-bit CPU | 8–16 GB RAM",
        "  - 2.5 GB Free Disk Space | 1080p Display",
    ]
    for i, hw in enumerate(hw_items):
        p = tf_hw.add_paragraph()
        p.text = hw
        p.font.name = FONT_NAME
        if ":" in hw:
            p.font.size = Pt(22)
            p.font.bold = True
            p.font.color.rgb = C_INDIGO_ACCENT if i == 0 else C_VIOLET_ACCENT
            p.space_before = Pt(10)
        else:
            p.font.size = Pt(20)
            p.font.color.rgb = C_TEXT_DARK
            p.space_before = Pt(4)


# =============================================================================
# SLIDE 7: IMPLEMENTATION — ARCHITECTURE (Dark Theme — Large Tier Boxes)
# =============================================================================
def build_slide_07_impl_arch(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_NAVY_DARK)
    add_header(slide, "Section 06 • Implementation — System Architecture", "Multi-Tiered System Architecture", dark_mode=True)

    # 4 Tiered Architectural Levels (Large & Readable, 22-26 pt)
    tiers = [
        ("TIER 1: INGESTION", "Streamlit Multi-Page UI  |  Direct Text Entry  |  Tesseract 5.5 OCR", C_CYAN_ACCENT),
        ("TIER 2: SANITIZATION", "Regex Wire-Tag Eradication  |  Sublinear TF-IDF (5,000 Features)", C_INDIGO_ACCENT),
        ("TIER 3: CLASSIFICATION", "Logistic Regression  |  Multinomial Naive Bayes  |  Platt-Scaled SVM", C_VIOLET_ACCENT),
        ("TIER 4: XAI & AUDIT", "Dual LIME & SHAP  |  DeBERTa-v3 Cross-Encoder NLI  |  SQLite 3-Month Retention", C_TEAL_ACCENT),
    ]

    card_w = Inches(11.53)
    card_h = Inches(1.05)
    gap = Inches(0.2)
    start_x = Inches(0.9)
    start_y = Inches(1.85)

    for i, (tag, detail, color) in enumerate(tiers):
        cy = start_y + i * (card_h + gap)
        add_card(slide, start_x, cy, card_w, card_h, bg_color=C_NAVY_CARD, border_color=color, border_width=2)

        tb = slide.shapes.add_textbox(start_x + Inches(0.3), cy + Inches(0.18), card_w - Inches(0.6), card_h - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = f"{tag}:  "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = color

        r2 = p1.add_run()
        r2.text = detail
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.bold = True
        r2.font.color.rgb = C_TEXT_LIGHT


# =============================================================================
# SLIDE 8: IMPLEMENTATION — METHODOLOGY WITH SCREENSHOT PLACEHOLDER
# =============================================================================
def build_slide_08_impl_method(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 06 • Implementation — Methodology", "Machine Learning & Preprocessing Methodology")

    # Left: 3 Concise Bullets (24 pt)
    col_w = Inches(5.2)
    left_x = Inches(0.9)
    top_y = Inches(1.85)

    tb = slide.shapes.add_textbox(left_x, top_y, col_w, Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    points = [
        ("Leakage Eradication", "Regex filters purge wire signatures (e.g. 'Reuters'), preventing artificial 99% memorization."),
        ("Model Calibration", "Linear SVM calibrated via 3-fold Platt scaling for true bounded posterior probabilities."),
        ("Selected Classifier", "Logistic Regression maps directly to linear Shapley attributions with <100ms inference."),
    ]
    for i, (title, desc) in enumerate(points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}:\n   "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_INDIGO_ACCENT

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.color.rgb = C_TEXT_DARK

        if i > 0:
            p.space_before = Pt(16)

    # Right: Large Empty Screenshot Placeholder
    right_x = Inches(6.5)
    pw = Inches(5.9)
    ph = Inches(4.8)
    add_empty_screenshot_placeholder(slide, right_x, top_y, pw, ph, "Insert Model Training / Evaluation Screenshot")


# =============================================================================
# SLIDE 9: IMPLEMENTATION — EXPLAINABILITY & NLI WITH SCREENSHOT PLACEHOLDER
# =============================================================================
def build_slide_09_impl_xai(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_NAVY_DARK)
    add_header(slide, "Section 06 • Implementation — Explainability", "Dual XAI & Evidence Corroboration", dark_mode=True)

    # Left: 3 Concise Bullets (24 pt)
    col_w = Inches(5.2)
    left_x = Inches(0.9)
    top_y = Inches(1.85)

    tb = slide.shapes.add_textbox(left_x, top_y, col_w, Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    points = [
        ("LIME Perturbation", "Fits local surrogate ridge regression over Monte Carlo text perturbations to capture local token effects."),
        ("SHAP Log-Odds", "Computes exact Shapley attributions via linear log-odds decomposition deterministically in <100ms."),
        ("Neural NLI Verifier", "Cross-encoder DeBERTa-v3 assesses factual premise entailment vs contradiction against reference evidence."),
    ]
    for i, (title, desc) in enumerate(points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}:\n   "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_CYAN_ACCENT

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.color.rgb = C_TEXT_LIGHT

        if i > 0:
            p.space_before = Pt(16)

    # Right: Large Empty Screenshot Placeholder
    right_x = Inches(6.5)
    pw = Inches(5.9)
    ph = Inches(4.8)
    add_empty_screenshot_placeholder(slide, right_x, top_y, pw, ph, "Insert XAI Feature Importance & Evidence Screenshot", dark_mode=True)


# =============================================================================
# SLIDE 10: OUTPUT SCREENSHOTS — EXECUTIVE DASHBOARD
# =============================================================================
def build_slide_10_screenshot_dashboard(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 07 • Output Screenshots — Dashboard", "Editorial Dashboard & Health Monitoring")

    # Left: 3 Clean Explanatory Points (24 pt)
    col_w = Inches(5.0)
    left_x = Inches(0.9)
    top_y = Inches(1.85)

    tb = slide.shapes.add_textbox(left_x, top_y, col_w, Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    bullets = [
        ("Executive Overview", "Displays real-time KPIs: total dispatches audited, likely fake count, and mean model confidence."),
        ("Velocity Monitoring", "Interactive time-series tracking of verification activity across recent editorial sessions."),
        ("System Readiness", "Instant status indicators for classifiers, OCR engines, and the SQLite audit database."),
    ]
    for i, (title, desc) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}:\n   "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_INDIGO_ACCENT

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.color.rgb = C_TEXT_DARK

        if i > 0:
            p.space_before = Pt(16)

    # Right: Large Wide Screenshot Placeholder
    right_x = Inches(6.3)
    pw = Inches(6.1)
    ph = Inches(4.8)
    add_empty_screenshot_placeholder(slide, right_x, top_y, pw, ph, "Insert Dashboard Screenshot")


# =============================================================================
# SLIDE 11: OUTPUT SCREENSHOTS — NEWS ANALYZER
# =============================================================================
def build_slide_11_screenshot_analyzer(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 07 • Output Screenshots — News Analyzer", "News Analyzer & Prediction Interface")

    # Left: 3 Clean Explanatory Points (24 pt)
    col_w = Inches(5.0)
    left_x = Inches(0.9)
    top_y = Inches(1.85)

    tb = slide.shapes.add_textbox(left_x, top_y, col_w, Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    bullets = [
        ("Dual Ingestion", "Independent input fields for Headline and Article Body with live character counters."),
        ("Sanitization Notice", "Real-time alerts when wire datelines or publisher tags are stripped."),
        ("Calibrated Output", "Displays Likely Real / Likely Fake classification badge and posterior probability gauge."),
    ]
    for i, (title, desc) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}:\n   "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_VIOLET_ACCENT

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.color.rgb = C_TEXT_DARK

        if i > 0:
            p.space_before = Pt(16)

    # Right: Large Wide Screenshot Placeholder
    right_x = Inches(6.3)
    pw = Inches(6.1)
    ph = Inches(4.8)
    add_empty_screenshot_placeholder(slide, right_x, top_y, pw, ph, "Insert News Analyzer Screenshot")


# =============================================================================
# SLIDE 12: OUTPUT SCREENSHOTS — OCR PIPELINE
# =============================================================================
def build_slide_12_screenshot_ocr(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 07 • Output Screenshots — OCR Pipeline", "Multimodal OCR Screenshot Ingestion")

    # Left: 3 Clean Explanatory Points (24 pt)
    col_w = Inches(5.0)
    left_x = Inches(0.9)
    top_y = Inches(1.85)

    tb = slide.shapes.add_textbox(left_x, top_y, col_w, Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    bullets = [
        ("Image Ingestion", "Accepts PNG, JPG, JPEG, and WEBP news screenshot clippings up to 10MB."),
        ("Vision Processing", "Automatic EXIF rotation, contrast normalization, and edge sharpening."),
        ("Smart Segmentation", "Heuristic parsing automatically splits candidate headline from body context."),
    ]
    for i, (title, desc) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}:\n   "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_TEAL_ACCENT

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.color.rgb = C_TEXT_DARK

        if i > 0:
            p.space_before = Pt(16)

    # Right: Large Wide Screenshot Placeholder
    right_x = Inches(6.3)
    pw = Inches(6.1)
    ph = Inches(4.8)
    add_empty_screenshot_placeholder(slide, right_x, top_y, pw, ph, "Insert OCR Workflow Screenshot")


# =============================================================================
# SLIDE 13: RESULTS & QUANTITATIVE EVALUATION (Dark Theme — Large Numbers)
# =============================================================================
def build_slide_13_results(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_NAVY_DARK)
    add_header(slide, "Section 08 • Results & Evaluation", "Empirical Evaluation & XAI Research Findings", dark_mode=True)

    # 4 Large Stat Highlight Cards (Numbers: 36 pt, Labels: 20-22 pt)
    stats = [
        ("100.0%", "Test Accuracy", "Held-out test split across all 3 sanitized linear models", C_CYAN_ACCENT),
        ("100.0%", "Sign Concordance", "Directional agreement between LIME and SHAP shared tokens", C_INDIGO_ACCENT),
        ("40.8%", "Top-5 Jaccard", "Overlap between local surrogate and Shapley attributions", C_VIOLET_ACCENT),
        ("35–50%", "Faithfulness Drop", "Confidence drop when masking top-5 tokens vs <2% for random", C_TEAL_ACCENT),
    ]

    card_w = Inches(2.7)
    card_h = Inches(2.8)
    gap = Inches(0.24)
    start_x = Inches(0.9)
    top_y = Inches(1.85)

    for i, (val, label, sub, color) in enumerate(stats):
        cx = start_x + i * (card_w + gap)
        add_card(slide, cx, top_y, card_w, card_h, bg_color=C_NAVY_CARD, border_color=color, border_width=2)

        tb = slide.shapes.add_textbox(cx + Inches(0.2), top_y + Inches(0.25), card_w - Inches(0.4), card_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.name = FONT_NAME
        p1.font.size = Pt(36)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.name = FONT_NAME
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_LIGHT
        p2.space_before = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.name = FONT_NAME
        p3.font.size = Pt(18)
        p3.font.color.rgb = C_TEXT_MUTED_L
        p3.space_before = Pt(8)

    # Bottom Takeaway Card (22 pt)
    takeaway = add_card(slide, start_x, Inches(4.9), Inches(11.53), Inches(1.8),
                        bg_color=C_NAVY_CARD, border_color=C_NAVY_BORDER, border_width=1.5)
    tb_t = slide.shapes.add_textbox(start_x + Inches(0.4), Inches(5.1), Inches(10.7), Inches(1.4))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0

    pt1 = tf_t.paragraphs[0]
    pt1.text = "Academic Takeaway:"
    pt1.font.name = FONT_NAME
    pt1.font.size = Pt(22)
    pt1.font.bold = True
    pt1.font.color.rgb = C_CYAN_ACCENT

    pt2 = tf_t.add_paragraph()
    pt2.text = "Removing wire-service datelines ensures models learn authentic linguistic deception rather than publisher signatures, while the token-masking test proves causal explanation faithfulness."
    pt2.font.name = FONT_NAME
    pt2.font.size = Pt(20)
    pt2.font.color.rgb = C_TEXT_LIGHT
    pt2.space_before = Pt(6)


# =============================================================================
# SLIDE 14: CONCLUSION (Dark Theme — Minimal High-Impact Takeaways)
# =============================================================================
def build_slide_14_conclusion(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_NAVY_DARK)
    add_header(slide, "Section 08 • Conclusion", "Project Contributions & Epistemic Governance", dark_mode=True)

    # 3 High-Impact Classroom Bullets (24 pt)
    tb = slide.shapes.add_textbox(Inches(0.9), Inches(1.85), Inches(11.53), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    points = [
        ("Black Box Opened", "Integrated simultaneous LIME and SHAP feature attributions alongside neural NLI corroboration to replace blind trust with verifiable evidence."),
        ("Publisher Leakage Solved", "Eliminated dateline bias prevalent in benchmark datasets, ensuring classifiers learn genuine stylistic deception markers."),
        ("Epistemic Modesty", "Designed as an editorial assistive copilot; explicitly communicates that statistical likelihood is never proof of factual truth."),
    ]
    for i, (title, desc) in enumerate(points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {title}: "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(24)
        r1.font.bold = True
        r1.font.color.rgb = C_CYAN_ACCENT

        r2 = p.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(22)
        r2.font.color.rgb = C_TEXT_LIGHT

        if i > 0:
            p.space_before = Pt(16)

    # Bottom Closing Banner
    b_card = add_card(slide, Inches(0.9), Inches(5.0), Inches(11.53), Inches(1.7),
                      bg_color=C_NAVY_CARD, border_color=C_CYAN_ACCENT, border_width=2)
    tb_b = slide.shapes.add_textbox(Inches(1.2), Inches(5.25), Inches(10.9), Inches(1.2))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

    pb1 = tf_b.paragraphs[0]
    pb1.text = "CORE PROJECT PHILOSOPHY:"
    pb1.font.name = FONT_NAME
    pb1.font.size = Pt(20)
    pb1.font.bold = True
    pb1.font.color.rgb = C_CYAN_ACCENT

    pb2 = tf_b.add_paragraph()
    pb2.text = "\"Intelligence Beyond the Headline: Transparent, accountable, and evidence-grounded AI.\""
    pb2.font.name = FONT_NAME
    pb2.font.size = Pt(24)
    pb2.font.bold = True
    pb2.font.color.rgb = C_TEXT_LIGHT
    pb2.space_before = Pt(6)


# =============================================================================
# SLIDE 15: LIMITATIONS & FUTURE SCOPE (Light Theme)
# =============================================================================
def build_slide_15_future_scope(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 09 • Future Scope", "Current Limitations & Strategic Roadmap")

    col_w = Inches(5.6)
    left_x = Inches(0.9)
    right_x = Inches(6.83)
    top_y = Inches(1.85)
    height = Inches(4.8)

    # Left: Honest Limitations (22 pt)
    add_card(slide, left_x, top_y, col_w, height, bg_color=C_WHITE_CARD, border_color=C_LIGHT_BORDER)
    tb_lim = slide.shapes.add_textbox(left_x + Inches(0.4), top_y + Inches(0.4), col_w - Inches(0.8), height - Inches(0.8))
    tf_lim = tb_lim.text_frame
    tf_lim.word_wrap = True
    tf_lim.margin_left = tf_lim.margin_top = tf_lim.margin_right = tf_lim.margin_bottom = 0

    pl_h = tf_lim.paragraphs[0]
    pl_h.text = "Current Project Limitations"
    pl_h.font.name = FONT_NAME
    pl_h.font.size = Pt(28)
    pl_h.font.bold = True
    pl_h.font.color.rgb = C_INDIGO_ACCENT

    lims = [
        "Stylometry Bounds: Cannot verify novel claims without corresponding reference evidence.",
        "Compression Noise: Tesseract OCR is sensitive to low-resolution social media image artifacts.",
        "Local Knowledge Base: Evidence retrieval is currently restricted to curated offline corpora.",
    ]
    for lim in lims:
        p = tf_lim.add_paragraph()
        p.text = f"•  {lim}"
        p.font.name = FONT_NAME
        p.font.size = Pt(22)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(14)

    # Right: Future Scope Roadmap (22 pt)
    add_card(slide, right_x, top_y, col_w, height, bg_color=C_WHITE_CARD, border_color=C_LIGHT_BORDER)
    tb_fut = slide.shapes.add_textbox(right_x + Inches(0.4), top_y + Inches(0.4), col_w - Inches(0.8), height - Inches(0.8))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True
    tf_fut.margin_left = tf_fut.margin_top = tf_fut.margin_right = tf_fut.margin_bottom = 0

    pf_h = tf_fut.paragraphs[0]
    pf_h.text = "Strategic Future Roadmap"
    pf_h.font.name = FONT_NAME
    pf_h.font.size = Pt(28)
    pf_h.font.bold = True
    pf_h.font.color.rgb = C_TEAL_ACCENT

    futs = [
        "Phase 1: Multimodal vision-language transformers (CLIP) & multilingual NLP (regional languages).",
        "Phase 2: Live Fact-Checking APIs (Google Fact Check Tools) & Knowledge Graph RAG.",
        "Phase 3: Conformal prediction for mathematically guaranteed uncertainty bounds.",
    ]
    for fut in futs:
        p = tf_fut.add_paragraph()
        p.text = f"→  {fut}"
        p.font.name = FONT_NAME
        p.font.size = Pt(22)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(14)


# =============================================================================
# SLIDE 16: REFERENCES (Light Theme — Clean High-Visibility Citations)
# =============================================================================
def build_slide_16_references(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_CANVAS_LIGHT)
    add_header(slide, "Section 10 • References", "Authoritative References & Bibliography")

    tb = slide.shapes.add_textbox(Inches(0.9), Inches(1.85), Inches(11.53), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    refs = [
        ("Ribeiro, M. T., Singh, S., & Guestrin, C. (2016)",
         "\"Why Should I Trust You?\": Explaining the Predictions of Any Classifier.",
         "ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 1135–1144. (LIME Foundation)"),
        ("Lundberg, S. M., & Lee, S.-I. (2017)",
         "A Unified Approach to Interpreting Model Predictions.",
         "Advances in Neural Information Processing Systems (NeurIPS 30), pp. 4765–4774. (SHAP Foundation)"),
        ("He, P., Gao, J., & Chen, W. (2021)",
         "DeBERTaV3: Improving DeBERTa using ELECTRA-style Pre-Training.",
         "arXiv preprint arXiv:2111.09543. (Neural NLI Architecture)"),
        ("Ahmed, H., Traore, I., & Saad, S. (2017)",
         "Detection of Online Fake News Using N-Gram Analysis and Machine Learning.",
         "Intelligent, Secure, and Dependable Systems in Distributed Infrastructure. (ISOT Corpus Provenance)"),
        ("Pedregosa, F., et al. (2011)",
         "Scikit-learn: Machine Learning in Python.",
         "Journal of Machine Learning Research (JMLR), 12, pp. 2825–2830. (Classifier Pipelines & Platt Scaling)"),
    ]

    for i, (authors, title, venue) in enumerate(refs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"•  {authors}: "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(20)
        r1.font.bold = True
        r1.font.color.rgb = C_INDIGO_ACCENT

        r2 = p.add_run()
        r2.text = f"{title} "
        r2.font.name = FONT_NAME
        r2.font.size = Pt(20)
        r2.font.italic = True
        r2.font.color.rgb = C_TEXT_DARK

        r3 = p.add_run()
        r3.text = f"— {venue}"
        r3.font.name = FONT_NAME
        r3.font.size = Pt(18)
        r3.font.color.rgb = C_TEXT_SLATE

        if i > 0:
            p.space_before = Pt(14)


# =============================================================================
# SLIDE 17: CLOSING & Q&A SLIDE (Dark Theme — Impactful Final Impression)
# =============================================================================
def build_slide_17_closing(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, C_NAVY_DARK)

    # Accent bar
    acc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.2), Inches(1.2), Inches(0.08))
    acc.fill.solid()
    acc.fill.fore_color.rgb = C_CYAN_ACCENT
    acc.line.fill.background()

    # Thank you
    tb_ty = slide.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(11.53), Inches(0.9))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_top = tf_ty.margin_right = tf_ty.margin_bottom = 0
    pty = tf_ty.paragraphs[0]
    pty.text = "Thank You"
    pty.font.name = FONT_NAME
    pty.font.size = Pt(44)
    pty.font.bold = True
    pty.font.color.rgb = C_TEXT_LIGHT

    # Subtitle
    tb_sub = slide.shapes.add_textbox(Inches(0.9), Inches(2.45), Inches(11.53), Inches(0.6))
    tf_s = tb_sub.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    ps = tf_s.paragraphs[0]
    ps.text = "VeriScope AI — Intelligence Beyond the Headline"
    ps.font.name = FONT_NAME
    ps.font.size = Pt(26)
    ps.font.bold = True
    ps.font.color.rgb = C_CYAN_ACCENT

    # Q&A Card
    qa_card = add_card(slide, Inches(0.9), Inches(3.4), Inches(11.53), Inches(2.2),
                       bg_color=C_NAVY_CARD, border_color=C_CYAN_ACCENT, border_width=2)
    tb_qa = slide.shapes.add_textbox(Inches(1.2), Inches(3.7), Inches(10.9), Inches(1.6))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True
    tf_qa.margin_left = tf_qa.margin_top = tf_qa.margin_right = tf_qa.margin_bottom = 0

    p_qh = tf_qa.paragraphs[0]
    p_qh.text = "Open for Questions & Viva Voce Discussion"
    p_qh.font.name = FONT_NAME
    p_qh.font.size = Pt(30)
    p_qh.font.bold = True
    p_qh.font.color.rgb = C_TEXT_LIGHT

    p_qb = tf_qa.add_paragraph()
    p_qb.text = "Amity Institute of Information Technology  |  Amity University, Noida  |  Examination 2026"
    p_qb.font.name = FONT_NAME
    p_qb.font.size = Pt(22)
    p_qb.font.color.rgb = C_TEXT_MUTED_L
    p_qb.space_before = Pt(10)


# =============================================================================
# MAIN REDESIGN GENERATOR
# =============================================================================
def main():
    print("=" * 70)
    print("VeriScope AI — High-Visibility Presentation Redesign Generator")
    print("=" * 70)

    out_file = Path("VeriScope_AI_Redesigned_Presentation.pptx")
    out_dir_file = Path("output/VeriScope_AI_Redesigned_Presentation.pptx")

    prs = create_deck()

    print("[01/17] Slide 1: Section 01 • Title Slide...")
    build_slide_01_title(prs)

    print("[02/17] Slide 2: Section 02 • Introduction of the Project...")
    build_slide_02_intro(prs)

    print("[03/17] Slide 3: Section 03 • Abstract...")
    build_slide_03_abstract(prs)

    print("[04/17] Slide 4: Section 04 • Points — Problem & Objectives...")
    build_slide_04_intro_points_p1(prs)

    print("[05/17] Slide 5: Section 04 • Points — Workflow & Users...")
    build_slide_05_intro_points_p2(prs)

    print("[06/17] Slide 6: Section 05 • Software & Hardware Configuration...")
    build_slide_06_tech_config(prs)

    print("[07/17] Slide 7: Section 06 • Implementation — Architecture...")
    build_slide_07_impl_arch(prs)

    print("[08/17] Slide 8: Section 06 • Implementation — Methodology...")
    build_slide_08_impl_method(prs)

    print("[09/17] Slide 9: Section 06 • Implementation — XAI & Evidence...")
    build_slide_09_impl_xai(prs)

    print("[10/17] Slide 10: Section 07 • Screenshots — Dashboard...")
    build_slide_10_screenshot_dashboard(prs)

    print("[11/17] Slide 11: Section 07 • Screenshots — News Analyzer...")
    build_slide_11_screenshot_analyzer(prs)

    print("[12/17] Slide 12: Section 07 • Screenshots — OCR Pipeline...")
    build_slide_12_screenshot_ocr(prs)

    print("[13/17] Slide 13: Section 08 • Results & Quantitative Evaluation...")
    build_slide_13_results(prs)

    print("[14/17] Slide 14: Section 08 • Conclusion & Governance...")
    build_slide_14_conclusion(prs)

    print("[15/17] Slide 15: Section 09 • Future Scope & Limitations...")
    build_slide_15_future_scope(prs)

    print("[16/17] Slide 16: Section 10 • References & Bibliography...")
    build_slide_16_references(prs)

    print("[17/17] Slide 17: Closing & Q&A Discussion...")
    build_slide_17_closing(prs)

    # Save to both workspace root and output/
    prs.save(str(out_file))
    out_dir_file.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_dir_file))

    print(f"\nSaved successfully:")
    print(f"  1. {out_file.resolve()} ({out_file.stat().st_size:,} bytes)")
    print(f"  2. {out_dir_file.resolve()} ({out_dir_file.stat().st_size:,} bytes)")
    print("=" * 70)


if __name__ == "__main__":
    main()
