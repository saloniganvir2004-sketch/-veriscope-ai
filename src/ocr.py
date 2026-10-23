"""
VeriScope AI - Image OCR & Preprocessing Engine
Extracts readable text from news screenshots, social media clippings, and photographs
using local Tesseract OCR and Pillow image preprocessing.
"""

import io
import re
import os
import shutil
import logging
from typing import Dict, Any, Optional, Union, Tuple
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import pytesseract

import config

logger = logging.getLogger("VeriScopeOCR")


def _find_tesseract_cmd() -> Optional[str]:
    """Discovers Tesseract binary across standard environment locations."""
    configured = config.OCR_CONFIG.get("tesseract_cmd", "")
    if configured and os.path.exists(configured):
        return configured

    which_path = shutil.which("tesseract")
    if which_path and os.path.exists(which_path):
        return which_path

    common_paths = [
        "/opt/homebrew/bin/tesseract",
        "/usr/local/bin/tesseract",
        "/usr/bin/tesseract",
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return None


_FOUND_TESSERACT = _find_tesseract_cmd()
if _FOUND_TESSERACT:
    pytesseract.pytesseract.tesseract_cmd = _FOUND_TESSERACT


def is_tesseract_available() -> Tuple[bool, str]:
    """
    Verifies that the Tesseract executable is installed and reachable by pytesseract.
    Returns (True, version_string) or (False, troubleshooting_instructions).
    """
    try:
        ver = pytesseract.get_tesseract_version()
        return True, f"Tesseract v{ver}"
    except Exception as e:
        return (
            False,
            "Tesseract OCR is not installed or not accessible on this system.\n\n"
            "On macOS, please install via Homebrew:\n"
            "    brew install tesseract\n\n"
            "Verify installation in terminal:\n"
            "    tesseract --version",
        )


def validate_image_bytes(file_bytes: bytes, filename: str = "") -> Tuple[bool, Optional[str]]:
    """
    Validates file size, extension, and decodability.
    Rejects corrupted, oversized, or unsupported files.
    """
    max_bytes = config.OCR_CONFIG.get("max_file_size_mb", 10) * 1024 * 1024
    if len(file_bytes) > max_bytes:
        return False, f"File exceeds maximum allowed size of {config.OCR_CONFIG['max_file_size_mb']}MB."

    if filename:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in config.OCR_CONFIG.get("allowed_extensions", ["jpg", "jpeg", "png", "webp"]):
            return False, f"Unsupported file extension '.{ext}'. Supported: JPG, PNG, WEBP."

    try:
        with Image.open(io.BytesIO(file_bytes)) as img:
            img.verify()
    except Exception as e:
        return False, f"Invalid or corrupted image file: {str(e)}"

    return True, None


def preprocess_image_for_ocr(img: Image.Image) -> Image.Image:
    """
    Optimizes image quality for OCR accuracy:
    1. Transposes EXIF orientation tags (e.g. photos taken sideways).
    2. Flattens transparency (RGBA/LA) onto a clean white background.
    3. Normalizes resolution (upscales small screenshot text, downscales massive images).
    4. Detects and corrects 90/180/270 degree rotation if OSD is available.
    5. Converts to high-contrast grayscale.
    6. Sharpens character edges.
    """
    # 1. Handle EXIF orientation
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    # 2. Composite transparency onto white background
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        alpha_img = img.convert("RGBA")
        background = Image.new("RGBA", alpha_img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(background, alpha_img).convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size

    # 3. Dynamic resizing for optimal OCR character height
    if width < 1200 and height < 1200:
        scale_factor = 1.6
        img = img.resize((int(width * scale_factor), int(height * scale_factor)), Image.Resampling.LANCZOS)
    elif width > 2800 or height > 2800:
        max_dim = 2600
        scale = max_dim / max(width, height)
        img = img.resize((int(width * scale), int(height * scale)), Image.Resampling.LANCZOS)

    # 4. Attempt orientation detection & rotation correction (OSD)
    try:
        osd = pytesseract.image_to_osd(img)
        rot_match = re.search(r"Rotate:\s*(\d+)", osd)
        if rot_match:
            angle = int(rot_match.group(1))
            if angle in (90, 180, 270):
                img = img.rotate(360 - angle, expand=True)
    except Exception:
        # Graceful fallback: sparse or unconventional layout may skip OSD safely
        pass

    # 5. Convert to Grayscale
    gray = img.convert("L")

    # 6. Contrast Enhancement
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.8)

    # 7. Gentle edge sharpening to clarify small fonts
    sharpened = enhanced.filter(ImageFilter.SHARPEN)

    return sharpened


def clean_ocr_text(raw_text: str) -> str:
    """
    Cleans raw OCR output:
    - Removes non-printable / control characters.
    - Preserves meaningful newlines between paragraphs while collapsing excessive gaps.
    - Trims whitespace.
    """
    if not raw_text:
        return ""

    # Remove non-printable control characters (except newline, tab)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", raw_text)

    # Normalize unicode quotation marks and dashes
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    text = text.replace("—", "-").replace("–", "-")

    # Collapse sequences of 3+ newlines to 2 newlines (paragraph boundary)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip trailing whitespace on each line
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines).strip()

    return text


