"""Reasoning wiring: strategies, abductions, inductions, contradictions.

Pass 2-4 connect the claims extracted in s2-s10 with explicit reasoning
strategies. Conventions:

* `support` -- soft deduction with author-specified prior on the
  implication warrant. The default for "premises imply conclusion".
* `deduction` -- rigid mathematical entailment (Prop. 1 derivation).
* `abduction` -- inference to best explanation (TPO's mechanism vs.
  alternative explanations of the sparse-reward gap).
* `induction` -- chained binary composite. Used twice:
  (i) Population claim "TPO matches PG-family on easy tasks" inducted
      over the bandit, MNIST, dense-token, and GSM8K settings.
  (ii) Population claim "TPO outperforms under sparse reward" inducted
       over sequential-reward Sec. 3.5, terminal-reward Sec. 3.6, and
       LLM RLVR Sec. 3.8 graph coloring.
* `contradiction` -- the prevailing PG view ("entanglement is
  fundamental") vs. TPO's empirical demonstration that decoupling
  works (sparse-reward gap). Also: KL-stabilised vs. no-KL GRPO.
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
    claim_entanglement_makes_pg_fragile,
    claim_fig1_dense_match,
    claim_fig1_sparse_outperform,
    claim_fig1_sparse_qualitative_gap,
    claim_headline_contribution,
    claim_pg_entangles_two_questions,
    claim_tpo_decouples,
    setup_sample_score_paradigm,
    setup_target_distribution,
    setup_two_questions,
)
from .s2_method import (
    claim_gradient_self_extinguishes,
    claim_prop1_gradient_p_minus_q,
    claim_prop1_target_unique,
    claim_prop1_unique_stationary,
    claim_q_fixed_supports_multi_epoch,
    claim_standardization_invariance,
    claim_token_level_grouping,
    claim_tpo_no_critic_no_dual,
    setup_kl_objective_eq4,
    setup_logits_and_group_policy,
    setup_loss_definition_eq3,
    setup_score_standardization,
    setup_target_definition_eq2,
)
from .s3_setup import (
    claim_dg_multi_epoch_unstable,
    claim_grpo_kl_strengthens_baseline,
    setup_baselines,
    setup_dg_single_epoch,
    setup_grouping_k,
    setup_grpo_strengthened,
    setup_matching_protocol,
    setup_optimizer_defaults,
)
from .s4_tabular_bandits import (
    claim_3_1_tpo_dg_fastest,
    claim_3_1_tpo_lowest_misalignment,
    claim_3_2_tpo_closest_to_ce,
    claim_beta_small_p_behavior,
    claim_beta_table,
    setup_multi_context_bandit,
    setup_one_hot_logit_form,
    setup_single_context_bandit,
)
from .s5_neural_bandit import (
    claim_concentrated_mistakes_prediction,
    claim_concentration_panel_observation,
    claim_concentration_panel_predicts,
    claim_grpo_collapses_to_reinforce,
    claim_mnist_final_errors,
    claim_mnist_tpo_fastest,
    claim_pg_grpo_grouppg_collapse_to_one_vs_rest,
    claim_tpo_dg_condition_on_action,
    setup_group_pg_ablation,
    setup_mnist_bandit,
)
from .s6_sequence_tasks import (
    claim_3_4_gap_widens,
    claim_3_5_population_match_dense,
    claim_3_5_sequential_only_tpo_dg,
    claim_per_state_targeting_explanation,
    claim_table1_steps_to_1pct,
    claim_table2_steps_to_1pct,
    setup_task_variants_3_5,
    setup_token_reversal,
)
from .s7_terminal_reward import (
    claim_3_6_interaction_match_unchanged,
    claim_3_6_steep_baseline_degradation,
    claim_3_7_no_anchor_hurts,
    claim_3_7_target_matching_essential,
    claim_3_8_graph_color_qwen_gap,
    claim_3_8_graph_color_r1_distill,
    claim_3_8_gsm8k_match,
    claim_3_8_knk_same_pattern,
    claim_3_8_population_llm_rlvr,
    claim_table3_terminal_results,
    setup_ablation_3_7,
    setup_llm_rlvr,
    setup_terminal_reward,
)
from .s8_analysis import (
    claim_4_1_grad_norm_collapse,
    claim_4_1_target_mass_allocation,
    claim_4_2_all_fail_fraction,
    claim_4_2_k_sweep,
    claim_4_2_zero_variance_masking_hurts,
    claim_4_2_zero_variance_neutrality,
    claim_4_3_epoch_sweep,
    claim_4_3_multi_epoch_speedup,
    claim_4_no_single_property,
    setup_section4_regime,
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
    claim_tpo_kl_regularised_operator,
)
from .s10_limitations import (
    claim_conclusion_restated,
    claim_lim_candidate_quality,
    claim_lim_low_variance_groups,
    claim_lim_scale_of_evaluation,
    claim_pg_view_entanglement_unavoidable,
)

# ===========================================================================
# Pass 2-4: Method-level reasoning (Sec. 2)
# ===========================================================================

# Proposition 1.1 (target uniqueness) and 1.2 (gradient form) are
# textbook math derivations from definitions only. We treat them as
# *independent leaf claims* (priors set in priors.py), since they have
# no premise claims -- only setting backgrounds. The substantive
# composite claim (1.3, unique stationary distribution = q) deduces
# from them.
#
# Proposition 1.3 -- unique stationary distribution.
strat_prop1_stationary = deduction(
    [claim_prop1_target_unique, claim_prop1_gradient_p_minus_q],
    claim_prop1_unique_stationary,
    reason=(
        "Combine @claim_prop1_target_unique (existence and uniqueness of "
        "$q$) with @claim_prop1_gradient_p_minus_q (gradient on group "
        "logits is $p^\\theta - q$): the gradient vanishes iff $p^\\theta "
        "= q$, which is unique by Prop 1.1. Hence $p^\\theta = q$ is the "
        "*unique* stationary distribution over the sampled candidates."
    ),
    prior=0.999,
)

# Self-extinguishing gradient property (combines Prop 1.2 + 1.3).
strat_self_extinguish = support(
    [claim_prop1_gradient_p_minus_q, claim_prop1_unique_stationary],
    claim_gradient_self_extinguishes,
    reason=(
        "From @claim_prop1_gradient_p_minus_q the per-step gradient on "
        "group logits is $p^\\theta - q$; from @claim_prop1_unique_stationary "
        "the unique fixed point is $p^\\theta = q$. Therefore as the policy "
        "approaches the target the gradient norm decays to zero. The "
        "claim adds the contrast 'PG-family losses do not share this fixed "
        "point' as an empirical observation (Sec. 4.1, Fig. 11(a)) -- the "
        "structural deduction is mathematical but the *behavioural* claim "
        "(self-extinguishing in practice) is supported, not deduced."
    ),
    prior=0.95,
)

# Stable multi-epoch from frozen q.
strat_q_frozen_multi_epoch = support(
    [claim_prop1_target_unique],
    claim_q_fixed_supports_multi_epoch,
    reason=(
        "When $q$ is computed once at rollout time (using rollout-snapshot "
        "$p^{\\text{old}}$ and standardized scores $u$) and treated as "
        "fixed across epochs, the multi-epoch problem reduces to "
        "minimising a *fixed* cross-entropy objective, which is a standard "
        "stable supervised problem. @claim_prop1_target_unique guarantees "
        "$q$ is well-defined and unique. The claim that *empirically* "
        "this gives stable multi-epoch behaviour is supported by Sec. 4.3."
    ),
    prior=0.92,
    background=[setup_loss_definition_eq3],
)

# Standardization invariance: leaf (textbook scale-invariance argument
# + Appendix D empirical robustness). Treat as independent claim.


# No critic, no dual loop -- structural property of finite candidate set.
strat_no_critic = support(
    [claim_prop1_target_unique],
    claim_tpo_no_critic_no_dual,
    reason=(
        "@claim_prop1_target_unique gives the target $q$ in *closed form* "
        "from rollout-snapshot probabilities $p^{\\text{old}}$ and "
        "standardized scores $u$. No critic or value estimate is needed "
        "to supply the improvement signal, and the dual / Lagrangian "
        "reduces to a simple normalisation rather than an inner "
        "optimization. This contrasts with REPS [@Peters2010REPS], MPO "
        "[@Abdolmaleki2018MPO], and V-MPO [@Song2020VMPO]."
    ),
    prior=0.97,
)

# Token-level grouping for autoregressive sequence models -- definitional.
strat_token_grouping = support(
    [claim_prop1_target_unique, claim_prop1_gradient_p_minus_q],
    claim_token_level_grouping,
    reason=(
        "The TPO machinery (target $q$ from @claim_prop1_target_unique; "
        "loss gradient $p^\\theta - q$ from @claim_prop1_gradient_p_minus_q) "
        "is defined per-group, so applying it at each prefix state of an "
        "autoregressive transformer produces TPO$_{\\text{token}}$ "
        "without any additional theoretical machinery."
    ),
    prior=0.95,
    background=[setup_logits_and_group_policy],
)

# ===========================================================================
# Section 3.1-3.2: tabular bandit reasoning
# ===========================================================================

# Sec. 3.1 result (TPO and DG converge fastest) supported by setup + the
# self-extinguishing property (TPO) and DG's sigmoid gating.
strat_3_1_result = support(
    [claim_gradient_self_extinguishes],
    claim_3_1_tpo_dg_fastest,
    reason=(
        "On the single-context bandit @setup_single_context_bandit, the "
        "self-extinguishing property @claim_gradient_self_extinguishes "
        "predicts that TPO will keep concentrating probability on $y^*$ "
        "even at low error (the gradient is non-zero whenever $p^\\theta "
        "\\ne q$, regardless of how close $\\pi(y^*)$ is to 1). PG and "
        "GRPO lack this property, which is why they plateau."
    ),
    prior=0.85,
    background=[setup_single_context_bandit],
)

strat_3_1_misalignment = support(
    [claim_gradient_self_extinguishes],
    claim_3_1_tpo_lowest_misalignment,
    reason=(
        "The same self-extinguishing structure @claim_gradient_self_extinguishes "
        "implies TPO's update direction stays anchored to the target "
        "$q$, which on this single-context one-hot bandit equals the "
        "oracle PG direction up to scale; GRPO's update keeps growing in "
        "the wrong direction as the policy concentrates because its "
        "scalar advantage weights do not vanish at convergence."
    ),
    prior=0.85,
    background=[setup_single_context_bandit],
)

# Beta table (App. B): leaf claim. Pure algebra; treated as independent.

strat_beta_small_p = deduction(
    [claim_beta_table],
    claim_beta_small_p_behavior,
    reason=(
        "Algebraic substitution into @claim_beta_table at $p_n = 0.1$, "
        "$A = 10$ ($\\lambda \\approx 28$): $\\beta_{\\text{TPO}} = "
        "0.1 \\cdot 27 / (0.9 + 28 \\cdot 0.1) = 2.7 / 3.7 \\approx 0.73$; "
        "$\\beta_{\\text{DG}} = 0.1 / 1.1 \\approx 0.091$; "
        "$\\beta_{\\text{GRPO}} = \\sqrt{0.1 / 0.9} \\approx 0.333$. "
        "Asymptotics for $p_n \\to 0$ follow from Taylor expansion."
    ),
    prior=0.99,
)

strat_3_2_result = support(
    [claim_beta_small_p_behavior],
    claim_3_2_tpo_closest_to_ce,
    reason=(
        "The closed-form analysis in @claim_beta_small_p_behavior shows "
        "TPO's per-context weight $\\beta_{\\text{TPO}}(p_n)$ stays close "
        "to CE's flat $\\beta = 1$ over the $p_n$ range traversed during "
        "training, while DG and GRPO vanish at small $p_n$ and waste step "
        "budget on already-easy contexts. This matches the experimental "
        "observation that TPO's average-error and direction-misalignment "
        "curves track CE's most closely (Figure 4)."
    ),
    prior=0.88,
    background=[setup_multi_context_bandit, setup_one_hot_logit_form],
)

# ===========================================================================
# Section 3.3: MNIST mechanism + ablation
# ===========================================================================

# MNIST final error table is a leaf observation (Figure 5(a) readout).
strat_mnist_tpo_fastest = support(
    [claim_mnist_final_errors],
    claim_mnist_tpo_fastest,
    reason=(
        "Direct readout from @claim_mnist_final_errors: TPO's final "
        "error of 2.9% is the lowest, and its 5%-error checkpoint at "
        "step 1,600 is earlier than DG's at step 2,200."
    ),
    prior=0.93,
)

# GRPO collapse to REINFORCE: leaf (App. C textbook calculation).

strat_pg_grouppg_collapse = deduction(
    [claim_grpo_collapses_to_reinforce],
    claim_pg_grpo_grouppg_collapse_to_one_vs_rest,
    reason=(
        "Appendix C derivation. PG: $g_{\\text{PG}} = p(e_y - \\pi) = p v$. "
        "Group PG (with K=10): $g_{\\text{Group PG}} = 6 p (e_y - \\pi) = "
        "6 g_{\\text{PG}}$. GRPO (single-sample, conditional on minibatch "
        "stats): from @claim_grpo_collapses_to_reinforce, also $\\propto p "
        "(e_y - \\pi)$. All three are scalar multiples of the one-vs-rest "
        "direction $v = e_y - \\pi$ in expectation."
    ),
    prior=0.99,
)

# TPO/DG condition on the sampled action: leaf claim (definitional fact
# about each method's update form, derived in Appendix C).


# Mechanism prediction.
strat_concentration_prediction = support(
    [claim_tpo_dg_condition_on_action, claim_pg_grpo_grouppg_collapse_to_one_vs_rest],
    claim_concentrated_mistakes_prediction,
    reason=(
        "The class-specific suppression structure @claim_tpo_dg_condition_on_action "
        "(only TPO does this) only helps when removing a *specific* wrong "
        "class is a useful redistribution, i.e. when wrong-class mass is "
        "concentrated on one or a few alternatives. The one-vs-rest "
        "collapse @claim_pg_grpo_grouppg_collapse_to_one_vs_rest of the "
        "non-TPO methods means they cannot exploit concentration. DG's "
        "symmetric one-vs-rest reduction (Appendix C) shows it does not "
        "have a comparable concentration-dependent term."
    ),
    prior=0.85,
)

# Concentration panel observation: leaf (Figure 5(b) numerical readout).


# Pair predicts vs. observes -> use abduction.
pred_concentrated = claim(
    "**TPO-mechanism prediction:** TPO's excess gain in $p_y$ over a "
    "generic one-vs-rest baseline rises with wrong-class concentration; "
    "DG's does not.",
    title="Prediction (TPO mechanism): excess gain rises with concentration",
)
pred_one_vs_rest_alt = claim(
    "**One-vs-rest-collapse prediction:** TPO's gain over the one-vs-rest "
    "baseline does not depend on wrong-class concentration -- if TPO's "
    "advantage came purely from a sharper scalar weight or from candidate "
    "diversity, the excess gain would be approximately concentration-"
    "independent.",
    title="Alt prediction (collapse): excess gain is concentration-independent",
)

s_h_concentration = support(
    [claim_tpo_dg_condition_on_action, claim_pg_grpo_grouppg_collapse_to_one_vs_rest],
    claim_concentration_panel_observation,
    reason=(
        "The TPO mechanism @claim_tpo_dg_condition_on_action -- "
        "class-specific suppression on a wrong sample -- predicts the "
        "concentration-rising excess gain shape (@pred_concentrated); "
        "@claim_pg_grpo_grouppg_collapse_to_one_vs_rest says the "
        "baselines have no such structure to exploit. Together they "
        "imply the rising shape observed in @claim_concentration_panel_observation."
    ),
    prior=0.85,
)
s_alt_concentration = support(
    [claim_pg_grpo_grouppg_collapse_to_one_vs_rest],
    claim_concentration_panel_observation,
    reason=(
        "Counter-hypothesis: if TPO's advantage came from a "
        "concentration-independent property shared with the PG family "
        "(sharper scalar weights, candidate set diversity, standardized-"
        "score signal), the excess gain over one-vs-rest would not rise "
        "with concentration -- yet @claim_concentration_panel_observation "
        "*does* show a rising shape, so the alternative does not explain "
        "the observation. Prior 0.25 reflects the alternative's low "
        "explanatory power."
    ),
    prior=0.25,
)
comp_concentration = compare(
    pred_concentrated,
    pred_one_vs_rest_alt,
    claim_concentration_panel_observation,
    reason=(
        "Figure 5(b) @claim_concentration_panel_observation shows excess "
        "gain rising from near zero (diffuse bin) to +0.073 (concentrated "
        "bin), and DG stays slightly negative throughout. This rising "
        "shape matches the TPO-mechanism prediction (@pred_concentrated) "
        "and contradicts the one-vs-rest-collapse prediction "
        "(@pred_one_vs_rest_alt)."
    ),
    prior=0.92,
)

abd_concentration = abduction(
    s_h_concentration,
    s_alt_concentration,
    comp_concentration,
    reason=(
        "Two competing explanations of why TPO outperforms PG-family "
        "baselines on MNIST. The TPO-mechanism story predicts a "
        "concentration-dependent gain; the one-vs-rest-collapse story "
        "predicts a flat gain. Figure 5(b) discriminates between them."
    ),
)

strat_concentration_predicts = support(
    [pred_concentrated, claim_concentration_panel_observation],
    claim_concentration_panel_predicts,
    reason=(
        "Combine the prediction @pred_concentrated (rising shape) with "
        "the observed shape in @claim_concentration_panel_observation: "
        "the predicted shape matches the observed shape qualitatively "
        "(both rise with concentration; DG flat-or-negative)."
    ),
    prior=0.9,
)

# ===========================================================================
# Section 3.4-3.5: dense token-level reasoning
# ===========================================================================

# Table 1 numerical: leaf observation (Sec. 3.4 measurement, prior in priors.py).
strat_3_4_gap_widens = support(
    [claim_table1_steps_to_1pct],
    claim_3_4_gap_widens,
    reason=(
        "Direct comparison within @claim_table1_steps_to_1pct: at $V = "
        "16$, TPO at 102 steps vs. baselines at 148 / 259 / 393 steps "
        "is a $1.5$-$3.9\\times$ gap. At $V = 2$, TPO at 58 vs. GRPO "
        "at 904 is a $15\\times$ gap."
    ),
    prior=0.95,
)

# Table 2 numerical: leaf observation (Sec. 3.5 measurement, prior in priors.py).
strat_3_5_dense = support(
    [claim_table2_steps_to_1pct],
    claim_3_5_population_match_dense,
    reason=(
        "Direct readout of the bag-of-tokens rows of "
        "@claim_table2_steps_to_1pct: TPO is fastest on all four target "
        "logics (81, 56, 55, 59 steps); the runner-up varies but is "
        "always 2-6x slower."
    ),
    prior=0.93,
)

strat_3_5_sequential = support(
    [claim_table2_steps_to_1pct],
    claim_3_5_sequential_only_tpo_dg,
    reason=(
        "Direct readout of the sequential-reward rows of "
        "@claim_table2_steps_to_1pct: TPO and DG have entries on all "
        "four target logics; GRPO and PPO have only '-' on all four."
    ),
    prior=0.95,
)

strat_per_state = support(
    [claim_standardization_invariance],
    claim_per_state_targeting_explanation,
    reason=(
        "The Appendix A convention @setup_score_standardization sets "
        "$u = 0$ on zero-variance groups; this combined with the target "
        "form makes $q = p^{\\text{old}}$ on prefixes after the first "
        "mistake, which is the structural reason TPO ignores those "
        "prefixes (no spurious signal). @claim_standardization_invariance "
        "ensures this behaviour is stable across score scales."
    ),
    prior=0.88,
    background=[setup_score_standardization, setup_target_definition_eq2],
)

# ===========================================================================
# Section 3.6 / 3.7 / 3.8 -- terminal reward & ablations
# ===========================================================================

# Table 3 numerical: leaf observation (Sec. 3.6 measurement, prior in priors.py).
strat_3_6_steep_degradation = support(
    [claim_table3_terminal_results],
    claim_3_6_steep_baseline_degradation,
    reason=(
        "Direct readout of the prompt-matched rows of @claim_table3_terminal_results: "
        "GRPO 14.5 -> 50.4 (3.5x); PPO 12.0 -> '-'; DG 33.8 -> '-'. TPO "
        "stays in 6-9% across all four $H$. The interaction-matched rows "
        "show TPO 1.8 -> 19.0 vs. baseline collapses."
    ),
    prior=0.95,
)

strat_3_6_interaction_match = support(
    [claim_table3_terminal_results],
    claim_3_6_interaction_match_unchanged,
    reason=(
        "Direct readout of the interaction-matched columns of "
        "@claim_table3_terminal_results: TPO is still lowest at every $H$. "
        "The widening of the gap relative to bag-of-tokens (where the "
        "paper notes interaction matching narrowed the gap substantially) "
        "supports the 'sparse signal extraction is the bottleneck' "
        "interpretation."
    ),
    prior=0.88,
)

# Sec 3.7 ablation results: leaf observations (priors in priors.py).


# Sec. 3.8 LLM RLVR readouts: leaf observations (priors in priors.py).
# These are the per-(model, task) measurement claims that get inducted
# into the population law @claim_3_8_population_llm_rlvr.

# Sec. 3.8 population conclusion -- induction over the (model, task) pairs.
s_llm_gsm8k = support(
    [claim_3_8_population_llm_rlvr],
    claim_3_8_gsm8k_match,
    reason=(
        "If the population claim @claim_3_8_population_llm_rlvr ('TPO's "
        "advantage transfers to billion-parameter LLM RLVR') holds, it "
        "predicts comparable GSM8K performance (saturation ceiling) plus "
        "a TPO early-learning advantage -- which is exactly what is "
        "observed."
    ),
    prior=0.88,
)
s_llm_graph = support(
    [claim_3_8_population_llm_rlvr],
    claim_3_8_graph_color_qwen_gap,
    reason=(
        "If the population claim @claim_3_8_population_llm_rlvr holds, "
        "it predicts on harder Reasoning Gym tasks the gap is wider -- "
        "the qualitative graph-coloring collapse of GRPO on Qwen3-1.7B "
        "is exactly this prediction at its sharpest."
    ),
    prior=0.88,
)
s_llm_knk = support(
    [claim_3_8_population_llm_rlvr],
    claim_3_8_knk_same_pattern,
    reason=(
        "If the population claim @claim_3_8_population_llm_rlvr holds, "
        "it predicts the same pattern on Knights & Knaves -- which is "
        "what is observed for both models."
    ),
    prior=0.85,
)
ind_llm_rlvr_12 = induction(
    s_llm_gsm8k,
    s_llm_graph,
    law=claim_3_8_population_llm_rlvr,
    reason=(
        "GSM8K and graph coloring are independent tasks with different "
        "score functions (exact-match vs. graph score); both confirm the "
        "population law @claim_3_8_population_llm_rlvr."
    ),
)
ind_llm_rlvr = induction(
    ind_llm_rlvr_12,
    s_llm_knk,
    law=claim_3_8_population_llm_rlvr,
    reason=(
        "Knights & Knaves is independent of GSM8K and graph coloring "
        "(different reasoning structure, different scorer); confirms the "
        "population law on a third independent task."
    ),
)

# ===========================================================================
# Section 4: mechanism analysis (single-cause vs. multi-cause structure)
# ===========================================================================

strat_4_1_grad_norm = support(
    [claim_gradient_self_extinguishes],
    claim_4_1_grad_norm_collapse,
    reason=(
        "The structural fixed-point property @claim_gradient_self_extinguishes "
        "predicts that TPO's gradient norm should decay to zero as "
        "$p^\\theta \\to q$, while GRPO has no such fixed point. Figure "
        "11(a) is the empirical confirmation -- TPO collapses to ~0 "
        "gradient by ep 300; GRPO maintains persistent gradient norms "
        "even after error plateaus at 12.7%."
    ),
    prior=0.9,
    background=[setup_section4_regime],
)

# Sec 4.1(b) and 4.2(a) all-fail fraction: leaf observations.

# Sec 4.2 zero-variance neutrality: this is a definitional claim that
# follows from the score-standardization convention + target form. Lift
# its underlying ingredient (the score-standardization convention as a
# claim) so we can attach a deduction. We treat the neutrality claim as
# a leaf -- its content is a textbook calculation, prior in priors.py.

# Sec 4.2 K-sweep, zv-masking results: leaf observations.

strat_4_3_speedup = support(
    [claim_q_fixed_supports_multi_epoch],
    claim_4_3_multi_epoch_speedup,
    reason=(
        "@claim_q_fixed_supports_multi_epoch predicts that multi-epoch "
        "TPO should be stable; the empirical 5x early speedup at episode "
        "400 (0.2% vs. 1.1%) is the realisation of that stability. DG's "
        "single-epoch limitation comes from @claim_dg_multi_epoch_unstable."
    ),
    prior=0.88,
    background=[setup_section4_regime],
)

# Sec 4.3 epoch sweep: leaf observation.

# Sec 4.1(b) target-mass allocation diagnostic supports the multi-causal
# synthesis: it is one of the patterns absent from baselines.
strat_4_1_alloc_supports_synthesis = support(
    [claim_4_1_target_mass_allocation],
    claim_4_no_single_property,
    reason=(
        "@claim_4_1_target_mass_allocation (TPO drives failed-candidate "
        "weight to ~0; GRPO does not) is one of the diagnostic patterns "
        "that distinguish TPO from baselines. It is part of the "
        "multi-causal synthesis @claim_4_no_single_property."
    ),
    prior=0.7,
)

# Sec 4.2 K-sweep supports the multi-causal synthesis (smooth degradation).
strat_4_2_k_sweep_supports = support(
    [claim_4_2_k_sweep],
    claim_4_no_single_property,
    reason=(
        "@claim_4_2_k_sweep documents that TPO's performance degrades "
        "smoothly with $K$ while GRPO's is non-monotonic. This is part "
        "of the diagnostic pattern @claim_4_no_single_property "
        "('performance degrades smoothly rather than abruptly when K or "
        "epoch count varies')."
    ),
    prior=0.75,
)

# Sec 4.2 zv-masking surprise also supports the multi-causal synthesis.
strat_4_2_zv_masking_supports = support(
    [claim_4_2_zero_variance_masking_hurts],
    claim_4_no_single_property,
    reason=(
        "@claim_4_2_zero_variance_masking_hurts is a surprise: the "
        "obvious 'just delete dead groups' intervention makes GRPO worse. "
        "This is consistent with the multi-causal story "
        "@claim_4_no_single_property: zero-variance neutrality is part "
        "of TPO's mechanism (@claim_4_2_zero_variance_neutrality), not "
        "an artifact to be patched out of GRPO."
    ),
    prior=0.7,
)

# Sec 4.2 neutrality (definitional) supports the masking-hurts result.
strat_neutrality_supports_masking = support(
    [claim_4_2_zero_variance_neutrality],
    claim_4_2_zero_variance_masking_hurts,
    reason=(
        "@claim_4_2_zero_variance_neutrality (TPO automatically gives "
        "$q = p^{\\text{old}}$ on zero-variance groups, hence anchor "
        "pullback in multi-epoch reuse) explains structurally why "
        "masking those groups in GRPO is harmful: the multi-epoch "
        "anchor pullback is *useful*, not noise."
    ),
    prior=0.75,
)

# Sec 4.3 epoch sweep supports the multi-causal synthesis.
strat_4_3_epoch_sweep_supports = support(
    [claim_4_3_epoch_sweep],
    claim_4_no_single_property,
    reason=(
        "@claim_4_3_epoch_sweep ('TPO < 2.3% across all epoch counts; "
        "GRPO non-monotonic') is the per-epoch-count form of the "
        "smooth-degradation pattern in @claim_4_no_single_property."
    ),
    prior=0.75,
)

# 3.7 ablation Group PG also corroborates the population-easy-match line
# via MNIST -- not really; better to corroborate the abduction.
# (Already in s_h_decouple's premise list as @claim_3_7_target_matching_essential.)

# 3.8 R1-distill graph color is part of the LLM RLVR population claim.
s_llm_graph_r1 = support(
    [claim_3_8_population_llm_rlvr],
    claim_3_8_graph_color_r1_distill,
    reason=(
        "@claim_3_8_population_llm_rlvr predicts the same TPO-better "
        "pattern across the (model, task) pairs. R1-Distill on graph "
        "coloring (TPO 0.96 vs. GRPO 0.81) is another instance."
    ),
    prior=0.8,
)

# Limitations are caveats whose acknowledgement supports the conclusion's
# scope (TPO matches/outperforms in the regimes tested).
strat_lim_supports_conclusion = support(
    [claim_lim_candidate_quality, claim_lim_scale_of_evaluation],
    claim_conclusion_restated,
    reason=(
        "The limitations @claim_lim_candidate_quality (TPO bounded by "
        "candidate quality; needs $K$ rollouts/context) and "
        "@claim_lim_scale_of_evaluation (1.5-1.7B params, 3 tasks) bound "
        "the scope of @claim_conclusion_restated. The conclusion is "
        "robustly supported *within* this scope; it does not extend to "
        "uncovered regimes."
    ),
    prior=0.7,
)

strat_4_no_single = support(
    [
        claim_4_1_grad_norm_collapse,
        claim_4_2_all_fail_fraction,
        claim_4_3_multi_epoch_speedup,
    ],
    claim_4_no_single_property,
    reason=(
        "The multi-causal claim is the conjunction of the three "
        "mechanism findings: gradient self-extinguishing "
        "(@claim_4_1_grad_norm_collapse), signal allocation on "
        "informative groups (@claim_4_2_all_fail_fraction), and stable "
        "multi-epoch reuse (@claim_4_3_multi_epoch_speedup). Each has "
        "been demonstrated; the synthesis is that they reinforce each "
        "other and are absent from the baselines."
    ),
    prior=0.85,
)

# ===========================================================================
# Motivation -- diagnosis claim wires into the related-work evidence
# ===========================================================================

# PG entangles two questions: this claim is essentially definitional
# given @setup_two_questions and the standard PG update form. We treat
# it as an independent leaf claim; the BP graph downstream uses it via
# @claim_entanglement_makes_pg_fragile.


strat_entanglement_fragile = support(
    [claim_pg_entangles_two_questions],
    claim_entanglement_makes_pg_fragile,
    reason=(
        "Given the entanglement @claim_pg_entangles_two_questions, "
        "miscalibration of the optimizer knobs (learning rate, clip, KL) "
        "directly distorts the intended redistribution. Sparse-reward "
        "regimes amplify this because the few informative groups have to "
        "dominate the average update; any miscalibration of step size "
        "relative to those rare gradients can stall learning -- exactly "
        "the pattern shown in Figure 1(b)."
    ),
    prior=0.85,
)

strat_tpo_decouples = support(
    [
        claim_prop1_target_unique,
        claim_prop1_gradient_p_minus_q,
        claim_prop1_unique_stationary,
    ],
    claim_tpo_decouples,
    reason=(
        "Proposition 1 components (@claim_prop1_target_unique, "
        "@claim_prop1_gradient_p_minus_q, @claim_prop1_unique_stationary) "
        "give the explicit Q1 (target $q$, in closed form) and the "
        "Q2-friendly cross-entropy form whose gradient $p^\\theta - q$ "
        "vanishes at $p^\\theta = q$. Together these are the formal "
        "statement that TPO decouples Q1 from Q2 by construction."
    ),
    prior=0.92,
)

# Figure 1 readouts: leaf observations (priors in priors.py).
# Note: strat_fig1_dense_supports_easy_match is moved to AFTER the
# population-easy-match claim is defined.

strat_fig1_qualitative = support(
    [claim_fig1_sparse_outperform],
    claim_fig1_sparse_qualitative_gap,
    reason=(
        "Direct interpretation of @claim_fig1_sparse_outperform: a "
        "near-zero error vs. near-1.0 error gap is qualitatively "
        "'solved-vs-not-learned', not a small percentage-point gap."
    ),
    prior=0.95,
)

# ===========================================================================
# Population claim 1: TPO matches PG-family on EASY tasks (induction)
# ===========================================================================

# A "law" claim that we confirm via several independent observations.
claim_population_easy_match = claim(
    "**Population law (easy tasks): TPO matches PG-family baselines on "
    "easier / dense-reward tasks.** Across the bandit (Sec. 3.1), "
    "multi-context bandit (Sec. 3.2), MNIST contextual bandit (Sec. "
    "3.3), dense-reward token-reversal vocabulary sweep (Sec. 3.4), "
    "and GSM8K (Sec. 3.8), TPO is *no worse* than the strongest "
    "PG-family baseline on each setting; it is often slightly faster. "
    "This is half of the headline contribution: 'matches on easy tasks'.",
    title="Population law: TPO matches PG-family on easy / dense-reward tasks",
)

s_easy_bandit = support(
    [claim_population_easy_match],
    claim_3_2_tpo_closest_to_ce,
    reason=(
        "If the population law @claim_population_easy_match holds, then "
        "on the multi-context bandit -- a relatively easy setting -- TPO "
        "should at least match the best PG-family baseline. The "
        "experimental observation @claim_3_2_tpo_closest_to_ce confirms "
        "this (TPO finishes lowest error among the RL methods)."
    ),
    prior=0.9,
)
s_easy_mnist = support(
    [claim_population_easy_match],
    claim_mnist_tpo_fastest,
    reason=(
        "@claim_population_easy_match predicts TPO matches or beats "
        "PG-family on the MNIST contextual bandit (a dense-reward, "
        "easy-task setting). Confirmed by @claim_mnist_tpo_fastest."
    ),
    prior=0.9,
)
s_easy_dense_token = support(
    [claim_population_easy_match],
    claim_3_5_population_match_dense,
    reason=(
        "@claim_population_easy_match predicts TPO matches or beats "
        "PG-family on the bag-of-tokens dense-reward token-reversal "
        "variants. Confirmed by @claim_3_5_population_match_dense."
    ),
    prior=0.9,
)
s_easy_gsm8k = support(
    [claim_population_easy_match],
    claim_3_8_gsm8k_match,
    reason=(
        "@claim_population_easy_match predicts TPO matches or beats "
        "GRPO on GSM8K (an easier task where both saturate). "
        "Confirmed by @claim_3_8_gsm8k_match."
    ),
    prior=0.85,
)

ind_easy_12 = induction(
    s_easy_bandit,
    s_easy_mnist,
    law=claim_population_easy_match,
    reason=(
        "Multi-context bandit and MNIST are independent (different state "
        "spaces, different policies, different reward variances); both "
        "confirm the easy-task law."
    ),
)
ind_easy_123 = induction(
    ind_easy_12,
    s_easy_dense_token,
    law=claim_population_easy_match,
    reason=(
        "Dense-reward token-reversal involves transformer sequence "
        "models -- a different architecture and a different reward "
        "structure; an additional independent confirmation."
    ),
)
ind_easy = induction(
    ind_easy_123,
    s_easy_gsm8k,
    law=claim_population_easy_match,
    reason=(
        "GSM8K with billion-parameter LLMs is independent of all the "
        "smaller-scale settings; an additional confirmation at scale."
    ),
)

# ===========================================================================
# Population claim 2: TPO outperforms PG-family under sparse reward
# ===========================================================================

claim_population_sparse_outperform = claim(
    "**Population law (sparse): TPO substantially outperforms PG-family "
    "baselines under sparse reward.** Across sequential-reward "
    "transformer tasks (Sec. 3.5), terminal-reward transformer tasks "
    "(Sec. 3.6), and harder LLM RLVR tasks like graph coloring (Sec. "
    "3.8), TPO solves tasks (or reaches substantially lower error) on "
    "which the best PG-family baseline either stalls or converges to a "
    "higher-error ceiling. This is the *headline* gap: not a small "
    "improvement, but a qualitative change in regime where the "
    "baselines do not learn at all and TPO does.",
    title="Population law: TPO substantially outperforms PG-family under sparse reward",
)

s_sparse_seq = support(
    [claim_population_sparse_outperform],
    claim_3_5_sequential_only_tpo_dg,
    reason=(
        "@claim_population_sparse_outperform predicts TPO outperforms "
        "GRPO/PPO under sparse reward. The sequential-reward observation "
        "@claim_3_5_sequential_only_tpo_dg (only TPO and DG converge; "
        "GRPO/PPO fail on all 4 target logics) is a direct confirmation."
    ),
    prior=0.92,
)
s_sparse_terminal = support(
    [claim_population_sparse_outperform],
    claim_3_6_steep_baseline_degradation,
    reason=(
        "@claim_population_sparse_outperform predicts TPO outperforms "
        "GRPO/PPO/DG under terminal reward as $H$ grows. The Sec. 3.6 "
        "observation @claim_3_6_steep_baseline_degradation -- baselines "
        "collapse with $H$ while TPO stays in 6-9% -- confirms this."
    ),
    prior=0.93,
)
s_sparse_llm = support(
    [claim_population_sparse_outperform],
    claim_3_8_graph_color_qwen_gap,
    reason=(
        "@claim_population_sparse_outperform predicts TPO substantially "
        "outperforms GRPO on harder LLM RLVR tasks. The Qwen3-1.7B "
        "graph-coloring observation @claim_3_8_graph_color_qwen_gap "
        "(GRPO ~0; TPO ~0.96) is the strongest confirmation at scale."
    ),
    prior=0.92,
)

ind_sparse_12 = induction(
    s_sparse_seq,
    s_sparse_terminal,
    law=claim_population_sparse_outperform,
    reason=(
        "Sequential-reward (Sec. 3.5) and terminal-reward (Sec. 3.6) "
        "are different sparsity levels and different reward structures, "
        "providing independent confirmations of the sparse-reward law."
    ),
)
ind_sparse = induction(
    ind_sparse_12,
    s_sparse_llm,
    law=claim_population_sparse_outperform,
    reason=(
        "LLM RLVR graph coloring on Qwen3-1.7B is at a different scale "
        "(billion-parameter model, real reasoning task) and uses a "
        "different scorer than the transformer tasks -- an independent "
        "confirmation at scale."
    ),
)

# ===========================================================================
# Headline contribution claim is the union of the two population laws.
# ===========================================================================

strat_headline = support(
    [claim_population_easy_match, claim_population_sparse_outperform],
    claim_headline_contribution,
    reason=(
        "The headline contribution is exactly the conjunction of: (i) "
        "@claim_population_easy_match -- TPO matches PG-family on easy "
        "tasks; (ii) @claim_population_sparse_outperform -- TPO "
        "substantially outperforms PG-family on sparse reward."
    ),
    prior=0.92,
)

# Conclusion claim is a restatement of the headline.
strat_conclusion = support(
    [claim_headline_contribution, claim_tpo_decouples],
    claim_conclusion_restated,
    reason=(
        "The conclusion combines @claim_headline_contribution with the "
        "design statement @claim_tpo_decouples: TPO is a single design "
        "choice that decouples Q1 from Q2, and that single choice "
        "delivers the headline pattern."
    ),
    prior=0.94,
)

# ===========================================================================
# CENTRAL ABDUCTION -- why does TPO win on sparse reward?
# ===========================================================================

# The hypothesis is the conceptual decoupling thesis from Section 4.
# The alternative is "the gain comes from a single confounding ingredient
# (anchor alone, target form alone, multi-epoch alone)" -- which would imply
# the ablations should not all consistently hurt.

claim_decoupling_explains_sparse_gap = claim(
    "**Hypothesis: the explicit Q1/Q2 decoupling -- realised through "
    "the closed-form target $q$, the cross-entropy fit to $q$, and the "
    "self-extinguishing $p^\\theta - q$ gradient -- is what causes "
    "TPO's sparse-reward advantage.** The mechanism is multi-causal "
    "(Sec. 4): self-extinguishing gradient (4.1) + signal concentration "
    "on informative groups (4.2) + stable multi-epoch reuse (4.3) all "
    "follow from the explicit-target structure and reinforce each other.",
    title="Hypothesis: explicit Q1/Q2 decoupling causes the sparse-reward gain",
)

claim_single_ingredient_alt = claim(
    "**Alternative: the sparse-reward gain comes from a *single* "
    "confounding ingredient -- e.g. just the $p^{\\text{old}}$ anchor, "
    "or just the cross-entropy loss form, or just the temperature "
    "$\\eta = 1$ choice -- rather than from explicit Q1/Q2 decoupling.** "
    "If true, removing any single one of the ingredients in the Sec. "
    "3.7 ablations should leave TPO mostly intact, and the Sec. 4 "
    "mechanism story would be redundant overdetermination.",
    title="Alternative: a single confounding ingredient explains the gain",
)

# Predictions.
pred_decoupling = claim(
    "**Decoupling-hypothesis prediction:** removing *any* of the three "
    "TPO ingredients (anchor, target matching, multi-epoch) should "
    "produce a substantial degradation, with the gaps widening under "
    "sparse reward; the empirical mechanism diagnostics (gradient norm "
    "collapse, all-fail elimination, smooth K and epoch sweeps) should "
    "all distinguish TPO from baselines.",
    title="Prediction (decoupling): all three ingredients matter; mechanism diagnostics distinguish TPO",
)

pred_single_ingredient = claim(
    "**Single-ingredient alternative's prediction:** at most one of "
    "the three TPO ingredients matters; removing the others should "
    "leave TPO performance essentially intact, and only one mechanism "
    "diagnostic should distinguish TPO from baselines.",
    title="Prediction (alt): only one ingredient matters; ablations are mostly redundant",
)

# Combined "ablations + mechanism diagnostics" as the observation.
claim_ablations_all_hurt_obs = claim(
    "**Joint observation: every ablation hurts; every mechanism "
    "diagnostic distinguishes TPO.** Sec. 3.7: TPO-no-anchor exceeds "
    "99% at $H = 10$ (vs. TPO 7.4%); Group PG also exceeds 99% (target "
    "matching ablation). Sec. 4.1: TPO grad norm collapses to ~0 by ep "
    "300; GRPO persists at 12.7% plateau. Sec. 4.2: TPO drives all-fail "
    "fraction to ~0 fastest; smooth K-sweep (8.9% -> 0.36% at K=64). "
    "Sec. 4.3: TPO < 2.3% across all epoch counts; GRPO non-monotonic "
    "(37.6% at 2 ep). Multi-epoch reuse works without tuning. Every "
    "single one of these patterns is consistent with the multi-causal "
    "decoupling story.",
    title="Joint obs: every ablation hurts; every diagnostic distinguishes TPO",
)

s_h_decouple = support(
    [claim_decoupling_explains_sparse_gap],
    claim_ablations_all_hurt_obs,
    reason=(
        "If the decoupling hypothesis @claim_decoupling_explains_sparse_gap "
        "holds (multi-causal mechanism), it predicts (@pred_decoupling) "
        "that every ablation should hurt and every mechanism diagnostic "
        "should distinguish TPO from baselines. The joint observation "
        "@claim_ablations_all_hurt_obs records exactly this pattern."
    ),
    prior=0.9,
)
s_alt_decouple = support(
    [claim_single_ingredient_alt],
    claim_ablations_all_hurt_obs,
    reason=(
        "If the alternative @claim_single_ingredient_alt held -- only a "
        "single ingredient mattered -- removing the *other* ingredients "
        "should leave TPO mostly intact and only one mechanism diagnostic "
        "should distinguish TPO from baselines (@pred_single_ingredient). "
        "The joint observation @claim_ablations_all_hurt_obs is *not* "
        "what the alternative predicts; prior 0.25 reflects this low "
        "explanatory power."
    ),
    prior=0.25,
)
comp_decouple = compare(
    pred_decoupling,
    pred_single_ingredient,
    claim_ablations_all_hurt_obs,
    reason=(
        "The joint observation @claim_ablations_all_hurt_obs -- every "
        "ablation hurts, every diagnostic distinguishes TPO -- matches "
        "the decoupling-hypothesis prediction (@pred_decoupling, "
        "everything matters) and is directly inconsistent with the "
        "single-ingredient prediction (@pred_single_ingredient, only one "
        "thing matters)."
    ),
    prior=0.95,
)

abd_decoupling = abduction(
    s_h_decouple,
    s_alt_decouple,
    comp_decouple,
    reason=(
        "Two competing explanations of TPO's sparse-reward advantage: "
        "(H) multi-causal Q1/Q2 decoupling vs. (Alt) a single "
        "confounding ingredient. The Sec. 3.7 ablations and Sec. 4 "
        "mechanism diagnostics jointly discriminate."
    ),
)

# Joint observation derived from constituent measurements. The five
# measurement claims jointly constitute the joint pattern; we wire them
# as premises to the joint-observation claim. The abduction structure
# uses this as the observation conclusion of s_h/s_alt explanations.
strat_joint_obs = support(
    [
        claim_3_7_no_anchor_hurts,
        claim_3_7_target_matching_essential,
        claim_4_1_grad_norm_collapse,
        claim_4_2_all_fail_fraction,
        claim_4_3_multi_epoch_speedup,
    ],
    claim_ablations_all_hurt_obs,
    reason=(
        "The joint observation @claim_ablations_all_hurt_obs is the "
        "conjunction of the five ablation/diagnostic measurements: "
        "@claim_3_7_no_anchor_hurts (Sec. 3.7), "
        "@claim_3_7_target_matching_essential (Sec. 3.7), "
        "@claim_4_1_grad_norm_collapse (Sec. 4.1), "
        "@claim_4_2_all_fail_fraction (Sec. 4.2), and "
        "@claim_4_3_multi_epoch_speedup (Sec. 4.3). All five hold; "
        "their conjunction is the joint pattern being explained."
    ),
    prior=0.95,
)

# ===========================================================================
# Related-work + setup-justification + Sec 4 supplementary supports.
# Placed here because they reference population claims and the Sec 4
# synthesis.
# ===========================================================================

strat_fig1_dense_supports_easy_match = support(
    [claim_fig1_dense_match],
    claim_population_easy_match,
    reason=(
        "Figure 1(a) @claim_fig1_dense_match is the headline preview of "
        "@claim_population_easy_match: on the dense-reward MNIST contextual "
        "bandit, TPO matches GRPO/DG. This is the easy-task limb of the "
        "headline, previewed in Figure 1."
    ),
    prior=0.85,
)

strat_grpo_kl_supports_strong_baseline = support(
    [claim_grpo_kl_strengthens_baseline],
    claim_population_sparse_outperform,
    reason=(
        "@claim_grpo_kl_strengthens_baseline shows the comparison "
        "uses the *strongest* GRPO variant (KL-anchored, $\\beta=0.04$), "
        "not a strawman. This is part of why TPO's outperformance "
        "@claim_population_sparse_outperform is meaningful: TPO beats "
        "the strengthened baseline, not a weakened one."
    ),
    prior=0.7,
)

strat_dg_multi_ep_supports_seq = support(
    [claim_dg_multi_epoch_unstable],
    claim_3_5_sequential_only_tpo_dg,
    reason=(
        "@claim_dg_multi_epoch_unstable justifies that DG runs at 1 "
        "epoch in @claim_3_5_sequential_only_tpo_dg is *not* a "
        "handicap on DG -- 1 epoch is the most favorable setting. So "
        "DG's failure on sequential-reward variants (where it does "
        "converge but slowly) is a real comparison."
    ),
    prior=0.7,
)

strat_target_matching_distinguishes = support(
    [claim_target_matching_family],
    claim_tpo_no_critic_no_dual,
    reason=(
        "@claim_target_matching_family lays out REPS / MPO / V-MPO / AWR / "
        "MDPO / regularised-MDP work that all use exponential tilting. "
        "The distinguishing closed-form-on-finite-candidate-set property "
        "(@claim_tpo_no_critic_no_dual) is what differentiates TPO "
        "within this family."
    ),
    prior=0.85,
)

strat_kl_op_view = support(
    [claim_target_matching_family],
    claim_tpo_kl_regularised_operator,
    reason=(
        "Reading TPO through the lens of @claim_target_matching_family: "
        "TPO is a KL-regularised improvement operator on the candidate "
        "simplex (rather than the full action space), which is the unifying "
        "view that connects it to the regularised-MDP framework."
    ),
    prior=0.85,
)

strat_group_pg_distinguish = support(
    [claim_group_based_pg_family],
    claim_population_sparse_outperform,
    reason=(
        "@claim_group_based_pg_family characterises RLOO/GRPO and the "
        "GRPO variants (Dr.GRPO, DAPO, GSPO) as scalar-weighted "
        "single-target updates on the candidate group. TPO replaces this "
        "with a target-distribution update; the empirical sparse-reward "
        "outperformance @claim_population_sparse_outperform is precisely "
        "where this structural difference matters."
    ),
    prior=0.6,
)

strat_dg_complementary_axis_use = support(
    [claim_dg_complementary_axis],
    claim_population_easy_match,
    reason=(
        "@claim_dg_complementary_axis explains why TPO does not "
        "*subsume* DG: they address complementary axes "
        "(within-context vs. across-context). On easy tasks (the regime "
        "of @claim_population_easy_match), this is why both methods "
        "perform comparably: neither is exposed to the other's failure "
        "regime."
    ),
    prior=0.6,
)

strat_difficulty_bias_caveat = support(
    [claim_difficulty_bias_residual],
    claim_lim_low_variance_groups,
    reason=(
        "The Sec. 5 caveat @claim_difficulty_bias_residual (TPO inherits "
        "low-variance difficulty bias from $z$-scoring) is exactly the "
        "structural reason for the Sec. 6 limitation "
        "@claim_lim_low_variance_groups about low-variance groups."
    ),
    prior=0.95,
)

strat_single_sample_pg_used = support(
    [claim_single_sample_pg_family],
    claim_pg_entangles_two_questions,
    reason=(
        "@claim_single_sample_pg_family confirms that REINFORCE / TRPO / "
        "PPO / REINFORCE++ / ReMax all use scalar advantage weights on "
        "the score-function gradient -- the structural pattern that "
        "@claim_pg_entangles_two_questions diagnoses as the entanglement "
        "of Q1 and Q2."
    ),
    prior=0.9,
)

strat_objective_corrections_orthogonal = support(
    [claim_objective_corrections_family],
    claim_lim_candidate_quality,
    reason=(
        "MaxRL/GDPO/MT-GRPO change *which* objective is optimised "
        "(@claim_objective_corrections_family); TPO is bounded by "
        "candidate quality (@claim_lim_candidate_quality) -- a different "
        "limitation that orthogonal corrections do not address. The "
        "complementarity is part of why the limitation persists."
    ),
    prior=0.5,
)

strat_off_policy_async_orthogonal = support(
    [claim_off_policy_async_family],
    claim_lim_scale_of_evaluation,
    reason=(
        "ScaleRL and IcePop @claim_off_policy_async_family operate at "
        "scale (trillion-scale thinking models). The Sec. 6 scale-of-"
        "evaluation limitation @claim_lim_scale_of_evaluation is "
        "precisely where these orthogonal off-policy strategies could "
        "compose with TPO; the open question is whether TPO's gains "
        "persist at that scale."
    ),
    prior=0.6,
)

strat_regression_preference_distance = support(
    [claim_regression_preference_family],
    claim_population_sparse_outperform,
    reason=(
        "@claim_regression_preference_family situates REBEL / PMPO / DPO "
        "/ KTO / IPO as *more distant* targets of comparison: TPO is "
        "online, setwise, and scorer-agnostic. The empirical comparisons "
        "@claim_population_sparse_outperform are with the closer-family "
        "PG-style baselines, not with these methods."
    ),
    prior=0.5,
)

# ===========================================================================
# Contradictions
# ===========================================================================

# 1. Prevailing PG view ("entanglement is unavoidable") vs TPO empirical demo.
contra_entanglement_vs_tpo = contradiction(
    claim_pg_view_entanglement_unavoidable,
    claim_population_sparse_outperform,
    reason=(
        "If entanglement of Q1 and Q2 were truly unavoidable in policy "
        "optimization, then no decoupled algorithm could reach low error "
        "on sparse-reward tasks where the entangled methods stall. TPO's "
        "demonstrated outperformance on sparse-reward "
        "(@claim_population_sparse_outperform) directly contradicts the "
        "view that entanglement is unavoidable "
        "(@claim_pg_view_entanglement_unavoidable). They cannot both be "
        "true."
    ),
    prior=0.95,
)

# 2. KL-stabilised vs no-KL GRPO -- not really a contradiction since both
# describe behaviour of GRPO under different settings. The claim that "GRPO
# (no KL) collapses" coexists peacefully with the strengthened-baseline
# justification claim. Skip.

__all__ = [
    # Method-level reasoning
    "strat_prop1_stationary",
    "strat_self_extinguish",
    "strat_q_frozen_multi_epoch",
    "strat_no_critic",
    "strat_token_grouping",
    # Tabular bandits
    "strat_3_1_result",
    "strat_3_1_misalignment",
    "strat_beta_small_p",
    "strat_3_2_result",
    # MNIST + concentration abduction
    "strat_mnist_tpo_fastest",
    "strat_pg_grouppg_collapse",
    "strat_concentration_prediction",
    "strat_concentration_predicts",
    "pred_concentrated",
    "pred_one_vs_rest_alt",
    "s_h_concentration",
    "s_alt_concentration",
    "comp_concentration",
    "abd_concentration",
    # Sequence
    "strat_3_4_gap_widens",
    "strat_3_5_dense",
    "strat_3_5_sequential",
    "strat_per_state",
    # Terminal reward
    "strat_3_6_steep_degradation",
    "strat_3_6_interaction_match",
    "s_llm_gsm8k",
    "s_llm_graph",
    "s_llm_knk",
    "ind_llm_rlvr_12",
    "ind_llm_rlvr",
    # Sec 4
    "strat_4_1_grad_norm",
    "strat_4_1_alloc_supports_synthesis",
    "strat_4_2_k_sweep_supports",
    "strat_4_2_zv_masking_supports",
    "strat_neutrality_supports_masking",
    "strat_4_3_speedup",
    "strat_4_3_epoch_sweep_supports",
    "strat_4_no_single",
    # Sec 4 -> Sec 3.8 R1
    "s_llm_graph_r1",
    # Limitations bounding scope
    "strat_lim_supports_conclusion",
    # Related-work anchors
    "strat_grpo_kl_supports_strong_baseline",
    "strat_dg_multi_ep_supports_seq",
    "strat_target_matching_distinguishes",
    "strat_kl_op_view",
    "strat_group_pg_distinguish",
    "strat_dg_complementary_axis_use",
    "strat_difficulty_bias_caveat",
    "strat_single_sample_pg_used",
    "strat_objective_corrections_orthogonal",
    "strat_off_policy_async_orthogonal",
    "strat_regression_preference_distance",
    # Fig 1 wiring
    "strat_fig1_dense_supports_easy_match",
    # Joint observation
    "strat_joint_obs",
    # Motivation
    "strat_entanglement_fragile",
    "strat_tpo_decouples",
    "strat_fig1_qualitative",
    # Population inductions
    "claim_population_easy_match",
    "s_easy_bandit",
    "s_easy_mnist",
    "s_easy_dense_token",
    "s_easy_gsm8k",
    "ind_easy_12",
    "ind_easy_123",
    "ind_easy",
    "claim_population_sparse_outperform",
    "s_sparse_seq",
    "s_sparse_terminal",
    "s_sparse_llm",
    "ind_sparse_12",
    "ind_sparse",
    # Headline + conclusion
    "strat_headline",
    "strat_conclusion",
    # Central abduction
    "claim_decoupling_explains_sparse_gap",
    "claim_single_ingredient_alt",
    "pred_decoupling",
    "pred_single_ingredient",
    "claim_ablations_all_hurt_obs",
    "s_h_decouple",
    "s_alt_decouple",
    "comp_decouple",
    "abd_decoupling",
    # Contradictions
    "contra_entanglement_vs_tpo",
]
