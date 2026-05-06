"""Priors for independent (leaf) claims in the 2604.23318 formalization.

Calibration philosophy
----------------------

* **Numerical readouts from figures and tables** (Tables 1-2 entries,
  Figure 1a/b correlations, Figure 3 AUC bins, Section 5.4-5.6 ablation
  numbers, Section 6 overhead percentages) -- **0.92-0.95**. Each is a
  3-seed mean +/- std measurement under a fixed checkpoint-selection
  protocol.

* **Theorem-bound leaf parts** (Theorem 1 (i) and (ii); Lemma 1; Remark
  C.1; Proposition D.1) -- **0.97-0.99**. Textbook math derivations
  given the stated assumptions.

* **Method-component leaves** (Algorithm 1 Steps 1-4 -- definitional
  reads of the algorithm) -- **0.97**. Pure descriptions of the
  algorithm.

* **Setup-justification claims** (related-work characterisations,
  diversity-of-eval, strong-baselines) -- **0.85-0.92**.

* **Hypotheses and alternatives in the central abduction**:
  - `claim_signal_explains_via_hidden_states` -- **0.7** (author's
    causal story; abduction's mechanism evidence pulls derived belief
    upward).
  - `claim_signal_alt_any_reweighting` -- **0.2** (alternative).

* **Foils for contradiction operators** -- **0.5** (let the
  contradiction operator do the BP work).

* **Predictions in the abductions** (`pred_*`) -- **0.5** (the
  comparison strategy plus the observed shape carry the signal).
"""

from .motivation import (
    claim_grpo_coarse_grained,
    claim_prm_supervision_cost,
)
from .s2_empirical_observation import (
    claim_fig1a_aggregate_anticorrelation,
    claim_fig1b_local_anticorrelation,
)
from .s3_method import (
    claim_appendix_h_max_vs_mean,
    claim_step1_min_distance,
    claim_step2_global_norm_norm,
    claim_step3_max_pooling,
    claim_step4_weighted_advantage,
)
from .s4_separation_theorem import (
    claim_appendix_d_first_moment_bound,
    claim_lemma1_sinkhorn_approximation,
    claim_prop_g1_multiple_divergences,
    claim_remark_c1_non_cancellation,
    claim_thm1_post_divergence_lower_bound,
    claim_thm1_pre_divergence_upper_bound,
)
from .s5_signal_analysis import (
    claim_fig3_auc_monotonic,
    claim_fig3_topleft_within_bin_separation,
)
from .s6_experimental_setup import (
    claim_diversity_of_evaluation,
    claim_strong_baselines,
)
from .s7_main_results import (
    claim_table1_llama_8b,
    claim_table1_qwen_14b,
    claim_table1_qwen_math_7b,
    claim_table2_code_results,
)
from .s8_ablations import (
    claim_5_4_1_distance_metric_ablation,
    claim_5_4_2_cross_vs_per_rollout,
    claim_5_5_span_stride_sensitivity,
    claim_5_6_rollout_group_size,
    claim_section6_overhead,
)
from .s9_qualitative import (
    claim_appendix_h3_prm_connection,
    claim_appendix_k_case_study,
    claim_related_credit_assignment,
    claim_related_token_reshaping,
)
from .s10_wiring import (
    claim_grpo_uniform_advantage_assumption,
    claim_prevailing_step_annotation_required,
    claim_signal_alt_any_reweighting,
    claim_signal_explains_via_hidden_states,
    pred_any_reweighting,
    pred_hidden_states_faithful,
)

