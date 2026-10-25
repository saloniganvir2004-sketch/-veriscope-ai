"""
VeriScope AI - Reinforcement Learning Contextual Bandit for Evidence Retrieval
Demonstrates Subject D (Reinforcement Learning: Algorithms and Applications).
Dynamically selects among evidence-search strategies based on query context
(entity density, sensationalism index, length), updating action-value estimates
from measured retrieval rewards.
"""

import json
import math
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

import config

logger = logging.getLogger("VeriScopeRLBandit")

BANDIT_STATE_PATH = config.ARTIFACTS_DIR / "rl_bandit_state.json"

# Three discrete evidence-retrieval search strategies (Arms)
STRATEGIES = [
    "entity_focused",       # Emphasizes named entities, institutions, and dates
    "semantic_hybrid",      # Balances TF-IDF keyword weights and headline semantics
    "keyphrase_ngram",      # Emphasizes contiguous bigram and trigram keyphrases
]


class EvidenceRetrievalBandit:
    """
    Upper Confidence Bound (UCB1) Contextual Multi-Armed Bandit for selecting
    optimal evidence retrieval strategies.

    Mathematical Formulation:
        A_t = argmax_a [ Q_t(a) + c * sqrt(ln(t) / N_t(a)) ]
    where:
        Q_t(a) is the estimated action value for strategy a,
        N_t(a) is the number of times strategy a has been selected,
        t is total retrieval trials,
        c is the exploration parameter (default c = 1.0).
    """

    def __init__(self, state_path: Path = BANDIT_STATE_PATH, exploration_c: float = 1.0):
        self.state_path = state_path
        self.exploration_c = exploration_c
        self.strategies = STRATEGIES
        self.counts: Dict[str, int] = {s: 0 for s in self.strategies}
        self.values: Dict[str, float] = {s: 0.0 for s in self.strategies}
        self.total_trials: int = 0
        self.reward_history: List[Dict[str, Any]] = []
        self._load_state()

    def _load_state(self) -> None:
        """Loads persisted bandit counts and value estimates from JSON."""
        if self.state_path.exists():
            try:
                data = json.loads(self.state_path.read_text(encoding="utf-8"))
                self.counts = data.get("counts", {s: 0 for s in self.strategies})
                self.values = data.get("values", {s: 0.0 for s in self.strategies})
                self.total_trials = data.get("total_trials", 0)
                self.reward_history = data.get("reward_history", [])[-50:]  # Keep recent 50
            except Exception as e:
                logger.warning(f"Could not load bandit state from {self.state_path}: {e}")

    def save_state(self) -> None:
        """Persists bandit policy state to artifacts directory."""
        try:
            payload = {
                "counts": self.counts,
                "values": {k: round(v, 4) for k, v in self.values.items()},
                "total_trials": self.total_trials,
                "reward_history": self.reward_history[-50:],
            }
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            self.state_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to persist bandit state: {e}")

    def select_strategy(self, context: Optional[Dict[str, Any]] = None) -> Tuple[str, Dict[str, float]]:
        """
        Selects the optimal retrieval strategy using UCB1 with contextual adjustment.
        If any strategy has 0 trials, it is chosen first to initialize action values.
        """
        self.total_trials += 1
        t = self.total_trials

        # 1. Warm-up: ensure each arm is pulled at least once
        for s in self.strategies:
            if self.counts[s] == 0:
                return s, {k: 0.0 for k in self.strategies}

        # 2. Contextual heuristic adjustments
        # e.g., if entity count is high, give a slight contextual prior to entity_focused
        context_boost: Dict[str, float] = {s: 0.0 for s in self.strategies}
        if context:
            entity_count = context.get("entity_count", 0)
            sensationalism = context.get("sensationalism_score", 0.0)

            if entity_count >= 2:
                context_boost["entity_focused"] += 0.15
            if sensationalism > 0.4:
                context_boost["keyphrase_ngram"] += 0.10
            context_boost["semantic_hybrid"] += 0.05

        # 3. Compute UCB scores
        ucb_scores: Dict[str, float] = {}
        for s in self.strategies:
            exploitation = self.values[s] + context_boost[s]
            exploration = self.exploration_c * math.sqrt(math.log(t) / self.counts[s])
            ucb_scores[s] = exploitation + exploration

        best_strategy = max(ucb_scores, key=lambda k: ucb_scores[k])
        return best_strategy, {k: round(v, 4) for k, v in ucb_scores.items()}

    def update(self, strategy: str, reward: float) -> None:
        """
        Incremental value update using running sample-average:
            Q_{n+1} = Q_n + (1 / n) * (R - Q_n)
        Reward scale: [-1.0, +1.0]
        """
        if strategy not in self.strategies:
            return

        self.counts[strategy] += 1
        n = self.counts[strategy]
        old_val = self.values[strategy]
        self.values[strategy] = old_val + (1.0 / n) * (reward - old_val)

        self.reward_history.append({
            "trial": self.total_trials,
            "strategy": strategy,
            "reward": round(reward, 3),
            "new_value": round(self.values[strategy], 3),
        })
        self.save_state()

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Returns empirical analytics for UI inspection and BI reporting."""
        avg_reward = (
            sum(r["reward"] for r in self.reward_history) / len(self.reward_history)
            if self.reward_history
            else 0.0
        )
        return {
            "total_decisions": self.total_trials,
            "strategy_pulls": self.counts,
            "estimated_values": {k: round(v, 4) for k, v in self.values.items()},
            "mean_recent_reward": round(avg_reward, 3),
            "best_current_strategy": max(self.values, key=lambda k: self.values[k]),
        }


def compute_retrieval_reward(
    top_similarity: float,
    verdict: Optional[str] = None,
    source_count: int = 1,
    entity_coverage: float = 0.5,
    nli_margin: float = 0.0,
) -> float:
    """
    Computes an objective, non-circular reward measuring Evidence Retrieval Quality.

    Academic Rationale (Subject D - Reinforcement Learning):
    The retrieval bandit learns to select the optimal query formulation strategy
    (entity_focused, semantic_hybrid, keyphrase_ngram) to maximize document relevance
    and information gain. Critically, the reward signal MUST NOT depend on whether the
    factual outcome is True or False; instead, it rewards:
      1. Retrieval relevance (cosine similarity between query and evidence)
      2. Entity grounding (proportion of query entities retrieved)
      3. Informativeness (NLI discriminative margin between entailment and contradiction)
      4. Penalizing empty or irrelevant retrievals.

    This eliminates circular confirmation bias while optimizing the search policy.
    Reward scale: strictly bounded in [-1.0, +1.0].
    """
    if source_count == 0 or top_similarity < 0.05:
        return -0.5  # Retrieval failure penalty

    # Core relevance score: scaled similarity [0, 1]
    relevance_score = min(max(top_similarity / 0.30, 0.0), 1.0)

    # Entity grounding score: [0, 1]
    grounding_score = min(max(entity_coverage, 0.0), 1.0)

    # NLI informativeness score: decisive margin |P(entail) - P(contradict)|
    info_score = min(max(nli_margin, 0.0), 1.0)

    # Composite objective reward (relevance 50%, grounding 30%, informativeness 20%)
    composite = 0.50 * relevance_score + 0.30 * grounding_score + 0.20 * info_score

    # Map to [-0.2, +1.0] for successful retrieval
    reward = round(-0.2 + 1.2 * composite, 3)
    return float(max(min(reward, 1.0), -1.0))
