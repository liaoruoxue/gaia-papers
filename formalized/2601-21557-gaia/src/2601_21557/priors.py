"""
Prior assignments for independent (leaf) claims in the MCE knowledge package.
Based on the paper: "Meta Context Engineering via Agentic Skill Evolution" (arXiv 2601.21557).
"""

from . import (
    # Motivation leaf claims (literature-reported biases)
    ce_bias_trajectory,
    ce_bias_list,
    ce_bias_graph,
    ce_brevity_bias,
    ce_bloat_bias,
    # MCE framework claim
    # (skill_unifies_levels is derived in Pass 3 — DO NOT set prior for derived claim)
    # Abduction components
    mce_predicts_improvement,
    alt_fixed_harness,
    pred_mce_better,
    pred_ace_competitive,
    # Empirical result claims (observed data — high confidence)
    mce_offline_gains,
    mce_online_gains,
    minimax_degrades_ace,
    # Ablation result claims (observed data — high confidence)
    ablation_bilevel_boost,
    ablation_agentic_base,
    ablation_fixed_skill_variance,
    # Complement alternative
    alt_model_capability,
    # Per-benchmark observation claims for induction (empirically observed)
    obs_finer,
    obs_uspto,
    obs_s2d,
    obs_law,
    obs_aegis,
)

PRIORS = {
    # ── Context Engineering biases (well-documented in literature) ─────────────
    ce_bias_trajectory: (
        0.88,
        "Richness-vs-generalization trade-off for case trajectories is well-documented across "
        "multiple CE papers (Wang 2024, Zhou 2025). High confidence in the limitation existing.",
    ),
    ce_bias_list: (
        0.85,
        "Flat list structure limitations are acknowledged and documented in Suzgun 2025 and Zhang 2026. "
        "Structural inexpressiveness is widely recognized.",
    ),
    ce_bias_graph: (
        0.82,
        "Graph memory latency and inconsistent retrieval gains are reported in Ai 2025, Xu 2025. "
        "Some uncertainty because graph approaches are actively improving.",
    ),
    ce_brevity_bias: (
        0.87,
        "GEPA's brevity bias is well-documented: the paper provides concrete token counts (1-2K) "
        "and notes failure on tasks requiring detail. High confidence.",
    ),
    ce_bloat_bias: (
        0.90,
        "ACE context bloat is empirically measured: up to 80K tokens after 5 epochs. "
        "Directly observable in the paper's Figure 3. Very high confidence.",
    ),

    # ── MCE design predictions and alternatives ────────────────────────────────
    mce_predicts_improvement: (
        0.82,
        "MCE's bi-level design is theoretically motivated, but its cross-domain superiority was "
        "not known before experiments. Moderate-high prior based on the theoretical motivation.",
    ),
    alt_fixed_harness: (
        0.40,
        "The fixed-harness alternative (ACE) has proven capable in prior work, but its structural "
        "limitations (rigidity, bloat) make it implausible that it achieves parity with a meta-level "
        "optimizer. Moderate prior reflecting ACE's genuine capability.",
    ),
    pred_mce_better: (
        0.75,
        "MCE's prediction of 5.6-53.8% improvement is directionally plausible given its design, "
        "though the exact range is uncertain before experiments. Moderate-high prior.",
    ),
    pred_ace_competitive: (
        0.35,
        "The claim that ACE can match a meta-level optimizer within 5% is implausible given "
        "the structural limitations of fixed harnesses. Low prior.",
    ),

    # ── Empirical result claims (directly observed, high confidence) ──────────
    mce_offline_gains: (
        0.95,
        "Table 1 of the paper directly reports these numbers. Results are from a controlled "
        "experimental setup with fair baselines. Very high confidence in the measurements.",
    ),
    mce_online_gains: (
        0.93,
        "Table 1 online setting results directly reported. Slightly lower confidence than offline "
        "due to single-pass constraint limiting MCE's full potential.",
    ),
    minimax_degrades_ace: (
        0.92,
        "Table 4 directly shows MiniMax M2.1 in ACE achieving 67% vs 70% with DeepSeek V3.1. "
        "This is a concrete empirical measurement. Very high confidence.",
    ),

    # ── Ablation results (directly observed) ──────────────────────────────────
    ablation_bilevel_boost: (
        0.92,
        "Table 3 directly shows 75% (full MCE) vs 73% (without skills). "
        "Concrete 2-point improvement on FiNER. High confidence.",
    ),
    ablation_agentic_base: (
        0.90,
        "Table 3 directly shows base-agent without skills: 73% vs ACE 71% offline, 67% vs ACE 64% online. "
        "Concrete empirical measurement. High confidence.",
    ),
    ablation_fixed_skill_variance: (
        0.85,
        "Table 3 shows fixed skill achieving 71% on FiNER (matching ACE), with noted high variance "
        "across tasks. Supported by qualitative discussion in the paper. High confidence.",
    ),

    # ── Complement alternative ─────────────────────────────────────────────────
    alt_model_capability: (
        0.15,
        "The model-capability explanation is ruled out empirically by Table 4 showing MiniMax M2.1 "
        "degrading ACE. Very low prior — the paper provides direct evidence against this.",
    ),

    # ── Per-benchmark observations (empirically measured, Table 1) ─────────────
    # These are the 'predictions' in the induction chain — each is a directly
    # measured empirical fact. Setting high priors anchors the induction correctly.
    obs_finer: (
        0.94,
        "MCE achieves 75% on FiNER vs ACE 71% — directly reported in Table 1. Very high confidence.",
    ),
    obs_uspto: (
        0.88,
        "MCE achieves 20% on USPTO-50k vs ACE 18% — directly reported in Table 1. "
        "Slightly lower confidence due to small absolute numbers (2pp gap).",
    ),
    obs_s2d: (
        0.95,
        "MCE achieves 89.2% vs ACE 79.2% on Symptom2Disease — directly reported, large 10pp margin.",
    ),
    obs_law: (
        0.91,
        "MCE achieves F1=0.70 vs ACE F1=0.65 on LawBench — directly reported in Table 1.",
    ),
    obs_aegis: (
        0.92,
        "MCE achieves F1=0.80 vs ACE F1=0.68 on AEGIS2 — directly reported in Table 1.",
    ),
}