PRIORS = {
    # ---------------------------------------------------------------
    # Section 2 -- empirical observation leaves (figure readouts)
    # ---------------------------------------------------------------
    claim_fig1a_aggregate_anticorrelation: (
        0.94,
        "Spearman -0.96 with closely aligned transition zones is a "
        "high-confidence quantitative readout from Figure 1(a). "
        "Small probability mass left for replication / aggregation "
        "drift.",
    ),
    claim_fig1b_local_anticorrelation: (
        0.94,
        "Spearman -0.42, p = 4.6e-59 over the |dAcc| >= 0.0625 "
        "subset is a high-confidence within-trajectory readout from "
        "Figure 1(b).",
    ),
    # ---------------------------------------------------------------
    # Section 3 method -- algorithm-step descriptions (definitional)
    # ---------------------------------------------------------------
    claim_step1_min_distance: (
        0.97,
        "Definitional read of Algorithm 1, Step 1 (line 4): minimum "
        "Sinkhorn distance to opposing-group spans.",
    ),
    claim_step2_global_norm_norm: (
        0.97,
        "Definitional read of Algorithm 1, Step 2 (lines 8-9): "
        "global mean hidden-state norm normalization preserves "
        "intra-group ordering.",
    ),
    claim_step3_max_pooling: (
        0.97,
        "Definitional read of Algorithm 1, Step 3 (line 13): max-"
        "pool over covering spans for token-level weight.",
    ),
    claim_step4_weighted_advantage: (
        0.97,
        "Definitional read of Algorithm 1, Step 4 (line 17): "
        "weighted advantage as advantage-times-weight.",
    ),
    claim_appendix_h_max_vs_mean: (
        0.93,
        "Appendix H.1 design-choice justification: max-pool > "
        "mean-pool for boundary tokens. Definitional argument.",
    ),
    # ---------------------------------------------------------------
    # Section 4 -- separation theorem leaf parts
    # ---------------------------------------------------------------
    claim_thm1_pre_divergence_upper_bound: (
        0.99,
        "Theorem 1 part (i): triangle inequality + (A3) on two "
        "empirical means of the same population mixture. Textbook "
        "calculation given the assumptions.",
    ),
    claim_thm1_post_divergence_lower_bound: (
        0.99,
        "Theorem 1 part (ii): reverse-triangle inequality + (A3) "
        "on two empirical means of distinct population mixtures. "
        "Textbook calculation given the assumptions.",
    ),
    claim_lemma1_sinkhorn_approximation: (
        0.98,
        "Appendix B Lemma 1: Sinkhorn approximation $W_1 \\leq W_\\epsilon "
        "\\leq W_1 + \\epsilon\\log n$. Standard result with a "
        "well-known proof.",
    ),
    claim_remark_c1_non_cancellation: (
        0.93,
        "Appendix C.1 Remark: $D(S) > 0$ as a regularity condition "
        "verified empirically by Section 5.1's monotonic AUC.",
    ),
    claim_appendix_d_first_moment_bound: (
        0.99,
        "Proposition D.1 (Appendix D): $W_1$ via KR duality bounds "
        "first-moment differences. Textbook KR-duality calculation.",
    ),
    claim_prop_g1_multiple_divergences: (
        0.88,
        "Appendix G Proposition G.1: extends single-divergence "
        "stylization to piecewise. Stated without full formal proof "
        "but follows from the same triangle-inequality machinery.",
    ),
    # ---------------------------------------------------------------
    # Section 5.1 -- signal analysis leaves
    # ---------------------------------------------------------------
    claim_fig3_auc_monotonic: (
        0.94,
        "Per-bin AUC values 0.644 -> 0.988 across 8 bins (Figure 3 "
        "right). Direct quantitative readout.",
    ),
    claim_fig3_topleft_within_bin_separation: (
        0.92,
        "Within-bin green > red stratification on Figure 3 top-"
        "left. Visual quantitative claim with high confidence.",
    ),
    # ---------------------------------------------------------------
    # Section 5.3 -- main results table readouts
    # ---------------------------------------------------------------
    claim_table1_qwen_math_7b: (
        0.94,
        "Direct readout of Table 1 top panel (Qwen2.5-Math-7B). "
        "Mean +/- std over 3 seeds; SHEAR avg 51.2 best.",
    ),
    claim_table1_llama_8b: (
        0.93,
        "Direct readout of Table 1 middle panel (Llama3.1-8B-"
        "Instruct). SHEAR avg 26.2 best.",
    ),
    claim_table1_qwen_14b: (
        0.93,
        "Direct readout of Table 1 bottom panel (Qwen2.5-14B-Base). "
        "SHEAR avg 46.9 best; PRM variants UNDERPERFORM GRPO.",
    ),
    claim_table2_code_results: (
        0.92,
        "Direct readout of Table 2 (code generation, avg@4). SHEAR "
        "improves over GRPO on all 3 backbones; smaller margins than "
        "math.",
    ),
    # ---------------------------------------------------------------
    # Section 5.4-5.6 -- ablation numerical readouts
    # ---------------------------------------------------------------
    claim_5_4_1_distance_metric_ablation: (
        0.93,
        "Direct readout of Figure 5(a): four numerical peak accuracies "
        "+ GRPO baseline. Wasserstein 0.5068, Chamfer 0.5051, MMD "
        "0.5061 > GRPO 0.4884 > Cosine 0.4837.",
    ),
    claim_5_4_2_cross_vs_per_rollout: (
        0.92,
        "Direct readout of Figure 5(b): cross-rollout 0.5068, per-"
        "rollout 0.4995, GRPO 0.4884. Both above baseline.",
    ),
    claim_5_5_span_stride_sensitivity: (
        0.9,
        "Figure 6 qualitative readout: insensitive to $w$, sensitive "
        "to $s$. Numerical curves not tabulated in main text.",
    ),
    claim_5_6_rollout_group_size: (
        0.9,
        "Figure 7 qualitative readout: SHEAR-GRPO gap widens at "
        "G=16. Two-condition comparison, qualitative interpretation.",
    ),
    claim_section6_overhead: (
        0.93,
        "Direct readout of Figure 8: +15.5%, +10.4%, +7.4% overhead "
        "across the three backbones; pattern (decreasing with model "
        "scale) is consistent with Sinkhorn fixed-cost reasoning.",
    ),
    # ---------------------------------------------------------------
    # Section 7 / Appendices -- related work, qualitative
    # ---------------------------------------------------------------
    claim_appendix_h3_prm_connection: (
        0.85,
        "Appendix H.3 interpretive connection: $\\omega^{(i)}_t$ "
        "qualitatively tracks $1 - \\text{PRM}(t)$ for incorrect "
        "rollouts. Interpretive, not empirically validated as a "
        "claim about real PRMs.",
    ),
    claim_appendix_k_case_study: (
        0.88,
        "Appendix K case study on a 4-tuples problem. Single "
        "qualitative example; the heatmap pattern is visually "
        "consistent with the population-level finding.",
    ),
    claim_related_credit_assignment: (
        0.9,
        "Section 7 related-work characterisation of the credit-"
        "assignment paradigm. Solid mid-level literature claim.",
    ),
    claim_related_token_reshaping: (
        0.88,
        "Section 7 related-work characterisation of token-level "
        "reshaping methods + latent-reasoning approaches.",
    ),
    # ---------------------------------------------------------------
    # Section 6 -- diversity / strong-baselines methodological framing
    # ---------------------------------------------------------------
    claim_diversity_of_evaluation: (
        0.9,
        "Methodological characterisation of the evaluation matrix. "
        "Solid high-level claim about the evaluation diversity.",
    ),
    claim_strong_baselines: (
        0.85,
        "Methodological characterisation of the baseline strength. "
        "Defensible but interpretive (one could disagree about "
        "whether other baselines should have been included).",
    ),
    # ---------------------------------------------------------------
    # Diagnoses (motivation level)
    # ---------------------------------------------------------------
    claim_grpo_coarse_grained: (
        0.95,
        "Definitional read of Eq. 1 of [@Chen2026SHEAR]: scalar "
        "advantage * score-function gradient at every token. Solid "
        "characterisation.",
    ),
    claim_prm_supervision_cost: (
        0.9,
        "Standard characterisation of the PRM training pipeline. "
        "Solid mid-level claim about the PRM family of methods.",
    ),
    # ---------------------------------------------------------------
    # Central abduction hypothesis / alternative
    # ---------------------------------------------------------------
    claim_signal_explains_via_hidden_states: (
        0.7,
        "The author's causal story: hidden-state distributions "
        "encode local reasoning quality faithfully, captured by "
        "$W_1$ via KR duality. Set at 0.7 to leave room for the "
        "abduction's mechanism evidence (cosine fails, distribution-"
        "aware metrics succeed) to pull the derived comparison "
        "belief upward.",
    ),
    claim_signal_alt_any_reweighting: (
        0.2,
        "Counter-hypothesis: any non-uniform token weighting "
        "suffices. Predicts cosine should also beat GRPO, which the "
        "data clearly reject (cosine 0.4837 < GRPO 0.4884). Set low "
        "because the alternative does not explain the joint "
        "observation.",
    ),
    # ---------------------------------------------------------------
    # Foils for contradiction operators
    # ---------------------------------------------------------------
    claim_prevailing_step_annotation_required: (
        0.5,
        "The implicit prevailing view that fine-grained credit "
        "assignment in RLVR requires step-level annotation (PRM "
        "framing). Set at neutral 0.5 so the contradiction with "
        "SHEAR's empirical demonstration does the BP work.",
    ),
    claim_grpo_uniform_advantage_assumption: (
        0.5,
        "The implicit vanilla-GRPO assumption that all tokens in a "
        "rollout deserve the same advantage. Set at neutral 0.5 so "
        "the contradiction with the within-trajectory empirical "
        "divergence finding does the BP work.",
    ),
    # ---------------------------------------------------------------
    # Abduction predictions
    # ---------------------------------------------------------------
    pred_hidden_states_faithful: (
        0.5,
        "Prediction under the hidden-state-faithful hypothesis: "
        "cosine fails, $W$/Chamfer/MMD all win, local + within-bin "
        "both hold. Kept neutral; the comparison strategy plus the "
        "observed Figure 5(a) shape carry the signal.",
    ),
    pred_any_reweighting: (
        0.5,
        "Prediction under the any-reweighting alternative: all "
        "weightings comparable; cosine should also beat GRPO. Kept "
        "neutral; the comparison strategy plus the observed shape "
        "carry the signal.",
    ),
}
