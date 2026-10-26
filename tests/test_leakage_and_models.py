"""
Unit and integration tests for leakage-safe dataset splitting, duplicate body isolation,
conflicting label detection, external ISOT dataset import, and three-model comparative evaluation metrics.
"""

import json
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

import config
from src.data_loader import (
    normalize_body_text,
    audit_and_group_dataset,
    leakage_safe_group_split,
    load_raw_dataset,
    is_external_dataset_available,
    load_external_isot_dataset,
    load_synthetic_dataset,
)


def test_normalize_body_text_strips_leakage_and_whitespace():
    raw_1 = "  WASHINGTON (Reuters) - The Federal Reserve announced new policy today.  "
    raw_2 = "the federal reserve announced new policy today."
    norm_1 = normalize_body_text(raw_1)
    norm_2 = normalize_body_text(raw_2)

    assert "reuters" not in norm_1
    assert "washington" not in norm_1
    assert norm_1 == norm_2

    # City with date and wire service
    raw_3 = "WASHINGTON, Dec 31 (Reuters) - The committee voted to approve the budget."
    norm_3 = normalize_body_text(raw_3)
    assert "reuters" not in norm_3
    assert "committee voted" in norm_3


def test_audit_and_group_dataset_detects_duplicates():
    # Build dataframe with duplicate bodies but different titles
    data = [
        {"title": "Title Variant 1", "text": "This is identical body text for testing.", "label": 0},
        {"title": "Title Variant 2", "text": "This is identical body text for testing.", "label": 0},
        {"title": "Title Variant 3", "text": "This is completely different body text.", "label": 1},
    ]
    df = pd.DataFrame(data)
    df_grouped, audit = audit_and_group_dataset(df)

    assert "body_hash" in df_grouped.columns
    assert audit["total_records"] == 3
    assert audit["unique_body_groups"] == 2
    assert audit["duplicate_records"] == 1
    assert audit["conflicting_labels_count"] == 0


def test_audit_and_group_dataset_raises_on_conflicting_labels():
    # Identical body text assigned conflicting labels
    data = [
        {"title": "Story A", "text": "Conflicting article body text here.", "label": 0},
        {"title": "Story B", "text": "Conflicting article body text here.", "label": 1},
    ]
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="conflicting labels"):
        audit_and_group_dataset(df)


def test_audit_and_group_dataset_drops_empty_records():
    # Dataframe with valid and empty records
    data = [
        {"title": "Valid Headline", "text": "This is substantive body text for classification.", "label": 0},
        {"title": "Empty Headline", "text": "   ", "label": 1},
        {"title": "Whitespace Only", "text": "\n\t  \n", "label": 1},
    ]
    df = pd.DataFrame(data)
    df_clean, audit = audit_and_group_dataset(df)

    assert len(df_clean) == 1
    assert audit["empty_records_dropped"] == 2
    assert audit["total_records"] == 1


def test_is_external_dataset_available():
    assert is_external_dataset_available() is True, "External ISOT True.csv and Fake.csv must be available"


def test_load_external_isot_dataset_structure():
    df = load_external_isot_dataset()
    assert len(df) > 40000, f"Expected >40,000 records in ISOT dataset, got {len(df)}"
    assert "label" in df.columns
    assert set(df["label"].unique()) == {0, 1}
    assert (df["text"].str.strip() != "").all(), "No empty text bodies allowed"


def test_synthetic_regression_dataset_preserved_untouched():
    synth_path = config.DATA_SYNTHETIC_PATH
    assert synth_path.exists(), "Synthetic regression benchmark must exist in data/raw/"
    df_synth = pd.read_csv(synth_path)
    assert len(df_synth) == 400, "Synthetic benchmark must preserve exactly 400 records"
    assert df_synth["text"].nunique() == 16, "Synthetic benchmark must preserve exactly 16 unique article bodies"


