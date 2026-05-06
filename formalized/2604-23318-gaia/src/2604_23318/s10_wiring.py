"""Reasoning wiring: strategies, abductions, inductions, contradictions.

Pass 2-4 connect the claims extracted in motivation through s9 with
explicit reasoning strategies.

Conventions:

* `support` -- soft deduction with author-specified prior on the
  implication warrant. Default for premise -> conclusion.
* `deduction` -- rigid mathematical entailment (Theorem 1, Theorem 2,
  Proposition F.1, Proposition D.1, Lemma 1).
* `abduction(s_h, s_alt, comp)` -- inference to best explanation.
  Used once: 'the Wasserstein-distance signal works because hidden-
  state distributions encode local reasoning quality' (H) vs. 'the
  gain comes from any token-level reweighting / better optimization
  noise' (Alt). Theorem strict-ordering + within-trajectory
  consistency + cosine-fails ablation discriminate.
* `induction` -- chained binary composite. Used twice:
    (a) 'SHEAR > GRPO' inducted over 6 (backbone, modality) pairs.
    (b) 'distribution-aware metrics > mean-only' inducted over W,
        Chamfer, MMD vs. Cosine.
* `contradiction()` -- (a) 'fine-grained credit assignment in RLVR
  requires per-step annotation' vs. SHEAR's outcome-only-label
  demonstration; (b) 'all tokens in a rollout deserve equal
  advantage (vanilla GRPO)' vs. the empirical span-level divergence
  finding.
"""

from gaia.lang import (
    abduction,
    claim,
    compare,
    contradiction,
    deduction,
    induction,
    support,
)

from .motivation import (
    claim_empirical_validation_announced,
    claim_grpo_coarse_grained,
    claim_headline_contribution,
    claim_hidden_state_signal_exists,
    claim_prm_supervision_cost,
    claim_separation_theorem_announced,
    claim_shear_method_announced,
    setup_credit_assignment_problem,
    setup_hidden_states_carry_signal,
    setup_prm_alternative,
    setup_rlvr_grpo_paradigm,
)
from .s2_empirical_observation import (
    claim_aggregate_and_local_complementary,
    claim_appendix_a_cross_sectional,
    claim_fig1a_aggregate_anticorrelation,
    claim_fig1b_local_anticorrelation,
    claim_self_supervised_signal_proposal,
    setup_diagnostic_protocol,
    setup_mutation_threshold,
    setup_sliding_window_diagnostic,
)
from .s3_method import (
    claim_advantage_direction_preserved,
    claim_appendix_h_max_vs_mean,
    claim_self_supervised_no_extra_model,
    claim_step1_min_distance,
    claim_step2_global_norm_norm,
    claim_step3_max_pooling,
    claim_step4_weighted_advantage,
    claim_w_captures_more_than_mean_shift,
    setup_grpo_update_eq1,
    setup_opposing_set_eq4,
    setup_span_decomposition_eq2,
    setup_wasserstein_definition,
)
from .s4_separation_theorem import (
    claim_appendix_d_first_moment_bound,
    claim_lemma1_sinkhorn_approximation,
    claim_prop_f1_correct_rollouts,
    claim_prop_g1_multiple_divergences,
    claim_remark_c1_non_cancellation,
    claim_thm1_post_divergence_lower_bound,
    claim_thm1_pre_divergence_upper_bound,
    claim_thm1_strict_separation,
    claim_thm2_design_justification,
    claim_thm2_group_separation,
    setup_a1_divergence_structure,
    setup_a2_bounded_support,
    setup_a3_concentration,
    setup_group_level_minimum,
    setup_population_distance,
)
from .s5_signal_analysis import (
    claim_fig3_auc_monotonic,
    claim_fig3_topleft_within_bin_separation,
    claim_signal_finite_sample_practical,
    claim_thm1_condition_verified,
    setup_section51_protocol,
)
from .s6_experimental_setup import (
    claim_diversity_of_evaluation,
    claim_strong_baselines,
    setup_backbones,
    setup_baselines,
    setup_checkpoint_selection,
    setup_code_eval,
    setup_math_eval,
    setup_training_datasets,
)
from .s7_main_results import (
    claim_code_smaller_margin_long_chains,
    claim_shear_beats_entropy_adv,
    claim_shear_beats_grpo_universal,
    claim_shear_beats_prm_on_math,
    claim_table1_llama_8b,
    claim_table1_qwen_14b,
    claim_table1_qwen_math_7b,
    claim_table2_code_results,
    claim_training_dynamics_fig4,
)
from .s8_ablations import (
    claim_5_4_1_distance_metric_ablation,
    claim_5_4_1_distributional_signal_richer,
    claim_5_4_2_cross_vs_per_rollout,
    claim_5_4_2_within_rollout_dominates,
    claim_5_5_span_stride_sensitivity,
    claim_5_6_rollout_group_size,
    claim_section6_overhead,
)
from .s9_qualitative import (
    claim_appendix_h3_prm_connection,
    claim_appendix_k_case_study,
    claim_pure_bottom_line,
    claim_related_credit_assignment,
    claim_related_token_reshaping,
    claim_section8_conclusion,
    setup_scope_limitations,
)

# ===========================================================================
# Pass 2 strategies: section 2 empirical observation
# ===========================================================================

# Aggregate + local independent observations -> complementary synthesis.
strat_complementary_signal = support(
    [claim_fig1a_aggregate_anticorrelation, claim_fig1b_local_anticorrelation],
    claim_aggregate_and_local_complementary,
    reason=(
        "@claim_fig1a_aggregate_anticorrelation alone could be a length "
        "artifact (both curves drift over chain position regardless of "
        "correctness). @claim_fig1b_local_anticorrelation isolates "
        "stride-wise local shifts within the same rollout, controlling "
        "for the length confound and showing reasoning-quality drops "
        "co-occur with hidden-state divergence rises *at the local "
        "stride scale*. Together they rule out the length-only "
        "alternative."
    ),
    prior=0.93,
    background=[setup_diagnostic_protocol, setup_sliding_window_diagnostic, setup_mutation_threshold],
)

