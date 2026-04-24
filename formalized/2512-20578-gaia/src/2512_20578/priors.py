"""Priors for the Gnosis self-awareness paper (arXiv 2512.20578).

All claims below are independent premises (leaf nodes in the BP graph).
Priors reflect reviewer confidence that the claim is true as stated,
informed by the paper's evidence, experimental rigor, and domain context.

Empirical observation claims (data tables, ablations, measured results):
  Confidence is high (0.90-0.95) — directly reported numbers from the paper.

Theoretical/hypothesis claims:
  Confidence is moderate (0.65-0.82) — the paper's interpretations.

Alternative/null hypothesis claims:
  Confidence is low (0.20-0.40) — competing explanations.
"""

from . import (
    # Contradiction node
    external_always_superior,
    # Motivation / background weaknesses
    external_judge_weakness,
    multi_sample_weakness,
    text_critique_weakness,
    internal_probe_weakness,
    chain_of_embedding_weakness,
    verbalized_conf_weakness,
    reward_model_cost,
    # Architecture descriptions
    hidden_circuit_arch,
    gated_fusion_arch,
    training_protocol,
    # Performance data tables
    gnosis_math_perf,
    gnosis_trivia_perf,
    gnosis_mmlu_perf,
    external_judge_perf,
    mlp_probe_perf,
    # Ablation data
    hidden_only_perf,
    attention_only_perf,
    cnn_stats_perf,
    attention_topology_ablation,
    attention_grid_ablation,
    hidden_component_ablation,
    # Transfer results
    transfer_math_results,
    transfer_trivia_results,
    transfer_mmlu_results,
    # Backbone stats
    backbone_accuracy_stats,
    # Interpretation / hypothesis
    shared_circuits_hypothesis,
    pred_shared,
    pred_no_shared,
    pred_gnosis_math,
    pred_ext_math,
    feature_analysis,
    # Limitation claims
    proprietary_model_limitation,
    transfer_fails_cross_family,
    # Alternatives (abduction)
    alt_external_math,
    alt_transfer_accidental,
)

