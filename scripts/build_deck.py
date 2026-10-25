#!/usr/bin/env python3
"""
VeriScope AI — Academic Integrated Project PowerPoint Generator
Generates a premium, fully editable 16:9 widescreen PowerPoint presentation
satisfying the exact 10-section academic curriculum for MSc AI & Data Analytics,
Amity University, Noida.
"""

import sys
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

# -----------------------------------------------------------------------------
# Color Palette Definitions (from Brand & Design Specifications)
# -----------------------------------------------------------------------------
C_MIDNIGHT     = RGBColor(16, 22, 47)     # #10162F - Primary Dark Background
C_MIDNIGHT_CARD= RGBColor(24, 32, 64)     # #182040 - Dark Card Surface
C_MIDNIGHT_TINT= RGBColor(34, 44, 86)     # #222C56 - Accent Dark Surface
C_CANVAS_BG    = RGBColor(248, 250, 252)  # #F8FAFC - Clean Off-White Canvas
C_WHITE        = RGBColor(255, 255, 255)  # #FFFFFF - Pure White Surface
C_ICE_BLUE     = RGBColor(234, 244, 255)  # #EAF4FF - Soft Ice Blue Accent Fill
C_BORDER_LIGHT = RGBColor(226, 232, 240)  # #E2E8F0 - Delicate Border
C_BORDER_DARK  = RGBColor(51, 65, 85)     # #334155 - Dark Card Border

C_INDIGO       = RGBColor(67, 56, 202)    # #4338CA - Rich Indigo Accent
C_VIOLET       = RGBColor(124, 58, 237)   # #7C3AED - Electric Violet Accent
C_CYAN         = RGBColor(34, 211, 238)   # #22D3EE - Bright Cyan Accent
C_TEAL         = RGBColor(15, 157, 138)   # #0F9D8A - Mint Teal Accent
C_AMBER        = RGBColor(245, 158, 11)   # #F59E0B - Warm Amber
C_ROSE         = RGBColor(225, 29, 72)    # #E11D48 - Coral Rose Accent

C_TEXT_DARK    = RGBColor(15, 23, 42)     # #0F172A - Deep Charcoal Text
C_TEXT_MUTED   = RGBColor(71, 85, 105)    # #475569 - Secondary Muted Text
C_TEXT_LIGHT   = RGBColor(248, 250, 252)  # #F8FAFC - Bright Light Text
C_TEXT_SLATE   = RGBColor(148, 163, 184)  # #94A3B8 - Slate Gray Subtitle

FONT_HEADING = "Arial"
FONT_BODY    = "Calibri"

SLIDE_WIDTH  = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def create_base_deck():
    """Initializes a 16:9 widescreen presentation."""
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    return prs


def add_slide_background(slide, color):
    """Adds a full-bleed colored background rectangle."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg


def add_header(slide, section_num_str, section_name, title_text, subtitle_text, dark_mode=False):
    """Creates a consistent, professional header across technical slides."""
    # Eyebrow pill / badge
    eyebrow_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8.5), Inches(0.35))
    tf_eye = eyebrow_box.text_frame
    tf_eye.word_wrap = True
    tf_eye.margin_left = tf_eye.margin_top = tf_eye.margin_right = tf_eye.margin_bottom = 0
    p_eye = tf_eye.paragraphs[0]
    p_eye.text = f"{section_num_str.upper()}  •  {section_name.upper()}"
    p_eye.font.name = FONT_HEADING
    p_eye.font.size = Pt(10)
    p_eye.font.bold = True
    p_eye.font.color.rgb = C_CYAN if dark_mode else C_INDIGO

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = C_TEXT_LIGHT if dark_mode else C_TEXT_DARK

    # Subtitle
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.5), Inches(0.35))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = C_TEXT_SLATE if dark_mode else C_TEXT_MUTED


def add_footer(slide, current_slide_num, total_slides=14, dark_mode=False):
    """Adds a standard footer with academic branding and slide numbering."""
    # Left brand & affiliation
    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(9.5), Inches(0.3))
    tf = foot_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "VeriScope AI  |  MSc Artificial Intelligence & Data Analytics  |  Amity University, Noida"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(100, 116, 139) if dark_mode else RGBColor(148, 163, 184)

    # Right slide counter
    num_box = slide.shapes.add_textbox(Inches(11.2), Inches(7.05), Inches(1.33), Inches(0.3))
    tf_num = num_box.text_frame
    tf_num.word_wrap = True
    tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"{current_slide_num:02d} / {total_slides:02d}"
    p_num.font.name = FONT_HEADING
    p_num.font.size = Pt(10)
    p_num.font.bold = True
    p_num.font.color.rgb = C_CYAN if dark_mode else C_INDIGO


def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT, border_width=1):
    """Draws a rounded rectangular card container for modern UI aesthetics."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape


# =============================================================================
# SLIDE 1: SECTION 1 — TITLE SLIDE
# =============================================================================
def build_slide_01_title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_MIDNIGHT)

    # Subtle ambient geometric accent shapes (contained cleanly within canvas)
    accent_circ1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.8), Inches(0.2), Inches(3.2), Inches(3.2))
    accent_circ1.fill.solid()
    accent_circ1.fill.fore_color.rgb = RGBColor(22, 32, 68)
    accent_circ1.line.fill.background()

    accent_circ2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.4), Inches(4.2), Inches(2.8), Inches(2.8))
    accent_circ2.fill.solid()
    accent_circ2.fill.fore_color.rgb = RGBColor(20, 28, 60)
    accent_circ2.line.fill.background()

    # Academic & Topic Eyebrow Badge
    badge_bg = add_card(slide, Inches(0.9), Inches(0.65), Inches(8.2), Inches(0.42),
                        bg_color=RGBColor(30, 41, 79), border_color=C_CYAN, border_width=1.5)
    tb_badge = slide.shapes.add_textbox(Inches(1.05), Inches(0.69), Inches(8.0), Inches(0.35))
    tf_b = tb_badge.text_frame
    tf_b.margin_top = tf_b.margin_left = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = "ACADEMIC INTEGRATED PROJECT  •  MSC ARTIFICIAL INTELLIGENCE AND DATA ANALYTICS"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(10.5)
    p_b.font.bold = True
    p_b.font.color.rgb = C_CYAN

    # Project Title
    tb_title = slide.shapes.add_textbox(Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.0))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_top = tf_title.margin_left = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = "VeriScope AI"
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE

    # Tagline
    tb_tag = slide.shapes.add_textbox(Inches(0.9), Inches(2.2), Inches(11.5), Inches(0.45))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_top = tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "Intelligence Beyond the Headline"
    p_tag.font.name = FONT_HEADING
    p_tag.font.size = Pt(21)
    p_tag.font.italic = True
    p_tag.font.color.rgb = C_CYAN

    # Research Topic Subtitle
    tb_top = slide.shapes.add_textbox(Inches(0.9), Inches(2.72), Inches(11.5), Inches(0.4))
    tf_top = tb_top.text_frame
    tf_top.word_wrap = True
    tf_top.margin_top = tf_top.margin_left = tf_top.margin_right = tf_top.margin_bottom = 0
    p_top = tf_top.paragraphs[0]
    p_top.text = "Project Topic: Fake News Detection Using Explainable AI  |  Amity University, Noida"
    p_top.font.name = FONT_BODY
    p_top.font.size = Pt(13)
    p_top.font.bold = True
    p_top.font.color.rgb = C_TEXT_LIGHT

    # Institution Container Card
    inst_card = add_card(slide, Inches(0.9), Inches(3.22), Inches(11.53), Inches(0.65),
                         bg_color=RGBColor(24, 34, 70), border_color=C_INDIGO, border_width=1)
    tb_inst = slide.shapes.add_textbox(Inches(1.1), Inches(3.32), Inches(11.1), Inches(0.45))
    tf_inst = tb_inst.text_frame
    tf_inst.margin_top = tf_inst.margin_left = tf_inst.margin_right = tf_inst.margin_bottom = 0
    p_inst = tf_inst.paragraphs[0]
    p_inst.text = "MSc Artificial Intelligence and Data Analytics  |  Amity University, Noida  |  Examination 2026"
    p_inst.font.name = FONT_HEADING
    p_inst.font.size = Pt(12)
    p_inst.font.bold = True
    p_inst.font.color.rgb = C_TEXT_LIGHT

    # Team Members Section Header
    tb_team_hdr = slide.shapes.add_textbox(Inches(0.9), Inches(4.3), Inches(8.0), Inches(0.35))
    tf_th = tb_team_hdr.text_frame
    tf_th.margin_top = tf_th.margin_left = tf_th.margin_right = tf_th.margin_bottom = 0
    p_th = tf_th.paragraphs[0]
    p_th.text = "PROJECT TEAM MEMBERS & RESPONSIBILITIES"
    p_th.font.name = FONT_HEADING
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = C_CYAN

    # 5 Team Member Cards (Horizontal Row)
    team = [
        ("Ayushman Kumar", "A010175625019", "NLP Preprocessing & Reference Corpus"),
        ("Astha Thapa", "A010175625014", "ML Classification & Hyperparameters"),
        ("Saloni Ganvir", "A010175625017", "Explainable AI (LIME/SHAP) & NLI"),
        ("Sarvesh", "A010175625016", "Editorial UI, Web App & OCR"),
        ("Sri Rinith", "A010175625018", "Model Evaluation & RL Bandit"),
    ]

    card_w = Inches(2.18)
    card_h = Inches(1.95)
    gap = Inches(0.15)
    start_x = Inches(0.9)
    y_pos = Inches(4.7)

    for i, (name, enrol, role) in enumerate(team):
        cx = start_x + i * (card_w + gap)
        # Card background
        add_card(slide, cx, y_pos, card_w, card_h,
                 bg_color=RGBColor(24, 32, 64), border_color=C_BORDER_DARK, border_width=1)

        # Pill indicator at top of card
        pill = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx + Inches(0.15), y_pos + Inches(0.15), Inches(0.4), Inches(0.06))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_CYAN if i == 2 else (C_VIOLET if i in (0, 1) else C_TEAL)
        pill.line.fill.background()

        # Text Frame
        tb_m = slide.shapes.add_textbox(cx + Inches(0.15), y_pos + Inches(0.3), card_w - Inches(0.3), card_h - Inches(0.4))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        tf_m.margin_top = tf_m.margin_left = tf_m.margin_right = tf_m.margin_bottom = 0

        p1 = tf_m.paragraphs[0]
        p1.text = name
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE

        p2 = tf_m.add_paragraph()
        p2.text = enrol
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_CYAN
        p2.space_before = Pt(3)

        p3 = tf_m.add_paragraph()
        p3.text = role
        p3.font.name = FONT_BODY
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = C_TEXT_SLATE
        p3.space_before = Pt(6)

    # Footer note on Title
    tb_foot = slide.shapes.add_textbox(Inches(0.9), Inches(6.9), Inches(11.5), Inches(0.3))
    tf_f = tb_foot.text_frame
    tf_f.margin_top = tf_f.margin_left = tf_f.margin_right = tf_f.margin_bottom = 0
    pf = tf_f.paragraphs[0]
    pf.text = "Amity University Uttar Pradesh, Sector 125, Noida  •  Integrated MSc Project Examination & Viva Voce 2026"
    pf.font.name = FONT_BODY
    pf.font.size = Pt(9.5)
    pf.font.color.rgb = RGBColor(100, 116, 139)