# Self-supervised signal proposal supported by complementary observation.
strat_self_supervised_proposal = support(
    [claim_aggregate_and_local_complementary],
    claim_self_supervised_signal_proposal,
    reason=(
        "@claim_aggregate_and_local_complementary establishes that the "
        "$W$-on-hidden-states signal carries genuine local reasoning-"
        "quality information (the necessary precondition). Since the "
        "computation uses *only* outcome-level labels $r^{(i)} \\in "
        "\\{0,1\\}$ to partition correct/incorrect within a GRPO group, "
        "the signal qualifies as self-supervised."
    ),
    prior=0.95,
    background=[setup_rlvr_grpo_paradigm],
)

# ===========================================================================
# Pass 2 strategies: section 4 separation theorem (deductions)
# ===========================================================================

# Theorem 1 part (i) -- pre-divergence upper bound. Pure deduction from
# (A1)-(A3) + triangle inequality. Treat as deduction from the assumption
# settings (no premise claims; assumptions are settings).
# To wire it as a *strategy*, support from (A2)+(A3) treated as background.
# Under gaia.lang, deduction takes premise claims; pure-derivation claims
# without premises are leaves. So leave Theorem 1 (i) as a leaf with high
# prior in priors.py (0.99 -- it's a textbook calculation given the
# assumptions).

# Theorem 1 part (iii) -- strict separation -- deduces from (i) + (ii).
strat_thm1_strict_sep = deduction(
    [claim_thm1_pre_divergence_upper_bound, claim_thm1_post_divergence_lower_bound],
    claim_thm1_strict_separation,
    reason=(
        "Combine @claim_thm1_pre_divergence_upper_bound ($E[W^{pre}_1] "
        "\\leq \\eta(n, d)$) with @claim_thm1_post_divergence_lower_bound "
        "($E[W^{post}_1] \\geq D(S) - \\eta(n, d)$): subtract to get "
        "$E[W^{post}_1] - E[W^{pre}_1] \\geq D(S) - 2\\eta(n, d) > 0$ "
        "when $D(S) > 2\\eta(n, d)$. Pure algebra given the two bounds."
    ),
    prior=0.999,
    background=[setup_a1_divergence_structure, setup_a2_bounded_support, setup_a3_concentration, setup_population_distance],
)

# Theorem 2 -- group-level separation -- deduces from Theorem 1 (i, ii)
# applied to each (k, j) opposing pair plus the latest-divergence-point
# definition.
strat_thm2_group_sep = deduction(
    [claim_thm1_pre_divergence_upper_bound, claim_thm1_post_divergence_lower_bound],
    claim_thm2_group_separation,
    reason=(
        "Theorem 2 generalises Theorem 1 to the group-level minimum: "
        "if $b \\leq \\tau^*$, at least one correct rollout has a "
        "matching pre-divergence span, so the minimum admits the "
        "pairwise pre-divergence upper bound (@claim_thm1_pre_divergence_upper_bound). "
        "If $a > \\tau^*$, for *every* opposing span the reverse-"
        "triangle pairwise lower bound (@claim_thm1_post_divergence_lower_bound) "
        "applies; taking the minimum yields the stated $D^*(S) - \\eta(n, d)$ "
        "result."
    ),
    prior=0.99,
    background=[setup_group_level_minimum],
)

# Theorem 2 design-justification: a soft consequence of the conditional
# theorem (low D* -> low weight is appropriate).
strat_thm2_design_justification = support(
    [claim_thm2_group_separation],
    claim_thm2_design_justification,
    reason=(
        "@claim_thm2_group_separation is *conditional* on $D^*(S) > "
        "2\\eta(n, d)$. Spans with small $D^*$ get small min-distance "
        "in expectation -- exactly the regime where the algorithm "
        "*correctly* assigns a low weight. So the algorithm's behaviour "
        "tracks the theorem's conditional structure: the low-weight "
        "regime is *not failure*, it is the appropriate response to "
        "indistinguishable spans."
    ),
    prior=0.92,
)

# Wasserstein > mean shift (Proposition D.1) deduction.
# Proposition D.1 itself is the leaf; the consequence
# claim_w_captures_more_than_mean_shift is the *interpretive summary*.
strat_w_richer_than_cosine = deduction(
    [claim_appendix_d_first_moment_bound],
    claim_w_captures_more_than_mean_shift,
    reason=(
        "@claim_appendix_d_first_moment_bound (Proposition D.1) gives "
        "$D(S) \\geq \\|(1/n) \\sum_t (m^-_t - m^+_t)\\|_2$ (linear $f$ "
        "bound) and $D(S) = \\sup_{\\|f\\|_{Lip} \\leq 1} \\ldots$ (KR "
        "duality). The supremum over all 1-Lipschitz functions strictly "
        "generalises the linear-$f$ bound, hence $W_1$ captures "
        "structural information beyond first-moment shift."
    ),
    prior=0.99,
)

# Symmetric correct-rollout result (Proposition F.1) -- structurally
# identical to Theorem 1.
strat_prop_f1_correct = deduction(
    [claim_thm1_strict_separation],
    claim_prop_f1_correct_rollouts,
    reason=(
        "@claim_thm1_strict_separation gives the strict separation for "
        "spans in incorrect rollouts. The proof of Proposition F.1 "
        "exchanges the roles of $P_t$ and $Q_t$ -- the structural "
        "argument (triangle / reverse-triangle inequality + (A3)) is "
        "symmetric in the two distributions. Hence the same bounds hold "
        "for spans in correct rollouts."
    ),
    prior=0.99,
)

# ===========================================================================
# Pass 2 strategies: Section 5.1 verification
# ===========================================================================

strat_auc_verifies_thm1_condition = support(
    [claim_fig3_auc_monotonic, claim_fig3_topleft_within_bin_separation],
    claim_thm1_condition_verified,
    reason=(
        "The monotonic AUC growth in @claim_fig3_auc_monotonic (0.644 "
        "at low $W$ -> 0.988 at high $W$) is the empirical analog of "
        "the population-level inequality $D(S) > 2\\eta(n, d)$ in "
        "Theorem 1. @claim_fig3_topleft_within_bin_separation confirms "
        "the within-bin correct-vs-incorrect stratification, ruling "
        "out the alternative that AUC growth is a pure aggregate "
        "artifact."
    ),
    prior=0.93,
    background=[setup_section51_protocol],
)

strat_signal_practical = support(
    [claim_thm1_condition_verified],
    claim_signal_finite_sample_practical,
    reason=(
        "@claim_thm1_condition_verified shows the strict-separation "
        "condition is empirically met *at finite sample sizes* used "
        "during training (AUC up to 0.99), not merely as an asymptotic "
        "guarantee. This validates using $W_1$ as a token-level weight "
        "in GRPO without external supervision."
    ),
    prior=0.93,
)