PRIORS = {
    # ── Contradiction node ────────────────────────────────────────────────────
    external_always_superior: (
        0.08,
        "The claim that external judges always outperform internal probes is refuted "
        "by the paper's results: Gnosis (internal, ~5M params) achieves AUROC 0.95 vs "
        "Skywork-8B (external, 8B params) at 0.90. The universal claim is very likely false."
    ),

    # ── Motivation / Background weaknesses ────────────────────────────────────
    external_judge_weakness: (
        0.88,
        "Well-documented: reward models and proprietary judges require significant "
        "extra compute. The paper provides concrete latency numbers (930ms, 2465ms) "
        "and AUROC comparisons."
    ),
    multi_sample_weakness: (
        0.82,
        "Self-consistency sampling cost is trivially verifiable (k completions = k× cost). "
        "Correlation weakness with per-instance correctness acknowledged in prior literature."
    ),
    text_critique_weakness: (
        0.80,
        "Verbalized confidence calibration failure is well-documented. "
        "The paper does not provide its own ablation; relies on prior work."
    ),
    internal_probe_weakness: (
        0.78,
        "The limitation of single-snapshot probes is conceptually well-argued. "
        "Indirect evidence via MLP-Prob baseline comparison in the paper."
    ),
    chain_of_embedding_weakness: (
        0.72,
        "CoE's limitation (no task-specific supervision) is a reasonable critique, "
        "but CoE is not directly ablated in the paper's main benchmarks."
    ),
    verbalized_conf_weakness: (
        0.80,
        "Supported by existing literature (Xiong et al. 2024). "
        "Claimed without direct experiment in this paper."
    ),
    reward_model_cost: (
        0.95,
        "Concrete latency numbers from Table 4 are directly measured. "
        "High confidence in these empirical values."
    ),

    # ── Architecture descriptions ──────────────────────────────────────────────
    hidden_circuit_arch: (
        0.92,
        "Architecture description from paper Section 3.1. "
        "High confidence it accurately describes the implemented system."
    ),
    gated_fusion_arch: (
        0.92,
        "Architecture description from Section 3.3. High confidence."
    ),
    training_protocol: (
        0.90,
        "Training details from Section 3.4 and Appendix. Dataset sizes and "
        "cost figures are directly reported. Slight uncertainty on full reproducibility."
    ),

    # ── Empirical performance data (Tables) ───────────────────────────────────
    gnosis_math_perf: (
        0.93,
        "Table 1 data directly reported. High confidence in accuracy of transcription. "
        "Small residual uncertainty on evaluation methodology details."
    ),
    gnosis_trivia_perf: (
        0.93,
        "Table 1 data directly reported. High confidence."
    ),
    gnosis_mmlu_perf: (
        0.92,
        "Table 1 data directly reported. Slightly lower confidence for MMLU-Pro "
        "as AUPR-e is notably weaker (0.56) indicating harder error detection task."
    ),
    external_judge_perf: (
        0.92,
        "External baseline data from Table 1. High confidence in reported numbers."
    ),
    mlp_probe_perf: (
        0.93,
        "Table 2 data directly reported. MLP-Prob baseline implemented by same authors; "
        "numbers are highly reliable."
    ),
    hidden_only_perf: (
        0.92,
        "Table 5 ablation data directly reported. High confidence."
    ),
    attention_only_perf: (
        0.92,
        "Table 5 ablation data directly reported. High confidence."
    ),
    cnn_stats_perf: (
        0.91,
        "Table 6 ablation data directly reported. High confidence."
    ),
    attention_topology_ablation: (
        0.91,
        "Table 7 ablation data directly reported. High confidence."
    ),
    attention_grid_ablation: (
        0.91,
        "Table 8 ablation data directly reported. High confidence."
    ),
    hidden_component_ablation: (
        0.92,
        "Table 9 ablation data directly reported. High confidence."
    ),
    backbone_accuracy_stats: (
        0.93,
        "Table 11 backbone outcome statistics directly reported. High confidence."
    ),

    # ── Transfer results ──────────────────────────────────────────────────────
    transfer_math_results: (
        0.92,
        "Table 3 transfer results directly reported. High confidence."
    ),
    transfer_trivia_results: (
        0.91,
        "Table 3 transfer results directly reported. High confidence."
    ),
    transfer_mmlu_results: (
        0.91,
        "Table 3 transfer results directly reported. High confidence."
    ),

    # ── Interpretation / Hypothesis claims ────────────────────────────────────
    shared_circuits_hypothesis: (
        0.68,
        "The shared internal circuit hypothesis is the paper's interpretation of "
        "transfer success. Plausible but not verified by direct circuit-level analysis. "
        "Transfer data supports it but alternative explanations exist."
    ),
    pred_shared: (
        0.72,
        "Prediction derived from shared_circuits_hypothesis. Moderate confidence "
        "matching the hypothesis's credibility."
    ),
    pred_no_shared: (
        0.30,
        "Prediction that transfer would fail if circuits differ. Low prior because "
        "the paper's results contradict this prediction."
    ),
    pred_gnosis_math: (
        0.85,
        "Prediction about Gnosis math performance. High prior because this "
        "prediction is directly confirmed by Table 1."
    ),
    pred_ext_math: (
        0.85,
        "Prediction about external judge performance. High prior — directly "
        "confirmed by Table 1 baselines."
    ),
    feature_analysis: (
        0.82,
        "Visualization-based analysis. Results are qualitative ('clear separation') "
        "without statistical significance testing. Moderate confidence."
    ),

    # ── Limitation claims ─────────────────────────────────────────────────────
    proprietary_model_limitation: (
        0.97,
        "Fundamental architectural constraint: proprietary API models do not expose "
        "internal activations. This is a hard constraint, not an empirical claim."
    ),
    transfer_fails_cross_family: (
        0.80,
        "Cross-family transfer failure described in paper's limitations. "
        "Not directly tested with full ablation tables; some uncertainty remains."
    ),

    # ── Alternative hypotheses (for abduction) ────────────────────────────────
    alt_external_math: (
        0.35,
        "Alternative: external judges explain math benchmark as well as Gnosis. "
        "Low prior because observed AUROC (0.90-0.91) is clearly below Gnosis (0.95). "
        "The alternative does not explain the observation as well as the hypothesis."
    ),
    alt_transfer_accidental: (
        0.28,
        "Alternative: transfer success due to dataset-level similarity not shared circuits. "
        "Low prior because this predicts random-level transfer on architecturally different "
        "models, which is not observed."
    ),
}
