"""Priors for independent (leaf) claims in the 2604.06159 formalization.

Calibration philosophy
----------------------

* **Numerical readouts from figures and tables (Sec. 3.1-3.8 panels and
  Tables 1-3) -- 0.92-0.95.** Each is a 10-30-seed mean +/- s.e.
  measurement; small probability mass left for replication / typo /
  aggregation drift.
* **Textbook math results** (Prop 1.1 target uniqueness, Prop 1.2
  gradient $p^\\theta - q$, Appendix B beta table, Appendix C
  GRPO-collapse calculation) -- **0.97-0.99**.
* **Related-work characterisations** -- 0.85-0.92.
* **Setup justifications** (KL-strengthens GRPO; DG diverges with >1
  epoch) -- 0.93-0.94.
* **Hypotheses and alternatives in the central abduction**:
  - `claim_decoupling_explains_sparse_gap` -- 0.7 (author's causal
    story; abduction's mechanism evidence pulls derived belief upward).
  - `claim_single_ingredient_alt` -- 0.2.
  - `claim_pg_view_entanglement_unavoidable` -- 0.5 (foil;
    contradiction operator does the work).
* **Predictions in the abductions** (`pred_*`) -- 0.5 (the comparison
  strategy plus the observed shape carry the signal).
"""

from .motivation import (
    claim_fig1_dense_match,
    claim_fig1_sparse_outperform,
    claim_pg_entangles_two_questions,
)
from .s10_limitations import claim_pg_view_entanglement_unavoidable
from .s11_wiring import (
    claim_decoupling_explains_sparse_gap,
    claim_single_ingredient_alt,
    pred_concentrated,
    pred_decoupling,
    pred_one_vs_rest_alt,
    pred_single_ingredient,
)
from .s2_method import (
    claim_prop1_gradient_p_minus_q,
    claim_prop1_target_unique,
    claim_standardization_invariance,
)
from .s3_setup import (
    claim_dg_multi_epoch_unstable,
    claim_grpo_kl_strengthens_baseline,
)
from .s4_tabular_bandits import claim_beta_table
from .s5_neural_bandit import (
    claim_grpo_collapses_to_reinforce,
    claim_mnist_final_errors,
    claim_tpo_dg_condition_on_action,
)
from .s6_sequence_tasks import (
    claim_table1_steps_to_1pct,
    claim_table2_steps_to_1pct,
)
from .s7_terminal_reward import (
    claim_3_7_no_anchor_hurts,
    claim_3_7_target_matching_essential,
    claim_table3_terminal_results,
)
from .s8_analysis import (
    claim_4_1_target_mass_allocation,
    claim_4_2_all_fail_fraction,
    claim_4_2_k_sweep,
    claim_4_2_zero_variance_neutrality,
    claim_4_3_epoch_sweep,
)
from .s9_related_work import (
    claim_dg_complementary_axis,
    claim_difficulty_bias_residual,
    claim_group_based_pg_family,
    claim_objective_corrections_family,
    claim_off_policy_async_family,
    claim_regression_preference_family,
    claim_single_sample_pg_family,
    claim_target_matching_family,
)