# =============================================================================
# SLIDE 2: SECTION 2 — INTRODUCTION OF THE PROJECT
# =============================================================================
def build_slide_02_intro(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 02", "Introduction of the Project",
               "The Disinformation Challenge & The Black-Box Dilemma",
               "Why automated text classification requires model interpretability and factual evidence verification.")
    add_footer(slide, 2)

    # Left Column: The Problem Context (3 Cards)
    card_w = Inches(5.6)
    left_x = Inches(0.8)

    # Card 1: The Online Information Crisis
    add_card(slide, left_x, Inches(1.8), card_w, Inches(1.5), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    tb1 = slide.shapes.add_textbox(left_x + Inches(0.25), Inches(1.95), card_w - Inches(0.5), Inches(1.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0
    p1 = tf1.paragraphs[0]
    p1.text = "1. Proliferation of Digital Disinformation"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = C_INDIGO
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Online news ecosystems circulate unverified claims, fabricated screenshots, and deceptive narratives at massive velocity. Manual editorial verification cannot scale with real-time digital propagation."
    p1_sub.font.name = FONT_BODY
    p1_sub.font.size = Pt(11)
    p1_sub.font.color.rgb = C_TEXT_MUTED
    p1_sub.space_before = Pt(4)

    # Card 2: The "Black Box" Dilemma
    add_card(slide, left_x, Inches(3.45), card_w, Inches(1.5), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    tb2 = slide.shapes.add_textbox(left_x + Inches(0.25), Inches(3.6), card_w - Inches(0.5), Inches(1.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = "2. The Opaque \"Black Box\" Classifier Dilemma"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_VIOLET
    p2_sub = tf2.add_paragraph()
    p2_sub.text = "Traditional NLP models output opaque probability scores (e.g. '89% Fake') without justification. Users and journalists cannot determine whether decisions reflect legitimate signals or spurious publisher bias."
    p2_sub.font.name = FONT_BODY
    p2_sub.font.size = Pt(11)
    p2_sub.font.color.rgb = C_TEXT_MUTED
    p2_sub.space_before = Pt(4)

    # Card 3: Prediction vs Proof
    add_card(slide, left_x, Inches(5.1), card_w, Inches(1.7), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    tb3 = slide.shapes.add_textbox(left_x + Inches(0.25), Inches(5.25), card_w - Inches(0.5), Inches(1.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
    p3 = tf3.paragraphs[0]
    p3.text = "3. Epistemic Principle: Prediction Alone Is Not Proof"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = C_ROSE
    p3_sub = tf3.add_paragraph()
    p3_sub.text = "Statistical text classification measures syntactic and stylometric similarity to training samples. It cannot establish factual truth. A false claim written in formal journalistic tone easily fools naive classifiers unless verified against external evidence."
    p3_sub.font.name = FONT_BODY
    p3_sub.font.size = Pt(11)
    p3_sub.font.color.rgb = C_TEXT_MUTED
    p3_sub.space_before = Pt(4)

    # Right Column: The VeriScope Verification Triad Container
    right_x = Inches(6.7)
    right_w = Inches(5.8)
    add_card(slide, right_x, Inches(1.8), right_w, Inches(5.0), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    # Triad Title inside Container
    tb_tr = slide.shapes.add_textbox(right_x + Inches(0.35), Inches(2.0), right_w - Inches(0.7), Inches(0.5))
    tf_tr = tb_tr.text_frame
    tf_tr.margin_left = tf_tr.margin_top = tf_tr.margin_right = tf_tr.margin_bottom = 0
    ptr = tf_tr.paragraphs[0]
    ptr.text = "The VeriScope AI Verification Triad"
    ptr.font.name = FONT_HEADING
    ptr.font.size = Pt(16)
    ptr.font.bold = True
    ptr.font.color.rgb = C_TEXT_DARK

    # Triad Stage 1
    s1 = add_card(slide, right_x + Inches(0.35), Inches(2.6), right_w - Inches(0.7), Inches(0.9),
                  bg_color=C_ICE_BLUE, border_color=C_INDIGO, border_width=1)
    tb_s1 = slide.shapes.add_textbox(right_x + Inches(0.5), Inches(2.7), right_w - Inches(1.0), Inches(0.7))
    tfs1 = tb_s1.text_frame
    tfs1.margin_left = tfs1.margin_top = tfs1.margin_right = tfs1.margin_bottom = 0
    p_s1 = tfs1.paragraphs[0]
    p_s1.text = "Stage 1: Headline & Content Analysis (NLP Classification)"
    p_s1.font.name = FONT_HEADING
    p_s1.font.size = Pt(12)
    p_s1.font.bold = True
    p_s1.font.color.rgb = C_INDIGO
    p_s1_sub = tfs1.add_paragraph()
    p_s1_sub.text = "Calibrated Logistic Regression / Linear SVM evaluates stylometric markers after publisher leakage sanitization."
    p_s1_sub.font.name = FONT_BODY
    p_s1_sub.font.size = Pt(10)
    p_s1_sub.font.color.rgb = C_TEXT_MUTED

    # Arrow 1
    arr1 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, right_x + Inches(2.7), Inches(3.55), Inches(0.4), Inches(0.2))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = C_INDIGO
    arr1.line.fill.background()

    # Triad Stage 2
    s2 = add_card(slide, right_x + Inches(0.35), Inches(3.8), right_w - Inches(0.7), Inches(0.9),
                  bg_color=RGBColor(245, 243, 255), border_color=C_VIOLET, border_width=1)
    tb_s2 = slide.shapes.add_textbox(right_x + Inches(0.5), Inches(3.9), right_w - Inches(1.0), Inches(0.7))
    tfs2 = tb_s2.text_frame
    tfs2.margin_left = tfs2.margin_top = tfs2.margin_right = tfs2.margin_bottom = 0
    p_s2 = tfs2.paragraphs[0]
    p_s2.text = "Stage 2: Model Interpretability (Dual XAI Engines)"
    p_s2.font.name = FONT_HEADING
    p_s2.font.size = Pt(12)
    p_s2.font.bold = True
    p_s2.font.color.rgb = C_VIOLET
    p_s2_sub = tfs2.add_paragraph()
    p_s2_sub.text = "Simultaneous LIME and SHAP feature attributions expose exact token contributions, verifying prediction faithfulness."
    p_s2_sub.font.name = FONT_BODY
    p_s2_sub.font.size = Pt(10)
    p_s2_sub.font.color.rgb = C_TEXT_MUTED

    # Arrow 2
    arr2 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, right_x + Inches(2.7), Inches(4.75), Inches(0.4), Inches(0.2))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = C_VIOLET
    arr2.line.fill.background()

    # Triad Stage 3
    s3 = add_card(slide, right_x + Inches(0.35), Inches(5.0), right_w - Inches(0.7), Inches(0.9),
                  bg_color=RGBColor(236, 253, 245), border_color=C_TEAL, border_width=1)
    tb_s3 = slide.shapes.add_textbox(right_x + Inches(0.5), Inches(5.1), right_w - Inches(1.0), Inches(0.7))
    tfs3 = tb_s3.text_frame
    tfs3.margin_left = tfs3.margin_top = tfs3.margin_right = tfs3.margin_bottom = 0
    p_s3 = tfs3.paragraphs[0]
    p_s3.text = "Stage 3: Evidence Corroboration (Cross-Encoder NLI)"
    p_s3.font.name = FONT_HEADING
    p_s3.font.size = Pt(12)
    p_s3.font.bold = True
    p_s3.font.color.rgb = C_TEAL
    p_s3_sub = tfs3.add_paragraph()
    p_s3_sub.text = "Cross-encoder DeBERTa-v3 assesses factual entailment against audited reference knowledge bases via UCB1 bandit."
    p_s3_sub.font.name = FONT_BODY
    p_s3_sub.font.size = Pt(10)
    p_s3_sub.font.color.rgb = C_TEXT_MUTED

    # Bottom Callout banner
    tb_call = slide.shapes.add_textbox(right_x + Inches(0.35), Inches(6.05), right_w - Inches(0.7), Inches(0.6))
    tfc = tb_call.text_frame
    tfc.word_wrap = True
    tfc.margin_left = tfc.margin_top = tfc.margin_right = tfc.margin_bottom = 0
    pc = tfc.paragraphs[0]
    pc.text = "Core Epistemic Takeaway: VeriScope AI is designed as an assistive editorial copilot for human analysts, replacing blind trust with verifiable evidence."
    pc.font.name = FONT_BODY
    pc.font.size = Pt(10)
    pc.font.italic = True
    pc.font.color.rgb = C_TEXT_MUTED


# =============================================================================
# SLIDE 3: SECTION 3 — ABSTRACT
# =============================================================================
def build_slide_03_abstract(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 03", "Abstract",
               "Academic Research Abstract & Platform Overview",
               "Concise 125-word formal summary of the problem, engineering implementation, and evaluation findings.")
    add_footer(slide, 3)

    # Master Abstract Container Card
    card_w = Inches(11.73)
    card_x = Inches(0.8)
    add_card(slide, card_x, Inches(1.85), card_w, Inches(2.6), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    # Eyebrow badge inside abstract card
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x + Inches(0.4), Inches(2.05), Inches(2.2), Inches(0.3))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_ICE_BLUE
    badge.line.color.rgb = C_INDIGO
    badge.line.width = Pt(1)
    tb_b = slide.shapes.add_textbox(card_x + Inches(0.4), Inches(2.07), Inches(2.2), Inches(0.3))
    tf_b = tb_b.text_frame
    tf_b.margin_top = tf_b.margin_left = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "FORMAL RESEARCH ABSTRACT"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = C_INDIGO

    # Abstract Text Body (Exactly ~125 words, rigorous academic style)
    abstract_text = (
        "Digital disinformation undermines public discourse, while standard deep-learning classifiers operate as "
        "uninterpretable black boxes whose statistical predictions lack factual justification. This integrated project presents "
        "VeriScope AI, an end-to-end editorial verification platform developed for the MSc in Artificial Intelligence and "
        "Data Analytics at Amity University, Noida. VeriScope AI integrates dual input modalities (manual text entry and Tesseract 5.5 "
        "OCR screenshot extraction), rigorous publisher leakage mitigation, calibrated linear classifiers (Logistic Regression, "
        "Multinomial Naive Bayes, Linear SVM with Platt scaling), dual Explainable AI engines (LIME and SHAP), and cross-encoder "
        "Natural Language Inference (DeBERTa-v3) driven by an Upper Confidence Bound (UCB1) contextual reinforcement learning bandit. "
        "The system achieves 100% directional sign concordance across intersecting features and demonstrates high causal "
        "faithfulness under token masking. VeriScope AI empowers editorial analysts with transparent, interpretable, and "
        "epistemically modest verification beyond ungrounded binary predictions."
    )

    tb_abs = slide.shapes.add_textbox(card_x + Inches(0.4), Inches(2.45), card_w - Inches(0.8), Inches(1.8))
    tf_abs = tb_abs.text_frame
    tf_abs.word_wrap = True
    tf_abs.margin_left = tf_abs.margin_top = tf_abs.margin_right = tf_abs.margin_bottom = 0
    p_abs = tf_abs.paragraphs[0]
    p_abs.text = abstract_text
    p_abs.font.name = FONT_BODY
    p_abs.font.size = Pt(12.5)
    p_abs.font.color.rgb = C_TEXT_DARK
    p_abs.line_spacing = 1.25

    # 4 Pillar Cards Highlighting Key Architectural Deliverables
    pillar_w = Inches(2.78)
    pillar_h = Inches(2.05)
    gap = Inches(0.2)
    y_p = Inches(4.7)

    pillars = [
        ("Multimodal Ingestion", "Dual Input Modalities",
         "Direct text entry & Tesseract 5.5 OCR extraction with EXIF rotation, contrast normalization, and layout segmentation.",
         C_INDIGO),
        ("Leakage Sanitization", "Eradicating Wire Bias",
         "Strict regex filters remove datelines (e.g. 'Reuters', 'AP'), forcing models to learn authentic deception stylometry.",
         C_VIOLET),
        ("Dual Explainability", "LIME & SHAP XAI Suite",
         "100% directional sign concordance between local surrogate perturbations and exact Shapley feature attributions.",
         C_CYAN),
        ("Factual Grounding", "Neural NLI Verifier",
         "Cross-encoder DeBERTa-v3 assesses premise-hypothesis entailment via an adaptive UCB1 reinforcement learning bandit.",
         C_TEAL),
    ]

    for i, (tag, title, desc, accent) in enumerate(pillars):
        px = card_x + i * (pillar_w + gap)
        add_card(slide, px, y_p, pillar_w, pillar_h, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

        # Top accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, px + Inches(0.2), y_p + Inches(0.18), Inches(0.6), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = accent
        line.line.fill.background()

        tb = slide.shapes.add_textbox(px + Inches(0.2), y_p + Inches(0.35), pillar_w - Inches(0.4), pillar_h - Inches(0.45))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = tag.upper()
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = accent

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_DARK
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10)
        p3.font.color.rgb = C_TEXT_MUTED
        p3.space_before = Pt(4)


# =============================================================================
# SLIDE 4: SECTION 4 — INTRODUCTION IN POINTS (PART 1: PROBLEM & OBJECTIVES)
# =============================================================================
def build_slide_04_intro_points_p1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 04", "Introduction of the Project in Points",
               "Problem Statement & Academic Objectives",
               "Clear formal formulation of research challenges and technical deliverables.")
    add_footer(slide, 4)

    col_w = Inches(5.7)
    left_x = Inches(0.8)
    right_x = Inches(6.8)
    top_y = Inches(1.8)
    height = Inches(5.0)

    # Left Container: Problem Statement
    add_card(slide, left_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_prob_hdr = slide.shapes.add_textbox(left_x + Inches(0.35), top_y + Inches(0.3), col_w - Inches(0.7), Inches(0.4))
    tf_ph = tb_prob_hdr.text_frame
    tf_ph.margin_top = tf_ph.margin_left = tf_ph.margin_right = tf_ph.margin_bottom = 0
    pph = tf_ph.paragraphs[0]
    pph.text = "PROBLEM STATEMENT"
    pph.font.name = FONT_HEADING
    pph.font.size = Pt(15)
    pph.font.bold = True
    pph.font.color.rgb = C_ROSE

    # Problem Statement summary box
    summary_card = add_card(slide, left_x + Inches(0.35), top_y + Inches(0.8), col_w - Inches(0.7), Inches(1.15),
                            bg_color=RGBColor(255, 241, 242), border_color=C_ROSE, border_width=1)
    tb_ps = slide.shapes.add_textbox(left_x + Inches(0.5), top_y + Inches(0.9), col_w - Inches(1.0), Inches(0.95))
    tf_ps = tb_ps.text_frame
    tf_ps.word_wrap = True
    tf_ps.margin_top = tf_ps.margin_left = tf_ps.margin_right = tf_ps.margin_bottom = 0
    pps = tf_ps.paragraphs[0]
    pps.text = "Users require automated assistance to evaluate potentially misleading news. However, automated predictions without human-understandable reasoning or corroborating evidence induce false confidence and fail to identify stylistic mimicry."
    pps.font.name = FONT_BODY
    pps.font.size = Pt(11)
    pps.font.bold = True
    pps.font.color.rgb = RGBColor(159, 18, 57)

    # Problem Breakdown Items
    prob_items = [
        ("Publisher Leakage Vulnerability",
         "Traditional academic fake news datasets suffer from wire-tag leakage (e.g. 'Reuters'). Classifiers memorize datelines rather than learning deceptive syntax."),
        ("The Algorithmic Black Box",
         "Standard NLP classifiers produce uncalibrated probabilities with zero attribution, leaving users unable to inspect which tokens influenced the prediction."),
        ("Conflation of Style & Factual Truth",
         "A classification label alone is not proof of veracity. Falsified stories formatted as legitimate journalism cannot be caught without external evidence retrieval."),
    ]

    item_y = top_y + Inches(2.15)
    for title, desc in prob_items:
        tb_item = slide.shapes.add_textbox(left_x + Inches(0.35), item_y, col_w - Inches(0.7), Inches(0.85))
        tf_i = tb_item.text_frame
        tf_i.word_wrap = True
        tf_i.margin_top = tf_i.margin_left = tf_i.margin_right = tf_i.margin_bottom = 0

        p1 = tf_i.paragraphs[0]
        p1.text = f"•  {title}"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK

        p2 = tf_i.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(2)

        item_y += Inches(0.9)

    # Right Container: Project Objectives
    add_card(slide, right_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_obj_hdr = slide.shapes.add_textbox(right_x + Inches(0.35), top_y + Inches(0.3), col_w - Inches(0.7), Inches(0.4))
    tf_oh = tb_obj_hdr.text_frame
    tf_oh.margin_top = tf_oh.margin_left = tf_oh.margin_right = tf_oh.margin_bottom = 0
    poh = tf_oh.paragraphs[0]
    poh.text = "RESEARCH & TECHNICAL OBJECTIVES"
    poh.font.name = FONT_HEADING
    poh.font.size = Pt(15)
    poh.font.bold = True
    poh.font.color.rgb = C_INDIGO

    objectives = [
        ("Accessible Multi-Modal Interface", "Provide an intuitive editorial workspace supporting direct text entry and OCR image screenshot ingestion."),
        ("Leakage-Sanitized ML Classification", "Implement rigorous regex sanitization and train calibrated classifiers (Logistic Regression, MNB, Linear SVM with Platt scaling)."),
        ("Dual Explainable AI Architecture", "Integrate local surrogate perturbations (LIME) and game-theoretic Shapley attributions (SHAP) for transparent token analysis."),
        ("Empirical XAI Benchmarking", "Evaluate explanation quality via Top-k Jaccard agreement, directional sign concordance, and causal token-masking faithfulness."),
        ("Factual Grounding via NLI", "Verify claims against an audited reference knowledge base using cross-encoder DeBERTa-v3 inference driven by a UCB1 bandit."),
        ("Epistemic Governance & Retention", "Enforce transparent uncertainty disclosures and an automated 3-calendar-month UTC data retention audit database in SQLite."),
    ]

    obj_y = top_y + Inches(0.8)
    for i, (title, desc) in enumerate(objectives):
        # Number badge
        nb = slide.shapes.add_shape(MSO_SHAPE.OVAL, right_x + Inches(0.35), obj_y, Inches(0.3), Inches(0.3))
        nb.fill.solid()
        nb.fill.fore_color.rgb = C_ICE_BLUE
        nb.line.color.rgb = C_INDIGO
        nb.line.width = Pt(1)
        tb_nb = slide.shapes.add_textbox(right_x + Inches(0.35), obj_y, Inches(0.3), Inches(0.3))
        tf_nb = tb_nb.text_frame
        tf_nb.margin_top = tf_nb.margin_left = tf_nb.margin_right = tf_nb.margin_bottom = 0
        p_nb = tf_nb.paragraphs[0]
        p_nb.alignment = PP_ALIGN.CENTER
        p_nb.text = str(i + 1)
        p_nb.font.name = FONT_HEADING
        p_nb.font.size = Pt(10)
        p_nb.font.bold = True
        p_nb.font.color.rgb = C_INDIGO

        # Content
        tb_o = slide.shapes.add_textbox(right_x + Inches(0.75), obj_y - Inches(0.02), col_w - Inches(1.1), Inches(0.65))
        tf_o = tb_o.text_frame
        tf_o.word_wrap = True
        tf_o.margin_top = tf_o.margin_left = tf_o.margin_right = tf_o.margin_bottom = 0

        p1 = tf_o.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK

        p2 = tf_o.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(1)

        obj_y += Inches(0.68)


# =============================================================================
# SLIDE 5: SECTION 4 — INTRODUCTION IN POINTS (PART 2: WORKFLOW & USERS)
# =============================================================================
def build_slide_05_intro_points_p2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_MIDNIGHT)
    add_header(slide, "SECTION 04", "Introduction of the Project in Points",
               "System Workflow & Intended Users",
               "End-to-end data pipeline from raw input to verified output and audience utility.", dark_mode=True)
    add_footer(slide, 5, dark_mode=True)

    # Workflow Section Header
    tb_wf_hdr = slide.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.5), Inches(0.35))
    tf_wh = tb_wf_hdr.text_frame
    tf_wh.margin_top = tf_wh.margin_left = tf_wh.margin_right = tf_wh.margin_bottom = 0
    pwh = tf_wh.paragraphs[0]
    pwh.text = "EDITABLE END-TO-END PIPELINE WORKFLOW"
    pwh.font.name = FONT_HEADING
    pwh.font.size = Pt(11)
    pwh.font.bold = True
    pwh.font.color.rgb = C_CYAN

    # 6-Stage Process Flow Diagram (Horizontal Nodes)
    flow_steps = [
        ("1. Input Ingestion", "Text Entry / OCR Screenshot", C_INDIGO),
        ("2. Preprocessing", "Regex Sanitizer & Tokenize", C_VIOLET),
        ("3. Representation", "TF-IDF Vectorizer (5k)", C_CYAN),
        ("4. Classification", "Calibrated Logistic Reg.", C_AMBER),
        ("5. Explainability", "Dual LIME & SHAP XAI", C_ROSE),
        ("6. Evidence & UI", "DeBERTa NLI & SQLite", C_TEAL),
    ]

    node_w = Inches(1.82)
    node_h = Inches(1.35)
    gap = Inches(0.16)
    start_x = Inches(0.8)
    y_flow = Inches(2.25)

    for i, (title, sub, color) in enumerate(flow_steps):
        nx = start_x + i * (node_w + gap)
        add_card(slide, nx, y_flow, node_w, node_h, bg_color=C_MIDNIGHT_CARD, border_color=color, border_width=1.5)

        tb = slide.shapes.add_textbox(nx + Inches(0.12), y_flow + Inches(0.15), node_w - Inches(0.24), node_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_SLATE
        p2.space_before = Pt(4)

        # Connector arrow to next stage
        if i < len(flow_steps) - 1:
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, nx + node_w + Inches(0.03), y_flow + Inches(0.55), Inches(0.1), Inches(0.18))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_TEXT_SLATE
            arr.line.fill.background()

    # Intended Users Section Header
    tb_u_hdr = slide.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(11.5), Inches(0.35))
    tf_uh = tb_u_hdr.text_frame
    tf_uh.margin_top = tf_uh.margin_left = tf_uh.margin_right = tf_uh.margin_bottom = 0
    puh = tf_uh.paragraphs[0]
    puh.text = "TARGET USER PERSONAS & OPERATIONAL SCOPE"
    puh.font.name = FONT_HEADING
    puh.font.size = Pt(11)
    puh.font.bold = True
    puh.font.color.rgb = C_CYAN

    # 4 User Persona Cards
    personas = [
        ("Fact-Checkers & Journalists",
         "Rapid preliminary triage of suspicious social media dispatches, identifying key manipulative keywords and contrasting against verified archives.",
         C_CYAN),
        ("Academic AI Researchers",
         "Benchmarking explanation fidelity, studying the publisher leakage flaw in public corpora, and testing LIME vs SHAP agreement metrics.",
         C_VIOLET),
        ("Media Literacy Educators",
         "Interactive classroom teaching tool demonstrating how algorithmic black boxes function, why models fail, and how evidence grounds claims.",
         C_AMBER),
        ("General News Readers",
         "An objective second-opinion reading companion for analyzing viral headlines with clear epistemic modesty disclosures and zero fake confidence.",
         C_TEAL),
    ]

    user_w = Inches(2.81)
    user_h = Inches(2.25)
    gap_u = Inches(0.16)
    y_user = Inches(4.3)

    for i, (p_title, p_desc, p_accent) in enumerate(personas):
        ux = start_x + i * (user_w + gap_u)
        add_card(slide, ux, y_user, user_w, user_h, bg_color=C_MIDNIGHT_CARD, border_color=C_BORDER_DARK, border_width=1)

        # Accent top bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, ux + Inches(0.15), y_user + Inches(0.15), Inches(0.5), Inches(0.05))
        bar.fill.solid()
        bar.fill.fore_color.rgb = p_accent
        bar.line.fill.background()

        tb_u = slide.shapes.add_textbox(ux + Inches(0.15), y_user + Inches(0.3), user_w - Inches(0.3), user_h - Inches(0.4))
        tfu = tb_u.text_frame
        tfu.word_wrap = True
        tfu.margin_top = tfu.margin_left = tfu.margin_right = tfu.margin_bottom = 0

        p1 = tfu.paragraphs[0]
        p1.text = p_title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE

        p2 = tfu.add_paragraph()
        p2.text = p_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_SLATE
        p2.space_before = Pt(6)


# =============================================================================
# SLIDE 6: SECTION 5 — SOFTWARE AND HARDWARE REQUIRED CONFIGURATION
# =============================================================================
def build_slide_06_tech_config(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 05", "Software & Hardware Required Configuration",
               "Technical Stack & System Environment",
               "Verified workspace dependencies and suggested development machine profiles.")
    add_footer(slide, 6)

    col_w = Inches(5.7)
    left_x = Inches(0.8)
    right_x = Inches(6.8)
    top_y = Inches(1.8)
    height = Inches(5.0)

    # Left Container: Software Stack
    add_card(slide, left_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_sw_hdr = slide.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(0.25), col_w - Inches(0.6), Inches(0.35))
    tf_sh = tb_sw_hdr.text_frame
    tf_sh.margin_top = tf_sh.margin_left = tf_sh.margin_right = tf_sh.margin_bottom = 0
    psh = tf_sh.paragraphs[0]
    psh.text = "SOFTWARE STACK SPECIFICATIONS"
    psh.font.name = FONT_HEADING
    psh.font.size = Pt(14)
    psh.font.bold = True
    psh.font.color.rgb = C_INDIGO

    # Section 1: Implemented in Project
    tb_imp = slide.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(0.65), col_w - Inches(0.6), Inches(0.25))
    tf_imp = tb_imp.text_frame
    tf_imp.margin_top = tf_imp.margin_left = tf_imp.margin_right = tf_imp.margin_bottom = 0
    pimp = tf_imp.paragraphs[0]
    pimp.text = "• Implemented & Verified in Project Workspace:"
    pimp.font.name = FONT_HEADING
    pimp.font.size = Pt(11)
    pimp.font.bold = True
    pimp.font.color.rgb = C_TEXT_DARK

    sw_items = [
        ("Python 3.12", "Core programming runtime with strict typing and modern syntax"),
        ("scikit-learn 1.4+", "Logistic Regression, Naive Bayes, Linear SVM & Platt Calibration"),
        ("LIME 0.2.0.1", "Local Interpretable Model-agnostic Explanations via Monte Carlo perturbations"),
        ("SHAP 0.44.0", "Game-theoretic Shapley additive feature attributions for linear models"),
        ("Tesseract OCR 5.5", "Local OCR engine with Pillow 10.2+ and pytesseract 0.3.10 wrapper"),
        ("Transformers & ONNX", "cross-encoder/nli-deberta-v3-base for genuine entailment inference"),
        ("Streamlit 1.33+", "Multi-page reactive editorial intelligence web application framework"),
        ("SQLite 3 Database", "Audit history logging with automated 3-calendar-month UTC purge"),
        ("Pytest 8.0+", "47 automated unit and integration tests passing in workspace"),
    ]

    sw_y = top_y + Inches(0.95)
    for pkg, purpose in sw_items:
        tb_item = slide.shapes.add_textbox(left_x + Inches(0.4), sw_y, col_w - Inches(0.8), Inches(0.3))
        tf_i = tb_item.text_frame
        tf_i.word_wrap = True
        tf_i.margin_top = tf_i.margin_left = tf_i.margin_right = tf_i.margin_bottom = 0

        p = tf_i.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{pkg}: "
        r1.font.name = FONT_HEADING
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_INDIGO

        r2 = p.add_run()
        r2.text = purpose
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED

        sw_y += Inches(0.32)

    # Section 2: Optional/Proposed Technologies
    tb_prop = slide.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(3.95), col_w - Inches(0.6), Inches(0.9))
    tf_pr = tb_prop.text_frame
    tf_pr.word_wrap = True
    tf_pr.margin_top = tf_pr.margin_left = tf_pr.margin_right = tf_pr.margin_bottom = 0
    ppr = tf_pr.paragraphs[0]
    ppr.text = "• Optional / Proposed Technologies for Future Expansion:"
    ppr.font.name = FONT_HEADING
    ppr.font.size = Pt(11)
    ppr.font.bold = True
    ppr.font.color.rgb = C_TEXT_DARK

    p_body = tf_pr.add_paragraph()
    p_body.text = "Live Web Fact-Checking APIs (Google Fact Check Tools / Bing News API) and Distributed Vector Stores (FAISS / Milvus) for high-scale enterprise knowledge retrieval."
    p_body.font.name = FONT_BODY
    p_body.font.size = Pt(9.5)
    p_body.font.color.rgb = C_TEXT_MUTED
    p_body.space_before = Pt(2)

    # Right Container: Hardware Specifications
    add_card(slide, right_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_hw_hdr = slide.shapes.add_textbox(right_x + Inches(0.3), top_y + Inches(0.25), col_w - Inches(0.6), Inches(0.35))
    tf_hh = tb_hw_hdr.text_frame
    tf_hh.margin_top = tf_hh.margin_left = tf_hh.margin_right = tf_hh.margin_bottom = 0
    phh = tf_hh.paragraphs[0]
    phh.text = "HARDWARE CONFIGURATION SPECIFICATIONS"
    phh.font.name = FONT_HEADING
    phh.font.size = Pt(14)
    phh.font.bold = True
    phh.font.color.rgb = C_VIOLET

    # Verified Development Machine
    tb_dev = slide.shapes.add_textbox(right_x + Inches(0.3), top_y + Inches(0.65), col_w - Inches(0.6), Inches(0.25))
    tf_dev = tb_dev.text_frame
    tf_dev.margin_top = tf_dev.margin_left = tf_dev.margin_right = tf_dev.margin_bottom = 0
    pdev = tf_dev.paragraphs[0]
    pdev.text = "• Actual Development Machine Configuration (Verified):"
    pdev.font.name = FONT_HEADING
    pdev.font.size = Pt(11)
    pdev.font.bold = True
    pdev.font.color.rgb = C_TEXT_DARK

    hw_actual = [
        ("Processor Architecture", "Apple Silicon ARM64 (M-Series SoC with Neural Engine)"),
        ("System Memory", "16 GB Unified Memory (LPDDR5)"),
        ("Persistent Storage", "High-Speed Solid State Drive (APFS Filesystem)"),
        ("Operating System", "macOS Sonoma / Sequoia (Unix environment)"),
        ("Hardware Acceleration", "MPS (Metal Performance Shaders) for PyTorch tensor ops"),
    ]

    h_y = top_y + Inches(0.95)
    for k, v in hw_actual:
        tb_item = slide.shapes.add_textbox(right_x + Inches(0.4), h_y, col_w - Inches(0.8), Inches(0.3))
        tf_i = tb_item.text_frame
        tf_i.word_wrap = True
        tf_i.margin_top = tf_i.margin_left = tf_i.margin_right = tf_i.margin_bottom = 0
        p = tf_i.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{k}: "
        r1.font.name = FONT_HEADING
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_VIOLET
        r2 = p.add_run()
        r2.text = v
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED
        h_y += Inches(0.38)

    # Suggested Minimum Configuration
    tb_sug = slide.shapes.add_textbox(right_x + Inches(0.3), top_y + Inches(2.95), col_w - Inches(0.6), Inches(0.25))
    tf_sug = tb_sug.text_frame
    tf_sug.margin_top = tf_sug.margin_left = tf_sug.margin_right = tf_sug.margin_bottom = 0
    psug = tf_sug.paragraphs[0]
    psug.text = "• Suggested Development & Viva Demonstration Configuration:"
    psug.font.name = FONT_HEADING
    psug.font.size = Pt(11)
    psug.font.bold = True
    psug.font.color.rgb = C_TEXT_DARK

    hw_suggested = [
        ("CPU", "Quad-Core 64-bit x86/ARM processor (Intel Core i5 / AMD Ryzen 5 / Apple M1)"),
        ("RAM", "8 GB minimum (16 GB recommended for Transformer NLI inference)"),
        ("Disk Space", "2.5 GB free disk space for models, virtual environment & OCR"),
        ("Display", "1920x1080 Full HD resolution for optimal editorial dashboard view"),
    ]

    hs_y = top_y + Inches(3.25)
    for k, v in hw_suggested:
        tb_item = slide.shapes.add_textbox(right_x + Inches(0.4), hs_y, col_w - Inches(0.8), Inches(0.3))
        tf_i = tb_item.text_frame
        tf_i.word_wrap = True
        tf_i.margin_top = tf_i.margin_left = tf_i.margin_right = tf_i.margin_bottom = 0
        p = tf_i.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{k}: "
        r1.font.name = FONT_HEADING
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = C_TEAL
        r2 = p.add_run()
        r2.text = v
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED
        hs_y += Inches(0.38)


# =============================================================================
# SLIDE 7: SECTION 6 — IMPLEMENTATION (SLIDE A: SYSTEM ARCHITECTURE)
# =============================================================================
def build_slide_07_impl_arch(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_MIDNIGHT)
    add_header(slide, "SECTION 06", "Implementation — Slide A",
               "System Architecture & Component Dataflow",
               "Tiered modular design matching verified codebase implementations in src/.", dark_mode=True)
    add_footer(slide, 7, dark_mode=True)

    # 5 Tiered Architectural Layers (Vertical Stack)
    card_w = Inches(11.73)
    card_x = Inches(0.8)
    layer_h = Inches(0.9)
    gap = Inches(0.12)
    start_y = Inches(1.8)

    layers = [
        ("LAYER 1: CLIENT INGESTION TIER (Streamlit Multi-Page UI)",
         "Direct Text Entry (Headline & Body)  |  File Uploader (PNG, JPG, WEBP screenshots up to 10MB)  |  Sample Dispatch Selector",
         C_CYAN),
        ("LAYER 2: VISION, OCR & PREPROCESSING TIER (src/ocr.py & src/preprocessing.py)",
         "Pillow EXIF Transpose & Dynamic Scaling  |  Tesseract 5.5 OCR (OSD Rotation, Layout Segmentation)  |  Regex Wire-Service Leakage Filter",
         C_INDIGO),
        ("LAYER 3: FEATURE REPRESENTATION & CLASSIFICATION TIER (src/train.py & src/predict.py)",
         "TF-IDF Vectorizer (5,000 max features, unigrams+bigrams, sublinear TF)  |  Logistic Regression (Primary)  |  MNB  |  Linear SVM + Platt Calibration",
         C_VIOLET),
        ("LAYER 4: EXPLAINABLE AI & NEURAL EVIDENCE TIER (src/lime_explainer.py, src/shap_explainer.py, src/nli_verifier.py)",
         "LIME Monte Carlo Local Perturbation Ridge  |  SHAP Linear Shapley Decomposition (<100ms)  |  Cross-Encoder DeBERTa-v3 NLI Verifier",
         C_ROSE),
        ("LAYER 5: REINFORCEMENT LEARNING & PERSISTENCE TIER (src/evidence_bandit.py & src/database.py)",
         "UCB1 Contextual Bandit (Adaptive Search Strategy Optimization)  |  SQLite Audit Database with Automated 3-Month UTC Purge Policy",
         C_TEAL),
    ]

    for i, (title, desc, accent) in enumerate(layers):
        ly = start_y + i * (layer_h + gap)
        add_card(slide, card_x, ly, card_w, layer_h, bg_color=C_MIDNIGHT_CARD, border_color=accent, border_width=1.5)

        # Accent tab
        tab = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, card_x + Inches(0.2), ly + Inches(0.15), Inches(0.4), Inches(0.06))
        tab.fill.solid()
        tab.fill.fore_color.rgb = accent
        tab.line.fill.background()

        tb = slide.shapes.add_textbox(card_x + Inches(0.2), ly + Inches(0.25), card_w - Inches(0.4), layer_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = accent

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_WHITE
        p2.space_before = Pt(3)

        # Connector arrow
        if i < len(layers) - 1:
            arr = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, card_x + Inches(5.8), ly + layer_h + Inches(0.01), Inches(0.16), gap - Inches(0.02))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_CYAN
            arr.line.fill.background()


# =============================================================================
# SLIDE 8: SECTION 6 — IMPLEMENTATION (SLIDE B: METHODOLOGY & ALGORITHMS)
# =============================================================================
def build_slide_08_impl_method(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 06", "Implementation — Slide B",
               "Core Methodology & Algorithmic Formulations",
               "Mathematical foundations of preprocessing, feature representation, classification, and XAI.")
    add_footer(slide, 8)

    col_w = Inches(5.7)
    left_x = Inches(0.8)
    right_x = Inches(6.8)
    card_h = Inches(2.4)
    top_y1 = Inches(1.8)
    top_y2 = Inches(4.35)

    # Panel 1: Preprocessing & TF-IDF
    add_card(slide, left_x, top_y1, col_w, card_h, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    tb1 = slide.shapes.add_textbox(left_x + Inches(0.25), top_y1 + Inches(0.2), col_w - Inches(0.5), card_h - Inches(0.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_top = tf1.margin_left = tf1.margin_right = tf1.margin_bottom = 0
    p1 = tf1.paragraphs[0]
    p1.text = "1. Publisher Leakage Mitigation & TF-IDF Vectorization"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(12.5)
    p1.font.bold = True
    p1.font.color.rgb = C_INDIGO
    p1_b = tf1.add_paragraph()
    p1_b.text = (
        "• Regex Leakage Eradication: Slices out wire service patterns such as '^([A-Z\\s]{2,25})?\\s*\\(\\s*Reuters\\s*\\)\\s*[-–—:]\\s*'\n"
        "• TF-IDF Representation: Unigrams + bigrams, sublinear term-frequency scaling w = (1 + log(tf)) * log(N/df), max 5,000 features.\n"
        "• Stratified Holdout: 70% Train (N=280), 15% Validation (N=60), 15% Held-Out Test (N=60). Vocabulary strictly locked to train split."
    )
    p1_b.font.name = FONT_BODY
    p1_b.font.size = Pt(10)
    p1_b.font.color.rgb = C_TEXT_MUTED
    p1_b.space_before = Pt(4)

    # Panel 2: Calibrated Classifiers
    add_card(slide, right_x, top_y1, col_w, card_h, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    tb2 = slide.shapes.add_textbox(right_x + Inches(0.25), top_y1 + Inches(0.2), col_w - Inches(0.5), card_h - Inches(0.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_top = tf2.margin_left = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = "2. Calibrated Machine Learning Classifiers"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(12.5)
    p2.font.bold = True
    p2.font.color.rgb = C_VIOLET
    p2_b = tf2.add_paragraph()
    p2_b.text = (
        "• Logistic Regression (Selected): Binomial posterior P(y=1|x) = σ(w^T x + b) with L2 regularization (C=1.0). Direct log-odds interpretability.\n"
        "• Multinomial Naive Bayes: P(c|x) ∝ P(c) ∏ P(x_i|c) with Laplace smoothing (α=0.1).\n"
        "• Linear SVM Calibration: Raw margin distance f(x) = w^T x + b calibrated via 3-fold internal Platt Scaling (CalibratedClassifierCV) to yield true bounded probabilities."
    )
    p2_b.font.name = FONT_BODY
    p2_b.font.size = Pt(10)
    p2_b.font.color.rgb = C_TEXT_MUTED
    p2_b.space_before = Pt(4)

    # Panel 3: Dual Explainability (LIME & SHAP)
    add_card(slide, left_x, top_y2, col_w, card_h, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    tb3 = slide.shapes.add_textbox(left_x + Inches(0.25), top_y2 + Inches(0.2), col_w - Inches(0.5), card_h - Inches(0.3))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_top = tf3.margin_left = tf3.margin_right = tf3.margin_bottom = 0
    p3 = tf3.paragraphs[0]
    p3.text = "3. Dual Explainable AI Engines (LIME & SHAP)"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(12.5)
    p3.font.bold = True
    p3.font.color.rgb = C_CYAN
    p3_b = tf3.add_paragraph()
    p3_b.text = (
        "• LIME: Local surrogate ridge regression fitted over Monte Carlo text perturbations: argmin_g L(f,g,π_x) + Ω(g).\n"
        "• SHAP: Game-theoretic Shapley attributions computed via linear log-odds decomposition: φ_i = w_i * (x_i - E[x_i]). Computes in <100ms.\n"
        "• Empirical Agreement: 100% directional sign concordance on intersecting tokens; high causal faithfulness verified via token masking."
    )
    p3_b.font.name = FONT_BODY
    p3_b.font.size = Pt(10)
    p3_b.font.color.rgb = C_TEXT_MUTED
    p3_b.space_before = Pt(4)

    # Panel 4: NLI & Contextual RL Bandit
    add_card(slide, right_x, top_y2, col_w, card_h, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    tb4 = slide.shapes.add_textbox(right_x + Inches(0.25), top_y2 + Inches(0.2), col_w - Inches(0.5), card_h - Inches(0.3))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    tf4.margin_top = tf4.margin_left = tf4.margin_right = tf4.margin_bottom = 0
    p4 = tf4.paragraphs[0]
    p4.text = "4. Neural NLI Claim Verification & RL Bandit"
    p4.font.name = FONT_HEADING
    p4.font.size = Pt(12.5)
    p4.font.bold = True
    p4.font.color.rgb = C_TEAL
    p4_b = tf4.add_paragraph()
    p4_b.text = (
        "• Cross-Encoder NLI: cross-encoder/nli-deberta-v3-base evaluates (Premise, Hypothesis) pairs into Entailment, Contradiction, Neutral.\n"
        "• Multi-Armed Bandit: UCB1 policy A_t = argmax_a [Q_t(a) + c * sqrt(ln(t)/N_t(a))] selecting between retrieval search strategies.\n"
        "• Non-Circular Reward: R = 0.50 S_rel + 0.30 E_cov + 0.20 M_nli rewarding relevance, grounding, and informativeness without confirmation bias."
    )
    p4_b.font.name = FONT_BODY
    p4_b.font.size = Pt(10)
    p4_b.font.color.rgb = C_TEXT_MUTED
    p4_b.space_before = Pt(4)


# =============================================================================
# SLIDE 9: SECTION 6 — IMPLEMENTATION (SLIDE C: COMPARISON & CONCEPTUAL XAI)
# =============================================================================
def build_slide_09_impl_xai_comparison(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_MIDNIGHT)
    add_header(slide, "SECTION 06", "Implementation — Slide C",
               "The Tripartite Verification Paradigm & Feature Attribution",
               "Differentiating statistical classification, evidence corroboration, and local explainability.", dark_mode=True)
    add_footer(slide, 9, dark_mode=True)

    # 3 Comparative Pillars (Top Row)
    pillar_w = Inches(3.75)
    pillar_h = Inches(2.35)
    gap = Inches(0.24)
    start_x = Inches(0.8)
    top_y = Inches(1.8)

    pillars = [
        ("STATISTICAL CLASSIFICATION",
         "Stylometric Pattern Matching",
         "• Predicts label from linguistic distributions learned during training.\n"
         "• High latency efficiency (<5ms inference).\n"
         "• Crucial Limitation: Measures stylistic resemblance, not factual veracity. Cannot detect well-written false claims.",
         C_INDIGO),
        ("EVIDENCE CORROBORATION",
         "Neural Cross-Encoder NLI",
         "• Compares headline hypothesis against audited premise evidence.\n"
         "• Categorizes into Entailment, Contradiction, or Insufficient Evidence.\n"
         "• Crucial Strength: Verifies real-world facts regardless of persuasive syntax.",
         C_TEAL),
        ("MODEL EXPLAINABILITY",
         "LIME & SHAP Feature Attributions",
         "• Decomposes predictions into token-level positive and negative weights.\n"
         "• LIME generates local perturbations; SHAP calculates exact Shapley values.\n"
         "• Crucial Strength: Eliminates black-box opacity; validates causal faithfulness.",
         C_VIOLET),
    ]

    for i, (tag, title, body, color) in enumerate(pillars):
        px = start_x + i * (pillar_w + gap)
        add_card(slide, px, top_y, pillar_w, pillar_h, bg_color=C_MIDNIGHT_CARD, border_color=color, border_width=1.5)

        tb = slide.shapes.add_textbox(px + Inches(0.2), top_y + Inches(0.18), pillar_w - Inches(0.4), pillar_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = tag
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = body
        p3.font.name = FONT_BODY
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = C_TEXT_SLATE
        p3.space_before = Pt(4)

    # Bottom Container: Conceptual Feature Explanation Demonstration
    bot_y = Inches(4.35)
    bot_w = Inches(11.73)
    bot_h = Inches(2.45)
    add_card(slide, start_x, bot_y, bot_w, bot_h, bg_color=C_MIDNIGHT_CARD, border_color=C_BORDER_DARK, border_width=1)

    tb_demo_hdr = slide.shapes.add_textbox(start_x + Inches(0.3), bot_y + Inches(0.18), bot_w - Inches(0.6), Inches(0.35))
    tf_dh = tb_demo_hdr.text_frame
    tf_dh.margin_top = tf_dh.margin_left = tf_dh.margin_right = tf_dh.margin_bottom = 0
    pdh = tf_dh.paragraphs[0]
    pdh.text = "CONCEPTUAL FEATURE ATTRIBUTION VISUALIZATION (Sample Dispatch Inspection)"
    pdh.font.name = FONT_HEADING
    pdh.font.size = Pt(11)
    pdh.font.bold = True
    pdh.font.color.rgb = C_CYAN

    # Sample Headline Box
    headline_card = add_card(slide, start_x + Inches(0.3), bot_y + Inches(0.55), bot_w - Inches(0.6), Inches(0.45),
                             bg_color=RGBColor(16, 22, 47), border_color=C_BORDER_DARK, border_width=1)
    tb_hl = slide.shapes.add_textbox(start_x + Inches(0.45), bot_y + Inches(0.62), bot_w - Inches(0.9), Inches(0.35))
    tf_hl = tb_hl.text_frame
    tf_hl.margin_top = tf_hl.margin_left = tf_hl.margin_right = tf_hl.margin_bottom = 0
    phl = tf_hl.paragraphs[0]
    r_h1 = phl.add_run()
    r_h1.text = "Analyzed Headline: "
    r_h1.font.name = FONT_HEADING
    r_h1.font.size = Pt(10.5)
    r_h1.font.bold = True
    r_h1.font.color.rgb = C_TEXT_SLATE
    r_h2 = phl.add_run()
    r_h2.text = "\"Federal Reserve Signals Emergency Interest Rate Overhaul Amid Unprecedented Economic Shock\""
    r_h2.font.name = FONT_BODY
    r_h2.font.size = Pt(10.5)
    r_h2.font.bold = True
    r_h2.font.color.rgb = C_WHITE

    # Token Attribution Demonstration Bars (Left: Likely Fake Indicators; Right: Likely Real Indicators)
    tb_fake_tok = slide.shapes.add_textbox(start_x + Inches(0.4), bot_y + Inches(1.1), Inches(5.3), Inches(1.2))
    tf_ft = tb_fake_tok.text_frame
    tf_ft.word_wrap = True
    tf_ft.margin_top = tf_ft.margin_left = tf_ft.margin_right = tf_ft.margin_bottom = 0
    pft = tf_ft.paragraphs[0]
    pft.text = "Tokens Pushing Toward Likely Fake (+Weight):"
    pft.font.name = FONT_HEADING
    pft.font.size = Pt(10.5)
    pft.font.bold = True
    pft.font.color.rgb = C_ROSE

    fake_tokens = [("unprecedented", "+0.384"), ("emergency", "+0.312"), ("shock", "+0.245")]
    for tok, wt in fake_tokens:
        p = tf_ft.add_paragraph()
        p.text = f"  •  \"{tok}\"  (Weight: {wt}) — Sensationalist booster token common in unverified text"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_SLATE
        p.space_before = Pt(2)

    tb_real_tok = slide.shapes.add_textbox(start_x + Inches(6.0), bot_y + Inches(1.1), Inches(5.3), Inches(1.2))
    tf_rt = tb_real_tok.text_frame
    tf_rt.word_wrap = True
    tf_rt.margin_top = tf_rt.margin_left = tf_rt.margin_right = tf_rt.margin_bottom = 0
    prt = tf_rt.paragraphs[0]
    prt.text = "Tokens Pushing Toward Likely Real (-Weight):"
    prt.font.name = FONT_HEADING
    prt.font.size = Pt(10.5)
    prt.font.bold = True
    prt.font.color.rgb = C_TEAL

    real_tokens = [("federal reserve", "-0.415"), ("interest rate", "-0.362"), ("signals", "-0.198")]
    for tok, wt in real_tokens:
        p = tf_rt.add_paragraph()
        p.text = f"  •  \"{tok}\"  (Weight: {wt}) — Institutional policy terminology aligned with verified wire dispatches"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_SLATE
        p.space_before = Pt(2)


# =============================================================================
# SLIDE 10: SECTION 7 — OUTPUT SCREENSHOTS (PART 1: DASHBOARD & TEXT ANALYZER)
# =============================================================================
def build_slide_10_screenshots_p1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 07", "Output Screenshots",
               "Application Interface — Executive Dashboard & News Analyzer",
               "Dedicated replaceable image placeholders for primary editorial workspace interfaces.")
    add_footer(slide, 10)

    col_w = Inches(5.7)
    left_x = Inches(0.8)
    right_x = Inches(6.8)
    top_y = Inches(1.8)
    height = Inches(5.0)

    # Frame 1: Dashboard
    add_card(slide, left_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_f1_hdr = slide.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(0.2), col_w - Inches(0.6), Inches(0.35))
    tf_f1h = tb_f1_hdr.text_frame
    tf_f1h.margin_top = tf_f1h.margin_left = tf_f1h.margin_right = tf_f1h.margin_bottom = 0
    pf1h = tf_f1h.paragraphs[0]
    pf1h.text = "Executive Dashboard & Analytics"
    pf1h.font.name = FONT_HEADING
    pf1h.font.size = Pt(13)
    pf1h.font.bold = True
    pf1h.font.color.rgb = C_INDIGO

    # Viewport Placeholder Box (Replaceable in PowerPoint)
    vp1 = add_card(slide, left_x + Inches(0.3), top_y + Inches(0.6), col_w - Inches(0.6), Inches(2.7),
                   bg_color=RGBColor(241, 245, 249), border_color=C_BORDER_LIGHT, border_width=1.5)
    tb_vp1 = slide.shapes.add_textbox(left_x + Inches(0.5), top_y + Inches(1.5), col_w - Inches(1.0), Inches(0.9))
    tf_vp1 = tb_vp1.text_frame
    tf_vp1.word_wrap = True
    tf_vp1.margin_top = tf_vp1.margin_left = tf_vp1.margin_right = tf_vp1.margin_bottom = 0
    pv1 = tf_vp1.paragraphs[0]
    pv1.alignment = PP_ALIGN.CENTER
    pv1.text = "[INSERT ACTUAL DASHBOARD SCREENSHOT]"
    pv1.font.name = FONT_HEADING
    pv1.font.size = Pt(13)
    pv1.font.bold = True
    pv1.font.color.rgb = C_INDIGO

    pv1_sub = tf_vp1.add_paragraph()
    pv1_sub.alignment = PP_ALIGN.CENTER
    pv1_sub.text = "Click shape or right-click 'Change Picture' in PowerPoint to insert actual UI capture"
    pv1_sub.font.name = FONT_BODY
    pv1_sub.font.size = Pt(9.5)
    pv1_sub.font.color.rgb = C_TEXT_MUTED
    pv1_sub.space_before = Pt(4)

    # Caption & Key Capabilities Callout
    tb_c1 = slide.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(3.4), col_w - Inches(0.6), Inches(1.4))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_top = tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_bottom = 0
    pc1_title = tf_c1.paragraphs[0]
    pc1_title.text = "Figure 7.1: VeriScope AI Executive Dashboard"
    pc1_title.font.name = FONT_HEADING
    pc1_title.font.size = Pt(11)
    pc1_title.font.bold = True
    pc1_title.font.color.rgb = C_TEXT_DARK

    pc1_body = tf_c1.add_paragraph()
    pc1_body.text = (
        "• Displays high-level verification KPI metrics: Total Analyzed, Flagged Fake, and Mean Confidence.\n"
        "• Real-time velocity tracking chart illustrating verification throughput across recent sessions.\n"
        "• System health indicators confirming model pipeline readiness, database connectivity, and OCR status."
    )
    pc1_body.font.name = FONT_BODY
    pc1_body.font.size = Pt(9.5)
    pc1_body.font.color.rgb = C_TEXT_MUTED
    pc1_body.space_before = Pt(3)

    # Frame 2: News Analyzer
    add_card(slide, right_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_f2_hdr = slide.shapes.add_textbox(right_x + Inches(0.3), top_y + Inches(0.2), col_w - Inches(0.6), Inches(0.35))
    tf_f2h = tb_f2_hdr.text_frame
    tf_f2h.margin_top = tf_f2h.margin_left = tf_f2h.margin_right = tf_f2h.margin_bottom = 0
    pf2h = tf_f2h.paragraphs[0]
    pf2h.text = "News Analyzer Workspace"
    pf2h.font.name = FONT_HEADING
    pf2h.font.size = Pt(13)
    pf2h.font.bold = True
    pf2h.font.color.rgb = C_VIOLET

    # Viewport Placeholder Box (Replaceable in PowerPoint)
    vp2 = add_card(slide, right_x + Inches(0.3), top_y + Inches(0.6), col_w - Inches(0.6), Inches(2.7),
                   bg_color=RGBColor(241, 245, 249), border_color=C_BORDER_LIGHT, border_width=1.5)
    tb_vp2 = slide.shapes.add_textbox(right_x + Inches(0.5), top_y + Inches(1.5), col_w - Inches(1.0), Inches(0.9))
    tf_vp2 = tb_vp2.text_frame
    tf_vp2.word_wrap = True
    tf_vp2.margin_top = tf_vp2.margin_left = tf_vp2.margin_right = tf_vp2.margin_bottom = 0
    pv2 = tf_vp2.paragraphs[0]
    pv2.alignment = PP_ALIGN.CENTER
    pv2.text = "[INSERT ACTUAL TEXT ANALYSIS SCREENSHOT]"
    pv2.font.name = FONT_HEADING
    pv2.font.size = Pt(13)
    pv2.font.bold = True
    pv2.font.color.rgb = C_VIOLET

    pv2_sub = tf_vp2.add_paragraph()
    pv2_sub.alignment = PP_ALIGN.CENTER
    pv2_sub.text = "Click shape or right-click 'Change Picture' in PowerPoint to insert actual UI capture"
    pv2_sub.font.name = FONT_BODY
    pv2_sub.font.size = Pt(9.5)
    pv2_sub.font.color.rgb = C_TEXT_MUTED
    pv2_sub.space_before = Pt(4)

    # Caption & Key Capabilities Callout
    tb_c2 = slide.shapes.add_textbox(right_x + Inches(0.3), top_y + Inches(3.4), col_w - Inches(0.6), Inches(1.4))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_top = tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_bottom = 0
    pc2_title = tf_c2.paragraphs[0]
    pc2_title.text = "Figure 7.2: News Analyzer Workspace Interface"
    pc2_title.font.name = FONT_HEADING
    pc2_title.font.size = Pt(11)
    pc2_title.font.bold = True
    pc2_title.font.color.rgb = C_TEXT_DARK

    pc2_body = tf_c2.add_paragraph()
    pc2_body.text = (
        "• Dual input fields: Dedicated text areas for News Headline and Article Context with live counters.\n"
        "• Pre-analysis publisher leakage notification alerting users when wire metadata is sanitized.\n"
        "• Immediate calibrated prediction badge (Likely Real vs Likely Fake) and posterior probability gauge."
    )
    pc2_body.font.name = FONT_BODY
    pc2_body.font.size = Pt(9.5)
    pc2_body.font.color.rgb = C_TEXT_MUTED
    pc2_body.space_before = Pt(3)


# =============================================================================
# SLIDE 11: SECTION 7 — OUTPUT SCREENSHOTS (PART 2: OCR & EXPLAINABLE AI LAB)
# =============================================================================
def build_slide_11_screenshots_p2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 07", "Output Screenshots",
               "Multimodal OCR Extraction & Explainable AI Lab",
               "Dedicated replaceable image placeholders for vision pipelines and model interpretability dashboards.")
    add_footer(slide, 11)

    col_w = Inches(5.7)
    left_x = Inches(0.8)
    right_x = Inches(6.8)
    top_y = Inches(1.8)
    height = Inches(5.0)

    # Frame 3: OCR Pipeline
    add_card(slide, left_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_f3_hdr = slide.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(0.2), col_w - Inches(0.6), Inches(0.35))
    tf_f3h = tb_f3_hdr.text_frame
    tf_f3h.margin_top = tf_f3h.margin_left = tf_f3h.margin_right = tf_f3h.margin_bottom = 0
    pf3h = tf_f3h.paragraphs[0]
    pf3h.text = "Tesseract 5.5 OCR Screenshot Ingestion"
    pf3h.font.name = FONT_HEADING
    pf3h.font.size = Pt(13)
    pf3h.font.bold = True
    pf3h.font.color.rgb = C_AMBER

    # Viewport Placeholder Box (Replaceable in PowerPoint)
    vp3 = add_card(slide, left_x + Inches(0.3), top_y + Inches(0.6), col_w - Inches(0.6), Inches(2.7),
                   bg_color=RGBColor(241, 245, 249), border_color=C_BORDER_LIGHT, border_width=1.5)
    tb_vp3 = slide.shapes.add_textbox(left_x + Inches(0.5), top_y + Inches(1.5), col_w - Inches(1.0), Inches(0.9))
    tf_vp3 = tb_vp3.text_frame
    tf_vp3.word_wrap = True
    tf_vp3.margin_top = tf_vp3.margin_left = tf_vp3.margin_right = tf_vp3.margin_bottom = 0
    pv3 = tf_vp3.paragraphs[0]
    pv3.alignment = PP_ALIGN.CENTER
    pv3.text = "[INSERT ACTUAL IMAGE/OCR SCREENSHOT]"
    pv3.font.name = FONT_HEADING
    pv3.font.size = Pt(13)
    pv3.font.bold = True
    pv3.font.color.rgb = C_AMBER

    pv3_sub = tf_vp3.add_paragraph()
    pv3_sub.alignment = PP_ALIGN.CENTER
    pv3_sub.text = "Click shape or right-click 'Change Picture' in PowerPoint to insert actual UI capture"
    pv3_sub.font.name = FONT_BODY
    pv3_sub.font.size = Pt(9.5)
    pv3_sub.font.color.rgb = C_TEXT_MUTED
    pv3_sub.space_before = Pt(4)

    # Caption & Key Capabilities Callout
    tb_c3 = slide.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(3.4), col_w - Inches(0.6), Inches(1.4))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_top = tf_c3.margin_left = tf_c3.margin_right = tf_c3.margin_bottom = 0
    pc3_title = tf_c3.paragraphs[0]
    pc3_title.text = "Figure 7.3: Image OCR Ingestion Pipeline"
    pc3_title.font.name = FONT_HEADING
    pc3_title.font.size = Pt(11)
    pc3_title.font.bold = True
    pc3_title.font.color.rgb = C_TEXT_DARK

    pc3_body = tf_c3.add_paragraph()
    pc3_body.text = (
        "• Drag-and-drop file uploader accepting PNG, JPG, JPEG, and WEBP formats up to 10MB.\n"
        "• Image preview with automatic EXIF orientation correction and adaptive contrast thresholding.\n"
        "• Automatic heuristic parsing separating candidate headline from body text, editable before analysis."
    )
    pc3_body.font.name = FONT_BODY
    pc3_body.font.size = Pt(9.5)
    pc3_body.font.color.rgb = C_TEXT_MUTED
    pc3_body.space_before = Pt(3)

    # Frame 4: Explainable AI Lab
    add_card(slide, right_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_f4_hdr = slide.shapes.add_textbox(right_x + Inches(0.3), top_y + Inches(0.2), col_w - Inches(0.6), Inches(0.35))
    tf_f4h = tb_f4_hdr.text_frame
    tf_f4h.margin_top = tf_f4h.margin_left = tf_f4h.margin_right = tf_f4h.margin_bottom = 0
    pf4h = tf_f4h.paragraphs[0]
    pf4h.text = "Explainable AI Lab & Evidence Verification"
    pf4h.font.name = FONT_HEADING
    pf4h.font.size = Pt(13)
    pf4h.font.bold = True
    pf4h.font.color.rgb = C_TEAL

    # Viewport Placeholder Box (Replaceable in PowerPoint)
    vp4 = add_card(slide, right_x + Inches(0.3), top_y + Inches(0.6), col_w - Inches(0.6), Inches(2.7),
                   bg_color=RGBColor(241, 245, 249), border_color=C_BORDER_LIGHT, border_width=1.5)
    tb_vp4 = slide.shapes.add_textbox(right_x + Inches(0.5), top_y + Inches(1.5), col_w - Inches(1.0), Inches(0.9))
    tf_vp4 = tb_vp4.text_frame
    tf_vp4.word_wrap = True
    tf_vp4.margin_top = tf_vp4.margin_left = tf_vp4.margin_right = tf_vp4.margin_bottom = 0
    pv4 = tf_vp4.paragraphs[0]
    pv4.alignment = PP_ALIGN.CENTER
    pv4.text = "[INSERT ACTUAL EXPLANATION OR EVIDENCE SCREENSHOT]"
    pv4.font.name = FONT_HEADING
    pv4.font.size = Pt(12)
    pv4.font.bold = True
    pv4.font.color.rgb = C_TEAL

    pv4_sub = tf_vp4.add_paragraph()
    pv4_sub.alignment = PP_ALIGN.CENTER
    pv4_sub.text = "Click shape or right-click 'Change Picture' in PowerPoint to insert actual UI capture"
    pv4_sub.font.name = FONT_BODY
    pv4_sub.font.size = Pt(9.5)
    pv4_sub.font.color.rgb = C_TEXT_MUTED
    pv4_sub.space_before = Pt(4)

    # Caption & Key Capabilities Callout
    tb_c4 = slide.shapes.add_textbox(right_x + Inches(0.3), top_y + Inches(3.4), col_w - Inches(0.6), Inches(1.4))
    tf_c4 = tb_c4.text_frame
    tf_c4.word_wrap = True
    tf_c4.margin_top = tf_c4.margin_left = tf_c4.margin_right = tf_c4.margin_bottom = 0
    pc4_title = tf_c4.paragraphs[0]
    pc4_title.text = "Figure 7.4: Explainable AI Lab & NLI Engine"
    pc4_title.font.name = FONT_HEADING
    pc4_title.font.size = Pt(11)
    pc4_title.font.bold = True
    pc4_title.font.color.rgb = C_TEXT_DARK

    pc4_body = tf_c4.add_paragraph()
    pc4_body.text = (
        "• Dual side-by-side horizontal bar charts comparing LIME and SHAP token feature attributions.\n"
        "• Quantitative agreement metrics: Top-5 Jaccard overlap and Directional Sign Concordance (100%).\n"
        "• Cross-encoder NLI evidence panel displaying entailment verdicts and decisive margin metrics."
    )
    pc4_body.font.name = FONT_BODY
    pc4_body.font.size = Pt(9.5)
    pc4_body.font.color.rgb = C_TEXT_MUTED
    pc4_body.space_before = Pt(3)


# =============================================================================
# SLIDE 12: SECTION 8 — CONCLUSION
# =============================================================================
def build_slide_12_conclusion(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_MIDNIGHT)
    add_header(slide, "SECTION 08", "Conclusion",
               "Key Contributions & Responsible AI Governance",
               "Synthesizing academic outcomes, engineering deliverables, and ethical limitations.", dark_mode=True)
    add_footer(slide, 12, dark_mode=True)

    # 3 Major Contribution Cards
    card_w = Inches(3.75)
    card_h = Inches(3.6)
    gap = Inches(0.24)
    start_x = Inches(0.8)
    top_y = Inches(1.8)

    cards = [
        ("ENGINEERING ACCOMPLISHMENTS",
         "Modular Multimodal Pipeline",
         "• Successfully developed an integrated, locally executable verification suite combining NLP, Computer Vision, XAI, and Reinforcement Learning.\n"
         "• Eradicated the critical Publisher Leakage flaw prevalent in academic fake news benchmarks.\n"
         "• Delivered calibrated linear models (Logistic Regression, MNB, Linear SVM + Platt Scaling) with sub-100ms inference.",
         C_CYAN),
        ("EXPLAINABILITY RESEARCH",
         "Dual XAI & Empirical Faithfulness",
         "• Validated dual local explanations: LIME and SHAP demonstrated 100% directional sign concordance on shared features.\n"
         "• Proved causal faithfulness: masking top-5 tokens dropped prediction confidence by 35–50 percentage points vs <2% for random tokens.\n"
         "• Deployed an objective contextual bandit optimizing evidence retrieval without circular confirmation bias.",
         C_VIOLET),
        ("RESPONSIBLE GOVERNANCE",
         "Epistemic Modesty & Privacy",
         "• Established that classification labels are decision aids, not definitive evidence of real-world factual truth.\n"
         "• Integrated cross-encoder NLI to ground claims against audited reference evidence archives.\n"
         "• Automated 3-calendar-month UTC data retention in SQLite, upholding strict privacy governance and zero fabricated confidence.",
         C_TEAL),
    ]

    for i, (tag, title, body, color) in enumerate(cards):
        px = start_x + i * (card_w + gap)
        add_card(slide, px, top_y, card_w, card_h, bg_color=C_MIDNIGHT_CARD, border_color=color, border_width=1.5)

        tb = slide.shapes.add_textbox(px + Inches(0.2), top_y + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = tag
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        p3.text = body
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10)
        p3.font.color.rgb = C_TEXT_SLATE
        p3.space_before = Pt(6)

    # Bottom Closing Impact Banner
    banner_y = Inches(5.6)
    banner_w = Inches(11.73)
    banner_h = Inches(1.15)
    add_card(slide, start_x, banner_y, banner_w, banner_h, bg_color=RGBColor(24, 34, 70), border_color=C_INDIGO, border_width=1.5)

    tb_ban = slide.shapes.add_textbox(start_x + Inches(0.35), banner_y + Inches(0.18), banner_w - Inches(0.7), banner_h - Inches(0.3))
    tf_b = tb_ban.text_frame
    tf_b.word_wrap = True
    tf_b.margin_top = tf_b.margin_left = tf_b.margin_right = tf_b.margin_bottom = 0

    p_b1 = tf_b.paragraphs[0]
    p_b1.text = "CORE PROJECT PHILOSOPHY: INTELLIGENCE BEYOND THE HEADLINE"
    p_b1.font.name = FONT_HEADING
    p_b1.font.size = Pt(11)
    p_b1.font.bold = True
    p_b1.font.color.rgb = C_CYAN

    p_b2 = tf_b.add_paragraph()
    p_b2.text = (
        "VeriScope AI demonstrates that the future of computational journalism and AI verification lies not in larger opaque models, "
        "but in transparent, interpretable, and evidence-grounded systems that respect epistemic boundaries and empower human editorial judgment."
    )
    p_b2.font.name = FONT_BODY
    p_b2.font.size = Pt(10.5)
    p_b2.font.bold = True
    p_b2.font.color.rgb = C_WHITE
    p_b2.space_before = Pt(3)


# =============================================================================
# SLIDE 13: SECTION 9 — FUTURE SCOPE
# =============================================================================
def build_slide_13_future_scope(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 09", "Future Scope",
               "Strategic Roadmap & Future Research Directions",
               "Four-phase evolution extending multimodal reasoning, dynamic fact-checking, and federated learning.")
    add_footer(slide, 13)

    # 4 Sequential Roadmap Cards
    card_w = Inches(2.78)
    card_h = Inches(4.7)
    gap = Inches(0.2)
    start_x = Inches(0.8)
    top_y = Inches(1.8)

    phases = [
        ("PHASE 1", "Multimodal Fusion & Multilingual NLP",
         "• Joint Vision-Language Transformers: Implement cross-attention models (e.g. CLIP / Flamingo) to detect discrepancies between news text and image captions.\n"
         "• Multilingual Support: Expand preprocessing and vectorization pipelines to audit regional Indian language dispatches (Hindi, Tamil, Bengali).\n"
         "• Robust OCR Enhancements: Integrate deep scene-text models (CRAFT / PaddleOCR) for low-resolution social media compression artifacts.",
         C_INDIGO),
        ("PHASE 2", "Live Fact-Checking & Knowledge Graph RAG",
         "• Dynamic Fact-Checking APIs: Connect directly to ClaimReview schema feeds and Google Fact Check Tools API for real-time claim retrieval.\n"
         "• Graph Neural Networks (GNNs): Construct entity-relation knowledge graphs to evaluate multi-hop claim consistency.\n"
         "• Distributed Vector Storage: Deploy scalable vector search indexes (FAISS / Milvus) over millions of verified historical records.",
         C_VIOLET),
        ("PHASE 3", "Bayesian Uncertainty & Active Learning",
         "• Rigorous Uncertainty Estimation: Implement Conformal Prediction and Monte Carlo Dropout to produce mathematically guaranteed prediction confidence sets.\n"
         "• Active Human-in-the-Loop: Allow editorial corrections from fact-checkers to trigger automated continuous model fine-tuning.\n"
         "• Causal Explanation Pruning: Develop automated counterfactual explanation generators highlighting minimal edits required to flip predictions.",
         C_AMBER),
        ("PHASE 4", "Decentralized Audits & Privacy Governance",
         "• Decentralized Provenance: Leverage tamper-evident cryptographic ledgers and Zero-Knowledge Proofs (ZKPs) for audit trail authenticity.\n"
         "• Federated Learning: Enable collaborative multi-newsroom model updates without aggregating sensitive investigative reporting data.\n"
         "• Real-Time Drift Monitoring: Deploy automated population stability index (PSI) tracking to detect concept drift in election news cycles.",
         C_TEAL),
    ]

    for i, (phase, title, body, color) in enumerate(phases):
        px = start_x + i * (card_w + gap)
        add_card(slide, px, top_y, card_w, card_h, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

        # Phase pill badge
        p_badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px + Inches(0.2), top_y + Inches(0.2), Inches(1.0), Inches(0.3))
        p_badge.fill.solid()
        p_badge.fill.fore_color.rgb = C_ICE_BLUE
        p_badge.line.color.rgb = color
        p_badge.line.width = Pt(1)
        tb_pb = slide.shapes.add_textbox(px + Inches(0.2), top_y + Inches(0.22), Inches(1.0), Inches(0.3))
        tf_pb = tb_pb.text_frame
        tf_pb.margin_top = tf_pb.margin_left = tf_pb.margin_right = tf_pb.margin_bottom = 0
        ppb = tf_pb.paragraphs[0]
        ppb.alignment = PP_ALIGN.CENTER
        ppb.text = phase
        ppb.font.name = FONT_HEADING
        ppb.font.size = Pt(9.5)
        ppb.font.bold = True
        ppb.font.color.rgb = color

        # Title & Body
        tb = slide.shapes.add_textbox(px + Inches(0.2), top_y + Inches(0.65), card_w - Inches(0.4), card_h - Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_DARK

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(6)

        # Connector arrow to next phase
        if i < len(phases) - 1:
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, px + card_w + Inches(0.04), top_y + Inches(2.2), Inches(0.12), Inches(0.2))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_BORDER_LIGHT
            arr.line.fill.background()


# =============================================================================
# SLIDE 14: SECTION 10 — REFERENCES
# =============================================================================
def build_slide_14_references(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, C_CANVAS_BG)
    add_header(slide, "SECTION 10", "References",
               "Academic Research & Technical Literature",
               "Authoritative publications and open-source frameworks underpinning the project implementation.")
    add_footer(slide, 14)

    col_w = Inches(5.7)
    left_x = Inches(0.8)
    right_x = Inches(6.8)
    top_y = Inches(1.8)
    height = Inches(5.0)

    # Left Container: Academic Research Papers
    add_card(slide, left_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_left_hdr = slide.shapes.add_textbox(left_x + Inches(0.3), top_y + Inches(0.25), col_w - Inches(0.6), Inches(0.35))
    tf_lh = tb_left_hdr.text_frame
    tf_lh.margin_top = tf_lh.margin_left = tf_lh.margin_right = tf_lh.margin_bottom = 0
    plh = tf_lh.paragraphs[0]
    plh.text = "ACADEMIC RESEARCH PUBLICATIONS"
    plh.font.name = FONT_HEADING
    plh.font.size = Pt(13)
    plh.font.bold = True
    plh.font.color.rgb = C_INDIGO

    academic_refs = [
        ("Ribeiro, M. T., Singh, S., & Guestrin, C. (2016).",
         "\"Why Should I Trust You?\": Explaining the Predictions of Any Classifier.",
         "ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16), pp. 1135–1144."),
        ("Lundberg, S. M., & Lee, S.-I. (2017).",
         "A Unified Approach to Interpreting Model Predictions.",
         "Advances in Neural Information Processing Systems (NeurIPS 30), pp. 4765–4774."),
        ("He, P., Gao, J., & Chen, W. (2021).",
         "DeBERTaV3: Improving DeBERTa using ELECTRA-style Pre-Training with Gradient-Disentangled Embedding.",
         "arXiv preprint arXiv:2111.09543."),
        ("Ahmed, H., Traore, I., & Saad, S. (2017).",
         "Detection of Online Fake News Using N-Gram Analysis and Machine Learning Techniques.",
         "Intelligent, Secure, and Dependable Systems in Distributed Infrastructure, pp. 127–138. (ISOT Dataset Provenance)."),
        ("Sutton, R. S., & Barto, A. G. (2018).",
         "Reinforcement Learning: An Introduction (2nd ed.).",
         "The MIT Press, Cambridge, MA. (Theoretical basis for UCB1 Multi-Armed Bandit)."),
    ]

    ref_y = top_y + Inches(0.65)
    for authors, title, venue in academic_refs:
        tb_r = slide.shapes.add_textbox(left_x + Inches(0.3), ref_y, col_w - Inches(0.6), Inches(0.75))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        tf_r.margin_top = tf_r.margin_left = tf_r.margin_right = tf_r.margin_bottom = 0

        p1 = tf_r.paragraphs[0]
        r1 = p1.add_run()
        r1.text = authors + " "
        r1.font.name = FONT_HEADING
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_TEXT_DARK

        r2 = p1.add_run()
        r2.text = title + " "
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.5)
        r2.font.italic = True
        r2.font.color.rgb = C_INDIGO

        r3 = p1.add_run()
        r3.text = venue
        r3.font.name = FONT_BODY
        r3.font.size = Pt(9)
        r3.font.color.rgb = C_TEXT_MUTED

        ref_y += Inches(0.82)

    # Right Container: Frameworks & Technical Documentation
    add_card(slide, right_x, top_y, col_w, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT)

    tb_right_hdr = slide.shapes.add_textbox(right_x + Inches(0.3), top_y + Inches(0.25), col_w - Inches(0.6), Inches(0.35))
    tf_rh = tb_right_hdr.text_frame
    tf_rh.margin_top = tf_rh.margin_left = tf_rh.margin_right = tf_rh.margin_bottom = 0
    prh = tf_rh.paragraphs[0]
    prh.text = "TECHNICAL FRAMEWORKS & SYSTEM SPECIFICATIONS"
    prh.font.name = FONT_HEADING
    prh.font.size = Pt(13)
    prh.font.bold = True
    prh.font.color.rgb = C_VIOLET

    tech_refs = [
        ("Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011).",
         "Scikit-learn: Machine Learning in Python.",
         "Journal of Machine Learning Research (JMLR), 12, pp. 2825–2830."),
        ("Smith, R. (2007).",
         "An Overview of the Tesseract OCR Engine.",
         "Ninth International Conference on Document Analysis and Recognition (ICDAR 2007), IEEE, pp. 629–633."),
        ("Wolf, T., Debut, L., Sanh, V., et al. (2020).",
         "Transformers: State-of-the-Art Natural Language Processing.",
         "Proceedings of the 2020 EMNLP System Demonstrations, pp. 38–45."),
        ("Streamlit Inc. (2024).",
         "Streamlit Documentation: The Fastest Way to Build Data Applications.",
         "Official API Reference & Architecture Guide, https://streamlit.io."),
        ("Hipp, R. (2024).",
         "SQLite Database Engine: Transactional, Serverless Embedded SQL Database.",
         "Official Documentation & Architecture Reference, https://sqlite.org."),
    ]

    tref_y = top_y + Inches(0.65)
    for authors, title, venue in tech_refs:
        tb_r = slide.shapes.add_textbox(right_x + Inches(0.3), tref_y, col_w - Inches(0.6), Inches(0.75))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        tf_r.margin_top = tf_r.margin_left = tf_r.margin_right = tf_r.margin_bottom = 0

        p1 = tf_r.paragraphs[0]
        r1 = p1.add_run()
        r1.text = authors + " "
        r1.font.name = FONT_HEADING
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = C_TEXT_DARK

        r2 = p1.add_run()
        r2.text = title + " "
        r2.font.name = FONT_BODY
        r2.font.size = Pt(9.5)
        r2.font.italic = True
        r2.font.color.rgb = C_VIOLET

        r3 = p1.add_run()
        r3.text = venue
        r3.font.name = FONT_BODY
        r3.font.size = Pt(9)
        r3.font.color.rgb = C_TEXT_MUTED

        tref_y += Inches(0.82)


# =============================================================================
# MAIN ORCHESTRATION FUNCTION
# =============================================================================
def main():
    print("=" * 70)
    print("VeriScope AI — Integrated Project PowerPoint Generator")
    print("=" * 70)

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "VeriScope_AI_Integrated_Project_Presentation.pptx"

    prs = create_base_deck()

    print("[1/14] Building Slide 1: Section 1 — Title Slide...")
    build_slide_01_title(prs)

    print("[2/14] Building Slide 2: Section 2 — Introduction of the Project...")
    build_slide_02_intro(prs)

    print("[3/14] Building Slide 3: Section 3 — Abstract...")
    build_slide_03_abstract(prs)

    print("[4/14] Building Slide 4: Section 4 — Intro in Points (Problem & Objectives)...")
    build_slide_04_intro_points_p1(prs)

    print("[5/14] Building Slide 5: Section 4 — Intro in Points (Workflow & Users)...")
    build_slide_05_intro_points_p2(prs)

    print("[6/14] Building Slide 6: Section 5 — Software & Hardware Configuration...")
    build_slide_06_tech_config(prs)

    print("[7/14] Building Slide 7: Section 6 — Implementation (Slide A: Architecture)...")
    build_slide_07_impl_arch(prs)

    print("[8/14] Building Slide 8: Section 6 — Implementation (Slide B: Methodology)...")
    build_slide_08_impl_method(prs)

    print("[9/14] Building Slide 9: Section 6 — Implementation (Slide C: XAI Paradigm)...")
    build_slide_09_impl_xai_comparison(prs)

    print("[10/14] Building Slide 10: Section 7 — Output Screenshots (Dashboard & Text)...")
    build_slide_10_screenshots_p1(prs)

    print("[11/14] Building Slide 11: Section 7 — Output Screenshots (OCR & XAI Lab)...")
    build_slide_11_screenshots_p2(prs)

    print("[12/14] Building Slide 12: Section 8 — Conclusion...")
    build_slide_12_conclusion(prs)

    print("[13/14] Building Slide 13: Section 9 — Future Scope...")
    build_slide_13_future_scope(prs)

    print("[14/14] Building Slide 14: Section 10 — References...")
    build_slide_14_references(prs)

    print(f"\nSaving presentation to: {output_path}...")
    prs.save(str(output_path))
    file_size = output_path.stat().st_size
    print(f"Successfully generated PowerPoint presentation! Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print("=" * 70)


if __name__ == "__main__":
    main()