# ===========================================================================
# Pass 2 strategies: Method (Section 3) inferences
# ===========================================================================

strat_method_self_supervised = support(
    [claim_step1_min_distance, claim_step4_weighted_advantage],
    claim_self_supervised_no_extra_model,
    reason=(
        "@claim_step1_min_distance computes Sinkhorn distances between "
        "in-group rollout span distributions (already-produced hidden "
        "states), partitioned by binary outcome labels (already-"
        "produced GRPO rewards). @claim_step4_weighted_advantage "
        "multiplies the existing GRPO advantage. No PRM training, no "
        "step-level annotation, no auxiliary forward passes -- the "
        "algorithm consumes only what GRPO already produces."
    ),
    prior=0.97,
    background=[setup_grpo_update_eq1, setup_opposing_set_eq4, setup_span_decomposition_eq2, setup_wasserstein_definition],
)

# Direction preservation -- definitional consequence of omega >= 0.
strat_direction_preserved = deduction(
    [claim_step3_max_pooling, claim_step4_weighted_advantage],
    claim_advantage_direction_preserved,
    reason=(
        "@claim_step3_max_pooling defines $\\omega^{(i)}_t = (1/\\bar n) "
        "\\max_k d^{(i)}_k$ where $d^{(i)}_k \\geq 0$ (Wasserstein "
        "distances) and $\\bar n > 0$, so $\\omega^{(i)}_t \\geq 0$. "
        "@claim_step4_weighted_advantage gives $\\tilde A^{(i)}_t = "
        "A^{(i)} \\cdot \\omega^{(i)}_t$, so $\\text{sign}(\\tilde A) = "
        "\\text{sign}(A)$."
    ),
    prior=0.999,
)

# ===========================================================================
# Pass 2 strategies: Section 5 main results -> aggregated qualitative claims
# ===========================================================================

# Each per-(backbone, modality) measurement is *predicted by* the
# universal law. We use the generative direction: support([law], obs).
s_grpo_qwen_math = support(
    [claim_shear_beats_grpo_universal],
    claim_table1_qwen_math_7b,
    reason=(
        "If the universal law @claim_shear_beats_grpo_universal holds "
        "(SHEAR > GRPO on every backbone x modality), it predicts "
        "SHEAR > GRPO on Qwen2.5-Math-7B math; @claim_table1_qwen_math_7b "
        "(SHEAR avg 51.2 > GRPO avg 49.6, +1.6 pts) is the confirming "
        "observation."
    ),
    prior=0.95,
)
s_grpo_llama = support(
    [claim_shear_beats_grpo_universal],
    claim_table1_llama_8b,
    reason=(
        "If the universal law holds, it predicts SHEAR > GRPO on "
        "Llama3.1-8B-Instruct math; @claim_table1_llama_8b (SHEAR "
        "avg 26.2 > GRPO avg 24.7, +1.5 pts) is the confirming "
        "observation."
    ),
    prior=0.95,
)
s_grpo_qwen14b = support(
    [claim_shear_beats_grpo_universal],
    claim_table1_qwen_14b,
    reason=(
        "If the universal law holds, it predicts SHEAR > GRPO on "
        "Qwen2.5-14B-Base math; @claim_table1_qwen_14b (SHEAR avg "
        "46.9 > GRPO avg 45.4, +1.5 pts) is the confirming observation."
    ),
    prior=0.95,
)
s_grpo_code = support(
    [claim_shear_beats_grpo_universal],
    claim_table2_code_results,
    reason=(
        "If the universal law holds, it predicts SHEAR > GRPO on the "
        "code modality across backbones; @claim_table2_code_results "
        "(SHEAR > GRPO on all 3 code backbones, +0.8/+1.1/+0.6 pts) "
        "is the confirming observation."
    ),
    prior=0.93,
)

# Cross-(backbone, modality) induction.
ind_universal_12 = induction(
    s_grpo_qwen_math,
    s_grpo_llama,
    law=claim_shear_beats_grpo_universal,
    reason=(
        "Qwen2.5-Math-7B and Llama3.1-8B-Instruct are independent "
        "model families (different pretraining, different tokenizers, "
        "different architectures); both confirm SHEAR > GRPO on math."
    ),
)
ind_universal_123 = induction(
    ind_universal_12,
    s_grpo_qwen14b,
    law=claim_shear_beats_grpo_universal,
    reason=(
        "Qwen2.5-14B-Base is a different model size (14B vs. 7B/8B) "
        "and a *base* (non-instruct) model; an additional independent "
        "confirmation at scale."
    ),
)
ind_universal = induction(
    ind_universal_123,
    s_grpo_code,
    law=claim_shear_beats_grpo_universal,
    reason=(
        "Code generation is a different modality from math reasoning "
        "(different reward structure, different chain length, "
        "different training set). Confirms the law on a third "
        "independent task family."
    ),
)

# PRM-comparison claim -- supported by Tables 1 (3 backbones).
strat_shear_beats_prm = support(
    [claim_table1_qwen_math_7b, claim_table1_llama_8b, claim_table1_qwen_14b],
    claim_shear_beats_prm_on_math,
    reason=(
        "All three Table 1 panels show SHEAR avg > both PRM(Reshape) "
        "and PRM(PURE) avgs. The 14B panel is the strongest: PRM "
        "variants fall *below* GRPO (-4.2 / -8.0 pts), consistent with "
        "the PRM-policy mismatch interpretation given in the paper."
    ),
    prior=0.92,
)

# Entropy-adv comparison -- supported by all three math panels.
strat_shear_beats_entropy = support(
    [claim_table1_qwen_math_7b, claim_table1_llama_8b, claim_table1_qwen_14b],
    claim_shear_beats_entropy_adv,
    reason=(
        "All three Table 1 panels show SHEAR avg > Entropy adv. avg "
        "(51.2>49.5, 26.2>25.1, 46.9>46.3). Consistent with the "
        "interpretation that distributional divergence carries strictly "
        "richer info than per-token entropy."
    ),
    prior=0.93,
)

