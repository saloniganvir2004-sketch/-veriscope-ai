"""
VeriScope AI - Page 4: Model Performance & Comparative Benchmark
Displays rigorous evaluation metrics, confusion matrices, per-class performance,
and model selection rationale across Logistic Regression, Naive Bayes, and Linear SVM.
"""

import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

import config
from src.utils import (
    load_custom_css,
    render_brand_header,
    build_confusion_matrix_heatmap,
)
from src.evidence_bandit import EvidenceRetrievalBandit

st.set_page_config(page_title="Model Performance | VeriScope AI", page_icon="📈", layout="wide")
load_custom_css()

render_brand_header(
    title="Model Benchmarking & Evaluation Suite",
    subtitle="Rigorous empirical evaluation on strictly held-out test data across three classification architectures.",
)

# Load Saved Evaluation Artifacts
comp_file = config.METRICS_DIR / "model_comparison.json"
cm_file = config.METRICS_DIR / "confusion_matrices.json"
cr_file = config.METRICS_DIR / "classification_reports.json"

if not comp_file.exists():
    st.error("Model evaluation artifacts not found. Please run the training pipeline first.")
    st.stop()

with open(comp_file, "r") as f:
    model_comparison = json.load(f)

with open(cm_file, "r") as f:
    confusion_matrices = json.load(f)

with open(cr_file, "r") as f:
    classification_reports = json.load(f)

best_model = model_comparison.get("best_model_name", "Logistic Regression")