def test_leakage_safe_group_split_zero_overlap():
    raw_df = load_raw_dataset(source="synthetic")
    train_df, val_df, test_df, report = leakage_safe_group_split(
        raw_df,
        train_ratio=config.TRAIN_RATIO,
        val_ratio=config.VAL_RATIO,
        test_ratio=config.TEST_RATIO,
        random_seed=config.RANDOM_SEED,
    )

    # 1. Verify zero body overlap across partitions
    train_hashes = set(train_df["body_hash"])
    val_hashes = set(val_df["body_hash"])
    test_hashes = set(test_df["body_hash"])

    assert train_hashes.isdisjoint(val_hashes), "Train and Val partitions leak article bodies!"
    assert train_hashes.isdisjoint(test_hashes), "Train and Test partitions leak article bodies!"
    assert val_hashes.isdisjoint(test_hashes), "Val and Test partitions leak article bodies!"

    # 2. Verify audit report fields
    assert report["zero_leakage_verified"] is True
    assert report["actual_records"]["train"] == len(train_df)
    assert report["actual_records"]["val"] == len(val_df)
    assert report["actual_records"]["test"] == len(test_df)
    assert len(train_df) + len(val_df) + len(test_df) == len(raw_df)


def test_three_model_comparison_metrics_persisted_and_distinct():
    comp_file = config.METRICS_DIR / "model_comparison.json"
    assert comp_file.exists(), "model_comparison.json must exist"

    with open(comp_file, "r") as f:
        comp = json.load(f)

    assert "comparison" in comp
    assert "test_evaluations" in comp
    evals = comp["test_evaluations"]

    # Must contain all three candidate architectures
    assert "Logistic Regression" in evals
    assert "Multinomial Naive Bayes" in evals
    assert "Linear SVM" in evals

    # Scores must NOT be identical across all three models (models exhibit distinct accuracy)
    lr_acc = evals["Logistic Regression"]["accuracy"]
    mnb_acc = evals["Multinomial Naive Bayes"]["accuracy"]
    svm_acc = evals["Linear SVM"]["accuracy"]

    assert lr_acc != mnb_acc, "Logistic Regression and Naive Bayes must have distinct test performance!"
    assert 0.0 <= lr_acc <= 1.0
    assert 0.0 <= mnb_acc <= 1.0
    assert 0.0 <= svm_acc <= 1.0


def test_confusion_matrices_shape_and_support():
    cm_file = config.METRICS_DIR / "confusion_matrices.json"
    comp_file = config.METRICS_DIR / "model_comparison.json"
    assert cm_file.exists(), "confusion_matrices.json must exist"
    assert comp_file.exists(), "model_comparison.json must exist"

    with open(cm_file, "r") as f:
        cms = json.load(f)
    with open(comp_file, "r") as f:
        comp = json.load(f)

    expected_support = comp.get("partition_sizes", {}).get("test", 6685)

    for m_name in ["Logistic Regression", "Multinomial Naive Bayes", "Linear SVM"]:
        assert m_name in cms
        cm = cms[m_name]
        assert len(cm) == 2
        assert len(cm[0]) == 2
        assert len(cm[1]) == 2
        total_support = cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1]
        assert total_support == expected_support, f"Expected {expected_support} test samples in CM for {m_name}, got {total_support}"


def test_synthetic_benchmark_comparison_persisted():
    synth_file = config.METRICS_DIR / "synthetic_benchmark_comparison.json"
    assert synth_file.exists(), "synthetic_benchmark_comparison.json must exist"
    with open(synth_file, "r") as f:
        data = json.load(f)
    assert "evaluations" in data
    assert "Logistic Regression" in data["evaluations"]


def test_presentation_dataset_sample_schema():
    sample_path = config.DATA_DIR / "presentation_sample.csv"
    assert sample_path.exists(), "data/presentation_sample.csv must exist"

    df = pd.read_csv(sample_path)
    assert len(df) >= 8, "Presentation sample must contain at least 8 representative rows"
    expected_cols = {"Article ID", "Category", "Headline", "Article Text Excerpt", "True Label"}
    assert expected_cols.issubset(set(df.columns))

    labels = set(df["True Label"].unique())
    assert labels == {"Likely Real", "Likely Fake"}
    assert df["Headline"].str.strip().ne("").all()
    assert df["Article Text Excerpt"].str.strip().ne("").all()


def test_dataset_methodology_doc_exists():
    doc_path = config.BASE_DIR / "docs" / "DATASET_METHODOLOGY_PPT.md"
    assert doc_path.exists(), "docs/DATASET_METHODOLOGY_PPT.md must exist"
    content = doc_path.read_text()
    assert "Dataset Overview" in content
    assert "Inclusion & Exclusion Criteria" in content
    assert "Leakage" in content
    assert "Group-Based" in content
    assert "Multinomial Naive Bayes" in content
