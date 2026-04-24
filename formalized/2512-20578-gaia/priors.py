"""Priors for the Gnosis self-awareness paper (arXiv 2512.20578).

All claims below are independent premises (leaf nodes in the BP graph).
Priors reflect author/reviewer confidence that the claim is true as stated,
informed by the paper's evidence, experimental rigor, and domain context.

Empirical observation claims (data tables, ablations, measured results):
  These come from paper's Tables 1-11 and are directly reported. Confidence
  is high (0.90-0.95) unless there is reason to doubt measurement reliability.

Theoretical/hypothesis claims:
  These express the paper's interpretations. Confidence is moderate (0.65-0.82).

Alternative/null hypothesis claims:
  These represent competing explanations. Confidence is low (0.20-0.40).
"""

from gaia.lang import prior

# ── Anonymous internal node ────────────────────────────────────────────────────
# _anon_002 is the compiler-generated contradiction helper (not_both_true)
# for the contradiction(external_always_superior, gnosis_superior_overall) operator.
# Prior on "not both can be true simultaneously" is very high.
prior("_anon_002", 0.95,
      "The external-judge-always-superior claim and Gnosis superiority claim "
      "cannot both be true; this disjunction is very likely satisfied.")

# ── Motivation / Background weaknesses ────────────────────────────────────────
prior("external_judge_weakness", 0.88,
      "Well-documented in the literature: reward models and proprietary judges "
      "require significant extra compute and often disagree with correctness. "
      "The paper provides concrete latency numbers (930ms, 2465ms) and AUROC data.")

prior("multi_sample_weakness", 0.82,
      "Self-consistency sampling costs are trivially verifiable (k completions = k× cost). "
      "The correlation weakness with per-instance correctness is acknowledged in literature "
      "but less rigorously quantified in this paper.")

prior("text_critique_weakness", 0.80,
      "Verbalized confidence calibration failure is well-documented in the literature. "
      "The paper does not provide its own ablation of this; claim rests on prior work.")

prior("internal_probe_weakness", 0.78,
      "The limitation of single-snapshot probes is conceptually well-argued. "
      "The paper provides indirect evidence via MLP-Prob baseline comparison.")

prior("chain_of_embedding_weakness", 0.72,
      "CoE's limitation (no task-specific supervision) is a reasonable critique, "
      "but CoE is not directly evaluated in this paper's main benchmarks.")

prior("verbalized_conf_weakness", 0.80,
      "Supported by existing literature (Xiong et al. 2024). "
      "Claimed without direct experiment in this paper.")

prior("reward_model_cost", 0.95,
      "Concrete latency numbers from Table 4 are directly measured and reported. "
      "High confidence in these empirical values.")

# ── Architecture descriptions ──────────────────────────────────────────────────
prior("hidden_circuit_arch", 0.92,
      "Architecture description comes directly from the paper's Section 3.1. "
      "High confidence it accurately describes the implemented system.")

prior("gated_fusion_arch", 0.92,
      "Architecture description from Section 3.3. High confidence.")

prior("training_protocol", 0.90,
      "Training details from Section 3.4 and Appendix. Dataset sizes and "
      "cost figures are directly reported. Slight uncertainty on reproducibility.")

# ── Empirical performance data (Tables) ───────────────────────────────────────
prior("gnosis_math_perf", 0.93,
      "Table 1 data directly reported in the paper. High confidence in accuracy "
      "of transcription. Small residual uncertainty on evaluation methodology details.")

prior("gnosis_trivia_perf", 0.93,
      "Table 1 data directly reported. High confidence.")

prior("gnosis_mmlu_perf", 0.92,
      "Table 1 data directly reported. Slightly lower confidence for MMLU-Pro "
      "as AUPR-e is notably weaker (0.56) indicating harder error detection task.")

prior("external_judge_perf", 0.92,
      "External baseline data from Table 1. High confidence in reported numbers.")

prior("mlp_probe_perf", 0.93,
      "Table 2 data directly reported. The MLP-Prob baseline is implemented "
      "by the same authors, so numbers are highly reliable.")

prior("hidden_only_perf", 0.92,
      "Table 5 ablation data directly reported. High confidence.")

prior("attention_only_perf", 0.92,
      "Table 5 ablation data directly reported. High confidence.")

prior("cnn_stats_perf", 0.91,
      "Table 6 ablation data directly reported. High confidence.")

prior("attention_topology_ablation", 0.91,
      "Table 7 ablation data directly reported. High confidence.")

prior("attention_grid_ablation", 0.91,
      "Table 8 ablation data directly reported. High confidence.")

prior("hidden_component_ablation", 0.92,
      "Table 9 ablation data directly reported. High confidence.")

prior("backbone_accuracy_stats", 0.93,
      "Table 11 backbone outcome statistics directly reported. High confidence.")

# ── Transfer results ──────────────────────────────────────────────────────────
prior("transfer_math_results", 0.92,
      "Table 3 transfer results directly reported. High confidence.")

prior("transfer_trivia_results", 0.91,
      "Table 3 transfer results directly reported. High confidence.")

prior("transfer_mmlu_results", 0.91,
      "Table 3 transfer results directly reported. High confidence.")

# ── Interpretation / Hypothesis claims ────────────────────────────────────────
prior("shared_circuits_hypothesis", 0.68,
      "The shared internal circuit hypothesis is the paper's interpretation of "
      "transfer success. Plausible but not directly verified by circuit-level analysis. "
      "Transfer data supports it but alternative explanations exist.")

prior("pred_shared", 0.72,
      "Prediction derived from shared_circuits_hypothesis. Moderate confidence "
      "matching the hypothesis's credibility.")

prior("pred_no_shared", 0.30,
      "Prediction that transfer would fail if circuits differ. Low prior because "
      "the paper's results contradict this prediction.")

prior("pred_gnosis_math", 0.85,
      "Prediction about Gnosis performance on math. High prior because this "
      "prediction is directly confirmed by Table 1.")

prior("pred_ext_math", 0.85,
      "Prediction about external judge performance. High prior — directly "
      "confirmed by Table 1 baselines.")

prior("feature_analysis", 0.82,
      "Visualization-based analysis. Results are qualitative ('clear separation') "
      "without statistical significance testing. Moderate confidence.")

# ── Limitation claims ─────────────────────────────────────────────────────────
prior("proprietary_model_limitation", 0.97,
      "Fundamental architectural constraint: proprietary API models do not expose "
      "internal activations. This is a hard constraint, not an empirical claim.")

prior("transfer_fails_cross_family", 0.80,
      "Cross-family transfer failure is described in the paper's limitations. "
      "Not directly tested with full ablation tables, so some uncertainty remains.")

# ── Alternative hypotheses (for abduction) ────────────────────────────────────
prior("alt_external_math", 0.35,
      "Alternative: external judges explain math benchmark as well as Gnosis. "
      "Low prior because observed AUROC (0.90-0.91) is clearly below Gnosis (0.95). "
      "The alternative does not explain the observation as well as the hypothesis.")

prior("alt_transfer_accidental", 0.28,
      "Alternative: transfer success due to dataset-level statistical similarity "
      "rather than shared internal circuits. Low prior because this alternative "
      "predicts random-level transfer on architecturally different models, "
      "which would need separate testing to rule out definitively.")