# Code-modality 'longest chain' interpretation.
strat_code_long_chains = support(
    [claim_table2_code_results],
    claim_code_smaller_margin_long_chains,
    reason=(
        "Within Table 2, SHEAR's improvements are smaller on the "
        "shortest benchmarks (HumanEval, MBPP) and largest on "
        "LiveCodeBench (longest, contamination-free). This pattern is "
        "what the method's design predicts: localized credit assignment "
        "needs long-enough chains for local errors to be distinguishable."
    ),
    prior=0.85,
)

# Training dynamics confirms sustained advantage.
strat_training_dynamics = support(
    [claim_table1_qwen_math_7b, claim_table1_llama_8b, claim_table1_qwen_14b],
    claim_training_dynamics_fig4,
    reason=(
        "Figure 4 shows the training-step trajectories of the same "
        "experiments aggregated in @claim_table1_qwen_math_7b, "
        "@claim_table1_llama_8b, @claim_table1_qwen_14b. The pattern "
        "(early-similar, late-divergent, no instability) is consistent "
        "across all three backbones."
    ),
    prior=0.85,
)

# Empirical-validation announced claim (motivation level) supported by
# the universal cross-setup law and the PRM-beating claim.
strat_empirical_validation = support(
    [
        claim_shear_beats_grpo_universal,
        claim_shear_beats_prm_on_math,
        claim_shear_beats_entropy_adv,
    ],
    claim_empirical_validation_announced,
    reason=(
        "@claim_empirical_validation_announced summarises three "
        "empirical claims: SHEAR > GRPO universally "
        "(@claim_shear_beats_grpo_universal); SHEAR > PRM on math "
        "(@claim_shear_beats_prm_on_math); SHEAR > Entropy adv. "
        "(@claim_shear_beats_entropy_adv). Their conjunction is the "
        "announced empirical validation."
    ),
    prior=0.95,
)

# ===========================================================================
# Pass 2 strategies: Section 5.4 ablation -- distance metric induction
# ===========================================================================

# Distribution-aware metrics succeed; mean-only fails. Induction over the
# four ablation variants (W, Chamfer, MMD vs. Cosine).

# Per-variant observation predicted by the law. Generative direction:
# support([law], obs).
# Note: the four ablation observations live in a single claim
# (@claim_5_4_1_distance_metric_ablation, the table), so we materialize
# the per-variant ablation observations as separate sub-observations
# of the law.
s_dist_w_obs = claim(
    "**Wasserstein variant beats GRPO baseline (peak 0.5068 vs. 0.4884).**",
    title="Sec 5.4.1 sub-observation: Wasserstein > GRPO",
)
s_dist_chamfer_obs = claim(
    "**Chamfer variant beats GRPO baseline (peak 0.5051 vs. 0.4884).**",
    title="Sec 5.4.1 sub-observation: Chamfer > GRPO",
)
s_dist_mmd_obs = claim(
    "**MMD-RBF variant beats GRPO baseline (peak 0.5061 vs. 0.4884).**",
    title="Sec 5.4.1 sub-observation: MMD > GRPO",
)
s_dist_cosine_obs = claim(
    "**Cosine variant *underperforms* GRPO baseline (peak 0.4837 < 0.4884).**",
    title="Sec 5.4.1 sub-observation: Cosine < GRPO (mean-only fails)",
)

# Each sub-observation supported by the umbrella ablation table.
strat_w_obs = support(
    [claim_5_4_1_distance_metric_ablation],
    s_dist_w_obs,
    reason="Direct readout from @claim_5_4_1_distance_metric_ablation row Wasserstein.",
    prior=0.97,
)
strat_chamfer_obs = support(
    [claim_5_4_1_distance_metric_ablation],
    s_dist_chamfer_obs,
    reason="Direct readout from @claim_5_4_1_distance_metric_ablation row Chamfer.",
    prior=0.97,
)
strat_mmd_obs = support(
    [claim_5_4_1_distance_metric_ablation],
    s_dist_mmd_obs,
    reason="Direct readout from @claim_5_4_1_distance_metric_ablation row MMD.",
    prior=0.97,
)
strat_cosine_obs = support(
    [claim_5_4_1_distance_metric_ablation],
    s_dist_cosine_obs,
    reason="Direct readout from @claim_5_4_1_distance_metric_ablation row Cosine.",
    prior=0.97,
)

# Now the law -> per-variant supports.
s_dist_w = support(
    [claim_5_4_1_distributional_signal_richer],
    s_dist_w_obs,
    reason=(
        "If the distributional-signal-richer law holds (full-distribution "
        "metrics beat the baseline; mean-only fails), then the optimal-"
        "transport variant should beat GRPO -- @s_dist_w_obs confirms."
    ),
    prior=0.9,
)
s_dist_chamfer = support(
    [claim_5_4_1_distributional_signal_richer],
    s_dist_chamfer_obs,
    reason=(
        "If the law holds, Chamfer (point-cloud, captures geometric "
        "coverage but not proper transport) should beat GRPO -- "
        "@s_dist_chamfer_obs confirms; independent confirmation."
    ),
    prior=0.85,
)
s_dist_mmd = support(
    [claim_5_4_1_distributional_signal_richer],
    s_dist_mmd_obs,
    reason=(
        "If the law holds, MMD-RBF (kernel-embedding, captures all "
        "moments via feature map) should beat GRPO -- @s_dist_mmd_obs "
        "confirms; independent confirmation."
    ),
    prior=0.85,
)
s_dist_cosine_negative = support(
    [claim_5_4_1_distributional_signal_richer],
    s_dist_cosine_obs,
    reason=(
        "If the law holds, Cosine (mean-only) should NOT beat GRPO "
        "(prediction includes the negative-direction case). "
        "@s_dist_cosine_obs (Cosine 0.4837 < GRPO 0.4884) confirms; "
        "Proposition D.1 (@claim_appendix_d_first_moment_bound) "
        "predicts this: mean-only metrics lose higher-order "
        "distributional information."
    ),
    prior=0.9,
)

ind_dist_aware_12 = induction(
    s_dist_w,
    s_dist_chamfer,
    law=claim_5_4_1_distributional_signal_richer,
    reason=(
        "Wasserstein and Chamfer are *independent* distributional "
        "metrics (different mathematical structure: optimal transport "
        "vs. point-cloud); both confirm the distribution-aware-metrics-"
        "win law."
    ),
)
ind_dist_aware = induction(
    ind_dist_aware_12,
    s_dist_mmd,
    law=claim_5_4_1_distributional_signal_richer,
    reason=(
        "MMD-RBF is a third independent distributional metric (kernel "
        "embedding via RBF feature map). A third confirmation. The "
        "Cosine negative result (also recorded as $s_dist_cosine_negative$) "
        "completes the picture: mean-only metrics fail."
    ),
)