PRIORS: dict = {
    # --------------------------------------------------------------
    # Headline measurements (Figure 1, Tables 1-3, ablations)
    # --------------------------------------------------------------
    claim_fig1_dense_match: (
        0.95,
        "Figure 1(a) MNIST contextual bandit, mean +/- s.e. over 20 "
        "seeds. Headline panel of the paper; the main claim (curves "
        "tightly clustered, all reach ~3-6% by step 8000) is "
        "qualitatively unambiguous in the figure.",
    ),
    claim_fig1_sparse_outperform: (
        0.95,
        "Figure 1(b) sparse-reward token reversal, 20 seeds. The "
        "GRPO/DG curves remain near 1.0 exact-match error; TPO drops "
        "to near 0. This is a qualitative gap, not a small delta -- "
        "extremely unlikely to be a measurement artifact.",
    ),
    claim_mnist_final_errors: (
        0.94,
        "Section 3.3 Figure 5(a) numerical readout. 20 seeds. The "
        "TPO 2.9% / PG 5.3% / GRPO 5.9% / Group PG 7.2% ordering is "
        "consistent across the figure and the body text.",
    ),
    claim_table1_steps_to_1pct: (
        0.94,
        "Section 3.4 Table 1, 20 seeds. Steps-to-1%-error is a "
        "well-defined milestone metric; TPO is fastest at every V "
        "with substantial margins.",
    ),
    claim_table2_steps_to_1pct: (
        0.93,
        "Section 3.5 Table 2, 10 seeds (fewer than other tables, so "
        "0.93 rather than 0.94). Aggregates 8 task variants; the "
        "qualitative claim 'TPO fastest on all 8' is robust to seed "
        "fluctuation.",
    ),
    claim_table3_terminal_results: (
        0.94,
        "Section 3.6 Table 3, terminal-reward exact-match error. "
        "Bold-best-at-every-cell is unambiguous given the magnitudes "
        "(TPO 6-9% vs. baselines collapsing).",
    ),
    claim_3_7_no_anchor_hurts: (
        0.92,
        "Section 3.7 ablation, 20 seeds. The 7.4% (full TPO) vs. >99% "
        "(no anchor) at H=10 is qualitatively dramatic. 0.92 (rather "
        "than 0.94) reflects that ablation-of-component results "
        "occasionally invert under different setups.",
    ),
    claim_3_7_target_matching_essential: (
        0.92,
        "Section 3.7 Group PG ablation. Same scale as no-anchor "
        "ablation; the >99% blowup at H=10 is unambiguous.",
    ),
    # --------------------------------------------------------------
    # Section 4 mechanism diagnostics
    # --------------------------------------------------------------
    claim_4_1_target_mass_allocation: (
        0.92,
        "Figure 11(b) per-candidate weight proxy diagnostic; 10 "
        "seeds. The qualitative claim (TPO drives failed-candidate "
        "weight to ~0; GRPO does not) is visible in the figure.",
    ),
    claim_4_2_all_fail_fraction: (
        0.93,
        "Figure 12(a), 10 seeds. The ~90% all-fail at init is "
        "consistent with the (1/V)^H = 0.4% per-sequence success "
        "rate, providing an independent sanity check on the value.",
    ),
    claim_4_2_k_sweep: (
        0.92,
        "Figure 13, 30 seeds. TPO smooth (8.9% -> 0.36%); GRPO "
        "non-monotonic with the K=64 worsening. 30 seeds give "
        "strong statistical robustness.",
    ),
    claim_4_2_zero_variance_neutrality: (
        0.99,
        "Direct mathematical corollary of the score-standardization "
        "convention (u=0 on zero-variance groups) plus the target "
        "definition (q proportional to p_old * exp(u/eta)). When "
        "u=0, q = p_old. Textbook calculation.",
    ),
    claim_4_3_epoch_sweep: (
        0.92,
        "Figure 16, 30 seeds. TPO < 2.3% across all epoch counts; "
        "GRPO non-monotonic (37.6% at 2 epochs). 30 seeds give "
        "strong robustness against fluke patterns.",
    ),
    # --------------------------------------------------------------
    # Math / textbook lift-from-paper
    # --------------------------------------------------------------
    claim_prop1_target_unique: (
        0.99,
        "Lagrangian on a strictly concave objective on the simplex; "
        "textbook KKT calculation. Almost-deterministic.",
    ),
    claim_prop1_gradient_p_minus_q: (
        0.99,
        "Standard softmax cross-entropy chain rule. Treating q as "
        "fixed (stop-gradient), the derivative is exactly p - q. "
        "Textbook calculation.",
    ),
    claim_beta_table: (
        0.99,
        "Appendix B pure algebra: substitute one-hot reward into "
        "exact population update, simplify. Mechanical.",
    ),
    claim_grpo_collapses_to_reinforce: (
        0.99,
        "Appendix C calculation. Conditional on (mu_B, sigma_B), "
        "g_GRPO = (p/sigma_B)(e_y - pi). Mechanical.",
    ),
    claim_tpo_dg_condition_on_action: (
        0.97,
        "Definitional plus Appendix C derivation. The 'TPO suppresses "
        "the sampled wrong class' direction is shown explicitly: "
        "g_-(j) = gamma(pi_j)(pi - e_j).",
    ),
    claim_standardization_invariance: (
        0.93,
        "Mathematical scale-invariance of z-scoring + Appendix D "
        "empirical robustness over eta in [0.25, 2]. The math is "
        "trivial; the empirical robustness gives an extra "
        "confidence check.",
    ),
    # --------------------------------------------------------------
    # Setup-justification empirical claims
    # --------------------------------------------------------------
    claim_grpo_kl_strengthens_baseline: (
        0.94,
        "Direct readout of Section 3.6 Table 3: GRPO (no KL) at "
        "H=7 is 66.6% vs. KL-anchored 14.5%; for H>=8, GRPO (no "
        "KL) shows no meaningful learning. The strengthening is "
        "deliberate and acknowledged in Appendix F.",
    ),
    claim_dg_multi_epoch_unstable: (
        0.94,
        "Direct readout of Appendix E: 4-epoch DG ends at 48.3% vs. "
        "1-epoch at 2.0% on reverse-copy terminal reward; 4-epoch "
        "worse in 7 of 8 prompt-matched token-reversal variants.",
    ),
    # --------------------------------------------------------------
    # Related-work family characterisations
    # --------------------------------------------------------------
    claim_target_matching_family: (
        0.9,
        "The author's reading of REPS / MPO / V-MPO / AWR / MDPO / "
        "regularised-MDP work as the same exponential-tilting "
        "family. Well-supported by the cited papers; small caveat "
        "for the AWR-fixed-scalar interpretation.",
    ),
    claim_group_based_pg_family: (
        0.9,
        "RLOO / GRPO and the GRPO variants (Dr.GRPO, DAPO, GSPO) "
        "all use scalar-weighted updates on the candidate group. "
        "Direct read-off from the cited methods.",
    ),
    claim_single_sample_pg_family: (
        0.92,
        "REINFORCE / TRPO / PPO / REINFORCE++ / ReMax all use scalar "
        "advantage weights on the score-function gradient. Long-"
        "established characterisation.",
    ),
    claim_dg_complementary_axis: (
        0.85,
        "DG is within-context vs. TPO is across-context. The "
        "complementarity claim is plausible but has not been "
        "tested by composing the two methods empirically; the "
        "paper notes only that they 'can be composed'.",
    ),
    claim_difficulty_bias_residual: (
        0.88,
        "Acknowledged caveat (Sec. 5 / Sec. 6). The structural "
        "argument (TPO inherits within-group z-scoring from GRPO, "
        "hence the same low-variance amplification) is solid; the "
        "claim is strengthened by Liu 2025 / Murphy 2025.",
    ),
    claim_regression_preference_family: (
        0.88,
        "REBEL / PMPO / DPO / KTO / IPO are correctly characterised "
        "as more distant comparisons (different loss families, often "
        "offline / pairwise).",
    ),
    claim_objective_corrections_family: (
        0.88,
        "MaxRL / GDPO / MT-GRPO change which objective is optimised "
        "(higher-order corrections, multi-reward decoupling, multi-"
        "task reweighting). Correctly placed as orthogonal.",
    ),
    claim_off_policy_async_family: (
        0.88,
        "ScaleRL and IcePop address staleness and engine mismatch "
        "respectively; correctly placed as orthogonal off-policy "
        "axes that compose with TPO.",
    ),
    # --------------------------------------------------------------
    # Diagnosis claim (PG entangles Q1 and Q2)
    # --------------------------------------------------------------
    claim_pg_entangles_two_questions: (
        0.92,
        "Definitional read of the standard PG/PPO/GRPO/DG update "
        "form: scalar advantage * score-function gradient. The "
        "implementation never expresses Q1 as a separate object. "
        "Solid characterisation but slightly interpretive (one "
        "could disagree about whether the Q1/Q2 distinction is the "
        "right framing).",
    ),
    # --------------------------------------------------------------
    # Central abduction hypothesis / alternative
    # --------------------------------------------------------------
    claim_decoupling_explains_sparse_gap: (
        0.7,
        "The author's causal story: explicit Q1/Q2 decoupling "
        "(closed-form target + cross-entropy + self-extinguishing "
        "gradient) is what causes TPO's sparse-reward advantage. "
        "Multi-causal mechanism. Set at 0.7 to leave room for the "
        "abduction's mechanism evidence (every ablation hurts; "
        "every diagnostic distinguishes TPO) to pull the derived "
        "comparison belief upward.",
    ),
    claim_single_ingredient_alt: (
        0.2,
        "Counter-hypothesis: only one ingredient matters. Predicts "
        "ablation-redundancy, which the data clearly reject "
        "(TPO-no-anchor and Group PG both >99% at H=10). Set low "
        "because the alternative does not explain the joint "
        "observation; pi(Alt) here measures explanatory power, not "
        "internal correctness.",
    ),
    # --------------------------------------------------------------
    # Foil for the contradiction operator
    # --------------------------------------------------------------
    claim_pg_view_entanglement_unavoidable: (
        0.5,
        "The implicit prevailing view that PG entanglement of Q1 "
        "and Q2 is unavoidable (must be tamed with clipping, KL, "
        "trust regions). Set at neutral 0.5 so the contradiction "
        "with the empirical sparse-reward outperformance does the "
        "BP work rather than the prior.",
    ),
    # --------------------------------------------------------------
    # Abduction predictions
    # --------------------------------------------------------------
    pred_concentrated: (
        0.5,
        "Prediction under the TPO-mechanism hypothesis: the excess "
        "gain over one-vs-rest rises with wrong-class concentration. "
        "Kept neutral; the comparison strategy plus the observed "
        "shape (Figure 5(b)) carry the signal.",
    ),
    pred_one_vs_rest_alt: (
        0.5,
        "Prediction under the one-vs-rest-collapse alternative: "
        "the excess gain is concentration-independent. Kept neutral; "
        "the comparison strategy plus the observed shape carry the "
        "signal.",
    ),
    pred_decoupling: (
        0.5,
        "Prediction under the decoupling hypothesis: every ablation "
        "hurts; every diagnostic distinguishes TPO. Kept neutral.",
    ),
    pred_single_ingredient: (
        0.5,
        "Prediction under the single-ingredient alternative: at "
        "most one ablation hurts; at most one diagnostic "
        "distinguishes TPO. Kept neutral.",
    ),
}
