"""
VeriScope AI - Natural Language Inference (NLI) Claim Verification Engine
Demonstrates genuine cross-encoder neural entailment/contradiction inference.

Architecture & Pipeline:
  Premise:    Retrieved verified evidence passage from reference archives
  Hypothesis: Specific user claim / headline to be audited
  Inference:  Pretrained DeBERTa Cross-Encoder (e.g. cross-encoder/nli-deberta-v3-base)
  Output:     Calibrated probabilities for Entailment, Contradiction, and Neutral

Epistemic Rigor:
  - Genuine neural inference: never fabricates NLI confidence or replaces inference with heuristics.
  - Conservative multi-evidence aggregation: flags conflicting sources explicitly.
  - Safe lazy loading and device selection (MPS Apple Silicon acceleration with CPU fallback).
  - Explicit 'Verification Unavailable' state if model dependencies or weights are inaccessible.
"""

import logging
from typing import Dict, Any, List, Optional, Tuple

import config

logger = logging.getLogger("VeriScopeNLI")

# Module-level cached verifier instance
_GLOBAL_NLI_VERIFIER: Optional["NLIVerifier"] = None


def is_nli_available() -> Tuple[bool, str]:
    """
    Checks if PyTorch and HuggingFace Transformers are importable
    and functional in the current runtime environment.
    """
    try:
        import torch
        import transformers
        return True, f"PyTorch {torch.__version__} & Transformers {transformers.__version__} available"
    except ImportError as e:
        return False, f"Missing dependency: {str(e)}. Install with: pip install torch transformers sentencepiece"
    except Exception as e:
        return False, f"Environment check failed: {str(e)}"