# ===========================================================================
# Pass 2 strategies: Section 5.4.2 cross-rollout ablation
# ===========================================================================

strat_within_rollout_dominates = support(
    [claim_5_4_2_cross_vs_per_rollout, claim_thm2_group_separation],
    claim_5_4_2_within_rollout_dominates,
    reason=(
        "@claim_5_4_2_cross_vs_per_rollout shows per-rollout "
        "normalization (which removes cross-rollout reweighting) still "
        "beats GRPO by +1.1 pts. This isolates the within-rollout "
        "ranking as the dominant signal source. @claim_thm2_group_"
        "separation directly addresses this within-rollout ranking, "
        "providing the theoretical anchor."
    ),
    prior=0.9,
)

# ===========================================================================
# Pass 2 strategies: Section 5.6 group size ablation
# ===========================================================================

# Larger G -> richer opposing set -> better W estimates -- empirical
# observation; treat as leaf with high prior in priors.py.

# ===========================================================================
# Pass 2 strategies: motivation-level diagnosis
# ===========================================================================

# Diagnoses (claim_grpo_coarse_grained, claim_prm_supervision_cost) are
# essentially definitional given the GRPO update form and PRM training
# protocol. Treat as independent leaves; the BP graph downstream uses
# them via the abductions and contradictions.

# ===========================================================================
# Pass 3 / Pass 4 strategies: methodological consistency
# ===========================================================================

# The method (announced in motivation) is exactly the algorithm in
# Section 3. Wire that up.
strat_shear_method_announced = support(
    [
        claim_step1_min_distance,
        claim_step2_global_norm_norm,
        claim_step3_max_pooling,
        claim_step4_weighted_advantage,
    ],
    claim_shear_method_announced,
    reason=(
        "The four-step Algorithm 1 components "
        "(@claim_step1_min_distance through @claim_step4_weighted_advantage) "
        "*are* the SHEAR method announced in the abstract / Section 1. "
        "Their conjunction defines $\\tilde A^{(i)}_t = A^{(i)} \\cdot "
        "\\omega^{(i)}_t$ via the four-step pipeline."
    ),
    prior=0.99,
)

# Separation theorem announced -- supported by Theorems 1 + 2 (formal results).
strat_separation_thm_announced = support(
    [claim_thm1_strict_separation, claim_thm2_group_separation],
    claim_separation_theorem_announced,
    reason=(
        "@claim_thm1_strict_separation is the pairwise separation "
        "theorem; @claim_thm2_group_separation extends it to the "
        "group-level minimum used in Algorithm 1. Together they "
        "*are* the separation theorem announced in Section 1 / "
        "abstract."
    ),
    prior=0.99,
)

# Hidden-state signal exists -- supported by Section 2 + Section 5.1.
strat_signal_exists = support(
    [
        claim_fig1a_aggregate_anticorrelation,
        claim_fig1b_local_anticorrelation,
        claim_signal_finite_sample_practical,
    ],
    claim_hidden_state_signal_exists,
    reason=(
        "@claim_fig1a_aggregate_anticorrelation (Spearman -0.96 "
        "aggregate) + @claim_fig1b_local_anticorrelation (Spearman "
        "-0.42 within-trajectory, p=4.6e-59) + @claim_signal_finite_"
        "sample_practical (Section 5.1 AUC up to 0.99) jointly "
        "establish the empirical claim announced in Section 1."
    ),
    prior=0.95,
)

# Headline contribution = signal exists + theorem + method + empirical
# validation.
strat_headline_contribution = support(
    [
        claim_hidden_state_signal_exists,
        claim_separation_theorem_announced,
        claim_shear_method_announced,
        claim_empirical_validation_announced,
    ],
    claim_headline_contribution,
    reason=(
        "The headline is the conjunction: (i) signal exists "
        "(@claim_hidden_state_signal_exists), (ii) separation theorem "
        "justifies it (@claim_separation_theorem_announced), (iii) "
        "SHEAR operationalises it (@claim_shear_method_announced), "
        "(iv) empirical validation confirms operationally (@claim_"
        "empirical_validation_announced)."
    ),
    prior=0.95,
)

# ===========================================================================
# Bottom-line conclusion
# ===========================================================================

strat_pure_bottom_line = support(
    [claim_headline_contribution, claim_section6_overhead],
    claim_pure_bottom_line,
    reason=(
        "The bottom line restates the headline contribution "
        "(@claim_headline_contribution) with the practical-cost qualifier "
        "from @claim_section6_overhead (<16% overhead)."
    ),
    prior=0.95,
)

strat_section8_conclusion = support(
    [claim_pure_bottom_line, claim_appendix_h3_prm_connection],
    claim_section8_conclusion,
    reason=(
        "The Section 8 conclusion is the bottom-line "
        "(@claim_pure_bottom_line) plus the PRM-connection interpretive "
        "framing (@claim_appendix_h3_prm_connection): SHEAR recovers "
        "the PRM signal from hidden-state distributional structure "
        "without step-level supervision."
    ),
    prior=0.93,
)

# ===========================================================================
# CENTRAL ABDUCTION: WHY does the W-signal work?
# ===========================================================================

claim_signal_explains_via_hidden_states = claim(
    "**Hypothesis: span-level Wasserstein distance on hidden states "
    "works because hidden-state distributions encode *local reasoning "
    "quality* in a structurally-faithful way (per the separation "
    "theorem and KR-duality argument).** The mechanism is: hidden "
    "states summarise the evolving reasoning context; reasoning "
    "errors induce systematic distributional differences that are "
    "*not* mean-shifts only but include shape / variance / higher-"
    "moment structure; the optimal-transport metric captures all "
    "1-Lipschitz functionals of this difference and so most "
    "completely transcribes local quality into a scalar weight.",
    title="Hypothesis: $W$ on hidden states works because hidden-state distributions encode local reasoning quality faithfully",
)

claim_signal_alt_any_reweighting = claim(
    "**Alternative hypothesis: SHEAR's gain comes from *any* token-"
    "level reweighting that breaks GRPO's uniform-advantage structure -- "
    "the specific choice of metric, the hidden-state representation, "
    "and the theoretical separation argument are not the load-"
    "bearing components.** Under this alternative, any "
    "non-degenerate weighting (e.g. random, entropy-only, mean-"
    "shift-only) should produce comparable improvement, because the "
    "real gain is just from optimization-noise reduction.",
    title="Alternative: any non-uniform token reweighting suffices; metric and hidden-states irrelevant",
)