def separate_headline_and_body(text: str) -> Tuple[str, str]:
    """
    Intelligently splits extracted text into a candidate headline and article body:
    1. If separated by double newlines, uses the first block as headline if <= 200 chars.
    2. Otherwise uses the first line if it's reasonably concise (<= 160 chars).
    3. Handles single-paragraph blocks gracefully.
    Always returns (headline, body) strings.
    """
    cleaned = (text or "").strip()
    if not cleaned:
        return "", ""

    # Check for paragraph boundary
    if "\n\n" in cleaned:
        parts = cleaned.split("\n\n", 1)
        first_part = parts[0].replace("\n", " ").strip()
        rest = parts[1].strip()
        if len(first_part) <= 220:
            return first_part, rest

    # Check line-by-line
    lines = [l.strip() for l in cleaned.splitlines() if l.strip()]
    if len(lines) > 1:
        first_line = lines[0]
        if len(first_line) <= 180:
            return first_line, "\n".join(lines[1:]).strip()

    # Single block / single line
    if len(cleaned) <= 140:
        return cleaned, ""

    # Long single block: split at first sentence boundary if appropriate
    sentence_match = re.search(r"^([^\.\?\!\n]{10,140}[\.\?\!])\s+(.*)$", cleaned, flags=re.DOTALL)
    if sentence_match:
        return sentence_match.group(1).strip(), sentence_match.group(2).strip()

    # Fallback: leave headline empty so user explicitly labels, or put first 100 chars
    return "", cleaned


def extract_text_from_image(
    image_input: Union[bytes, io.BytesIO, Image.Image],
    filename: str = "",
) -> Dict[str, Any]:
    """
    Full OCR pipeline:
    Validates, decodes, preprocesses, and executes OCR via local Tesseract.
    Returns structured results including separated candidate headline and body.
    """
    # 0. Check Tesseract availability
    tess_available, tess_msg = is_tesseract_available()
    if not tess_available:
        return {
            "success": False,
            "text": "",
            "headline": "",
            "body": "",
            "word_count": 0,
            "char_count": 0,
            "dimensions": (0, 0),
            "error": tess_msg,
        }

    # 1. Load Image
    try:
        if isinstance(image_input, bytes):
            is_valid, err = validate_image_bytes(image_input, filename)
            if not is_valid:
                return {
                    "success": False,
                    "text": "",
                    "headline": "",
                    "body": "",
                    "word_count": 0,
                    "char_count": 0,
                    "dimensions": (0, 0),
                    "error": err,
                }
            img = Image.open(io.BytesIO(image_input))
        elif isinstance(image_input, io.BytesIO):
            img_bytes = image_input.getvalue()
            is_valid, err = validate_image_bytes(img_bytes, filename)
            if not is_valid:
                return {
                    "success": False,
                    "text": "",
                    "headline": "",
                    "body": "",
                    "word_count": 0,
                    "char_count": 0,
                    "dimensions": (0, 0),
                    "error": err,
                }
            img = Image.open(image_input)
        elif isinstance(image_input, Image.Image):
            img = image_input
        else:
            return {
                "success": False,
                "text": "",
                "headline": "",
                "body": "",
                "word_count": 0,
                "char_count": 0,
                "dimensions": (0, 0),
                "error": "Unsupported image input type.",
            }

        orig_w, orig_h = img.size

        # 2. Preprocess
        processed_img = preprocess_image_for_ocr(img)

        # 3. Run OCR with Tesseract
        custom_config = r"--oem 3 --psm 6"  # Assume a uniform block of text
        try:
            raw_text = pytesseract.image_to_string(processed_img, config=custom_config)
        except Exception:
            # Fallback to default PSM if psm 6 encounters irregular layout
            raw_text = pytesseract.image_to_string(processed_img)

        cleaned_text = clean_ocr_text(raw_text)

        words = cleaned_text.split()
        word_count = len(words)
        char_count = len(cleaned_text)

        if word_count == 0 or char_count < 10:
            return {
                "success": False,
                "text": "",
                "headline": "",
                "body": "",
                "raw_text": raw_text,
                "word_count": word_count,
                "char_count": char_count,
                "dimensions": (orig_w, orig_h),
                "error": "No readable text detected in the uploaded image. Please ensure the image contains clear, legible text.",
            }

        headline, body = separate_headline_and_body(cleaned_text)

        return {
            "success": True,
            "text": cleaned_text,
            "headline": headline,
            "body": body,
            "raw_text": raw_text,
            "word_count": word_count,
            "char_count": char_count,
            "dimensions": (orig_w, orig_h),
            "error": None,
        }

    except Exception as e:
        logger.error(f"OCR execution failed: {e}")
        return {
            "success": False,
            "text": "",
            "headline": "",
            "body": "",
            "word_count": 0,
            "char_count": 0,
            "dimensions": (0, 0),
            "error": f"OCR processing failed: {str(e)}",
        }