class NLIVerifier:
    """
    Neural Natural Language Inference (NLI) Verifier.
    Performs cross-encoder pair classification mapping (Premise, Hypothesis) to
    probabilities over {Contradiction, Entailment, Neutral}.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        device_preference: Optional[str] = None,
    ):
        self.model_name = model_name or getattr(config, "NLI_MODEL_NAME", "cross-encoder/nli-deberta-v3-base")
        self.fallback_model_name = getattr(config, "NLI_FALLBACK_MODEL_NAME", "cross-encoder/nli-deberta-v3-small")
        self.device_preference = device_preference or config.NLI_CONFIG.get("device_preference", "mps")

        self.model = None
        self.tokenizer = None
        self.device = None
        self.label_mapping: Dict[int, str] = {}
        self.is_loaded = False
        self.load_error: Optional[str] = None
        self._mock_inference_func = None

    def set_mock_inference(self, mock_func=None):
        """Allows test suites to simulate NLI model output deterministically."""
        self._mock_inference_func = mock_func

    def _select_device(self):
        """Selects optimal hardware acceleration on Apple Silicon Mac M5."""
        import torch
        if self.device_preference == "mps" and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            try:
                # Test MPS allocation
                t = torch.zeros(1, device="mps")
                del t
                logger.info("Using Apple Silicon MPS acceleration for NLI inference.")
                return torch.device("mps")
            except Exception as e:
                logger.warning(f"MPS initialization failed ({e}), falling back to CPU.")
        logger.info("Using CPU for NLI inference.")
        return torch.device("cpu")

    def load_model(self) -> bool:
        """
        Lazily loads the pretrained NLI cross-encoder model and tokenizer.
        Guarantees that weights are loaded once and cached in memory.
        """
        if self.is_loaded and self.model is not None and self.tokenizer is not None:
            return True

        avail, reason = is_nli_available()
        if not avail:
            self.load_error = reason
            logger.warning(f"Cannot load NLI model: {reason}")
            return False

        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForSequenceClassification

            self.device = self._select_device()
            logger.info(f"Loading NLI cross-encoder model: {self.model_name}...")

            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            except Exception as load_primary_err:
                logger.warning(f"Failed loading primary model {self.model_name} ({load_primary_err}). Trying fallback: {self.fallback_model_name}")
                self.model_name = self.fallback_model_name
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

            self.model.to(self.device)
            self.model.eval()

            # Inspect model id2label mapping
            raw_id2label = getattr(self.model.config, "id2label", None)
            if raw_id2label and isinstance(raw_id2label, dict):
                # Standardize label strings to lowercase ('entailment', 'contradiction', 'neutral')
                self.label_mapping = {int(k): str(v).lower() for k, v in raw_id2label.items()}
            else:
                # Default mapping for cross-encoder/nli-deberta models:
                # 0: contradiction, 1: entailment, 2: neutral
                self.label_mapping = {0: "contradiction", 1: "entailment", 2: "neutral"}

            self.is_loaded = True
            self.load_error = None
            logger.info(f"NLI model successfully loaded on {self.device}. Labels: {self.label_mapping}")
            return True

        except Exception as e:
            self.is_loaded = False
            self.load_error = str(e)
            logger.error(f"Error loading NLI model weights: {e}")
            return False

    def verify_pair(self, premise: str, hypothesis: str) -> Dict[str, Any]:
        """
        Runs neural NLI inference on a single (Premise, Hypothesis) pair.

        Parameters:
            premise: Verified reference evidence passage text.
            hypothesis: User-submitted claim or headline.

        Returns:
            Dict containing:
                - available: bool (whether genuine inference ran)
                - probabilities: {entailment, contradiction, neutral}
                - stance: 'SUPPORTS' | 'CONTRADICTS' | 'NEUTRAL'
                - confidence: highest probability value
                - margin: |P(entailment) - P(contradiction)|
                - premise: str
                - hypothesis: str
                - model_name: str
        """
        clean_premise = (premise or "").strip()
        clean_hypothesis = (hypothesis or "").strip()

        if self._mock_inference_func is not None:
            return self._mock_inference_func(clean_premise, clean_hypothesis)

        if not clean_premise or not clean_hypothesis:
            return {
                "available": True,
                "probabilities": {"entailment": 0.0, "contradiction": 0.0, "neutral": 1.0},
                "stance": "NEUTRAL",
                "confidence": 1.0,
                "margin": 0.0,
                "premise": clean_premise,
                "hypothesis": clean_hypothesis,
                "error": "Empty premise or hypothesis text",
                "model_name": self.model_name,
            }

        if not self.is_loaded:
            success = self.load_model()
            if not success:
                return {
                    "available": False,
                    "probabilities": {"entailment": 0.0, "contradiction": 0.0, "neutral": 0.0},
                    "stance": "UNAVAILABLE",
                    "confidence": 0.0,
                    "margin": 0.0,
                    "premise": clean_premise,
                    "hypothesis": clean_hypothesis,
                    "error": self.load_error or "NLI model weights not loaded",
                    "model_name": self.model_name,
                }

        try:
            import torch

            max_len = config.NLI_CONFIG.get("max_length", 512)
            inputs = self.tokenizer(
                clean_premise,
                clean_hypothesis,
                truncation=True,
                max_length=max_len,
                return_tensors="pt",
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs_tensor = torch.softmax(logits, dim=-1).squeeze(0)

            raw_probs = probs_tensor.cpu().tolist()

            # Map to standard labels
            probs = {"entailment": 0.0, "contradiction": 0.0, "neutral": 0.0}
            for idx, prob_val in enumerate(raw_probs):
                lbl_name = self.label_mapping.get(idx, f"label_{idx}")
                if "entail" in lbl_name:
                    probs["entailment"] = round(float(prob_val), 4)
                elif "contra" in lbl_name:
                    probs["contradiction"] = round(float(prob_val), 4)
                else:
                    probs["neutral"] = round(float(prob_val), 4)

            # Decision criteria
            ent_thresh = config.NLI_CONFIG.get("entailment_threshold", 0.60)
            contra_thresh = config.NLI_CONFIG.get("contradiction_threshold", 0.60)
            margin_thresh = config.NLI_CONFIG.get("neutral_margin", 0.15)

            p_ent = probs["entailment"]
            p_contra = probs["contradiction"]
            p_neu = probs["neutral"]

            margin = abs(p_ent - p_contra)

            if p_ent >= ent_thresh and (p_ent - p_contra) >= margin_thresh:
                stance = "SUPPORTS"
                confidence = p_ent
            elif p_contra >= contra_thresh and (p_contra - p_ent) >= margin_thresh:
                stance = "CONTRADICTS"
                confidence = p_contra
            else:
                stance = "NEUTRAL"
                confidence = max(p_neu, 1.0 - margin)

            return {
                "available": True,
                "probabilities": probs,
                "stance": stance,
                "confidence": round(confidence, 4),
                "margin": round(margin, 4),
                "premise": clean_premise,
                "hypothesis": clean_hypothesis,
                "model_name": self.model_name,
                "device": str(self.device),
            }

        except Exception as e:
            logger.error(f"NLI pair inference failed: {e}")
            return {
                "available": False,
                "probabilities": {"entailment": 0.0, "contradiction": 0.0, "neutral": 0.0},
                "stance": "UNAVAILABLE",
                "confidence": 0.0,
                "margin": 0.0,
                "premise": clean_premise,
                "hypothesis": clean_hypothesis,
                "error": str(e),
                "model_name": self.model_name,
            }

    def verify_claim_against_passages(
        self,
        claim: str,
        passages: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Evaluates a claim against multiple retrieved evidence passages individually,
        then performs principled, conservative evidence aggregation.

        Aggregation Principles:
          1. Individual evaluation: Every evidence passage is verified as a premise.
          2. Conflict detection: If one credible source supports and another refutes,
             the system explicitly flags a conflict rather than choosing arbitrarily.
          3. Conservative verdict: Insufficient Evidence is returned when passages
             are neutral, low-confidence, or lack decisive corroboration.
        """
        if not claim or not claim.strip():
            return {
                "final_verdict": "Insufficient Evidence",
                "badge_style": "badge-insufficient",
                "overall_confidence": 0.0,
                "conflict_detected": False,
                "reasoning": "No claim text provided for verification.",
                "passage_evaluations": [],
                "nli_available": True,
                "mean_margin": 0.0,
            }

        if not passages:
            return {
                "final_verdict": "Insufficient Evidence",
                "badge_style": "badge-insufficient",
                "overall_confidence": 0.0,
                "conflict_detected": False,
                "reasoning": "No relevant reference passages were retrieved above the similarity threshold.",
                "passage_evaluations": [],
                "nli_available": True,
                "mean_margin": 0.0,
            }

        # Deduplicate passages to ensure distinct evidence identities
        unique_passages: List[Dict[str, Any]] = []
        seen_ids = set()
        seen_texts = set()
        for p in passages:
            p_id = str(p.get("id", "")).strip()
            p_text = str(p.get("passage", "")).strip()
            if p_id and p_id in seen_ids:
                continue
            if p_text and p_text in seen_texts:
                continue
            if p_id:
                seen_ids.add(p_id)
            if p_text:
                seen_texts.add(p_text)
            unique_passages.append(p)

        evaluations: List[Dict[str, Any]] = []
        support_count = 0
        contradict_count = 0
        neutral_count = 0
        total_margin = 0.0
        nli_available_any = False

        for p_idx, p in enumerate(unique_passages):
            passage_text = p.get("passage", "")
            nli_res = self.verify_pair(premise=passage_text, hypothesis=claim)

            if nli_res["available"]:
                nli_available_any = True

            probs = nli_res.get("probabilities", {})
            p_ent = probs.get("entailment", 0.0)
            p_contra = probs.get("contradiction", 0.0)
            raw_stance = nli_res.get("stance", "NEUTRAL")

            is_supporting = (raw_stance == "SUPPORTS" or (p_ent >= 0.60 and p_ent > p_contra))
            is_contradicting = (raw_stance == "CONTRADICTS" or (p_contra >= 0.60 and p_contra > p_ent))

            if is_supporting and not is_contradicting:
                support_count += 1
                stance = "SUPPORTS"
            elif is_contradicting and not is_supporting:
                contradict_count += 1
                stance = "CONTRADICTS"
            else:
                neutral_count += 1
                stance = "NEUTRAL"

            margin = nli_res.get("margin", abs(p_ent - p_contra))
            total_margin += margin

            eval_entry = {
                "passage_index": p_idx,
                "passage_id": p.get("id", f"P-{p_idx+1}"),
                "title": p.get("title", "Untitled Passage"),
                "publisher": p.get("publisher", p.get("source", "Reference Source")),
                "date": p.get("date", "Undated"),
                "url": p.get("url", "#"),
                "passage_excerpt": passage_text[:280] + ("..." if len(passage_text) > 280 else ""),
                "similarity_score": p.get("similarity_score", 0.0),
                "nli_stance": stance,
                "probabilities": probs,
                "nli_confidence": nli_res.get("confidence", max(p_ent, p_contra)),
                "margin": margin,
                "provenance_type": p.get("provenance_type", "OFFICIAL_INSTITUTION"),
            }
            evaluations.append(eval_entry)

        mean_margin = round(total_margin / len(unique_passages), 4) if unique_passages else 0.0

        # If NLI model was completely unavailable
        if not nli_available_any and self.load_error:
            return {
                "final_verdict": "Insufficient Evidence",
                "badge_style": "badge-insufficient",
                "overall_confidence": 0.0,
                "conflict_detected": False,
                "reasoning": (
                    f"Neural NLI inference could not be executed ({self.load_error}). "
                    "In adherence to academic integrity, rule-based heuristics will not be substituted for neural NLI."
                ),
                "passage_evaluations": evaluations,
                "nli_available": False,
                "mean_margin": 0.0,
            }

        # Multi-Evidence Aggregation Logic
        conflict_detected = (support_count > 0 and contradict_count > 0)

        if conflict_detected:
            final_verdict = "Insufficient Evidence"
            badge_style = "badge-insufficient"
            reasoning = (
                f"Conflicting evidence detected across retrieved records ({support_count} supporting vs {contradict_count} refuting). "
                "Because verified sources yield conflicting stances on this specific assertion, the platform conservatively "
                "withholds a definitive truth verdict pending further corroboration."
            )
            overall_confidence = 0.50

        elif contradict_count > 0:
            final_verdict = "Contradicted by Available Evidence"
            badge_style = "badge-fake"
            top_contra = max((e for e in evaluations if e["nli_stance"] == "CONTRADICTS"), key=lambda x: x["nli_confidence"])
            p_name = top_contra["publisher"]
            p_prob = top_contra["probabilities"].get("contradiction", top_contra["nli_confidence"])
            reasoning = (
                f"Verified dispatches from {p_name} directly contradict the submitted claim with {p_prob*100:.1f}% NLI contradiction confidence. "
                f"The premise logically refutes key assertions in the headline."
            )
            overall_confidence = p_prob

        elif support_count > 0:
            final_verdict = "Supported by Available Evidence"
            badge_style = "badge-real"
            top_sup = max((e for e in evaluations if e["nli_stance"] == "SUPPORTS"), key=lambda x: x["nli_confidence"])
            p_name = top_sup["publisher"]
            p_prob = top_sup["probabilities"].get("entailment", top_sup["nli_confidence"])
            reasoning = (
                f"Factual records from {p_name} logically entail this claim with {p_prob*100:.1f}% NLI entailment confidence. "
                f"The evidence independently confirms the core assertion."
            )
            overall_confidence = p_prob

        else:
            final_verdict = "Insufficient Evidence"
            badge_style = "badge-insufficient"
            reasoning = (
                "The retrieved evidence passages do not provide decisive entailment or contradiction regarding this specific claim "
                f"(NLI evaluated {neutral_count} passages as neutral or ambiguous). External records neither confirm nor refute the assertion."
            )
            overall_confidence = 0.20

        return {
            "final_verdict": final_verdict,
            "badge_style": badge_style,
            "overall_confidence": round(overall_confidence, 4),
            "conflict_detected": conflict_detected,
            "support_count": support_count,
            "contradict_count": contradict_count,
            "neutral_count": neutral_count,
            "reasoning": reasoning,
            "passage_evaluations": evaluations,
            "nli_available": nli_available_any,
            "mean_margin": mean_margin,
            "model_name": self.model_name,
        }


def get_nli_verifier() -> NLIVerifier:
    """Returns the process-wide cached singleton NLIVerifier."""
    global _GLOBAL_NLI_VERIFIER
    if _GLOBAL_NLI_VERIFIER is None:
        _GLOBAL_NLI_VERIFIER = NLIVerifier()
    return _GLOBAL_NLI_VERIFIER
