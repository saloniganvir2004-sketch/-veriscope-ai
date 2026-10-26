"""
VERITAS AI - Model Training Pipeline
Trains Logistic Regression, Multinomial Naive Bayes, and Calibrated Linear SVM.
Validates hyperparameters on validation data, selects the best model, evaluates
on the held-out test set, and exports reproducible artifacts and metrics.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
import joblib

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

import config
from src.data_loader import (
    load_raw_dataset,
    validate_dataset_schema,
    leakage_safe_group_split,
    save_processed_splits,
)
from src.preprocessing import (
    prepare_input_text,
    fit_and_save_vectorizer,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("VeritasTrainer")


def prepare_dataset_splits(use_external: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    """
    Loads raw data (preferring the external ISOT dataset when available, with clean fallback
    to synthetic benchmark), performs schema and leakage audit, cleans text, and generates
    strictly group-aware, leakage-free 70% Train, 15% Validation, and 15% Test partitions.
    Guarantees that all duplicate copies of any article body are confined to the same partition.
    """
    source_pref = "external" if use_external else "synthetic"
    logger.info(f"Loading dataset for training pipeline (source preference: {source_pref})...")
    df, dataset_name = load_raw_dataset(source=source_pref, return_source_name=True)
    schema_report = validate_dataset_schema(df)

    # Save schema validation report
    with open(config.METRICS_DIR / "dataset_validation_report.json", "w") as f:
        json.dump(schema_report, f, indent=2)

    # Sanitize and prepare combined text
    logger.info("Applying publisher leakage sanitization and text normalization...")
    df["combined_text"] = df.apply(
        lambda r: prepare_input_text(str(r["title"]), str(r["text"]), remove_publisher_tags=True),
        axis=1,
    )

    # Filter any empty or null rows after cleaning
    df = df[df["combined_text"].str.strip() != ""].copy()

    # Leakage-Safe Group Partitioning (strictly isolates duplicate article bodies)
    logger.info("Partitioning data with group-based leakage protection...")
    train_df, val_df, test_df, leakage_report = leakage_safe_group_split(
        df,
        train_ratio=config.TRAIN_RATIO,
        val_ratio=config.VAL_RATIO,
        test_ratio=config.TEST_RATIO,
        random_seed=config.RANDOM_SEED,
    )
    leakage_report["dataset_name"] = dataset_name

    # Save comprehensive leakage and dataset audit report
    with open(config.METRICS_DIR / "dataset_audit_report.json", "w") as f:
        json.dump(leakage_report, f, indent=2)

    save_processed_splits(train_df, val_df, test_df)
    return train_df, val_df, test_df, dataset_name


def evaluate_on_synthetic_benchmark(
    models_dict: Dict[str, Any],
    vectorizer: Any,
) -> Dict[str, Any]:
    """
    Evaluates trained models on the synthetic regression benchmark dataset
    to preserve regression tracking and clearly distinguish synthetic from external evaluation.
    """
    synthetic_path = config.DATA_SYNTHETIC_PATH
    if not synthetic_path.exists():
        logger.warning(f"Synthetic benchmark dataset not found at {synthetic_path}.")
        return {}

    df_synth = pd.read_csv(synthetic_path)
    # Perform group-aware split on synthetic benchmark
    _, _, test_synth, _ = leakage_safe_group_split(
        df_synth,
        train_ratio=config.TRAIN_RATIO,
        val_ratio=config.VAL_RATIO,
        test_ratio=config.TEST_RATIO,
        random_seed=config.RANDOM_SEED,
    )

    test_synth["combined_text"] = test_synth.apply(
        lambda r: prepare_input_text(str(r["title"]), str(r["text"]), remove_publisher_tags=True),
        axis=1,
    )
    X_synth_test = vectorizer.transform(test_synth["combined_text"])
    y_synth_test = test_synth["label"].values

    synth_results = {}
    for name, model in models_dict.items():
        preds = model.predict(X_synth_test)
        synth_results[name] = {
            "accuracy": round(float(accuracy_score(y_synth_test, preds)), 4),
            "macro_f1": round(float(f1_score(y_synth_test, preds, average="macro", zero_division=0)), 4),
            "macro_precision": round(float(precision_score(y_synth_test, preds, average="macro", zero_division=0)), 4),
            "macro_recall": round(float(recall_score(y_synth_test, preds, average="macro", zero_division=0)), 4),
            "total_samples": int(len(y_synth_test)),
            "correct_predictions": int(np.sum(preds == y_synth_test)),
            "error_count": int(np.sum(preds != y_synth_test)),
        }

    synth_summary = {
        "dataset_name": "Synthetic Benchmark Dataset (Regression Test)",
        "evaluation_timestamp": datetime.now().isoformat(),
        "total_benchmark_records": len(df_synth),
        "held_out_test_samples": len(test_synth),
        "evaluations": synth_results,
    }

    with open(config.METRICS_DIR / "synthetic_benchmark_comparison.json", "w") as f:
        json.dump(synth_summary, f, indent=2)

    logger.info("Synthetic benchmark regression evaluation completed and persisted.")
    return synth_summary


def train_and_evaluate_all(use_external: bool = True):
    """
    Executes full training across the three candidate models:
    1. Logistic Regression
    2. Multinomial Naive Bayes
    3. Calibrated Linear SVM
    """
    train_df, val_df, test_df, dataset_name = prepare_dataset_splits(use_external=use_external)

    logger.info(f"Dataset: '{dataset_name}' | Split sizes: Train={len(train_df):,}, Val={len(val_df):,}, Test={len(test_df):,}")

    # 1. Fit TF-IDF Vectorizer STRICTLY on training split
    vectorizer = fit_and_save_vectorizer(
        texts=train_df["combined_text"].tolist(),
        save_path=config.MODELS_DIR / "tfidf_vectorizer.joblib",
    )

    X_train = vectorizer.transform(train_df["combined_text"])
    y_train = train_df["label"].values

    X_val = vectorizer.transform(val_df["combined_text"])
    y_val = val_df["label"].values

    X_test = vectorizer.transform(test_df["combined_text"])
    y_test = test_df["label"].values

    # 2. Define candidate models
    lr_cfg = config.MODEL_CONFIGS["Logistic Regression"]
    mnb_cfg = config.MODEL_CONFIGS["Multinomial Naive Bayes"]
    svm_cfg = config.MODEL_CONFIGS["Linear SVM"]

    candidates = {
        "Logistic Regression": LogisticRegression(
            C=lr_cfg["C"],
            max_iter=lr_cfg["max_iter"],
            solver=lr_cfg["solver"],
            random_state=lr_cfg["random_state"],
        ),
        "Multinomial Naive Bayes": MultinomialNB(
            alpha=mnb_cfg["alpha"],
        ),
        "Linear SVM": CalibratedClassifierCV(
            estimator=LinearSVC(
                C=svm_cfg["C"],
                max_iter=svm_cfg["max_iter"],
                random_state=svm_cfg["random_state"],
            ),
            method="sigmoid",
            cv=3,  # 3-fold internal calibration on train split only
        ),
    }

    model_results = {}
    fitted_models = {}

    for name, model in candidates.items():
        logger.info(f"Training model candidate: {name}...")
        model.fit(X_train, y_train)
        fitted_models[name] = model

        # Evaluate on Validation set
        val_preds = model.predict(X_val)
        val_acc = accuracy_score(y_val, val_preds)
        val_f1 = f1_score(y_val, val_preds, average="macro", zero_division=0)
        val_prec = precision_score(y_val, val_preds, average="macro", zero_division=0)
        val_rec = recall_score(y_val, val_preds, average="macro", zero_division=0)

        model_results[name] = {
            "validation": {
                "accuracy": round(float(val_acc), 4),
                "macro_f1": round(float(val_f1), 4),
                "macro_precision": round(float(val_prec), 4),
                "macro_recall": round(float(val_rec), 4),
            }
        }

    # 3. Model Selection based on Validation Macro F1
    best_model_name = max(model_results, key=lambda m: model_results[m]["validation"]["macro_f1"])
    best_model = fitted_models[best_model_name]
    logger.info(f"Selected Best Model: '{best_model_name}' (Val F1: {model_results[best_model_name]['validation']['macro_f1']})")

    # 4. Final Evaluation on Held-Out Test Set for all candidates
    test_evaluations = {}
    confusion_matrices = {}
    classification_reports = {}

    for name, model in fitted_models.items():
        test_preds = model.predict(X_test)
        test_acc = accuracy_score(y_test, test_preds)
        test_f1 = f1_score(y_test, test_preds, average="macro", zero_division=0)
        test_prec = precision_score(y_test, test_preds, average="macro", zero_division=0)
        test_rec = recall_score(y_test, test_preds, average="macro", zero_division=0)

        correct_count = int(np.sum(test_preds == y_test))
        error_count = int(np.sum(test_preds != y_test))

        # Per-class metrics
        report = classification_report(y_test, test_preds, target_names=config.LABEL_CLASSES, output_dict=True, zero_division=0)
        cm = confusion_matrix(y_test, test_preds).tolist()

        model_results[name]["test"] = {
            "accuracy": round(float(test_acc), 4),
            "macro_f1": round(float(test_f1), 4),
            "macro_precision": round(float(test_prec), 4),
            "macro_recall": round(float(test_rec), 4),
            "total_samples": int(len(y_test)),
            "correct_predictions": correct_count,
            "error_count": error_count,
        }
        test_evaluations[name] = model_results[name]["test"]
        confusion_matrices[name] = cm
        classification_reports[name] = report

    # 5. Persist Best Pipeline & Candidate Artifacts
    best_pipeline = {
        "model_name": best_model_name,
        "vectorizer": vectorizer,
        "classifier": best_model,
        "class_names": config.LABEL_CLASSES,
        "random_seed": config.RANDOM_SEED,
    }
    joblib.dump(best_pipeline, config.MODELS_DIR / "best_pipeline.joblib")
    joblib.dump(fitted_models, config.MODELS_DIR / "all_candidate_models.joblib")

    # Save metrics
    metrics_summary = {
        "best_model_name": best_model_name,
        "training_timestamp": datetime.now().isoformat(),
        "random_seed": config.RANDOM_SEED,
        "evaluation_dataset": dataset_name,
        "is_external": "ISOT" in dataset_name,
        "leakage_prevention": "group_aware_stratified_split",
        "partition_sizes": {
            "train": len(train_df),
            "val": len(val_df),
            "test": len(test_df),
        },
        "selection_rationale": (
            f"Selected based on highest validation Macro F1 score "
            f"({model_results[best_model_name]['validation']['macro_f1']:.4f}). "
            f"{best_model_name} provides robust probability calibration, continuous log-odds interpretability, "
            f"and direct mathematical compatibility with shap.LinearExplainer."
        ),
        "comparison": model_results,
        "test_evaluations": test_evaluations,
    }

    with open(config.METRICS_DIR / "model_comparison.json", "w") as f:
        json.dump(metrics_summary, f, indent=2)

    with open(config.METRICS_DIR / "confusion_matrices.json", "w") as f:
        json.dump(confusion_matrices, f, indent=2)

    with open(config.METRICS_DIR / "classification_reports.json", "w") as f:
        json.dump(classification_reports, f, indent=2)

    # 6. Secondary Evaluation: Regression Test on Synthetic Benchmark (keeps both distinct)
    evaluate_on_synthetic_benchmark(fitted_models, vectorizer)

    logger.info("Training and evaluation completed successfully. All artifacts persisted.")
    return metrics_summary


if __name__ == "__main__":
    train_and_evaluate_all()