# Predictions.
pred_hidden_states_faithful = claim(
    "**Hidden-state-faithful prediction:** (i) Mean-only metrics "
    "(cosine) should *fail* because they drop the higher-moment "
    "information the separation theorem proves is informative. (ii) "
    "The within-trajectory local association (Section 2 Figure 1b, "
    "Spearman -0.42) and the within-bin AUC stratification (Section "
    "5.1 Figure 3) should *both* hold, because the signal is local-"
    "reasoning-quality-tracking, not aggregate-only. (iii) "
    "Distribution-aware metrics other than $W_1$ (Chamfer, MMD) "
    "should *also* succeed because they all capture distributional "
    "info beyond mean shift -- but $W_1$ should be tightest.",
    title="Prediction (faithful): cosine fails; W/Chamfer/MMD all win; local + within-bin both hold",
)

pred_any_reweighting = claim(
    "**Any-reweighting alternative's prediction:** All token-level "
    "weightings should be roughly comparable in benefit; in "
    "particular, mean-only weights (cosine) should *not* "
    "underperform GRPO because they still break uniformity.",
    title="Prediction (alt): all reweightings comparable; cosine should also beat GRPO",
)

s_h_signal = support(
    [claim_signal_explains_via_hidden_states],
    claim_5_4_1_distance_metric_ablation,
    reason=(
        "If the hidden-state-faithful hypothesis "
        "@claim_signal_explains_via_hidden_states holds, then "
        "(@pred_hidden_states_faithful) cosine should fail (mean-only "
        "discards informative higher moments) while $W_1$, Chamfer, "
        "MMD all succeed. The observed Section 5.4.1 numbers "
        "(@claim_5_4_1_distance_metric_ablation: cosine 0.4837 < "
        "GRPO 0.4884; $W_1$/Chamfer/MMD 0.50-0.51 > GRPO) match this "
        "prediction exactly."
    ),
    prior=0.93,
)
s_alt_signal = support(
    [claim_signal_alt_any_reweighting],
    claim_5_4_1_distance_metric_ablation,
    reason=(
        "If the any-reweighting alternative @claim_signal_alt_any_"
        "reweighting held, all weightings should be roughly comparable "
        "in benefit; cosine should not actively *hurt* learning. The "
        "observed cosine 0.4837 < GRPO 0.4884 *contradicts* this "
        "alternative's prediction. Prior 0.2 reflects the "
        "alternative's low explanatory power."
    ),
    prior=0.2,
)
comp_signal = compare(
    pred_hidden_states_faithful,
    pred_any_reweighting,
    claim_5_4_1_distance_metric_ablation,
    reason=(
        "The Section 5.4.1 ablation (@claim_5_4_1_distance_metric_ablation) "
        "discriminates: cosine UNDERPERFORMS GRPO (consistent with the "
        "faithful-hypothesis prediction; inconsistent with the any-"
        "reweighting alternative); the three distribution-aware "
        "metrics OUTPERFORM (consistent with both H and Alt, but the "
        "Alt does not predict the cosine failure)."
    ),
    prior=0.95,
)

abd_signal_mechanism = abduction(
    s_h_signal,
    s_alt_signal,
    comp_signal,
    reason=(
        "Two competing explanations of why SHEAR works: (H) the "
        "hidden-state distributions faithfully encode local reasoning "
        "quality and the choice of distributional metric matters; "
        "(Alt) any non-uniform token weighting suffices. The Section "
        "5.4.1 ablation discriminates: cosine actively hurts (predicted "
        "by H, contradicted by Alt); distribution-aware metrics win "
        "consistently. The within-trajectory local association "
        "(Section 2 Fig 1b) and the within-bin AUC stratification "
        "(Section 5.1) further reinforce the faithful-encoding "
        "hypothesis."
    ),
)

# ===========================================================================
# CONTRADICTIONS
# ===========================================================================

# Contradiction 1: prevailing assumption "fine-grained credit assignment
# in RLVR requires per-step annotation" vs. SHEAR's outcome-only
# demonstration.
claim_prevailing_step_annotation_required = claim(
    "**Prevailing assumption: fine-grained credit assignment in RLVR "
    "requires per-step annotation (or a separately trained PRM that "
    "consumes such annotation).** Under this view, the absence of "
    "step-level labels makes process-level credit signals "
    "fundamentally inaccessible; outcome-only labels can only "
    "support coarse-grained credit. This is the framing implicit in "
    "the PRM line of work [@Lightman2023PRM; @Cui2025PRIME] that "
    "treats step-level supervision as the *enabling* ingredient for "
    "process-level credit.",
    title="Prevailing view: fine-grained credit -> step-level annotation needed",
)

contra_no_annotation_required = contradiction(
    claim_prevailing_step_annotation_required,
    claim_empirical_validation_announced,
    reason=(
        "If fine-grained credit assignment in RLVR fundamentally "
        "required per-step annotation (or a PRM that uses such "
        "annotation), no outcome-only-label method could match or "
        "exceed PRM-based methods on tasks where PRMs are well-suited. "
        "@claim_empirical_validation_announced demonstrates exactly "
        "the opposite: SHEAR (outcome-only labels) beats both PRM("
        "Reshape) and PRM(PURE) on every math backbone, with the "
        "gap *widening* on the larger Qwen2.5-14B-Base. They cannot "
        "both be true."
    ),
    prior=0.93,
)

# Contradiction 2: vanilla GRPO assumption "all tokens in a rollout
# deserve equal advantage" vs. the empirical span-level divergence.
claim_grpo_uniform_advantage_assumption = claim(
    "**Implicit vanilla-GRPO assumption: all tokens in a rollout "
    "deserve the *same* advantage.** Eq. 1 of [@Chen2026SHEAR] "
    "applies the scalar $A^{(i)}$ uniformly to every token in "
    "rollout $y^{(i)}$. The implicit claim is that no within-rollout "
    "token-level structure is reliably extractable from outcome-only "
    "labels, so uniform attribution is the appropriate default.",
    title="Vanilla GRPO assumption: uniform per-token advantage is the right default",
)

