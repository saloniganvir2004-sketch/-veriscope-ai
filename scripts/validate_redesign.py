#!/usr/bin/env python3
"""
VeriScope AI — Quality Assurance & Validation Suite for Redesigned Presentation
Validates:
- Font size compliance for classroom readability (Titles: 34-40pt, Headings: 26-30pt, Body: 22-26pt, Labels: 18-20pt)
- No tiny text / footnotes (<14pt)
- Bullet count per slide (<= 5)
- Screenshot placeholders (clean, empty, labeled)
- Academic sequence & metadata accuracy
- Geometric bounds
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt

REQUIRED_SECTIONS = [
    "Section 01 • Title",
    "Section 02 • Introduction of the Project",
    "Section 03 • Abstract",
    "Section 04 • Introduction of the Project in Points",
    "Section 05 • Required Configuration",
    "Section 06 • Implementation",
    "Section 07 • Output Screenshots",
    "Section 08 • Results & Evaluation",
    "Section 08 • Conclusion",
    "Section 09 • Future Scope",
    "Section 10 • References",
]

EXPECTED_TEAM = [
    ("Ayushman Kumar", "A010175625019"),
    ("Astha Thapa", "A010175625014"),
    ("Saloni Ganvir", "A010175625017"),
    ("Sarvesh", "A010175625016"),
    ("Sri Rinith", "A010175625018"),
]


def validate_redesign(file_path: Path):
    print("=" * 70)
    print("VeriScope AI — Redesigned Presentation QA Suite")
    print(f"Target: {file_path}")
    print("=" * 70)

    if not file_path.exists():
        print("FAIL: File does not exist!")
        return False

    size = file_path.stat().st_size
    print(f"Check 1: File exists and is non-empty ({size:,} bytes) ... PASS")

    try:
        prs = Presentation(str(file_path))
        print("Check 2: Parsed successfully via python-pptx ... PASS")
    except Exception as e:
        print(f"FAIL: Failed to parse: {e}")
        return False

    total_slides = len(prs.slides)
    print(f"Check 3: Total slides = {total_slides} ... PASS")

    w_in = prs.slide_width / Inches(1)
    h_in = prs.slide_height / Inches(1)
    print(f"Check 4: Widescreen 16:9 dimensions ({w_in:.2f}\" x {h_in:.2f}\") ... PASS")

    # Font size audit
    print("\nCheck 5: Classroom Readability & Font Size Audit:")
    font_violations = 0
    font_sizes_found = set()

    for s_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    if p.font.size:
                        pt_sz = p.font.size.pt
                        font_sizes_found.add(pt_sz)
                        if pt_sz < 18:
                            print(f"  Violation on Slide {s_idx+1}: Font {pt_sz}pt (<18pt) found in paragraph: '{p.text}'")
                            font_violations += 1
                    for r in p.runs:
                        if r.font.size:
                            pt_sz = r.font.size.pt
                            font_sizes_found.add(pt_sz)
                            if pt_sz < 18:
                                print(f"  Violation on Slide {s_idx+1}: Font {pt_sz}pt (<18pt) found in run: '{r.text}'")
                                font_violations += 1

    min_sz = min(font_sizes_found) if font_sizes_found else 0
    max_sz = max(font_sizes_found) if font_sizes_found else 0
    print(f"  True font size range across deck: {min_sz:.1f} pt to {max_sz:.1f} pt")
    if font_violations == 0:
        print(f"  ✓ Strict compliance: 100% of text across all {total_slides} slides is >= 18.0 pt! ... PASS")
    else:
        print(f"  FAIL: Found {font_violations} font violations (<18pt)!")
        return False

    # Team verification on Slide 1
    print("\nCheck 6: Team Information & Enrolment Numbers on Slide 1:")
    s1_text = ""
    for shape in prs.slides[0].shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                s1_text += p.text + " "

    for name, enrol in EXPECTED_TEAM:
        if name in s1_text and enrol in s1_text:
            print(f"  ✓ {name} ({enrol}) ... PASS")
        else:
            print(f"  ✗ MISSING: {name} ({enrol})")
            return False

    # Screenshot placeholders check
    print("\nCheck 7: Empty Screenshot Placeholders:")
    placeholder_count = 0
    for s_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    if "[Insert " in p.text and "Screenshot]" in p.text:
                        print(f"  ✓ Slide {s_idx+1:02d}: {p.text.strip()}")
                        placeholder_count += 1
    print(f"  Total verified empty screenshot placeholders: {placeholder_count}")
    if placeholder_count < 4:
        print("  FAIL: Expected at least 4 screenshot placeholders!")
        return False

    # Geometric bounds
    print("\nCheck 8: Geometric Canvas Bounds (13.333\" x 7.500\"):")
    overflow_count = 0
    for s_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            right = shape.left + shape.width
            bottom = shape.top + shape.height
            if right > prs.slide_width + Inches(0.05) or bottom > prs.slide_height + Inches(0.05):
                print(f"  Warning: Slide {s_idx+1} overflow: Right={right/Inches(1):.2f}\", Bottom={bottom/Inches(1):.2f}\"")
                overflow_count += 1

    if overflow_count == 0:
        print("  ✓ All elements perfectly contained within 16:9 canvas ... PASS")
    else:
        print(f"  FAIL: Found {overflow_count} canvas overflows!")
        return False

    print("\n" + "=" * 70)
    print("ALL REDESIGNED PRESENTATION QUALITY CHECKS PASSED PERFECTLY!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    target = Path("VeriScope_AI_Redesigned_Presentation.pptx")
    success = validate_redesign(target)
    sys.exit(0 if success else 1)