# Top Selection Banner
st.markdown(
    f"""
    <div class="veritas-card" style="border-left: 4px solid {config.COLOR_THEME['primary']};">
        <div class="veritas-card-header">
            Production Model Selection: {best_model}
        </div>
        <p style="color: #334155; font-size: 0.95rem; line-height: 1.6; margin: 0;">
            <strong>Selection Rationale:</strong> Model selection was conducted strictly using the
            <strong>validation partition Macro F1-score</strong>. {best_model} was selected due to its
            superior probabilistic calibration, continuous log-odds interpretability, and seamless mathematical
            integration with <code>shap.LinearExplainer</code>.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Benchmark Summary Table
st.markdown("### Comparative Performance Matrix (Held-Out Test Set)")

table_rows = []
for m_name, test_metrics in model_comparison.get("test_evaluations", {}).items():
    is_best = (m_name == best_model)
    table_rows.append({
        "Model Candidate": f"★ {m_name} (Selected)" if is_best else m_name,
        "Test Accuracy": f"{test_metrics['accuracy']*100:.2f}%",
        "Macro F1": f"{test_metrics['macro_f1']:.4f}",
        "Macro Precision": f"{test_metrics['macro_precision']:.4f}",
        "Macro Recall": f"{test_metrics['macro_recall']:.4f}",
    })

df_metrics = pd.DataFrame(table_rows)
st.dataframe(df_metrics, hide_index=True, width="stretch")

# Comparative Bar Chart
models = list(model_comparison.get("test_evaluations", {}).keys())
accuracies = [model_comparison["test_evaluations"][m]["accuracy"] * 100 for m in models]
f1_scores = [model_comparison["test_evaluations"][m]["macro_f1"] * 100 for m in models]
precisions = [model_comparison["test_evaluations"][m]["macro_precision"] * 100 for m in models]
recalls = [model_comparison["test_evaluations"][m]["macro_recall"] * 100 for m in models]

fig_comp = go.Figure()
fig_comp.add_trace(go.Bar(name="Accuracy", x=models, y=accuracies, marker_color=config.COLOR_THEME["primary"]))
fig_comp.add_trace(go.Bar(name="Macro F1", x=models, y=f1_scores, marker_color=config.COLOR_THEME["secondary"]))
fig_comp.add_trace(go.Bar(name="Precision", x=models, y=precisions, marker_color=config.COLOR_THEME["real"]))
fig_comp.add_trace(go.Bar(name="Recall", x=models, y=recalls, marker_color="#D97706"))

fig_comp.update_layout(
    barmode="group",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title=dict(text="Architecture Metric Comparison (%)", font=dict(color="#0F172A", size=13)),
    height=320,
    legend=dict(font=dict(color="#475569"), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(tickfont=dict(color="#0F172A")),
    yaxis=dict(title="Score (%)", range=[0, 105], tickfont=dict(color="#64748B"), gridcolor="#E2E8F0"),
)
st.plotly_chart(fig_comp, width="stretch")

st.write("")

# Deep-Dive Section for Selected Model
st.markdown("### Architecture Diagnostics & Confusion Analysis")

selected_model_inspect = st.selectbox(
    "Select Model Architecture to Inspect:",
    options=models,
    index=models.index(best_model) if best_model in models else 0,
)

diag_col1, diag_col2 = st.columns([1, 1])

with diag_col1:
    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                Confusion Matrix: {selected_model_inspect}
            </div>
        """,
        unsafe_allow_html=True,
    )
    if selected_model_inspect in confusion_matrices:
        cm = confusion_matrices[selected_model_inspect]
        fig_cm = build_confusion_matrix_heatmap(cm, config.LABEL_CLASSES)
        st.plotly_chart(fig_cm, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

with diag_col2:
    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                Per-Class Precision, Recall & F1
            </div>
        """,
        unsafe_allow_html=True,
    )
    if selected_model_inspect in classification_reports:
        cr = classification_reports[selected_model_inspect]
        class_rows = []
        for cls_name in config.LABEL_CLASSES:
            if cls_name in cr:
                class_rows.append({
                    "Class": cls_name,
                    "Precision": f"{cr[cls_name]['precision']:.4f}",
                    "Recall": f"{cr[cls_name]['recall']:.4f}",
                    "F1-Score": f"{cr[cls_name]['f1-score']:.4f}",
                    "Support": cr[cls_name]["support"],
                })
        st.dataframe(pd.DataFrame(class_rows), hide_index=True, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# REINFORCEMENT LEARNING CONTEXTUAL BANDIT ANALYTICS (SUBJECT D)
# =============================================================================
st.write("")
st.markdown("### Reinforcement Learning: Contextual Bandit Evidence Routing")
st.caption("Demonstrating MSc Subject D (Reinforcement Learning). An Upper Confidence Bound (UCB1) multi-armed bandit dynamically selects the optimal evidence-retrieval strategy.")

bandit = EvidenceRetrievalBandit()
b_stats = bandit.get_summary_statistics()

rl_col1, rl_col2 = st.columns([1.2, 1])

strategy_names = {
    "entity_focused": "Entity-Focused (Institutions & Dates)",
    "semantic_hybrid": "Semantic Hybrid (TF-IDF & Headline)",
    "keyphrase_ngram": "Keyphrase N-gram (Bigrams/Trigrams)",
}

with rl_col1:
    st.markdown(
        """
        <div class="veritas-card">
            <div class="veritas-card-header">
                Multi-Armed Strategy Value Estimates & Pull Counts
            </div>
            <p style="color: #64748B; font-size: 0.85rem; margin-bottom: 14px;">
                Online exploration-exploitation trade-off using UCB1: <code>A_t = argmax_a [ Q_t(a) + c √(ln(t) / N_t(a)) ]</code>.
            </p>
        """,
        unsafe_allow_html=True,
    )

    strategy_rows = []
    for s_id, s_label in strategy_names.items():
        pulls = b_stats["strategy_pulls"].get(s_id, 0)
        q_val = b_stats["estimated_values"].get(s_id, 0.0)
        is_best_rl = (s_id == b_stats["best_current_strategy"])
        strategy_rows.append({
            "Retrieval Strategy": f"★ {s_label}" if is_best_rl else s_label,
            "Total Decisions": pulls,
            "Estimated Value (Q)": f"{q_val:+.4f}",
            "Exploration Status": "Exploiting" if is_best_rl else "Active Exploration",
        })
    st.dataframe(pd.DataFrame(strategy_rows), hide_index=True, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

with rl_col2:
    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                RL Agent Diagnostics
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 8px;">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.88rem;">
                    <span style="color: #64748B;">Total Routing Decisions:</span>
                    <strong style="color: #0F172A;">{b_stats['total_decisions']}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.88rem;">
                    <span style="color: #64748B;">Mean Strategy Reward:</span>
                    <strong style="color: {config.COLOR_THEME['primary']};">{b_stats['mean_recent_reward']:+.3f}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; font-size: 0.88rem;">
                    <span style="color: #64748B;">Optimal Arm:</span>
                    <strong style="color: #15803D;">{strategy_names.get(b_stats['best_current_strategy'], b_stats['best_current_strategy'])}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.88rem;">
                    <span style="color: #64748B;">Action-Value Update:</span>
                    <span style="color: #334155; font-size: 0.82rem;">Incremental Sample-Average</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =============================================================================
# NATURAL LANGUAGE INFERENCE (NLI) & EVIDENCE VERIFICATION (SUBJECT B)
# =============================================================================
st.write("")
st.markdown("### Neural Natural Language Inference (NLI) Architecture")
st.caption("Demonstrating Subject B (Natural Language Processing). Cross-Encoder DeBERTa models evaluate logical entailment between evidence premises and claim hypotheses.")

nli_col1, nli_col2 = st.columns([1.2, 1])

with nli_col1:
    st.markdown(
        f"""
        <div class="veritas-card">
            <div class="veritas-card-header">
                Cross-Encoder NLI Specification
            </div>
            <p style="color: #64748B; font-size: 0.86rem; margin-bottom: 12px;">
                Pretrained sequence-pair cross-encoder mapping joint token representations to 3-way logical relations.
            </p>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px; margin-bottom: 12px; font-size: 0.88rem; line-height: 1.6;">
                <div><strong>Primary Architecture:</strong> <code>{config.NLI_MODEL_NAME}</code></div>
                <div><strong>Fallback Architecture:</strong> <code>{config.NLI_FALLBACK_MODEL_NAME}</code></div>
                <div><strong>Inference Formulation:</strong> Premise = Retrieved Evidence Passage &nbsp;|&nbsp; Hypothesis = Extracted User Claim</div>
                <div><strong>Optimization:</strong> Apple Silicon MPS acceleration with automatic CPU fallback</div>
            </div>
            <div style="font-size: 0.84rem; color: #475569;">
                <strong>Decision Thresholds:</strong> Entailment threshold $P \\ge 0.60$ · Contradiction threshold $P \\ge 0.60$ · Confidence margin $\\Delta \\ge 0.15$.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nli_col2:
    st.markdown(
        """
        <div class="veritas-card">
            <div class="veritas-card-header">
                Multi-Evidence Conservative Aggregation
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 8px; font-size: 0.88rem;">
                <div style="border-bottom: 1px solid #F1F5F9; padding-bottom: 6px;">
                    <strong style="color: #15803D;">Supported:</strong>
                    <span style="color: #64748B;">At least one verified source strongly entails the claim with zero credible refutations.</span>
                </div>
                <div style="border-bottom: 1px solid #F1F5F9; padding-bottom: 6px;">
                    <strong style="color: #DC2626;">Contradicted:</strong>
                    <span style="color: #64748B;">At least one verified fact-check refutes the claim with zero credible corroborations.</span>
                </div>
                <div>
                    <strong style="color: #475569;">Insufficient Evidence:</strong>
                    <span style="color: #64748B;">Passages are neutral, similarity is below threshold, or conflicting sources are detected.</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# Methodology & Calibration Notes
st.markdown("### Methodology & Probability Calibration")
st.markdown(
    """
    1. **Strict Data Leakage Controls:**
       - All wire-service publisher headers (e.g., `(Reuters)`, `(AP)`, `WASHINGTON —`) were stripped via regex before text transformation.
       - The TF-IDF vocabulary (5,000 max features, sublinear scaling) was **strictly fitted only on the 70% training split**.

    2. **Linear SVM Probability Calibration:**
       - Raw Support Vector Machines output signed geometric margin distances ($w^T x + b$), not true posterior probabilities.
       - To provide valid probabilities without test leakage, `LinearSVC` was calibrated using **Platt Sigmoid Scaling** via `CalibratedClassifierCV(method='sigmoid', cv=3)` on internal training folds.

    3. **Generalization Boundaries:**
       - While high accuracy is achieved on benchmark distributions, language deception patterns shift dynamically over time. Models should be monitored for concept drift when exposed to novel geopolitical topics.
    """
)