contra_uniform_vs_divergence = contradiction(
    claim_grpo_uniform_advantage_assumption,
    claim_aggregate_and_local_complementary,
    reason=(
        "If GRPO's uniform-advantage assumption were correct -- i.e. "
        "no within-rollout token-level structure is reliably "
        "extractable from outcome-only labels -- then there would be "
        "no signal in @claim_aggregate_and_local_complementary "
        "linking *local* hidden-state divergence to *local* "
        "reasoning-quality shifts. Section 2's within-trajectory "
        "Spearman -0.42 (p = 4.6e-59) directly demonstrates such a "
        "signal *does* exist. They cannot both be true."
    ),
    prior=0.92,
)

# ===========================================================================
# Setup -> claim wiring (related work + related concept supports)
# ===========================================================================

strat_grpo_coarse_diagnosis = support(
    [claim_related_credit_assignment],
    claim_grpo_coarse_grained,
    reason=(
        "@claim_related_credit_assignment characterises GRPO as "
        "uniform-advantage and PRMs as the dominant fine-grained "
        "alternative. The diagnosis @claim_grpo_coarse_grained is the "
        "definitional form of this characterisation."
    ),
    prior=0.93,
)

strat_prm_cost_diagnosis = support(
    [claim_related_credit_assignment],
    claim_prm_supervision_cost,
    reason=(
        "@claim_related_credit_assignment lays out the PRM annotation "
        "cost and transfer-gap problems; @claim_prm_supervision_cost "
        "is the specific diagnosis of these costs as the motivation "
        "for SHEAR's PRM-free approach."
    ),
    prior=0.92,
)

# ===========================================================================
# Limitations -> conclusion-scope support
# ===========================================================================

strat_limitations_bound_scope = support(
    [claim_pure_bottom_line],
    claim_section8_conclusion,
    reason=(
        "@claim_pure_bottom_line bounds the conclusion's scope to "
        "the regimes empirically tested. @setup_scope_limitations "
        "(scope: mixed-outcome groups, conditional theorem, single-"
        "divergence stylization, 7-14B model scale) are the explicit "
        "caveats whose acknowledgement supports the conclusion's "
        "scope."
    ),
    prior=0.85,
    background=[setup_scope_limitations],
)

# ===========================================================================
# Wire up remaining orphan claims (supplementary supports)
# ===========================================================================

# Section 5.5 (span/stride) and 5.6 (group size) ablations confirm the
# robustness of the SHEAR design choices, supporting the universal law.
strat_5_5_span_stride = support(
    [claim_shear_beats_grpo_universal],
    claim_5_5_span_stride_sensitivity,
    reason=(
        "If the universal law @claim_shear_beats_grpo_universal holds "
        "with default $w=100$, $s=25$, the law's robustness predicts "
        "that small perturbations of these hyperparameters should still "
        "outperform GRPO. @claim_5_5_span_stride_sensitivity confirms: "
        "$w \\in \\{80, 100, 120\\}$ all near-equivalent; smaller $s$ "
        "is preferable but the family is robustly above GRPO."
    ),
    prior=0.85,
)

strat_5_6_group_size = support(
    [claim_shear_beats_grpo_universal],
    claim_5_6_rollout_group_size,
    reason=(
        "If the universal law @claim_shear_beats_grpo_universal holds "
        "AND the within-rollout signal scales with the size of the "
        "opposing set (richer contrastive evidence -> better $W$ "
        "estimates), the law predicts the SHEAR-GRPO gap should "
        "*widen* at larger $G$. @claim_5_6_rollout_group_size confirms: "
        "the gap widens at $G = 16$, with SHEAR (G=16) > SHEAR (G=8) > "
        "GRPO (G=16) > GRPO (G=8)."
    ),
    prior=0.85,
)

# Appendix A.1 cross-sectional analysis supports the local-association
# claim by *controlling for chain length*.
strat_appendix_a_cross_section = support(
    [claim_aggregate_and_local_complementary],
    claim_appendix_a_cross_sectional,
    reason=(
        "@claim_aggregate_and_local_complementary asserts the W-signal "
        "is independent of length. The Appendix A.1 cross-sectional "
        "analysis @claim_appendix_a_cross_sectional confirms this by "
        "stratifying W within position bins: even within the early "
        "(0, 250] position bin, higher W weakly but consistently "
        "corresponds to lower accuracy (Spearman -0.055, p=7.6e-18); "
        "the correlation strengthens at later position bins. "
        "Independent of length."
    ),
    prior=0.88,
)

# Appendix H.1 max-pooling vs mean-pooling design justification
# supports the Step 3 claim.
strat_appendix_h1_max_pool = support(
    [claim_appendix_h_max_vs_mean],
    claim_step3_max_pooling,
    reason=(
        "@claim_appendix_h_max_vs_mean (Appendix H.1) gives the design-"
        "level justification for the max-pooling choice in Step 3 "
        "(@claim_step3_max_pooling): for boundary tokens, max-pooling "
        "preserves the post-divergence signal while mean-pooling "
        "dilutes it."
    ),
    prior=0.92,
)

# Appendix K case study -- corroborates the Section 5.1 finding via a
# single qualitative example.
strat_appendix_k_case = support(
    [claim_signal_finite_sample_practical],
    claim_appendix_k_case_study,
    reason=(
        "@claim_signal_finite_sample_practical asserts the W-signal "
        "is operational at finite sample sizes. The Appendix K case "
        "study @claim_appendix_k_case_study qualitatively visualises "
        "this on a single 4-tuples competition problem: the Wasserstein "
        "matrix between (correct, incorrect) shows clear high-discrepancy "
        "regions in post-divergence span indices."
    ),
    prior=0.85,
)

# Diversity-of-evaluation setup claim supports the universal law.
strat_diversity_of_eval = support(
    [claim_diversity_of_evaluation],
    claim_shear_beats_grpo_universal,
    reason=(
        "@claim_diversity_of_evaluation describes the heterogeneous "
        "evaluation matrix (3 model families, 3 parameter scales, 2 "
        "modalities, 10 benchmarks). This diversity is the methodological "
        "precondition for the universal cross-(backbone, modality) law "
        "@claim_shear_beats_grpo_universal -- a SHEAR-improves claim "
        "across this matrix is meaningful precisely because the matrix "
        "spans non-overlapping settings."
    ),
    prior=0.85,
)

