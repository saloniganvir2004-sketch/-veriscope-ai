"""
VeriScope AI - Central Configuration
Defines paths, random seeds, hyperparameters, editorial design tokens, OCR settings, and research constants.
"""

from pathlib import Path

# -----------------------------------------------------------------------------
# 1. Project Directory Structure
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODELS_DIR = ARTIFACTS_DIR / "models"
METRICS_DIR = ARTIFACTS_DIR / "metrics"
EXPERIMENTS_DIR = ARTIFACTS_DIR / "xai_experiments"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"

DB_PATH = ARTIFACTS_DIR / "veritas_history.db"

# Ensure all critical folders exist
for p in [DATA_RAW_DIR, DATA_PROCESSED_DIR, MODELS_DIR, METRICS_DIR, EXPERIMENTS_DIR, REPORTS_DIR, ASSETS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 2. Dataset & Splitting Parameters
# -----------------------------------------------------------------------------
RANDOM_SEED = 42

# Label definitions: 0 = Real, 1 = Fake
LABEL_REAL = 0
LABEL_FAKE = 1
LABEL_NAMES = {LABEL_REAL: "Likely Real", LABEL_FAKE: "Likely Fake"}
LABEL_CLASSES = ["Likely Real", "Likely Fake"]

# Split ratios
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Leakage Sanitization regex patterns (Publisher and wire service headers)
WIRE_SERVICE_PATTERNS = [
    r"^\s*([A-Z\s]{2,25})?\s*\(\s*Reuters\s*\)\s*[-–—:]\s*",
    r"^\s*([A-Z\s]{2,25})?\s*\(\s*(AP|Associated Press|Bloomberg|AFP)\s*\)\s*[-–—:]\s*",
    r"^\s*[A-Z\s]{2,25}\s*[-–—]\s*",  # General all-caps city prefix like "WASHINGTON —"
    r"\(Reuters\)",
    r"\(AP\)",
    r"\(Bloomberg\)",
]

# -----------------------------------------------------------------------------
# 3. Text Preprocessing & Vectorization
# -----------------------------------------------------------------------------
TFIDF_CONFIG = {
    "max_features": 5000,
    "ngram_range": (1, 2),
    "sublinear_tf": True,
    "min_df": 2,
    "max_df": 0.95,
    "stop_words": "english",
}

# -----------------------------------------------------------------------------
# 4. Model Training & Hyperparameters
# -----------------------------------------------------------------------------
MODEL_CONFIGS = {
    "Logistic Regression": {
        "C": 1.0,
        "max_iter": 1000,
        "solver": "liblinear",
        "random_state": RANDOM_SEED,
    },
    "Multinomial Naive Bayes": {
        "alpha": 0.1,
    },
    "Linear SVM": {
        "C": 0.5,
        "max_iter": 2000,
        "random_state": RANDOM_SEED,
    },
}

# -----------------------------------------------------------------------------
# 5. Explainable AI (XAI) Configurations
# -----------------------------------------------------------------------------
LIME_CONFIG = {
    "num_features": 10,
    "num_samples": 400,
    "random_state": RANDOM_SEED,
}

SHAP_CONFIG = {
    "max_evals": 400,
    "top_k_features": 10,
}

# XAI Research Evaluation
XAI_EVAL_CONFIG = {
    "top_k_agreement": [5, 10],
    "perturbation_noise_rate": 0.10,  # 10% character/word jitter
    "stability_trials": 5,
}

# -----------------------------------------------------------------------------
# 6. OCR & Image Preprocessing Settings
# -----------------------------------------------------------------------------
OCR_CONFIG = {
    "tesseract_cmd": "/opt/homebrew/bin/tesseract",
    "allowed_extensions": ["jpg", "jpeg", "png", "webp"],
    "max_file_size_mb": 10,
    "max_text_length": 25000,
    "min_text_length": 25,
}

# -----------------------------------------------------------------------------
# 7. UI / UX Design System Tokens: Editorial Intelligence
# -----------------------------------------------------------------------------
BRAND_NAME = "VeriScope AI"
BRAND_TAGLINE = "Intelligence Beyond the Headline."
PROJECT_TITLE = "Fake News Detection Using Explainable AI"

DISCLAIMER_TEXT = (
    "VeriScope AI predicts whether news resembles patterns in its training data. "
    "Predictions and feature explanations are not definitive evidence of factual truth. "
    "Verify important claims using reliable sources."
)

COLOR_THEME = {
    "bg_body": "#F8F9FA",          # Warm stone / off-white reading area
    "surface": "#FFFFFF",          # Pure white cards
    "surface_alt": "#F1F5F9",      # Crisp light slate container
    "border": "#E2E8F0",           # Soft border
    "border_subtle": "#CBD5E1",    # Separator line
    "primary": "#0E7490",          # Muted deep teal accent
    "primary_hover": "#155E75",    # Darker teal for interaction
    "secondary": "#334155",        # Slate blue
    "real": "#15803D",             # Restrained sage green
    "real_bg": "rgba(21, 128, 61, 0.08)",
    "real_border": "rgba(21, 128, 61, 0.25)",
    "fake": "#DC2626",             # Restrained coral red
    "fake_bg": "rgba(220, 38, 38, 0.08)",
    "fake_border": "rgba(220, 38, 38, 0.25)",
    "text_main": "#0F172A",        # Deep midnight ink
    "text_secondary": "#334155",   # Charcoal slate
    "text_muted": "#64748B",       # Subtle caption text
}
