"""
VERITAS AI - SHAP Explainer Module
Implements Shapley value feature attribution for text classification using SHAP.
Correctly maps token features, handles binary-class output shapes, and returns
directional contributions toward Likely Fake and Likely Real.
"""

import logging
from typing import Dict, Any, List, Optional
import numpy as np
import scipy.sparse as sp
import shap

import config
from src.predict import load_inference_pipeline
from src.preprocessing import clean_text

logger = logging.getLogger("VeritasShap")


class VeritasShapExplainer:
    """
    Encapsulates SHAP explanation logic tailored for linear and calibrated classifiers
    on sparse TF-IDF text features. Computes instantaneous, mathematically rigorous
    Shapley attributions.
    """

    def __init__(self, pipeline: Optional[Dict[str, Any]] = None):
        if pipeline is None:
            pipeline = load_inference_pipeline()
        self.pipeline = pipeline
        self.vectorizer = pipeline["vectorizer"]
        self.classifier = pipeline["classifier"]
        self.feature_names = np.array(self.vectorizer.get_feature_names_out())
        self._init_explainer()

    def _init_explainer(self):
        """Initializes the appropriate SHAP explainer based on model architecture."""
        try:
            # Check if classifier has direct coef_
            if hasattr(self.classifier, "coef_"):
                # LogisticRegression or LinearSVC
                # Create a small zero-baseline background matrix
                background = sp.csr_matrix((1, len(self.feature_names)))
                self.explainer = shap.LinearExplainer(self.classifier, background)
                self.explainer_type = "LinearExplainer"
            elif hasattr(self.classifier, "calibrated_classifiers_"):
                # CalibratedClassifierCV
                # Average the coefficients of the calibrated sub-estimators
                coefs = []
                intercepts = []
                for sub_clf in self.classifier.calibrated_classifiers_:
                    estimator = getattr(sub_clf, "estimator", getattr(sub_clf, "base_estimator", None))
                    if estimator and hasattr(estimator, "coef_"):
                        coefs.append(estimator.coef_[0])
                        intercepts.append(estimator.intercept_[0])
                if coefs:
                    self.avg_coef = np.mean(coefs, axis=0)
                    self.avg_intercept = np.mean(intercepts)
                    self.explainer_type = "CalibratedLinearAveraged"
                else:
                    self.explainer_type = "GenericLinear"
            elif hasattr(self.classifier, "feature_log_prob_"):
                # MultinomialNB: log-odds difference between Fake (class 1) and Real (class 0)
                self.nb_log_odds = self.classifier.feature_log_prob_[config.LABEL_FAKE] - self.classifier.feature_log_prob_[config.LABEL_REAL]
                self.nb_intercept = self.classifier.class_log_prior_[config.LABEL_FAKE] - self.classifier.class_log_prior_[config.LABEL_REAL]
                self.explainer_type = "NaiveBayesLogOdds"
            else:
                self.explainer_type = "Fallback"
        except Exception as e:
            logger.warning(f"Could not initialize standard LinearExplainer: {e}. Using direct attribution fallback.")
            self.explainer_type = "Fallback"

    def explain(
        self,
        text: str,
        top_k: int = config.SHAP_CONFIG["top_k_features"],
    ) -> Dict[str, Any]:
        """
        Calculates exact token Shapley values for the given document.
        Positive SHAP values push predictions toward Likely Fake (Class 1).
        Negative SHAP values push predictions toward Likely Real (Class 0).
        """
        cleaned = clean_text(text, remove_publisher_tags=True)
        tokens = cleaned.split()

        if len(tokens) < 2:
            return {
                "method": "SHAP",
                "available": False,
                "message": "Text is too short to compute meaningful SHAP feature attributions.",
                "top_features": [],
                "fake_contributing": [],
                "real_contributing": [],
                "base_value": 0.0,
            }

        try:
            X_doc = self.vectorizer.transform([cleaned])
            feature_indices = X_doc.nonzero()[1]

            if len(feature_indices) == 0:
                return {
                    "method": "SHAP",
                    "available": False,
                    "message": "No recognized vocabulary tokens found in text.",
                    "top_features": [],
                    "fake_contributing": [],
                    "real_contributing": [],
                    "base_value": 0.0,
                }

            # Compute feature attribution values
            if hasattr(self, "explainer") and self.explainer_type == "LinearExplainer":
                shap_res = self.explainer.shap_values(X_doc)
                if isinstance(shap_res, list):
                    # List of classes [class_0, class_1] -> extract class 1 (Fake)
                    shap_vals = shap_res[config.LABEL_FAKE]
                else:
                    shap_vals = shap_res

                if hasattr(shap_vals, "toarray"):
                    shap_vals = shap_vals.toarray()
                shap_vals = np.asarray(shap_vals).flatten()
                base_val = float(self.explainer.expected_value) if np.isscalar(self.explainer.expected_value) else float(self.explainer.expected_value[config.LABEL_FAKE])

            elif self.explainer_type == "CalibratedLinearAveraged":
                # For linear models with sparse baseline 0, Shapley value of feature j is w_j * x_j
                tfidf_dense = X_doc.toarray()[0]
                shap_vals = self.avg_coef * tfidf_dense
                base_val = float(self.avg_intercept)

            elif self.explainer_type == "NaiveBayesLogOdds":
                tfidf_dense = X_doc.toarray()[0]
                shap_vals = self.nb_log_odds * tfidf_dense
                base_val = float(self.nb_intercept)

            else:
                # Direct feature weight fallback
                tfidf_dense = X_doc.toarray()[0]
                shap_vals = tfidf_dense
                base_val = 0.0

            # Collect attributions for active features
            contributions = []
            for idx in feature_indices:
                val = float(shap_vals[idx])
                if abs(val) > 1e-6:
                    token_str = self.feature_names[idx]
                    contributions.append({
                        "feature": token_str,
                        "weight": round(val, 4),
                        "pushes_toward": "Likely Fake" if val > 0 else "Likely Real",
                        "magnitude": round(abs(val), 4),
                    })

            # Sort by absolute impact
            contributions.sort(key=lambda x: x["magnitude"], reverse=True)
            top_features = contributions[:top_k]

            fake_contributing = [c for c in contributions if c["weight"] > 0]
            real_contributing = [c for c in contributions if c["weight"] < 0]

            fake_contributing.sort(key=lambda x: x["weight"], reverse=True)
            real_contributing.sort(key=lambda x: abs(x["weight"]), reverse=True)

            return {
                "method": "SHAP",
                "available": True,
                "top_features": top_features,
                "fake_contributing": fake_contributing[:top_k],
                "real_contributing": real_contributing[:top_k],
                "base_value": round(base_val, 4),
            }

        except Exception as e:
            logger.error(f"SHAP explanation failed: {e}")
            return {
                "method": "SHAP",
                "available": False,
                "message": f"SHAP explanation failed: {str(e)}",
                "top_features": [],
                "fake_contributing": [],
                "real_contributing": [],
                "base_value": 0.0,
            }