# Lemma 1 (Sinkhorn approximation) directly supports the practical
# applicability of the separation theorem at the algorithm level.
strat_lemma1_supports_method = support(
    [claim_lemma1_sinkhorn_approximation],
    claim_self_supervised_no_extra_model,
    reason=(
        "@claim_lemma1_sinkhorn_approximation (Appendix B) bounds the "
        "Sinkhorn approximation gap by $\\epsilon \\log n \\approx 20.8$ "
        "with the paper's hyperparameters. This bound is what makes the "
        "Sinkhorn-based @claim_self_supervised_no_extra_model practical: "
        "the approximation preserves ranking when the true separation "
        "exceeds 20.8 (verified empirically in Section 5.1)."
    ),
    prior=0.88,
)

# Proposition G.1 (multi-divergence) extends Theorem 1 to the realistic
# multi-divergence setting -- supports the algorithm's robustness.
strat_propG1_supports_algorithm_robustness = support(
    [claim_prop_g1_multiple_divergences],
    claim_thm2_group_separation,
    reason=(
        "@claim_prop_g1_multiple_divergences (Appendix G) extends the "
        "single-divergence stylization (A1) to piecewise / multi-"
        "divergence rollouts: spans fully within an aligned regime "
        "satisfy the pre-divergence bound, spans fully within a "
        "drifted regime satisfy the post-divergence bound, and spans "
        "straddling a boundary exhibit intermediate distances "
        "proportional to the drifted fraction. This corroborates "
        "@claim_thm2_group_separation under realistic chain structures."
    ),
    prior=0.85,
)

# Related-work characterization: token-level reshaping -- supports
# motivation diagnosis (entropy is scalar / insufficient).
strat_related_token_reshaping_supports_signal = support(
    [claim_related_token_reshaping],
    claim_shear_beats_entropy_adv,
    reason=(
        "@claim_related_token_reshaping characterises Entropy-adv. "
        "[@Cheng2025EntropyAdv] as a scalar-entropy reshaping that "
        "cannot reliably distinguish productive reasoning pivots from "
        "genuine errors. SHEAR's distributional metric carries strictly "
        "richer info; @claim_shear_beats_entropy_adv (SHEAR > Entropy "
        "on every math backbone) confirms the empirical consequence "
        "of this characterisation."
    ),
    prior=0.8,
)

# Remark C.1 non-cancellation is verified empirically by Sec 5.1.
strat_remark_c1_verified = support(
    [claim_signal_finite_sample_practical],
    claim_remark_c1_non_cancellation,
    reason=(
        "@claim_remark_c1_non_cancellation requires $D(S) > 0$ as a "
        "regularity condition (else theorem trivially holds with both "
        "sides 0). The Section 5.1 empirical verification "
        "@claim_signal_finite_sample_practical (monotonically increasing "
        "AUC) confirms $D(S) > 0$ in practice."
    ),
    prior=0.92,
)

# Strong-baselines characterization supports the meaningfulness of the
# main results.
strat_strong_baselines_supports_results = support(
    [claim_strong_baselines],
    claim_shear_beats_prm_on_math,
    reason=(
        "@claim_strong_baselines characterises the PRM baselines as "
        "competitive 7B-scale process-reward-model variants (PURE, "
        "PRM(Reshape adv.) using Qwen2.5-Math-PRM-7B [@Zhang2025QwenPRM]). "
        "The fact that @claim_shear_beats_prm_on_math compares to these "
        "*non-strawman* baselines -- and beats them -- is what makes "
        "the result meaningful."
    ),
    prior=0.8,
)

__all__ = [
    # Section 2 wiring
    "strat_complementary_signal",
    "strat_self_supervised_proposal",
    # Section 4 wiring
    "strat_thm1_strict_sep",
    "strat_thm2_group_sep",
    "strat_thm2_design_justification",
    "strat_w_richer_than_cosine",
    "strat_prop_f1_correct",
    # Section 5.1 wiring
    "strat_auc_verifies_thm1_condition",
    "strat_signal_practical",
    # Method wiring
    "strat_method_self_supervised",
    "strat_direction_preserved",
    # Section 5.3 wiring
    "s_grpo_qwen_math",
    "s_grpo_llama",
    "s_grpo_qwen14b",
    "s_grpo_code",
    "ind_universal_12",
    "ind_universal_123",
    "ind_universal",
    "strat_shear_beats_prm",
    "strat_shear_beats_entropy",
    "strat_code_long_chains",
    "strat_training_dynamics",
    "strat_empirical_validation",
    # Section 5.4 ablation wiring
    "s_dist_w",
    "s_dist_chamfer",
    "s_dist_mmd",
    "s_dist_cosine_negative",
    "ind_dist_aware_12",
    "ind_dist_aware",
    "strat_within_rollout_dominates",
    # Method-level
    "strat_shear_method_announced",
    "strat_separation_thm_announced",
    "strat_signal_exists",
    "strat_headline_contribution",
    "strat_pure_bottom_line",
    "strat_section8_conclusion",
    # Central abduction
    "claim_signal_explains_via_hidden_states",
    "claim_signal_alt_any_reweighting",
    "pred_hidden_states_faithful",
    "pred_any_reweighting",
    "s_h_signal",
    "s_alt_signal",
    "comp_signal",
    "abd_signal_mechanism",
    # Contradictions
    "claim_prevailing_step_annotation_required",
    "contra_no_annotation_required",
    "claim_grpo_uniform_advantage_assumption",
    "contra_uniform_vs_divergence",
    # Diagnosis support
    "strat_grpo_coarse_diagnosis",
    "strat_prm_cost_diagnosis",
    # Scope
    "strat_limitations_bound_scope",
    # Supplementary supports
    "strat_5_5_span_stride",
    "strat_5_6_group_size",
    "strat_appendix_a_cross_section",
    "strat_appendix_h1_max_pool",
    "strat_appendix_k_case",
    "strat_diversity_of_eval",
    "strat_lemma1_supports_method",
    "strat_propG1_supports_algorithm_robustness",
    "strat_related_token_reshaping_supports_signal",
    "strat_remark_c1_verified",
    "strat_strong_baselines_supports_results",
    # Per-variant ablation observations + supports
    "s_dist_w_obs",
    "s_dist_chamfer_obs",
    "s_dist_mmd_obs",
    "s_dist_cosine_obs",
    "strat_w_obs",
    "strat_chamfer_obs",
    "strat_mmd_obs",
    "strat_cosine_obs",
]
