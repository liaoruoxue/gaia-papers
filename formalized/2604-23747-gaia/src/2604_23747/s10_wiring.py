"""Pass 2 wiring: strategies, abductions, inductions, contradictions.

Conventions
-----------

* `support` -- soft deduction with author-specified prior. The default for
  "premises imply conclusion" with empirical or interpretive uncertainty.
* `deduction` -- rigid logical entailment. Used for the formal step from the
  gradient-accumulation contract violation (mechanism) to the dropped-
  micro-batch effect (consequence).
* `compare` -- two predictions vs an observation; sub-strategy of `abduction`.
* `abduction` -- inference to best explanation. Used once: the central
  thesis question (does the bug-attribution hypothesis explain the
  observed mixed-policy gains, or do mixed-policy methods represent a
  genuine methodological advance?).
* `induction` -- chained binary composite. Used once: the population law
  "fixed SFT-then-RL beats every evaluated mixed-policy method on math
  benchmarks" inducted over (i) Qwen2.5-Math-7B + (ii) Llama-3.1-8B model
  families.
* `contradiction` -- two contradictions:
    (i) the published mixed-policy advantage claim vs the corrected-baseline
        SFT-then-RL outperformance (cannot both be true);
    (ii) "the optimizer bug is small / cosmetic" alternative vs the paper's
        attribution that the optimizer bug accounts for most of the gap.
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
    claim_baseline_suspicion,
    claim_compute_efficiency_headline,
    claim_implications,
    claim_intuitive_motivation_for_mixing,
    claim_llama_headline,
    claim_mixed_policy_gains_reported,
    claim_optimizer_bug_dominant,
    claim_qwen_headline,
    claim_two_bug_thesis,
    setup_evaluation_protocol,
    setup_llm_reasoning_regime,
    setup_mixed_policy_definition,
)
from .s2_related_work import (
    claim_hpt_method,
    claim_luffy_method,
    claim_other_mixed_policy_methods,
    claim_prefix_rft_method,
    claim_relift_method,
    claim_srft_method,
    setup_llama_base,
    setup_openr1_dataset,
    setup_qwen_base,
)
from .s3_setup import (
    claim_chat_template_unified,
    claim_luffy_relift_reimpl,
    claim_reproduction_design,
    setup_compute_setup,
    setup_evaluation_benchmarks,
    setup_flops_accounting,
    setup_grpo_500_steps,
    setup_seed_protocol,
    setup_sft_then_rl_pipeline,
    setup_truncated_rl_50,
)
from .s4_optimizer_bug import (
    claim_bug_introduced_in_pr,
    claim_bug_mechanism,
    claim_bug_propagation,
    claim_grad_norm_suppressed,
    claim_mean_loss_shifted,
    claim_optimizer_fix,
    claim_optimizer_fix_validated,
    setup_gradient_accumulation_contract,
    setup_zero_offload,
)
from .s5_loss_aggregation_bug import (
    claim_inherited_from_pretrain,
    claim_loss_agg_fix,
    claim_loss_agg_mechanism,
    claim_loss_agg_smaller_effect,
    claim_loss_agg_variability,
    claim_patched_matches_verl,
    setup_dp_ranks,
    setup_per_token_mean_loss,
)
from .s6_attribution import (
    claim_attribution_table,
    claim_baseline_openrlhf,
    claim_dynamics_decomposition,
    claim_hyperparam_sensitivity,
    claim_optimizer_dominates_attribution,
    claim_row_both,
    claim_row_loss_agg_only,
    claim_row_optimizer_only,
    claim_row_verl,
    setup_table2_subset,
)
from .s7_corrected_results import (
    claim_efficiency_gap,
    claim_llama_failure_explanation,
    claim_llama_mixed_policy_table,
    claim_llama_plus_22p2,
    claim_llama_sft,
    claim_llama_sft_then_rl,
    claim_per_method_corrected_beats_each,
    claim_perceived_gains_attribution,
    claim_qwen_mixed_policy_table,
    claim_qwen_ood_competitive,
    claim_qwen_plus_3p8,
    claim_qwen_reproduction,
    claim_qwen_sft_corrected,
    claim_qwen_sft_then_rl,
)
from .s8_truncated_rl import (
    claim_compute_efficiency_synthesis,
    claim_dense_reward_from_sft,
    claim_flops_decomposition,
    claim_flops_table,
    claim_truncated_beats_mixed_policy,
    claim_truncated_id_results,
    claim_truncated_ood_results,
)
from .s9_discussion import (
    claim_alt_methodological_advance,
    claim_entropy_dynamics,
    claim_implication_cross_framework,
    claim_implication_other_areas,
    claim_lim_domain_scope,
    claim_lim_mixed_atop_corrected,
    claim_lim_model_families,
    claim_lim_relift_hpt_unverified,
    claim_obs_cross_framework_match,
    claim_pred_alt_explains,
    claim_pred_bug_explains,
    claim_qwen_training_dynamics,
    claim_response_length_dynamics,
    claim_restored_confidence,
    claim_synthesis_baselines_deflated,
)


# ===========================================================================
# Section 2.1 (s4_optimizer_bug): mechanism -> consequences
# ===========================================================================

# The dropped-micro-batch effect is a deductive consequence of the bug's
# mechanism given the gradient-accumulation contract: if the copy-to-CPU
# only fires on micro_step_id == 0, then by the contract the optimizer
# sees only g_0 instead of sum(g_0..g_{K-1}). This is a deterministic step.
strat_grad_norm_from_mechanism = deduction(
    [claim_bug_mechanism],
    claim_grad_norm_suppressed,
    background=[setup_gradient_accumulation_contract, setup_zero_offload],
)

strat_mean_loss_shifted = support(
    [claim_bug_mechanism],
    claim_mean_loss_shifted,
    reason=(
        "Under the bug mechanism (@claim_bug_mechanism), only the first "
        "micro-batch's gradients reach the optimizer, which means the "
        "effective batch size is reduced by a factor of K (number of "
        "micro-batches per step). A K-fold smaller effective batch "
        "increases gradient noise and produces a measurably different "
        "optimization trajectory; empirically this shifts the mean of the "
        "SFT loss curve relative to a correctly-trained run "
        "(@setup_gradient_accumulation_contract). The shift is "
        "experimentally measurable but not strictly deterministic in "
        "magnitude (depends on the loss landscape), hence support rather "
        "than deduction."
    ),
    prior=0.92,
    background=[setup_gradient_accumulation_contract, setup_zero_offload],
)

strat_bug_propagation_evidenced = support(
    [claim_bug_mechanism, claim_bug_introduced_in_pr],
    claim_bug_propagation,
    reason=(
        "The propagation claim (@claim_bug_propagation) follows from "
        "(a) the bug being a regression in DeepSpeed itself "
        "(@claim_bug_introduced_in_pr, PR #6550), and (b) the mechanism "
        "(@claim_bug_mechanism) sitting in DeepSpeed's ZeRO Stage 1/2 "
        "offloaded-optimizer code path. Any framework that wraps "
        "DeepSpeed for distributed SFT with offloaded optimizers (TRL, "
        "OpenRLHF, Llama-Factory) inherits the buggy code path."
    ),
    prior=0.95,
    background=[setup_zero_offload],
)

strat_optimizer_fix_correctness = support(
    [claim_bug_mechanism, claim_optimizer_fix],
    claim_optimizer_fix_validated,
    reason=(
        "The fix's correctness (@claim_optimizer_fix_validated) follows "
        "from (a) the mechanism (@claim_bug_mechanism) localizing the "
        "issue to an erroneous else-guard around copy_gradients_to_cpu(), "
        "and (b) the fix (@claim_optimizer_fix) removing exactly that "
        "guard. The patched optimizer is independently corroborated by "
        "matching loss / grad-norm with two reference baselines "
        "(GPU-resident DeepSpeed and verl FSDP)."
    ),
    prior=0.96,
)

# ===========================================================================
# Section 2.2 (s5_loss_aggregation_bug): mechanism -> consequences
# ===========================================================================

strat_loss_agg_inherited = support(
    [claim_loss_agg_mechanism],
    claim_inherited_from_pretrain,
    reason=(
        "The pretrain-inheritance claim (@claim_inherited_from_pretrain) "
        "follows from the mechanism (@claim_loss_agg_mechanism): the "
        "mean-of-means weighting is correct *only* when each mini-batch "
        "and rank has equal active-token counts (which holds in pretrain "
        "due to data packing) and incorrect otherwise. SFT loses data "
        "packing because prompts and responses vary in length, so the "
        "bug surfaces only in SFT contexts."
    ),
    prior=0.95,
    background=[setup_per_token_mean_loss, setup_dp_ranks],
)

strat_loss_agg_variability = support(
    [claim_loss_agg_mechanism],
    claim_loss_agg_variability,
    reason=(
        "Under the mean-of-means mechanism (@claim_loss_agg_mechanism), "
        "the per-step loss is a weighted average of mini-batch means with "
        "weights independent of token counts. Since per-mini-batch token "
        "counts fluctuate step-to-step in SFT, the resulting loss curve "
        "exhibits step-to-step variability that disappears once token-"
        "level aggregation (@setup_per_token_mean_loss) is used."
    ),
    prior=0.93,
    background=[setup_per_token_mean_loss],
)

strat_loss_agg_fix_correctness = support(
    [claim_loss_agg_mechanism, claim_loss_agg_fix],
    claim_patched_matches_verl,
    reason=(
        "The corrected algorithm (@claim_loss_agg_fix) implements the "
        "per-token mean (@setup_per_token_mean_loss) by globally "
        "all-reducing token sums and counts before dividing, exactly "
        "what the contract requires. Combined with the optimizer fix, "
        "this brings OpenRLHF's SFT result (54.0 +/- 0.2) into "
        "statistical equivalence with the independently-implemented "
        "verl SFT (53.8 +/- 0.1) on the Table 2 subset "
        "(@claim_patched_matches_verl)."
    ),
    prior=0.94,
    background=[setup_per_token_mean_loss, setup_dp_ranks],
)

# ===========================================================================
# Section 4 (s6_attribution): per-bug attribution from Table 2
# ===========================================================================

strat_attribution_table_from_rows = support(
    [
        claim_baseline_openrlhf,
        claim_row_loss_agg_only,
        claim_row_optimizer_only,
        claim_row_both,
        claim_row_verl,
    ],
    claim_attribution_table,
    reason=(
        "The per-bug attribution table (@claim_attribution_table) is "
        "assembled directly from the five Table 2 rows: baseline 48.3 "
        "(@claim_baseline_openrlhf), + fix loss aggregation 49.1 "
        "(@claim_row_loss_agg_only, +0.8), + fix optimizer 53.4 "
        "(@claim_row_optimizer_only, +5.1), + fix both 54.0 "
        "(@claim_row_both, +5.7), verl reference 53.8 (@claim_row_verl). "
        "The attribution arithmetic is deterministic given the rows."
    ),
    prior=0.97,
    background=[setup_table2_subset],
)

strat_optimizer_dominates_from_attribution = support(
    [claim_attribution_table],
    claim_optimizer_dominates_attribution,
    reason=(
        "The 'optimizer dominates' attribution finding "
        "(@claim_optimizer_dominates_attribution) is the qualitative "
        "interpretation of the quantitative attribution table "
        "(@claim_attribution_table): +5.1 of the +5.7 total gap "
        "(approximately 89%) is attributable to fixing the optimizer "
        "bug alone, while the loss-aggregation fix contributes +0.8 "
        "(approximately 14%, partially overlapping with the optimizer "
        "fix when stacked). The dominance ranking is unambiguous given "
        "the per-bug deltas."
    ),
    prior=0.96,
)

strat_dynamics_from_mechanisms = support(
    [
        claim_grad_norm_suppressed,
        claim_mean_loss_shifted,
        claim_loss_agg_variability,
    ],
    claim_dynamics_decomposition,
    reason=(
        "The Fig. 2 per-bug-dynamics decomposition "
        "(@claim_dynamics_decomposition) is the conjunction of three "
        "per-bug effects: optimizer-bug suppresses grad norm "
        "(@claim_grad_norm_suppressed), optimizer-bug shifts loss mean "
        "(@claim_mean_loss_shifted), and aggregation-bug introduces "
        "loss variability (@claim_loss_agg_variability). Each bug has a "
        "distinct, separable signature in the training curves."
    ),
    prior=0.94,
)

# Hyperparameter sensitivity is independent of the bugs but explains SRFT's
# specific case
strat_hyperparam_explains_srft = support(
    [claim_hyperparam_sensitivity, claim_srft_method],
    claim_perceived_gains_attribution,
    reason=(
        "For SRFT specifically (@claim_srft_method), the perceived "
        "mixed-policy advantage is attributable not to the framework "
        "bugs but to the weak SFT learning rate (@claim_hyperparam_"
        "sensitivity, 5x10^-6 vs the 5x10^-5 used by LUFFY/ReLIFT), "
        "which alone accounts for ~5.5 of the ~7.6 point apparent gain. "
        "This is a separate baseline-deflation mechanism that "
        "complements the bug attribution for the OpenRLHF-/Llama-"
        "Factory-trained baselines (@claim_perceived_gains_attribution)."
    ),
    prior=0.92,
)

# ===========================================================================
# s7_corrected_results: per-method corrected-baseline outperformance
# ===========================================================================

strat_qwen_headline_from_plus_3p8 = support(
    [claim_qwen_plus_3p8],
    claim_qwen_headline,
    reason=(
        "The motivation-section Qwen headline (@claim_qwen_headline) "
        "is the abstract-level statement of the corrected-baseline "
        "ID outperformance (@claim_qwen_plus_3p8: SFT-then-RL 57.0 "
        "ID vs SRFT 53.2 ID = +3.8). Identical empirical content; "
        "this strategy connects the abstract claim to its in-paper "
        "realization."
    ),
    prior=0.97,
)

strat_llama_headline_from_plus_22p2 = support(
    [claim_llama_plus_22p2],
    claim_llama_headline,
    reason=(
        "The motivation-section Llama headline (@claim_llama_headline) "
        "is the abstract-level statement of the corrected-baseline "
        "outperformance on Llama-3.1-8B (@claim_llama_plus_22p2: "
        "43.7 vs 21.5 = +22.2)."
    ),
    prior=0.97,
)

strat_loss_agg_small_effect_from_attribution = support(
    [claim_attribution_table],
    claim_loss_agg_smaller_effect,
    reason=(
        "The 'loss aggregation bug is the smaller effect' claim "
        "(@claim_loss_agg_smaller_effect, +0.6 to +0.8 of the total "
        "+5.7 gap) is the row-arithmetic of the attribution table "
        "(@claim_attribution_table): 49.1 - 48.3 = +0.8 (loss-agg "
        "alone), and 54.0 - 53.4 = +0.6 (loss-agg on top of optimizer "
        "fix)."
    ),
    prior=0.96,
)

strat_qwen_3p8_from_results = support(
    [claim_qwen_sft_then_rl, claim_qwen_mixed_policy_table],
    claim_qwen_plus_3p8,
    reason=(
        "The +3.8 Qwen2.5-Math-7B headline (@claim_qwen_plus_3p8) is "
        "arithmetic on the corrected SFT-then-RL ID average "
        "(@claim_qwen_sft_then_rl, 57.0) and the best published "
        "mixed-policy ID average (@claim_qwen_mixed_policy_table, "
        "SRFT 53.2): 57.0 - 53.2 = +3.8."
    ),
    prior=0.97,
    background=[setup_evaluation_benchmarks, setup_qwen_base],
)

strat_per_method_from_results = support(
    [claim_qwen_sft_then_rl, claim_qwen_mixed_policy_table],
    claim_per_method_corrected_beats_each,
    reason=(
        "The per-method margins (@claim_per_method_corrected_beats_each) "
        "are the row-by-row differences between the corrected SFT-then-"
        "RL ID average (@claim_qwen_sft_then_rl, 57.0) and each "
        "mixed-policy method's ID average from Table 1 "
        "(@claim_qwen_mixed_policy_table)."
    ),
    prior=0.97,
    background=[setup_evaluation_benchmarks],
)

strat_qwen_reproduction_evidenced = support(
    [claim_luffy_relift_reimpl, claim_loss_agg_fix],
    claim_qwen_reproduction,
    reason=(
        "The reproduction numbers (@claim_qwen_reproduction, LUFFY 46.3 "
        "ID / ReLIFT 48.8 ID) come from reimplementing the methods in "
        "verl with the loss-aggregation fix patched into their training "
        "loops (@claim_luffy_relift_reimpl + @claim_loss_agg_fix). The "
        "reproductions are *fair* in the sense that they use the methods' "
        "own original RL hyperparameters; only the loss aggregation "
        "issue is patched."
    ),
    prior=0.92,
    background=[setup_compute_setup],
)

strat_perceived_gains_synthesis = support(
    [
        claim_attribution_table,
        claim_hyperparam_sensitivity,
        claim_qwen_reproduction,
        claim_luffy_method,
        claim_relift_method,
        claim_prefix_rft_method,
    ],
    claim_perceived_gains_attribution,
    reason=(
        "The synthesis attribution (@claim_perceived_gains_attribution) "
        "combines the bug-attribution table (@claim_attribution_table), "
        "the SRFT hyperparameter-sensitivity finding (@claim_hyperparam_"
        "sensitivity), and the lower reproduction scores (@claim_qwen_"
        "reproduction). LUFFY (@claim_luffy_method) and Prefix-RFT "
        "(@claim_prefix_rft_method, inheriting LUFFY's baseline) are "
        "attributed to OpenRLHF/DeepSpeed bugs; ReLIFT "
        "(@claim_relift_method) to Llama-Factory bugs; SRFT to "
        "weak-LR hyperparameters."
    ),
    prior=0.92,
)

# ===========================================================================
# Llama-3.1-8B headline
# ===========================================================================

strat_llama_22p2_from_results = support(
    [claim_llama_sft_then_rl, claim_llama_mixed_policy_table],
    claim_llama_plus_22p2,
    reason=(
        "The +22.2 Llama-3.1-8B headline (@claim_llama_plus_22p2) is "
        "arithmetic on the corrected SFT-then-RL average "
        "(@claim_llama_sft_then_rl, 43.7) and the best published "
        "mixed-policy average (@claim_llama_mixed_policy_table, "
        "HPT 21.5): 43.7 - 21.5 = +22.2."
    ),
    prior=0.97,
    background=[setup_evaluation_benchmarks, setup_llama_base],
)

strat_llama_failure_explanation = support(
    [claim_llama_failure_explanation, claim_efficiency_gap],
    claim_restored_confidence,
    reason=(
        "The dramatic Llama gap (@claim_llama_failure_explanation: +22.2 "
        "vs Qwen's +3.8) supports the broader 'restored confidence' "
        "claim (@claim_restored_confidence) precisely because Llama-3.1-8B "
        "stress-tests the SFT bootstrapping role. The efficiency-gap "
        "argument (@claim_efficiency_gap) makes explicit that mixed-"
        "policy methods cannot match SFT-then-RL's sample efficiency "
        "when pre-training lacks the relevant domain knowledge."
    ),
    prior=0.9,
    background=[setup_llama_base],
)

# ===========================================================================
# Truncated 50-step variant: s8_truncated_rl
# ===========================================================================

strat_truncated_id_outperforms = support(
    [claim_truncated_id_results, claim_qwen_mixed_policy_table],
    claim_truncated_beats_mixed_policy,
    reason=(
        "The truncated 50-step variant beating mixed-policy "
        "(@claim_truncated_beats_mixed_policy) follows from the truncated "
        "ID score (@claim_truncated_id_results, 55.6) exceeding the best "
        "published mixed-policy ID score (@claim_qwen_mixed_policy_table, "
        "SRFT 53.2): 55.6 - 53.2 = +2.4."
    ),
    prior=0.96,
    background=[setup_truncated_rl_50, setup_evaluation_benchmarks],
)

strat_compute_efficiency_synthesis = support(
    [
        claim_truncated_id_results,
        claim_truncated_ood_results,
        claim_flops_table,
        claim_dense_reward_from_sft,
    ],
    claim_compute_efficiency_synthesis,
    reason=(
        "The compute-efficiency synthesis (@claim_compute_efficiency_"
        "synthesis) combines the truncated-RL accuracy results "
        "(@claim_truncated_id_results, @claim_truncated_ood_results), "
        "the FLOPs comparison (@claim_flops_table: 3.63 vs 6.65 vs "
        "8.76 x 10^19), and the SFT-bootstraps-dense-reward mechanism "
        "(@claim_dense_reward_from_sft) which makes 50 steps sufficient."
    ),
    prior=0.93,
    background=[setup_truncated_rl_50, setup_flops_accounting],
)

strat_compute_efficiency_headline_supported = support(
    [claim_truncated_beats_mixed_policy, claim_flops_table],
    claim_compute_efficiency_headline,
    reason=(
        "The compute-efficiency headline claim (@claim_compute_efficiency_"
        "headline) is the conjunction of accuracy outperformance "
        "(@claim_truncated_beats_mixed_policy: 55.6 ID > 53.2 SRFT) and "
        "FLOPs reduction (@claim_flops_table: 3.63 < 6.65 LUFFY < 8.76 "
        "ReLIFT). Both the accuracy and the compute leg must hold."
    ),
    prior=0.95,
)

strat_flops_table_from_decomposition = support(
    [claim_flops_decomposition],
    claim_flops_table,
    reason=(
        "The Table 6 FLOPs comparison (@claim_flops_table) follows from "
        "the explicit FLOPs decomposition for each method "
        "(@claim_flops_decomposition: SFT 2.43e19 + 50-step RL 1.20e19 "
        "= 3.63e19 for SFT-then-RL; analogous decompositions for LUFFY "
        "and ReLIFT)."
    ),
    prior=0.95,
    background=[setup_flops_accounting],
)

# ===========================================================================
# Headline thesis: two-bug attribution
# ===========================================================================

strat_two_bug_thesis_from_mechanisms = support(
    [claim_bug_mechanism, claim_loss_agg_mechanism, claim_attribution_table],
    claim_two_bug_thesis,
    reason=(
        "The two-bug thesis (@claim_two_bug_thesis) is the conjunction "
        "of (i) the optimizer-bug mechanism (@claim_bug_mechanism), (ii) "
        "the loss-aggregation-bug mechanism (@claim_loss_agg_mechanism), "
        "and (iii) the attribution table (@claim_attribution_table) "
        "which quantifies the joint 5.7-point deflation."
    ),
    prior=0.96,
)

strat_optimizer_dominant_headline = support(
    [claim_optimizer_dominates_attribution, claim_dynamics_decomposition],
    claim_optimizer_bug_dominant,
    reason=(
        "The headline 'optimizer dominates' claim "
        "(@claim_optimizer_bug_dominant) follows from the attribution "
        "finding (@claim_optimizer_dominates_attribution, +5.1 of +5.7 "
        "is the optimizer fix) and is corroborated by the per-bug "
        "training-dynamics decomposition (@claim_dynamics_decomposition: "
        "only the optimizer bug suppresses grad norms)."
    ),
    prior=0.95,
)

# ===========================================================================
# Synthesis: published gains = deflated baselines
# ===========================================================================

strat_synthesis_baselines_deflated = support(
    [
        claim_two_bug_thesis,
        claim_perceived_gains_attribution,
        claim_qwen_plus_3p8,
        claim_llama_plus_22p2,
        claim_patched_matches_verl,
    ],
    claim_synthesis_baselines_deflated,
    reason=(
        "The Section 6 synthesis (@claim_synthesis_baselines_deflated) "
        "is the conjunction of: the two-bug thesis "
        "(@claim_two_bug_thesis), the per-method attribution of "
        "perceived gains to deflated baselines "
        "(@claim_perceived_gains_attribution), the Qwen +3.8 result "
        "(@claim_qwen_plus_3p8), the Llama +22.2 result "
        "(@claim_llama_plus_22p2), and the cross-framework "
        "OpenRLHF/verl match (@claim_patched_matches_verl) which rules "
        "out implementation-specific artifacts."
    ),
    prior=0.94,
)

# ===========================================================================
# Implications
# ===========================================================================

strat_implications_synthesis = support(
    [
        claim_synthesis_baselines_deflated,
        claim_implication_cross_framework,
        claim_implication_other_areas,
        claim_restored_confidence,
    ],
    claim_implications,
    reason=(
        "The motivation-section implication claim (@claim_implications) "
        "is the conjunction of three sub-implications: cross-framework "
        "validation as norm (@claim_implication_cross_framework), "
        "potential broader effect on other ML areas "
        "(@claim_implication_other_areas), and restored confidence in "
        "SFT-then-RL (@claim_restored_confidence). The synthesis "
        "(@claim_synthesis_baselines_deflated) is the empirical anchor."
    ),
    prior=0.93,
)

strat_cross_framework_implication = support(
    [claim_patched_matches_verl, claim_bug_propagation],
    claim_implication_cross_framework,
    reason=(
        "The cross-framework-validation implication "
        "(@claim_implication_cross_framework) is justified by (a) the "
        "fact that the patched OpenRLHF and verl converge on equivalent "
        "scores (@claim_patched_matches_verl), demonstrating that "
        "running two frameworks would have caught the bug; and (b) the "
        "wide propagation of the optimizer bug across TRL/OpenRLHF/"
        "Llama-Factory (@claim_bug_propagation), demonstrating that a "
        "single buggy upstream framework can affect many downstream "
        "training stacks simultaneously."
    ),
    prior=0.92,
)

strat_other_areas_implication = support(
    [claim_bug_propagation],
    claim_implication_other_areas,
    reason=(
        "The 'other research areas' implication "
        "(@claim_implication_other_areas) follows directly from the "
        "general-purpose nature of the affected frameworks "
        "(@claim_bug_propagation, TRL/OpenRLHF/Llama-Factory): SFT is "
        "used in many ML subfields besides mixed-policy LLM-reasoning, "
        "and any 2024-2026 SFT result that used DeepSpeed CPU-offload "
        "is potentially affected."
    ),
    prior=0.9,
)

strat_restored_confidence = support(
    [claim_qwen_plus_3p8, claim_llama_plus_22p2],
    claim_restored_confidence,
    reason=(
        "The 'restored confidence in SFT-then-RL' implication "
        "(@claim_restored_confidence) follows from both headline "
        "outperformance results: +3.8 on Qwen2.5-Math-7B "
        "(@claim_qwen_plus_3p8) and +22.2 on Llama-3.1-8B "
        "(@claim_llama_plus_22p2). Two independent model families "
        "show SFT-then-RL on top once baselines are corrected."
    ),
    prior=0.94,
)

# ===========================================================================
# INDUCTION: population law over the two model families
# ===========================================================================

claim_population_law = claim(
    "**Population law: once both SFT bugs are corrected, the standard "
    "SFT-then-RL pipeline outperforms every published mixed-policy "
    "method on math reasoning benchmarks across the model families "
    "evaluated in the mixed-policy literature.** This is the paper's "
    "central empirical generalization, supported by the Qwen2.5-Math-7B "
    "+3.8 result (in-distribution math benchmarks) and the "
    "Llama-3.1-8B +22.2 result (math subset on which all methods "
    "report scores) [@Limozin2026SFTthenRL, Sec. 4; Sec. 4.1].",
    title="Population law: corrected SFT-then-RL > every mixed-policy across both model families",
)

# Generative direction: the law predicts each per-model headline result.
s_law_predicts_qwen = support(
    [claim_population_law],
    claim_qwen_plus_3p8,
    reason=(
        "Generative direction: the population law (@claim_population_law) "
        "predicts that corrected SFT-then-RL beats every evaluated "
        "mixed-policy method on Qwen2.5-Math-7B; the +3.8 ID-average "
        "headline (@claim_qwen_plus_3p8) is the realization of this "
        "prediction for the Qwen model family."
    ),
    prior=0.92,
    background=[setup_qwen_base],
)

s_law_predicts_llama = support(
    [claim_population_law],
    claim_llama_plus_22p2,
    reason=(
        "Generative direction: the population law (@claim_population_law) "
        "predicts that corrected SFT-then-RL beats every evaluated "
        "mixed-policy method on Llama-3.1-8B; the +22.2 average "
        "headline (@claim_llama_plus_22p2) is the realization for the "
        "Llama model family."
    ),
    prior=0.92,
    background=[setup_llama_base],
)

induction_population_law = induction(
    s_law_predicts_qwen,
    s_law_predicts_llama,
    law=claim_population_law,
    reason=(
        "The two model families test the law in *independent* regimes: "
        "Qwen2.5-Math-7B (math-emphasized pre-training) and Llama-3.1-8B "
        "(general-purpose, little pre-trained math). Both confirm the "
        "law -- corrected SFT-then-RL outperforms every published "
        "mixed-policy method -- which jointly induces the population "
        "law to a higher confidence than either single observation alone "
        "would warrant. The +3.8 vs +22.2 magnitude difference further "
        "speaks to the *robustness* of the law across pre-training "
        "regimes."
    ),
)

# ===========================================================================
# CENTRAL ABDUCTION: bug-attribution H vs methodological-advance Alt
# ===========================================================================

# Hypothesis: bug-attribution thesis (@claim_synthesis_baselines_deflated)
# Alternative: mixed-policy methods are a real advance and SFT-then-RL's
# apparent superiority is implementation-specific (@claim_alt_methodological_advance)
# Discriminating observation: cross-framework match (@claim_obs_cross_framework_match)

s_bug_supports = support(
    [claim_synthesis_baselines_deflated],
    claim_obs_cross_framework_match,
    reason=(
        "Under the bug-attribution hypothesis "
        "(@claim_synthesis_baselines_deflated), two independent SFT "
        "stacks both lacking the bugs (patched OpenRLHF and verl) are "
        "expected to converge to statistically equivalent SFT scores, "
        "because both now satisfy the gradient-accumulation contract "
        "and the per-token-mean loss contract. The 54.0 vs 53.8 match "
        "(@claim_obs_cross_framework_match) is exactly this prediction."
    ),
    prior=0.96,
)

s_alt_supports = support(
    [claim_alt_methodological_advance],
    claim_obs_cross_framework_match,
    reason=(
        "Under the methodological-advance alternative "
        "(@claim_alt_methodological_advance), the cross-framework match "
        "between two corrected stacks is awkward: the alternative would "
        "have to attribute the convergence to shared evaluation noise, "
        "but the standard deviations are tight (0.1-0.2) and the "
        "per-benchmark scores agree row-by-row across the Table 2 "
        "subset. The alternative cannot easily explain why the "
        "OpenRLHF stack ends up at exactly the verl number after the "
        "two specific bug fixes."
    ),
    prior=0.3,
)

comp_bug_vs_methodology = compare(
    claim_pred_bug_explains,
    claim_pred_alt_explains,
    claim_obs_cross_framework_match,
    reason=(
        "The bug-attribution prediction (@claim_pred_bug_explains) "
        "expects cross-framework convergence after the two specific bug "
        "fixes plus the predicted per-bug dynamics signatures (loss-"
        "aggregation -> variability; optimizer -> mean shift + "
        "suppressed grad norm). The methodological-advance alternative "
        "(@claim_pred_alt_explains) expects cross-framework "
        "*divergence* (because mixed-policy is supposed to be doing "
        "real work that SFT-then-RL cannot replicate). The 54.0 vs 53.8 "
        "cross-framework match (@claim_obs_cross_framework_match) "
        "discriminates strongly in favor of the bug-attribution "
        "prediction."
    ),
    prior=0.95,
)

abd_bug_explains_gains = abduction(
    s_bug_supports,
    s_alt_supports,
    comp_bug_vs_methodology,
    reason=(
        "Both hypotheses attempt to explain the same observation -- "
        "the substantial pre-correction gap between mixed-policy methods "
        "and SFT-then-RL baselines, *and* the cross-framework "
        "convergence after the specific bug fixes. The bug-attribution "
        "hypothesis (@claim_synthesis_baselines_deflated) predicts both "
        "the gap (deflated baselines) and the convergence (two correct "
        "implementations of the same algorithm). The methodological-"
        "advance alternative (@claim_alt_methodological_advance) "
        "predicts only the gap, and is awkward at explaining why two "
        "SFT implementations converge to identical scores once the "
        "specific bug fixes are applied. The Table 2 cross-framework "
        "match (@claim_obs_cross_framework_match) is the discriminating "
        "observation."
    ),
)

# ===========================================================================
# CONTRADICTION 1: published mixed-policy advantage vs corrected outperformance
# ===========================================================================

# We model the published-claim foil as a derived position so it picks up the
# contradiction tension with the corrected-baseline outperformance.
claim_published_advantage_holds = claim(
    "**Foil position: the published mixed-policy advantage over "
    "SFT-then-RL is a real methodological advance.** Under this "
    "position, the reported numbers in [@LUFFY; @ReLIFT; @SRFT; "
    "@PrefixRFT; @HPT] reflect a true superiority of mixing on- and "
    "off-policy signals within a single stage, and the SFT-then-RL "
    "pipeline is genuinely outperformed. This is the prevailing "
    "claim in the mixed-policy literature [@Limozin2026SFTthenRL, "
    "Sec. 1].",
    title="Foil: the published mixed-policy advantage is a real methodological advance",
)

strat_foil_from_motivation = support(
    [claim_mixed_policy_gains_reported, claim_intuitive_motivation_for_mixing],
    claim_published_advantage_holds,
    reason=(
        "The foil position (@claim_published_advantage_holds) is the "
        "literal claim made in the mixed-policy literature "
        "(@claim_mixed_policy_gains_reported), motivated by the "
        "intuitive complementarity argument "
        "(@claim_intuitive_motivation_for_mixing). The literature "
        "presents this as an established result."
    ),
    prior=0.9,
)

contra_published_vs_corrected = contradiction(
    claim_published_advantage_holds,
    claim_qwen_plus_3p8,
    reason=(
        "The foil (@claim_published_advantage_holds: published "
        "mixed-policy is genuinely better than SFT-then-RL) and the "
        "corrected-baseline result (@claim_qwen_plus_3p8: corrected "
        "SFT-then-RL beats every evaluated mixed-policy method on "
        "Qwen2.5-Math-7B by +3.8 ID points) cannot both be true. If "
        "corrected SFT-then-RL outperforms every mixed-policy method "
        "evaluated, then the published mixed-policy advantage cannot "
        "be a real methodological advance; conversely, if the published "
        "advantage is real, then the corrected-baseline result must be "
        "wrong."
    ),
    prior=0.95,
)

# ===========================================================================
# CONTRADICTION 2: optimizer-bug-is-cosmetic vs optimizer-bug-dominates
# ===========================================================================

claim_optimizer_bug_cosmetic = claim(
    "**Alternative attribution: the CPU-offloaded optimizer bug is a "
    "minor / cosmetic detail that does not materially affect SFT "
    "performance.** Under this position, a bug that drops K-1 of K "
    "micro-batches' gradients would either (i) be visible in standard "
    "training metrics and thus already caught in code review, or (ii) "
    "have only marginal impact because effective batch size 1 is still "
    "trainable. This view treats the deflation as primarily caused by "
    "other factors (hyperparameters, evaluation choice, model variance) "
    "rather than the optimizer code.",
    title="Alt-attribution: the optimizer bug is small / cosmetic, not the dominant cause",
)

contra_optimizer_cosmetic_vs_dominant = contradiction(
    claim_optimizer_bug_cosmetic,
    claim_optimizer_dominates_attribution,
    reason=(
        "The 'optimizer bug is cosmetic' alternative attribution "
        "(@claim_optimizer_bug_cosmetic) and the paper's quantitative "
        "attribution finding (@claim_optimizer_dominates_attribution: "
        "the optimizer fix recovers ~5.1 of the ~5.7 total gap, ~89%) "
        "cannot both be true. The +5.1 average-score gain measured "
        "across 6 benchmarks at 3 seeds is too large to call cosmetic; "
        "the suppressed gradient norms in Fig. 2 (right) provide a "
        "direct empirical signature; the cross-framework convergence "
        "after the fix corroborates the attribution. The two positions "
        "are incompatible."
    ),
    prior=0.96,
)

# ===========================================================================
# Other supporting strategies
# ===========================================================================

strat_baseline_suspicion_supported = support(
    [
        claim_luffy_method,
        claim_relift_method,
        claim_prefix_rft_method,
        claim_hpt_method,
    ],
    claim_baseline_suspicion,
    reason=(
        "The motivation-section suspicion (@claim_baseline_suspicion) "
        "that the published baselines are deflated is grounded in the "
        "specific SFT-stack choices of each method: LUFFY uses OpenRLHF "
        "(@claim_luffy_method), ReLIFT uses Llama-Factory "
        "(@claim_relift_method), Prefix-RFT inherits LUFFY's baseline "
        "(@claim_prefix_rft_method), and HPT does not detail its setup "
        "but is assumed to inherit the same affected pipelines "
        "(@claim_hpt_method). All four choices route through frameworks "
        "subsequently shown to have the bugs."
    ),
    prior=0.88,
    background=[setup_mixed_policy_definition],
)

strat_qwen_ood_competitive = support(
    [claim_qwen_sft_then_rl, claim_qwen_mixed_policy_table],
    claim_qwen_ood_competitive,
    reason=(
        "OOD competitiveness (@claim_qwen_ood_competitive: "
        "SFT-then-RL 59.9 OOD = second-best, beaten only by SRFT "
        "62.5) follows from the OOD column of the corrected SFT-then-RL "
        "result (@claim_qwen_sft_then_rl) and the OOD numbers in "
        "Table 1 (@claim_qwen_mixed_policy_table)."
    ),
    prior=0.95,
)

strat_llama_failure_supported = support(
    [claim_llama_failure_explanation],
    claim_efficiency_gap,
    reason=(
        "The fundamental-efficiency-gap argument "
        "(@claim_efficiency_gap) is a generalization of the Llama "
        "failure-mode explanation (@claim_llama_failure_explanation): "
        "where pre-training does not cover the target domain, "
        "mixed-policy methods cannot match SFT-then-RL's sample "
        "efficiency because the RL signal is too sparse early on."
    ),
    prior=0.9,
    background=[setup_llama_base],
)

# Per-method baselines and reproduction connect the related-work module
# to the synthesis claims (so they don't orphan)
strat_qwen_sft_corrected_supports_then_rl = support(
    [claim_qwen_sft_corrected],
    claim_qwen_sft_then_rl,
    reason=(
        "The corrected SFT-then-RL result (@claim_qwen_sft_then_rl, "
        "57.0 ID) builds on the corrected SFT result "
        "(@claim_qwen_sft_corrected, 52.2 ID): the +4.8-point ID lift "
        "from adding 500 GRPO steps over the corrected SFT checkpoint "
        "is the realized RL contribution."
    ),
    prior=0.95,
    background=[setup_grpo_500_steps, setup_qwen_base],
)

strat_llama_sft_supports_then_rl = support(
    [claim_llama_sft],
    claim_llama_sft_then_rl,
    reason=(
        "The corrected Llama-3.1-8B SFT-then-RL result "
        "(@claim_llama_sft_then_rl, 43.7) builds on the corrected SFT "
        "result (@claim_llama_sft, 33.9): the +9.8-point average lift "
        "from adding 500 GRPO steps is the realized RL contribution. "
        "On Llama the SFT contribution alone already exceeds every "
        "mixed-policy method (33.9 > 21.5)."
    ),
    prior=0.95,
    background=[setup_grpo_500_steps, setup_llama_base],
)

# Wire the training-dynamics observations into the discussion's claims so
# they are not orphaned
strat_dynamics_supports_efficiency = support(
    [
        claim_qwen_training_dynamics,
        claim_response_length_dynamics,
        claim_entropy_dynamics,
    ],
    claim_dense_reward_from_sft,
    reason=(
        "The dense-reward-from-SFT mechanism (@claim_dense_reward_from_sft) "
        "is supported by three Fig. 3 observations: training reward "
        "(@claim_qwen_training_dynamics: SFT-then-RL starts above "
        "mixed-policy plateaus), response length "
        "(@claim_response_length_dynamics: SFT-then-RL converges down "
        "while mixed-policy diverges up), and policy entropy "
        "(@claim_entropy_dynamics: SFT-then-RL is in a refining "
        "regime, mixed-policy is exploring)."
    ),
    prior=0.92,
)

# Limitations bear on the broader implications
strat_limitations_to_implications = support(
    [
        claim_lim_domain_scope,
        claim_lim_model_families,
        claim_lim_mixed_atop_corrected,
        claim_lim_relift_hpt_unverified,
    ],
    claim_implications,
    reason=(
        "The four declared limitations -- domain scope "
        "(@claim_lim_domain_scope), model families "
        "(@claim_lim_model_families), mixed-policy atop a corrected "
        "SFT (@claim_lim_mixed_atop_corrected), and unverified "
        "ReLIFT/HPT configs (@claim_lim_relift_hpt_unverified) -- "
        "qualify but do not invalidate the implication-level claim "
        "(@claim_implications); they bound the scope under which the "
        "implication holds. They are part of the picture the paper "
        "communicates."
    ),
    prior=0.85,
)

# Setup-implications wiring (so settings-only claims are not orphans)
strat_chat_template_implies_synthesis = support(
    [claim_chat_template_unified],
    claim_synthesis_baselines_deflated,
    reason=(
        "The chat-template observation (@claim_chat_template_unified) "
        "-- that Llama-3.1-8B follows the full Qwen prompt fine when "
        "SFT is correctly implemented, contrary to prior reports -- is "
        "additional evidence that the prior literature's "
        "'undertrained-baseline' symptoms (template mismatch, "
        "hand-tuned simplifications) were artifacts of the same "
        "underlying SFT bugs. This corroborates the synthesis "
        "(@claim_synthesis_baselines_deflated)."
    ),
    prior=0.85,
)

strat_reproduction_design_supports_attribution = support(
    [claim_reproduction_design],
    claim_attribution_table,
    reason=(
        "The progressive-bug-fix reproduction design "
        "(@claim_reproduction_design) is the methodological vehicle "
        "that produces the per-bug attribution table "
        "(@claim_attribution_table). Without the careful four-variant "
        "isolation, the per-bug deltas could not be cleanly attributed."
    ),
    prior=0.95,
    background=[setup_seed_protocol, setup_table2_subset],
)

# Other-mixed-policy-methods + qualitative claims
strat_other_methods_supports_implication = support(
    [claim_other_mixed_policy_methods, claim_bug_propagation],
    claim_implication_other_areas,
    reason=(
        "The seven other mixed-policy methods flagged for SFT auditing "
        "(@claim_other_mixed_policy_methods) plus the wide propagation "
        "of the optimizer bug (@claim_bug_propagation) jointly support "
        "the broader-areas implication (@claim_implication_other_areas) "
        "that the bug attribution likely extends beyond the five "
        "directly-evaluated methods."
    ),
    prior=0.85,
)

# Setup pipelines anchor the corrected-results claims
strat_sft_then_rl_pipeline_supports_qwen_sft = support(
    [claim_two_bug_thesis],
    claim_qwen_sft_corrected,
    reason=(
        "The corrected SFT result on Qwen2.5-Math-7B "
        "(@claim_qwen_sft_corrected, 52.2 ID) is the verl baseline that "
        "the two-bug thesis (@claim_two_bug_thesis) predicts: when both "
        "bugs are absent (verl never had them), SFT achieves the "
        "level corresponding to the bug-fixed Table 2 score of 53.8 -- "
        "which Table 2 confirms within seed variance."
    ),
    prior=0.92,
    background=[setup_sft_then_rl_pipeline, setup_qwen_base],
)

strat_llama_sft_supported = support(
    [claim_two_bug_thesis, claim_chat_template_unified],
    claim_llama_sft,
    reason=(
        "The corrected Llama-3.1-8B SFT result (@claim_llama_sft, 33.9) "
        "is the realization of the two-bug thesis "
        "(@claim_two_bug_thesis) on the Llama family, combined with the "
        "unified-chat-template observation (@claim_chat_template_unified) "
        "which removes another previously-introduced confound."
    ),
    prior=0.9,
    background=[setup_sft_then_rl_pipeline, setup_llama_base],
)

__all__ = [
    "claim_population_law",
    "s_law_predicts_qwen",
    "s_law_predicts_llama",
    "induction_population_law",
    "claim_published_advantage_holds",
    "claim_optimizer_bug_cosmetic",
    "strat_grad_norm_from_mechanism",
    "strat_mean_loss_shifted",
    "strat_bug_propagation_evidenced",
    "strat_optimizer_fix_correctness",
    "strat_loss_agg_inherited",
    "strat_loss_agg_variability",
    "strat_loss_agg_fix_correctness",
    "strat_attribution_table_from_rows",
    "strat_optimizer_dominates_from_attribution",
    "strat_dynamics_from_mechanisms",
    "strat_hyperparam_explains_srft",
    "strat_qwen_3p8_from_results",
    "strat_qwen_headline_from_plus_3p8",
    "strat_llama_headline_from_plus_22p2",
    "strat_loss_agg_small_effect_from_attribution",
    "strat_per_method_from_results",
    "strat_qwen_reproduction_evidenced",
    "strat_perceived_gains_synthesis",
    "strat_llama_22p2_from_results",
    "strat_llama_failure_explanation",
    "strat_truncated_id_outperforms",
    "strat_compute_efficiency_synthesis",
    "strat_compute_efficiency_headline_supported",
    "strat_flops_table_from_decomposition",
    "strat_two_bug_thesis_from_mechanisms",
    "strat_optimizer_dominant_headline",
    "strat_synthesis_baselines_deflated",
    "strat_implications_synthesis",
    "strat_cross_framework_implication",
    "strat_other_areas_implication",
    "strat_restored_confidence",
    "s_bug_supports",
    "s_alt_supports",
    "comp_bug_vs_methodology",
    "abd_bug_explains_gains",
    "strat_foil_from_motivation",
    "contra_published_vs_corrected",
    "contra_optimizer_cosmetic_vs_dominant",
    "strat_baseline_suspicion_supported",
    "strat_qwen_ood_competitive",
    "strat_llama_failure_supported",
    "strat_qwen_sft_corrected_supports_then_rl",
    "strat_llama_sft_supports_then_rl",
    "strat_dynamics_supports_efficiency",
    "strat_limitations_to_implications",
    "strat_chat_template_implies_synthesis",
    "strat_reproduction_design_supports_attribution",
    "strat_other_methods_supports_implication",
    "strat_sft_then_rl_pipeline_supports_qwen_sft",
    "strat_llama_sft_supported",
]
