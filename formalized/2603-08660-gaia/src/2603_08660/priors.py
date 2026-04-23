"""Prior assignments for independent (leaf) claims in the 2603-08660 formalization.

Run `gaia check --hole .` to see which claims need priors.
Priors are reviewer judgments about plausibility of each independent premise
before inference; they reflect strength of evidence in the source.

Paper: "How Far Can Unsupervised RLVR Scale LLM Training?" (arXiv 2603.08660)
Venue: ICLR 2026
"""

from . import (
    # Section 2 taxonomy — documented reward formulas and descriptions
    certainty_rewards_overview,
    ensemble_rewards_overview,
    unlabeled_data_rewards,
    gen_verify_asymmetry_rewards,
    intrinsic_self_referential,
    # Section 3 theory
    one_step_update_dynamics,
    # Motivation
    supervision_bottleneck,
    # Section 4/5 empirical observations
    small_dataset_stability,
    kl_divergence_small_vs_large,
    ood_generalization_obs,
    ttt_stability_observation,
    # Section 6
    collapse_step_values,
    mcs_hyperparameter_robustness,
    alt_passk_predictor,
    # Section 7
    self_verify_no_collapse,
    instruction_alignment_key,
    alt_intrinsic_explain_countdown,
    # Comparison/abduction helper claims
    pred_mcs,
    pred_passk,
    pred_self_verify,
    pred_intrinsic_countdown,
)

PRIORS = {
    # ── Section 2: Taxonomy — documented reward formulas ───────────────────────────────────

    certainty_rewards_overview: (
        0.97,
        "Reward formulas are stated explicitly in Table 1 of the paper; factual description of published methods.",
    ),
    ensemble_rewards_overview: (
        0.97,
        "Reward formulas are stated explicitly in Table 2 of the paper; factual description of published methods.",
    ),
    unlabeled_data_rewards: (
        0.95,
        "Factual taxonomy of published external reward methods, each with citations. High confidence.",
    ),
    gen_verify_asymmetry_rewards: (
        0.95,
        "Well-established asymmetry property; multiple concrete examples cited (LADDER, AZR, AlphaProof).",
    ),
    intrinsic_self_referential: (
        0.99,
        "Definitional: intrinsic rewards are defined as deriving from model's own distributions. "
        "This is a logical/definitional property, not an empirical claim.",
    ),

    # ── Section 3: Theory ─────────────────────────────────────────────────────────────────

    one_step_update_dynamics: (
        0.90,
        "Derived from standard KL-regularized RL optimal policy closed form. Two assumptions "
        "(majority stability A1, effective learning A2) are empirically validated in Appendix A.1.",
    ),

    # ── Motivation ───────────────────────────────────────────────────────────────────────

    supervision_bottleneck: (
        0.93,
        "Widely acknowledged limitation in the field; cited multiple times and reinforced by "
        "multiple concurrent works. Core motivation of the paper.",
    ),

    # ── Section 4/5: Empirical observations ─────────────────────────────────────────────

    ood_generalization_obs: (
        0.88,
        "Surprising finding: all 6 training configurations show OOD improvement (Figure 5). "
        "Replicated across different problem selections, but limited to one model architecture.",
    ),
    small_dataset_stability: (
        0.92,
        "Verified across 3 random seeds for key sizes {32, 128, 512}; DAPO-32 never collapses, "
        "DAPO-512 always does. Strong within-paper evidence.",
    ),
    kl_divergence_small_vs_large: (
        0.94,
        "Directly computed metric (Figure 7); DAPO-32 KL = 0.057 vs DAPO-512 at ~2x higher. "
        "High-confidence measurement.",
    ),
    ttt_stability_observation: (
        0.87,
        "Single experiment (AMC23 40-problem TTT vs DAPO-17k), but clearly visualized in Figure 8. "
        "Consistent with small-dataset finding.",
    ),

    # ── Section 6: Model Collapse Step ──────────────────────────────────────────────────

    collapse_step_values: (
        0.93,
        "Directly measured for 7 models; results visualized in Figure 11 and listed as "
        "[34, 40, 160, 221, 245, 280, 383]. High-confidence measurement.",
    ),
    mcs_hyperparameter_robustness: (
        0.85,
        "Tested across 3 rollout counts and 3 mini-batch sizes (Figure 12); "
        "relative rankings preserved across settings. Moderate-high confidence.",
    ),
    alt_passk_predictor: (
        0.88,
        "Pass@k is an established metric with well-known saturation properties on "
        "multiple-choice. Both strengths and limitations are accurately described.",
    ),
    pred_mcs: (
        0.88,
        "Based on Figure 11: MCS rankings match GT Gain rankings exactly for all 7 models.",
    ),
    pred_passk: (
        0.60,
        "Pass@k shows ranking inversions (Qwen2.5-Math anomalously high) and saturation; "
        "lower reliability than MCS.",
    ),

    # ── Section 7: External rewards ──────────────────────────────────────────────────────

    self_verify_no_collapse: (
        0.86,
        "Observed in Figure 13: Reward Accuracy recovers after step ~200 exploitation phase, "
        "Ground Truth Reward continues rising. Single task (Countdown), two model sizes.",
    ),
    instruction_alignment_key: (
        0.85,
        "Figure 14 shows clear prompt sensitivity difference between base and instruction-aligned "
        "models. Two prompts tested on both; consistent pattern.",
    ),
    alt_intrinsic_explain_countdown: (
        0.30,
        "Trajectory-Level Entropy's explanatory power for Countdown task performance: LOW. "
        "The intrinsic reward achieves substantially lower validation accuracy than Self-Verification "
        "and cannot sustain improvement (Figure 13). Pi(Alt) reflects whether intrinsic alone "
        "can explain the observed performance — it cannot.",
    ),
    pred_self_verify: (
        0.87,
        "Based on Figure 13: Self-Verification reaches high validation accuracy "
        "without collapse on Countdown.",
    ),
    pred_intrinsic_countdown: (
        0.35,
        "Trajectory-Level Entropy achieves substantially lower accuracy with degradation on "
        "Countdown; its prediction quality is low.",
    ),
}
