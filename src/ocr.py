"""
VeriScope AI - Image OCR & Preprocessing Engine
Extracts readable text from news screenshots, social media clippings, and photographs
using local Tesseract OCR and Pillow image preprocessing.
"""

import io
import re
import os
import logging
from typing import Dict, Any, Optional, Union, Tuple
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import pytesseract

import config

logger = logging.getLogger("VeriScopeOCR")

# Configure tesseract executable location if available
if os.path.exists(config.OCR_CONFIG.get("tesseract_cmd", "")):
    pytesseract.pytesseract.tesseract_cmd = config.OCR_CONFIG["tesseract_cmd"]


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
    4. Converts to high-contrast grayscale.
    5. Sharpens character edges.
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
    # Small text benefits from upscaling with high-quality resampling
    if width < 1200 and height < 1200:
        scale_factor = 1.6
        img = img.resize((int(width * scale_factor), int(height * scale_factor)), Image.Resampling.LANCZOS)
    elif width > 2800 or height > 2800:
        max_dim = 2600
        scale = max_dim / max(width, height)
        img = img.resize((int(width * scale), int(height * scale)), Image.Resampling.LANCZOS)

    # 4. Convert to Grayscale
    gray = img.convert("L")

    # 5. Contrast Enhancement
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.8)

    # 6. Gentle edge sharpening to clarify small fonts
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


def extract_text_from_image(
    image_input: Union[bytes, io.BytesIO, Image.Image],
    filename: str = "",
) -> Dict[str, Any]:
    """
    Full OCR pipeline:
    Validates, decodes, preprocesses, and executes OCR via local Tesseract.
    Returns structured results.
    """
    # Load Image
    try:
        if isinstance(image_input, bytes):
            is_valid, err = validate_image_bytes(image_input, filename)
            if not is_valid:
                return {"success": False, "text": "", "error": err}
            img = Image.open(io.BytesIO(image_input))
        elif isinstance(image_input, io.BytesIO):
            img_bytes = image_input.getvalue()
            is_valid, err = validate_image_bytes(img_bytes, filename)
            if not is_valid:
                return {"success": False, "text": "", "error": err}
            img = Image.open(image_input)
        elif isinstance(image_input, Image.Image):
            img = image_input
        else:
            return {"success": False, "text": "", "error": "Unsupported image input type."}

        orig_w, orig_h = img.size

        # Preprocess
        processed_img = preprocess_image_for_ocr(img)

        # Run OCR with Tesseract
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
                "raw_text": raw_text,
                "word_count": word_count,
                "char_count": char_count,
                "dimensions": (orig_w, orig_h),
                "error": "No readable text detected in the uploaded image. Please ensure the image contains clear, legible text.",
            }

        return {
            "success": True,
            "text": cleaned_text,
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
            "error": f"OCR processing failed: {str(e)}",
        }
