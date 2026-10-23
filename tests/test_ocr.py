"""
Unit tests for Image Validation, Preprocessing, and Local Tesseract OCR extraction.
"""

import io
from PIL import Image, ImageDraw
import pytest

from src.ocr import (
    validate_image_bytes,
    preprocess_image_for_ocr,
    clean_ocr_text,
    extract_text_from_image,
    is_tesseract_available,
    separate_headline_and_body,
)


def create_synthetic_news_image(text: str) -> bytes:
    """Helper creating a crisp in-memory PNG with black text on white background."""
    img = Image.new("RGB", (800, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((30, 40), text, fill=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_tesseract_availability():
    avail, info = is_tesseract_available()
    assert isinstance(avail, bool)
    assert isinstance(info, str)
    if avail:
        assert "Tesseract" in info


def test_separate_headline_and_body():
    # 1. Separated by paragraph
    t1 = "Breaking News: Central Bank Lowers Rates\n\nThe Federal Reserve decided to lower interest rates today."
    h1, b1 = separate_headline_and_body(t1)
    assert h1 == "Breaking News: Central Bank Lowers Rates"
    assert "Federal Reserve" in b1

    # 2. Separated by newline
    t2 = "Shock Claim on Mars Exploration\nNASA uncovered new geological structures."
    h2, b2 = separate_headline_and_body(t2)
    assert h2 == "Shock Claim on Mars Exploration"
    assert "geological structures" in b2

    # 3. Short single sentence
    t3 = "Just a short single headline."
    h3, b3 = separate_headline_and_body(t3)
    assert h3 == "Just a short single headline."
    assert b3 == ""

    # 4. Empty string
    h4, b4 = separate_headline_and_body("")
    assert h4 == ""
    assert b4 == ""


def test_preprocess_image_rgba_and_resizing():
    # RGBA image with transparency
    rgba_img = Image.new("RGBA", (400, 300), color=(255, 255, 255, 128))
    processed = preprocess_image_for_ocr(rgba_img)
    # Output should be in Grayscale mode 'L'
    assert processed.mode == "L"
    # Should be upscaled for small original size
    assert processed.size[0] >= 400


def test_validate_image_bytes_valid_png():
    img_bytes = create_synthetic_news_image("Federal Reserve meeting announcement.")
    is_valid, err = validate_image_bytes(img_bytes, "test.png")
    assert is_valid is True
    assert err is None


def test_validate_image_bytes_invalid_extension():
    img_bytes = b"not an image"
    is_valid, err = validate_image_bytes(img_bytes, "test.pdf")
    assert is_valid is False
    assert "Unsupported file extension" in err


def test_validate_image_bytes_corrupted_data():
    img_bytes = b"corrupted header bytes"
    is_valid, err = validate_image_bytes(img_bytes, "test.png")
    assert is_valid is False
    assert "Invalid or corrupted image" in err


def test_clean_ocr_text():
    dirty = "Line 1 \n\n\n\n\n Line 2   \x00\x05\nLine 3"
    cleaned = clean_ocr_text(dirty)
    assert "\x00" not in cleaned
    assert "Line 1" in cleaned
    assert "Line 2" in cleaned
    assert "\n\n\n" not in cleaned


def test_extract_text_from_image_synthetic():
    text_content = "Headline: Central Bank Holds Benchmark Interest Rate Steady\n\nOfficials concluded their monthly policy meeting."
    img_bytes = create_synthetic_news_image(text_content)
    res = extract_text_from_image(img_bytes, "headline.png")

    assert res["success"] is True
    assert res["error"] is None
    assert "Benchmark" in res["text"] or "Interest" in res["text"] or "Rate" in res["text"]
    assert res["word_count"] > 3
    assert "headline" in res
    assert "body" in res


def test_extract_text_from_blank_image():
    # Blank white image with no text
    blank = Image.new("RGB", (400, 200), color=(255, 255, 255))
    buf = io.BytesIO()
    blank.save(buf, format="PNG")
    res = extract_text_from_image(buf.getvalue(), "blank.png")

    assert res["success"] is False
    assert "No readable text detected" in res["error"]
