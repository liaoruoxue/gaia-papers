"""Pass 2 wiring: strategies, abductions, inductions, contradictions.

Conventions:

* `support` -- soft deduction with author-specified prior. The default for
  "premises imply conclusion" with empirical or interpretive uncertainty.
* `induction` -- chained binary composite. Used twice:
    (i) per-iteration evidence over the four named AHE peaks (iter 2, 5, 6, 8)
        supporting the law "the AHE outer loop is a stable harness optimizer
        on Terminal-Bench 2";
    (ii) per-base-model-family evidence over five alternate base models
         supporting the law "the frozen AHE harness transfers across base-
         model families with consistently positive gain".
* `abduction` -- inference to best explanation. Used once: the central
  thesis question (does the 3-pillar observability design cause the
  observed pattern of {main result + transfer + factual-structure
  localization}, or do trivial alternatives -- bigger LM, more
  iterations, benchmark overfitting -- explain it).
* `contradiction` -- two contradictions:
    (i) the prevailing assumption that harness engineering must be manual
        vs the AHE demonstration of autonomous evolution;
    (ii) the assumption that the system prompt is the main lever vs the
         component-localization ablation showing the prompt regresses
         while tools/middleware/memory carry the gain.
"""

from gaia.lang import (
    abduction,
    claim,
    compare,
    contradiction,
    induction,
    support,
)

from .motivation import (
    claim_ahe_three_pillars,
    claim_existing_evolution_partial,
    claim_harness_central_to_perf,
    claim_main_terminal_headline,
    claim_manual_harness_practice,
    claim_observability_bottleneck,
    claim_optimal_harness_model_specific,
    claim_two_structural_obstacles,
    claim_swe_transfer_headline,
    claim_cross_family_headline,
    claim_ablation_headline,
    claim_three_contributions,
    setup_three_obstacles,
    setup_terminal_bench_2,
    setup_swebench_verified,
    setup_harness_definition,
    setup_coding_agent_regime,
)
from .s2_related_work import (
    claim_ace_method,
    claim_ahe_combinatorial_whole,
    claim_ahe_minimal_human_prior,
    claim_codex_human_baseline,
    claim_eval_infrastructure,
    claim_evaluation_horizons,
    claim_harness_engineering_definition,
    claim_meta_harness,
    claim_program_structure_methods,
    claim_prompt_instruction_methods,
    claim_self_critique_methods,
    claim_tfgrpo_method,
)
from .s3_setup import (
    claim_attribute_before_distill,
    claim_design_principle_observability,
    claim_explore_agent_seed_skills,
    setup_ahe_outer_loop,
    setup_evaluation_setup,
    setup_k_rollouts,
    setup_models_used,
    setup_role_agents,
    setup_runtime_infrastructure,
    setup_seed_nexau0,
)
from .s4_component_observability import (
    claim_component_type_table,
    claim_decoupling_realizes_observability,
    claim_explicit_revertible_action_space,
    claim_minimal_seed_attribution,
    setup_seven_component_types,
    setup_workspace_git_history,
)
from .s5_experience_observability import (
    claim_distillation_realizes_experience_obs,
    claim_partial_pass_anchor,
    claim_per_task_pass_fail_grounding,
    claim_token_compression,
    setup_agent_debugger_framework,
    setup_layered_corpus_artifacts,
    setup_progressive_disclosure,
)
from .s6_decision_observability import (
    claim_controllability_blocks_shortcuts,
    claim_decision_observability_solves_o3,
    claim_evidence_driven_targeting,
    claim_falsifiable_contract,
    claim_fix_attribution_quantitative,
    claim_per_round_regression_breakdown,
    claim_regression_attribution_quantitative,
    claim_regression_blindness,
    setup_attribution_check,
    setup_change_manifest,
    setup_two_hard_constraints,
)
from .s7_main_results import (
    claim_ace_pass1,
    claim_ahe_beats_human_baselines,
    claim_ahe_beats_self_evolution_baselines,
    claim_ahe_pass1,
    claim_codex_pass1,
    claim_hard_tier_exception,
    claim_iter2_peak,
    claim_iter5_peak,
    claim_iter6_peak,
    claim_iter8_peak,
    claim_iteration_trajectory,
    claim_layer_mismatch_explanation,
    claim_margin_vs_ace,
    claim_margin_vs_codex,
    claim_margin_vs_seed,
    claim_margin_vs_tfgrpo,
    claim_other_human_baselines,
    claim_seed_pass1,
    claim_terminal_results_table,
    claim_tfgrpo_pass1,
)
from .s8_transfer import (
    claim_all_five_positive,
    claim_cross_family_dominate,
    claim_cross_model_table,
    claim_deepseek_transfer,
    claim_evolved_components_general,
    claim_gemini_transfer,
    claim_gpt54_med_transfer,
    claim_gpt54_xhigh_transfer,
    claim_non_monotone_within_family,
    claim_qwen_transfer,
    claim_succ_per_mtok_table,
    claim_swe_aggregate_success,
    claim_swe_aggregate_tokens,
    claim_swe_concentration,
    claim_swe_table_pass1,
    claim_swe_table_tokens,
)
from .s9_ablations import (
    claim_ablation_table,
    claim_attribution_is_asymmetric,
    claim_factual_structure_transfers,
    claim_memory_failure_surface,
    claim_memory_only_delta,
    claim_middleware_failure_surface,
    claim_middleware_only_delta,
    claim_non_additive_interaction,
    claim_per_round_fix_breakdown,
    claim_prompt_failure_surface,
    claim_prompt_only_regression,
    claim_regression_blindness_explains_non_monotone,
    claim_tool_failure_surface,
    claim_tool_only_delta,
)
from .s10_discussion import (
    claim_alt_manual_only,
    claim_alt_prompt_is_main_lever,
    claim_complementary_to_model_training,
    claim_lim_benchmark_scope,
    claim_lim_operating_point,
    claim_lim_self_modification_governance,
    claim_lim_two_evolution_limits,
    claim_obs_3pillar_pattern,
    claim_observability_driven_evolution_works,
    claim_pred_3pillar_explains,
    claim_pred_alt_explains,
)


# ============================================================================
# Section 4 (s4_component_observability): pillar 1 internal wiring
# ============================================================================

strat_component_type_table_anchor = support(
    [claim_ahe_three_pillars],
    claim_component_type_table,
    reason=(
        "The component-type table (@claim_component_type_table) is "
        "the documentation form of the seven-component substrate "
        "(@setup_seven_component_types) as presented to the Evolve "
        "Agent in Appendix B.2; it formalizes pillar 1 of AHE "
        "(@claim_ahe_three_pillars) into an actionable lookup with "
        "files, characteristics, and when-to-use guidance."
    ),
    prior=0.95,
    background=[setup_seven_component_types],
)

strat_decoupling_from_components = support(
    [claim_component_type_table],
    claim_decoupling_realizes_observability,
    reason=(
        "Component observability (@claim_decoupling_realizes_observability) "
        "is realized by the seven loosely-coupled component types each "
        "exposed at fixed mount points (@setup_seven_component_types) -- "
        "documented in the component-type table presented to the Evolve "
        "Agent (@claim_component_type_table). Loose coupling is what "
        "makes failure-to-component mapping single-valued: a middleware "
        "change does not affect the prompt, and a skill change does not "
        "touch any tool, so each pass-rate delta localizes to one file."
    ),
    prior=0.95,
    background=[setup_seven_component_types],
)

strat_action_space_from_git_history = support(
    [claim_decoupling_realizes_observability],
    claim_explicit_revertible_action_space,
    reason=(
        "The action space is explicit and revertible "
        "(@claim_explicit_revertible_action_space) because (a) the "
        "decoupled components give a typed action set 'modify "
        "component class c at file path p' "
        "(@claim_decoupling_realizes_observability), and (b) "
        "workspace git history (@setup_workspace_git_history) "
        "provides commit-level rollback granularity at the same "
        "file boundary."
    ),
    prior=0.94,
    background=[setup_workspace_git_history, setup_seven_component_types],
)

strat_minimal_seed_supports_attribution = support(
    [claim_ahe_minimal_human_prior],
    claim_minimal_seed_attribution,
    reason=(
        "The minimal-seed attribution argument "
        "(@claim_minimal_seed_attribution) is a direct consequence of "
        "the minimal-human-prior design distinction "
        "(@claim_ahe_minimal_human_prior) anchored in the seed "
        "definition (@setup_seed_nexau0): a bash-only seed with no "
        "middleware / skills / memory means every iteration's "
        "components are added by the loop, so credit assignment is "
        "unambiguous."
    ),
    prior=0.95,
    background=[setup_seed_nexau0],
)

# ============================================================================
# Section 5 (s5_experience_observability): pillar 2 internal wiring
# ============================================================================

strat_token_compression_from_setup = support(
    [claim_ahe_three_pillars],
    claim_token_compression,
    reason=(
        "The 1000x compression (@claim_token_compression, 10M -> 10K) "
        "follows from the layered corpus structure "
        "(@setup_layered_corpus_artifacts, overview + per-task "
        "summaries + raw fallback) plus progressive disclosure "
        "(@setup_progressive_disclosure, agent reads only summaries by "
        "default). Pillar 2 of the AHE design "
        "(@claim_ahe_three_pillars) explicitly cites this 10M->10K "
        "distillation as its empirical signature."
    ),
    prior=0.93,
    background=[setup_layered_corpus_artifacts, setup_progressive_disclosure],
)

strat_distillation_realizes_pillar2 = support(
    [claim_token_compression, claim_ahe_three_pillars],
    claim_distillation_realizes_experience_obs,
    reason=(
        "Experience observability (@claim_distillation_realizes_"
        "experience_obs) is realized by the Agent Debugger framework "
        "(@setup_agent_debugger_framework) producing the layered "
        "corpus (@setup_layered_corpus_artifacts) at the compressed "
        "scale (@claim_token_compression). Pillar 2 in AHE "
        "(@claim_ahe_three_pillars) is exactly this distillation "
        "step, where the Evolve Agent receives structured root "
        "causes class-by-class rather than raw logs."
    ),
    prior=0.94,
    background=[setup_agent_debugger_framework, setup_layered_corpus_artifacts],
)

strat_per_task_pass_fail_grounding = support(
    [claim_distillation_realizes_experience_obs],
    claim_per_task_pass_fail_grounding,
    reason=(
        "Per-task analysis grounding (@claim_per_task_pass_fail_"
        "grounding) is part of the layered corpus design "
        "(@setup_layered_corpus_artifacts L1): each per-task report "
        "explicitly carries the pass/fail status of every rollout, "
        "anchoring the report's narrative in the verifier verdict. "
        "This grounding is what makes Pillar 2 distillation "
        "(@claim_distillation_realizes_experience_obs) usable as "
        "evidence rather than as opinion."
    ),
    prior=0.95,
    background=[setup_layered_corpus_artifacts],
)

strat_partial_pass_from_k = support(
    [claim_per_task_pass_fail_grounding],
    claim_partial_pass_anchor,
    reason=(
        "Partial-pass diagnosis (@claim_partial_pass_anchor) is "
        "available because k=2 rollouts per task (@setup_k_rollouts) "
        "produce per-task pass/fail vectors that can be partial, and "
        "the Agent Debugger groups traces with the same query into "
        "one environment (@setup_layered_corpus_artifacts). The "
        "per-task pass/fail grounding (@claim_per_task_pass_fail_"
        "grounding) makes the partial-pass partition usable for "
        "diagnosis."
    ),
    prior=0.94,
    background=[setup_k_rollouts, setup_layered_corpus_artifacts],
)

# ============================================================================
# Section 6 (s6_decision_observability): pillar 3 internal wiring
# ============================================================================

strat_falsifiable_contract = support(
    [claim_ahe_three_pillars],
    claim_falsifiable_contract,
    reason=(
        "The falsifiable-contract claim (@claim_falsifiable_contract) "
        "follows from the conjunction of (a) the manifest schema "
        "(@setup_change_manifest) requiring predicted_fixes and "
        "risk_tasks per edit, (b) the attribution check "
        "(@setup_attribution_check) intersecting predictions with "
        "observed deltas and rolling back at file granularity, and "
        "(c) the two hard constraints (@setup_two_hard_constraints) "
        "preventing the Evolve Agent from rationalizing edits away. "
        "Pillar 3 in the AHE design (@claim_ahe_three_pillars) is "
        "exactly the realization of this contract structure."
    ),
    prior=0.95,
    background=[
        setup_change_manifest,
        setup_attribution_check,
        setup_two_hard_constraints,
    ],
)

strat_controllability_blocks = support(
    [claim_falsifiable_contract],
    claim_controllability_blocks_shortcuts,
    reason=(
        "Controllability bounds (@claim_controllability_blocks_shortcuts) "
        "are exactly constraint C1 of the two hard constraints "
        "(@setup_two_hard_constraints): workspace-only writes, read-"
        "only verifier/tracer/LLM-config, non-deletable seed prompt. "
        "The list of blocked shortcuts (disabling verifier, swapping "
        "model, raising reasoning budget) is exactly what these "
        "read-only restrictions cover. The falsifiable-contract "
        "claim (@claim_falsifiable_contract) names these restrictions "
        "as one of its three components."
    ),
    prior=0.96,
    background=[setup_two_hard_constraints],
)

strat_decision_solves_o3 = support(
    [
        claim_falsifiable_contract,
        claim_controllability_blocks_shortcuts,
    ],
    claim_decision_observability_solves_o3,
    reason=(
        "Decision observability solves attribution opacity "
        "(@claim_decision_observability_solves_o3, obstacle O3) via "
        "(a) the falsifiable-contract structure (@claim_falsifiable_"
        "contract), (b) controllability bounds preventing self-"
        "rationalization (@claim_controllability_blocks_shortcuts), "
        "and (c) automatic file-granularity rollback when predicted "
        "fixes do not materialize (@setup_attribution_check)."
    ),
    prior=0.94,
    background=[setup_three_obstacles, setup_attribution_check],
)

strat_evidence_driven_from_metrics = support(
    [claim_fix_attribution_quantitative],
    claim_evidence_driven_targeting,
    reason=(
        "Evidence-driven targeting (@claim_evidence_driven_targeting) "
        "is the qualitative interpretation of the quantitative fix "
        "metrics (@claim_fix_attribution_quantitative): fix-precision "
        "33.7% / fix-recall 51.4% sit ~5x above the 6.5% / 10.6% "
        "random baselines, so each edit lands on a real anticipated "
        "target rather than on an arbitrary subset."
    ),
    prior=0.95,
)

strat_regression_blindness_from_metrics = support(
    [claim_regression_attribution_quantitative, claim_per_round_regression_breakdown],
    claim_regression_blindness,
    reason=(
        "Regression blindness (@claim_regression_blindness) is the "
        "qualitative interpretation of the quantitative regression "
        "metrics (@claim_regression_attribution_quantitative): "
        "regression-precision 11.8% / regression-recall 11.1% sit "
        "only ~2x above the 5.6% / 5.4% random baselines, with the "
        "per-round breakdown (@claim_per_round_regression_breakdown, "
        "43 predicted, 5 landed; 40 unforeseen actual) confirming "
        "near-random performance."
    ),
    prior=0.94,
)

# ============================================================================
# Section 7 (s7_main_results): margin arithmetic + headlines
# ============================================================================

strat_margin_vs_seed = support(
    [claim_ahe_pass1, claim_seed_pass1],
    claim_margin_vs_seed,
    reason=(
        "The +7.3 pp seed margin (@claim_margin_vs_seed) is arithmetic "
        "on AHE 77.0% (@claim_ahe_pass1) and seed 69.7% "
        "(@claim_seed_pass1): 77.0 - 69.7 = +7.3."
    ),
    prior=0.97,
    background=[setup_terminal_bench_2],
)

strat_margin_vs_codex = support(
    [claim_ahe_pass1, claim_codex_pass1],
    claim_margin_vs_codex,
    reason=(
        "The +5.1 pp Codex margin (@claim_margin_vs_codex) is "
        "arithmetic on AHE 77.0% (@claim_ahe_pass1) and Codex 71.9% "
        "(@claim_codex_pass1): 77.0 - 71.9 = +5.1."
    ),
    prior=0.97,
    background=[setup_terminal_bench_2],
)

strat_margin_vs_ace = support(
    [claim_ahe_pass1, claim_ace_pass1],
    claim_margin_vs_ace,
    reason=(
        "The +8.1 pp ACE margin (@claim_margin_vs_ace) is arithmetic "
        "on AHE 77.0% (@claim_ahe_pass1) and ACE 68.9% "
        "(@claim_ace_pass1): 77.0 - 68.9 = +8.1."
    ),
    prior=0.97,
    background=[setup_terminal_bench_2],
)

strat_margin_vs_tfgrpo = support(
    [claim_ahe_pass1, claim_tfgrpo_pass1],
    claim_margin_vs_tfgrpo,
    reason=(
        "The +4.7 pp TF-GRPO margin (@claim_margin_vs_tfgrpo) is "
        "arithmetic on AHE 77.0% (@claim_ahe_pass1) and TF-GRPO 72.3% "
        "(@claim_tfgrpo_pass1): 77.0 - 72.3 = +4.7."
    ),
    prior=0.97,
    background=[setup_terminal_bench_2],
)

strat_terminal_results_table = support(
    [
        claim_ahe_pass1,
        claim_seed_pass1,
        claim_codex_pass1,
        claim_ace_pass1,
        claim_tfgrpo_pass1,
        claim_other_human_baselines,
    ],
    claim_terminal_results_table,
    reason=(
        "The Terminal-Bench 2 results table (@claim_terminal_results_"
        "table) is assembled from the per-method scores: AHE 77.0% "
        "(@claim_ahe_pass1), seed 69.7% (@claim_seed_pass1), Codex "
        "71.9% (@claim_codex_pass1), ACE 68.9% (@claim_ace_pass1), "
        "TF-GRPO 72.3% (@claim_tfgrpo_pass1), other human baselines "
        "47.2/62.9% (@claim_other_human_baselines). The table is "
        "deterministic given these per-method numbers."
    ),
    prior=0.97,
    background=[setup_terminal_bench_2],
)

strat_beats_human = support(
    [claim_margin_vs_codex, claim_other_human_baselines],
    claim_ahe_beats_human_baselines,
    reason=(
        "AHE beats every human-designed harness (@claim_ahe_beats_"
        "human_baselines) follows from (a) the +5.1 pp margin over "
        "Codex CLI, the strongest panel member (@claim_margin_vs_"
        "codex), and (b) the lower scores of the other two human "
        "harnesses (@claim_other_human_baselines, opencode 47.2% / "
        "terminus-2 62.9%)."
    ),
    prior=0.96,
    background=[setup_terminal_bench_2],
)

strat_beats_self_evolution = support(
    [claim_margin_vs_ace, claim_margin_vs_tfgrpo],
    claim_ahe_beats_self_evolution_baselines,
    reason=(
        "AHE beats both self-evolution baselines (@claim_ahe_beats_"
        "self_evolution_baselines) follows from the +8.1 pp ACE "
        "margin (@claim_margin_vs_ace) and the +4.7 pp TF-GRPO "
        "margin (@claim_margin_vs_tfgrpo), both starting from the "
        "same NexAU0 seed."
    ),
    prior=0.96,
    background=[setup_terminal_bench_2],
)

strat_layer_mismatch = support(
    [
        claim_ace_method,
        claim_tfgrpo_method,
        claim_factual_structure_transfers,
    ],
    claim_layer_mismatch_explanation,
    reason=(
        "The layer-mismatch explanation (@claim_layer_mismatch_"
        "explanation) follows from (a) ACE editing only the in-"
        "context playbook (@claim_ace_method), (b) TF-GRPO editing "
        "only the trajectory-distribution prior (@claim_tfgrpo_"
        "method), and (c) the factual-structure-transfers finding "
        "(@claim_factual_structure_transfers) that the gain lives "
        "in tools/middleware/memory rather than the prompt."
    ),
    prior=0.94,
)

strat_iteration_trajectory = support(
    [claim_iter2_peak, claim_iter5_peak, claim_iter6_peak, claim_iter8_peak],
    claim_iteration_trajectory,
    reason=(
        "The 4-peak iteration trajectory (@claim_iteration_trajectory) "
        "is the conjunction of the four winning rounds documented in "
        "the case studies: peak 1 at iter 2 (@claim_iter2_peak), "
        "peak 2 at iter 5 (@claim_iter5_peak), peak 3 at iter 6 "
        "(@claim_iter6_peak), peak 4 at iter 8 (@claim_iter8_peak)."
    ),
    prior=0.94,
)

strat_main_terminal_headline = support(
    [claim_margin_vs_seed],
    claim_main_terminal_headline,
    reason=(
        "The motivation-section headline (@claim_main_terminal_"
        "headline: 69.7% -> 77.0%, surpasses Codex 71.9% / ACE 68.9% "
        "/ TF-GRPO 72.3%) is anchored in the +7.3 pp seed margin "
        "(@claim_margin_vs_seed). The 'surpasses' clause restates "
        "the per-baseline margins (@claim_margin_vs_codex +5.1, "
        "@claim_margin_vs_ace +8.1, @claim_margin_vs_tfgrpo +4.7) "
        "and the human/self-evolution panel comparison "
        "(@claim_ahe_beats_human_baselines, "
        "@claim_ahe_beats_self_evolution_baselines)."
    ),
    prior=0.95,
    background=[
        claim_margin_vs_codex,
        claim_margin_vs_ace,
        claim_margin_vs_tfgrpo,
        claim_ahe_beats_human_baselines,
        claim_ahe_beats_self_evolution_baselines,
    ],
)

strat_hard_tier_exception = support(
    [claim_ahe_pass1, claim_codex_pass1, claim_memory_only_delta],
    claim_hard_tier_exception,
    reason=(
        "The Hard-tier exception (@claim_hard_tier_exception: AHE "
        "53.3% vs Codex 56.7%) is observable in the Hard-difficulty "
        "columns of AHE (@claim_ahe_pass1, 53.3%) and Codex "
        "(@claim_codex_pass1, 56.7%); the attribution to component "
        "interference rather than missing capability is supported by "
        "the memory-only ablation lift on Hard "
        "(@claim_memory_only_delta, 63.3% on Hard exceeds full AHE)."
    ),
    prior=0.94,
)

# ============================================================================
# Section 8 (s8_transfer): cross-benchmark + cross-model wiring
# ============================================================================

strat_swe_table = support(
    [claim_swe_aggregate_success, claim_swe_concentration],
    claim_swe_table_pass1,
    reason=(
        "The SWE-bench-verified pass@1 table (@claim_swe_table_"
        "pass1) is summarized by the aggregate success rate "
        "(@claim_swe_aggregate_success) and the per-repo "
        "concentration pattern (@claim_swe_concentration)."
    ),
    prior=0.94,
    background=[setup_swebench_verified],
)

strat_succ_per_mtok = support(
    [claim_swe_table_pass1, claim_swe_table_tokens],
    claim_succ_per_mtok_table,
    reason=(
        "The Succ/Mtok table (@claim_succ_per_mtok_table) is "
        "deterministic arithmetic on the pass@1 table "
        "(@claim_swe_table_pass1) and Tokens_k table "
        "(@claim_swe_table_tokens): Succ/Mtok = pass@1 * 10^3 / "
        "Tokens_k."
    ),
    prior=0.97,
    background=[setup_swebench_verified],
)

strat_swe_transfer_headline = support(
    [claim_swe_aggregate_success, claim_swe_aggregate_tokens],
    claim_swe_transfer_headline,
    reason=(
        "The SWE-bench-verified transfer headline (@claim_swe_"
        "transfer_headline: tops aggregate at 12% fewer tokens) is "
        "the conjunction of the aggregate-success result "
        "(@claim_swe_aggregate_success: 75.6% beats seed 75.2%) and "
        "the aggregate-tokens result (@claim_swe_aggregate_tokens: "
        "461k vs seed 526k = -12.4%)."
    ),
    prior=0.96,
    background=[setup_swebench_verified],
)

strat_swe_concentration = support(
    [claim_swe_table_pass1],
    claim_swe_concentration,
    reason=(
        "The per-repo concentration pattern (@claim_swe_concentration) "
        "is read off the pass@1 table (@claim_swe_table_pass1): "
        "django +1.8 pp and sphinx-doc +2.3 pp (largest, most token-"
        "expensive) lead; small-repo regressions on scikit-learn / "
        "pydata / astropy are within pass@1 variance for n < 35."
    ),
    prior=0.92,
    background=[setup_swebench_verified],
)

strat_cross_model_table = support(
    [
        claim_gpt54_med_transfer,
        claim_gpt54_xhigh_transfer,
        claim_qwen_transfer,
        claim_gemini_transfer,
        claim_deepseek_transfer,
    ],
    claim_cross_model_table,
    reason=(
        "The cross-model table (@claim_cross_model_table) is the "
        "conjunction of the five per-base measurements: GPT-5.4 med "
        "+2.3 (@claim_gpt54_med_transfer), GPT-5.4 xhigh +2.3 "
        "(@claim_gpt54_xhigh_transfer), qwen-3.6-plus +6.3 "
        "(@claim_qwen_transfer), gemini-3.1-flash-lite +5.1 "
        "(@claim_gemini_transfer), deepseek-v4-flash +10.1 "
        "(@claim_deepseek_transfer)."
    ),
    prior=0.95,
    background=[setup_models_used, setup_terminal_bench_2],
)

strat_all_five_positive = support(
    [
        claim_gpt54_med_transfer,
        claim_gpt54_xhigh_transfer,
        claim_qwen_transfer,
        claim_gemini_transfer,
        claim_deepseek_transfer,
    ],
    claim_all_five_positive,
    reason=(
        "All-five-positive (@claim_all_five_positive) is the conjunction "
        "that all five per-base measurements (@claim_gpt54_med_transfer, "
        "@claim_gpt54_xhigh_transfer, @claim_qwen_transfer, "
        "@claim_gemini_transfer, @claim_deepseek_transfer) report "
        "strictly positive deltas."
    ),
    prior=0.96,
)

strat_non_monotone_within = support(
    [
        claim_gpt54_med_transfer,
        claim_gpt54_xhigh_transfer,
        claim_main_terminal_headline,
    ],
    claim_non_monotone_within_family,
    reason=(
        "The non-monotone within-family profile (@claim_non_monotone_"
        "within_family: med +2.3 / high +7.3 / xhigh +2.3) is read off "
        "the three GPT-5.4 measurements: medium +2.3 "
        "(@claim_gpt54_med_transfer), high +7.3 "
        "(@claim_main_terminal_headline), xhigh +2.3 "
        "(@claim_gpt54_xhigh_transfer)."
    ),
    prior=0.95,
)

strat_cross_family_dominate = support(
    [
        claim_qwen_transfer,
        claim_gemini_transfer,
        claim_deepseek_transfer,
        claim_non_monotone_within_family,
    ],
    claim_cross_family_dominate,
    reason=(
        "Cross-family dominance (@claim_cross_family_dominate) "
        "follows from the three cross-family deltas all >= +5 pp "
        "(@claim_qwen_transfer +6.3, @claim_gemini_transfer +5.1, "
        "@claim_deepseek_transfer +10.1) versus the within-family "
        "deltas of +2.3 each (@claim_non_monotone_within_family)."
    ),
    prior=0.94,
)

strat_cross_family_headline = support(
    [
        claim_qwen_transfer,
        claim_gemini_transfer,
        claim_deepseek_transfer,
    ],
    claim_cross_family_headline,
    reason=(
        "The cross-family transfer headline (@claim_cross_family_"
        "headline: +5.1 to +10.1 pp on three alternate model "
        "families) is the conjunction of the three cross-family "
        "measurements (@claim_qwen_transfer, @claim_gemini_transfer, "
        "@claim_deepseek_transfer)."
    ),
    prior=0.96,
)

strat_evolved_general = support(
    [
        claim_swe_transfer_headline,
        claim_cross_family_headline,
        claim_all_five_positive,
    ],
    claim_evolved_components_general,
    reason=(
        "Evolved components encode general experience "
        "(@claim_evolved_components_general) follows from the "
        "conjunction of (a) cross-benchmark transfer to SWE-bench-"
        "verified (@claim_swe_transfer_headline), (b) cross-family "
        "transfer to three alternate model families "
        "(@claim_cross_family_headline), and (c) all five cross-"
        "model gains positive (@claim_all_five_positive)."
    ),
    prior=0.93,
)

# ============================================================================
# Section 9 (s9_ablations): component ablation table -> localization headline
# ============================================================================

strat_ablation_table = support(
    [claim_prompt_only_regression],
    claim_ablation_table,
    reason=(
        "Table 3 (@claim_ablation_table) is assembled from the "
        "per-component-swap measurements (@claim_memory_only_delta "
        "+5.6 pp, @claim_tool_only_delta +3.3 pp, "
        "@claim_middleware_only_delta +2.2 pp, "
        "@claim_prompt_only_regression -2.3 pp), the seed baseline "
        "(@claim_seed_pass1, 69.7%), and the full-AHE row "
        "(@claim_ahe_pass1, 77.0%). The prompt-only regression is "
        "the single most discriminating cell since it carries the "
        "negation of the prompt-is-main-lever foil. The other rows "
        "are referenced as background (independently anchored "
        "data)."
    ),
    prior=0.95,
    background=[
        setup_terminal_bench_2,
        claim_memory_only_delta,
        claim_tool_only_delta,
        claim_middleware_only_delta,
        claim_seed_pass1,
        claim_ahe_pass1,
    ],
)

strat_factual_structure = support(
    [claim_ablation_table],
    claim_factual_structure_transfers,
    reason=(
        "The localization claim (@claim_factual_structure_transfers) "
        "follows from reading the ablation table (@claim_ablation_"
        "table): tools +3.3 (@claim_tool_only_delta), middleware "
        "+2.2 (@claim_middleware_only_delta), memory +5.6 "
        "(@claim_memory_only_delta) all carry the gain on their own; "
        "system prompt -2.3 (@claim_prompt_only_regression) "
        "regresses. The pattern (three positive single-component "
        "lifts on factual-structure components vs the unique "
        "regression on prose-level strategy) is the localization "
        "fingerprint."
    ),
    prior=0.95,
)

strat_non_additive = support(
    [
        claim_memory_only_delta,
        claim_tool_only_delta,
        claim_middleware_only_delta,
        claim_margin_vs_seed,
    ],
    claim_non_additive_interaction,
    reason=(
        "Non-additivity (@claim_non_additive_interaction) is the "
        "arithmetic observation that the three positive single-"
        "component gains sum to +11.1 pp (@claim_memory_only_delta "
        "+5.6 + @claim_tool_only_delta +3.3 + @claim_middleware_only_"
        "delta +2.2) but full AHE achieves only +7.3 pp "
        "(@claim_margin_vs_seed); plus the Hard-tier observation "
        "that memory-only (63.3%) exceeds full AHE (53.3%) on Hard."
    ),
    prior=0.95,
)

strat_ablation_headline = support(
    [claim_factual_structure_transfers],
    claim_ablation_headline,
    reason=(
        "The motivation-section ablation headline "
        "(@claim_ablation_headline) is the abstract-level statement "
        "of the localization finding (@claim_factual_structure_"
        "transfers): tools / middleware / memory carry the gain "
        "while the prompt regresses."
    ),
    prior=0.97,
)

strat_attribution_asymmetric = support(
    [claim_evidence_driven_targeting, claim_regression_blindness],
    claim_attribution_is_asymmetric,
    reason=(
        "The asymmetric-attribution finding (@claim_attribution_is_"
        "asymmetric) is the conjunction of the evidence-driven fix "
        "side (@claim_evidence_driven_targeting, 5x random) and the "
        "blind regression side (@claim_regression_blindness, only "
        "2x random)."
    ),
    prior=0.95,
)

strat_per_round_fix = support(
    [claim_fix_attribution_quantitative, claim_iteration_trajectory],
    claim_per_round_fix_breakdown,
    reason=(
        "Per-round fix breakdown (@claim_per_round_fix_breakdown) is "
        "the round-by-round decomposition of the cross-iteration fix "
        "metrics (@claim_fix_attribution_quantitative); the per-"
        "round counts track the iteration trajectory "
        "(@claim_iteration_trajectory)."
    ),
    prior=0.93,
)

strat_regression_explains_non_monotone = support(
    [claim_regression_blindness, claim_iteration_trajectory],
    claim_regression_blindness_explains_non_monotone,
    reason=(
        "Regression blindness explains the non-monotone steps "
        "(@claim_regression_blindness_explains_non_monotone) "
        "because the agent foresees only ~11% of regressions "
        "(@claim_regression_blindness), so edits that fix one "
        "cluster sometimes introduce uncaught regressions, "
        "producing the oscillations visible in the iteration "
        "trajectory (@claim_iteration_trajectory)."
    ),
    prior=0.93,
)

# ============================================================================
# Section 10 (s10_discussion): synthesis + observation pattern
# ============================================================================

strat_obs_3pillar_pattern = support(
    [
        claim_main_terminal_headline,
        claim_swe_transfer_headline,
        claim_cross_family_headline,
        claim_factual_structure_transfers,
    ],
    claim_obs_3pillar_pattern,
    reason=(
        "The 3-element observation pattern (@claim_obs_3pillar_"
        "pattern) is the conjunction of the four headline results: "
        "main +7.3 pp (@claim_main_terminal_headline), SWE transfer "
        "(@claim_swe_transfer_headline), cross-family transfer "
        "(@claim_cross_family_headline), and component-localization "
        "(@claim_factual_structure_transfers)."
    ),
    prior=0.95,
)

strat_synthesis = support(
    [
        claim_main_terminal_headline,
        claim_swe_transfer_headline,
        claim_cross_family_headline,
        claim_ablation_headline,
        claim_ahe_three_pillars,
    ],
    claim_observability_driven_evolution_works,
    reason=(
        "The conclusion synthesis (@claim_observability_driven_"
        "evolution_works) is the conjunction of the four headline "
        "results -- main result (@claim_main_terminal_headline), "
        "SWE transfer (@claim_swe_transfer_headline), cross-family "
        "(@claim_cross_family_headline), ablation (@claim_ablation_"
        "headline) -- under the AHE 3-pillar design "
        "(@claim_ahe_three_pillars)."
    ),
    prior=0.93,
)

strat_complementary = support(
    [
        claim_observability_driven_evolution_works,
        claim_optimal_harness_model_specific,
    ],
    claim_complementary_to_model_training,
    reason=(
        "The complementary-to-model-training claim "
        "(@claim_complementary_to_model_training) follows from "
        "(a) AHE works as a harness-level evolver "
        "(@claim_observability_driven_evolution_works), and "
        "(b) the optimal harness is model-specific "
        "(@claim_optimal_harness_model_specific), so a harness "
        "evolver and base-model retraining are orthogonal axes."
    ),
    prior=0.9,
)

strat_three_contributions = support(
    [
        claim_ahe_three_pillars,
        claim_main_terminal_headline,
        claim_swe_transfer_headline,
        claim_cross_family_headline,
        claim_lim_two_evolution_limits,
    ],
    claim_three_contributions,
    reason=(
        "The three stated contributions (@claim_three_contributions) "
        "are: (i) the AHE formulation (@claim_ahe_three_pillars), "
        "(ii) the empirical results (@claim_main_terminal_headline + "
        "@claim_swe_transfer_headline + @claim_cross_family_"
        "headline), and (iii) the two analyzed limits "
        "(@claim_lim_two_evolution_limits)."
    ),
    prior=0.95,
)

strat_lim_two_evolution_limits = support(
    [claim_non_additive_interaction, claim_attribution_is_asymmetric],
    claim_lim_two_evolution_limits,
    reason=(
        "The two evolution limits (@claim_lim_two_evolution_limits) "
        "are (i) non-additive component interactions "
        "(@claim_non_additive_interaction) and (ii) regression-side "
        "attribution blindness (@claim_attribution_is_asymmetric)."
    ),
    prior=0.95,
)

# ============================================================================
# Motivation-section AHE three pillars supported by the three pillar setups
# ============================================================================

strat_three_pillars_synth = support(
    [
        claim_decoupling_realizes_observability,
        claim_distillation_realizes_experience_obs,
        claim_falsifiable_contract,
    ],
    claim_ahe_three_pillars,
    reason=(
        "The 3-pillar AHE description (@claim_ahe_three_pillars) is "
        "the conjunction of the three pillar realizations: "
        "Pillar 1 -- component observability "
        "(@claim_decoupling_realizes_observability), "
        "Pillar 2 -- experience observability "
        "(@claim_distillation_realizes_experience_obs), "
        "Pillar 3 -- decision observability "
        "(@claim_falsifiable_contract)."
    ),
    prior=0.96,
)

strat_observability_bottleneck_supports_3pillar = support(
    [
        claim_observability_bottleneck,
        claim_ahe_three_pillars,
    ],
    claim_pred_3pillar_explains,
    reason=(
        "The 3-pillar prediction (@claim_pred_3pillar_explains) "
        "follows from the central insight that observability is the "
        "bottleneck (@claim_observability_bottleneck) plus the "
        "specific 3-pillar realization (@claim_ahe_three_pillars) "
        "addressing the three obstacles. The prediction's specific "
        "fingerprint -- (a) main result + (b) cross-target transfer "
        "+ (c) factual-structure localization -- discriminates from "
        "trivial alternatives."
    ),
    prior=0.93,
)

strat_alt_predicts_subsets = support(
    [claim_alt_manual_only],
    claim_pred_alt_explains,
    reason=(
        "The alternative-predicts-subsets claim "
        "(@claim_pred_alt_explains) is anchored in the foil "
        "(@claim_alt_manual_only) but expanded to three concrete "
        "trivial alternatives (bigger LM, more iterations, "
        "benchmark overfitting). Each predicts only a strict "
        "subset of the observed pattern, and the overfitting "
        "alternative actually predicts the *opposite* of the "
        "transfer observations."
    ),
    prior=0.55,
)

# ============================================================================
# Background wiring: observability-bottleneck claim from the 3 obstacles
# ============================================================================

strat_two_obstacles_motivation = support(
    [claim_existing_evolution_partial],
    claim_two_structural_obstacles,
    reason=(
        "The two-obstacle synthesis (@claim_two_structural_obstacles, "
        "for joint multi-component evolution: unstructured "
        "trajectories + tight component coupling) is a refinement of "
        "the three obstacles (@setup_three_obstacles, action space + "
        "trajectories + attribution) viewed under the partial-"
        "evolution literature observation (@claim_existing_evolution_"
        "partial) -- the literature handles single-component "
        "optimization but stalls on these two obstacles when scaling "
        "to multi-component."
    ),
    prior=0.92,
    background=[setup_three_obstacles],
)

strat_observability_insight = support(
    [claim_two_structural_obstacles],
    claim_observability_bottleneck,
    reason=(
        "The observability-is-bottleneck insight "
        "(@claim_observability_bottleneck) is justified by the "
        "structural obstacles (@claim_two_structural_obstacles, "
        "@setup_three_obstacles): each obstacle is essentially an "
        "observability problem -- the action space (lack of "
        "structural observability), the trajectories (lack of "
        "experience observability), and attribution (lack of "
        "decision observability). The 3-pillar pattern is therefore "
        "what observability infrastructure looks like for harness "
        "evolution."
    ),
    prior=0.9,
    background=[setup_three_obstacles],
)

strat_manual_practice = support(
    [
        claim_optimal_harness_model_specific,
        claim_existing_evolution_partial,
    ],
    claim_manual_harness_practice,
    reason=(
        "Manual practice (@claim_manual_harness_practice) is the "
        "consequence of (a) the model-specificity of optimal "
        "harnesses (@claim_optimal_harness_model_specific) -- each "
        "new base model needs a re-tuned harness -- and (b) the "
        "absence of mature joint-evolution methods "
        "(@claim_existing_evolution_partial)."
    ),
    prior=0.9,
    background=[setup_harness_definition],
)

# ============================================================================
# INDUCTION 1: per-iteration AHE peaks support 'AHE outer loop is a
# stable harness optimizer'
# ============================================================================

claim_law_ahe_stable_optimizer = claim(
    "**Population law: the AHE outer loop is a stable harness "
    "optimizer on Terminal-Bench 2.** Across the 10-iteration AHE "
    "campaign, multiple distinct iterations produce documented "
    "winning rounds with mechanistically-attributable component "
    "edits. The law is supported by four named peaks (iter 2, 5, 6, "
    "8) at distinct constraint levels (prompt, tool, middleware) "
    "[@Lin2026AHE, Sec. C].",
    title="Law: AHE outer loop is a stable harness optimizer (4 peaks at distinct iterations + constraint levels)",
)

s_law_predicts_iter2 = support(
    [claim_law_ahe_stable_optimizer],
    claim_iter2_peak,
    reason=(
        "Generative direction: the law (@claim_law_ahe_stable_"
        "optimizer) predicts that AHE produces winning-round edits "
        "with mechanism-traceable attribution; the iter-2 peak "
        "(@claim_iter2_peak) is the contract-first / shell-timeout "
        "realization at the prompt + tool level."
    ),
    prior=0.9,
)

s_law_predicts_iter5 = support(
    [claim_law_ahe_stable_optimizer],
    claim_iter5_peak,
    reason=(
        "Generative direction: the law (@claim_law_ahe_stable_"
        "optimizer) predicts winning-round edits at multiple "
        "constraint levels; the iter-5 peak (@claim_iter5_peak) is "
        "the publish-state realization at prompt + tool level."
    ),
    prior=0.9,
)

s_law_predicts_iter6 = support(
    [claim_law_ahe_stable_optimizer],
    claim_iter6_peak,
    reason=(
        "Generative direction: the law (@claim_law_ahe_stable_"
        "optimizer) predicts winning-round edits at multiple "
        "constraint levels; the iter-6 peak (@claim_iter6_peak) is "
        "the protected-entrypoint + execution-risk-middleware "
        "realization at tool + middleware level."
    ),
    prior=0.9,
)

s_law_predicts_iter8 = support(
    [claim_law_ahe_stable_optimizer],
    claim_iter8_peak,
    reason=(
        "Generative direction: the law (@claim_law_ahe_stable_"
        "optimizer) predicts winning-round edits across the "
        "trajectory, including improving prior edits; the iter-8 "
        "peak (@claim_iter8_peak) is the hard-block + FRAMEWORK-"
        "reminder realization at tool + middleware level, the "
        "76.97% high-water mark."
    ),
    prior=0.9,
)

ind_iter25 = induction(
    s_law_predicts_iter2,
    s_law_predicts_iter5,
    law=claim_law_ahe_stable_optimizer,
    reason=(
        "Iter-2 (prompt + tool, contract-first) and iter-5 "
        "(prompt + tool, publish-state) are independent successful "
        "rounds at different iterations targeting different failure "
        "patterns. Both confirm the law that AHE produces "
        "mechanism-attributable winning rounds."
    ),
)

ind_iter256 = induction(
    ind_iter25,
    s_law_predicts_iter6,
    law=claim_law_ahe_stable_optimizer,
    reason=(
        "Iter-6 adds a third independent peak at a different "
        "constraint level (tool + middleware: protected entrypoints "
        "+ ExecutionRiskHintsMiddleware). The middleware-level "
        "evidence is qualitatively new because it shows AHE can "
        "produce edits at any of the seven component levels, not "
        "just prompt/tool."
    ),
)

ind_iter2568 = induction(
    ind_iter256,
    s_law_predicts_iter8,
    law=claim_law_ahe_stable_optimizer,
    reason=(
        "Iter-8 adds a fourth independent peak that is "
        "qualitatively different: it improves prior edits "
        "(hardening the iter-5 guard, salience-promoting iter-6 "
        "middleware reminders) rather than introducing new "
        "patterns. This shows AHE iterates productively over its "
        "own prior decisions, not just adding new rules. The "
        "iteration produces the run's high-water mark."
    ),
)

# ============================================================================
# INDUCTION 2: per-base-model-family transfer supports 'frozen AHE
# transfers across base-model families'
# ============================================================================

claim_law_cross_family_transfer = claim(
    "**Population law: the frozen AHE harness transfers across base-"
    "model families with consistently positive gain on Terminal-"
    "Bench 2.** The law is supported by five independent base-model "
    "evaluations: GPT-5.4 medium, GPT-5.4 xhigh, gemini-3.1-flash-"
    "lite-preview, qwen-3.6-plus, deepseek-v4-flash "
    "[@Lin2026AHE, Sec. 4.3].",
    title="Law: frozen AHE transfers cross-family (5 alternate bases, all positive)",
)

s_xfam_predicts_qwen = support(
    [claim_law_cross_family_transfer],
    claim_qwen_transfer,
    reason=(
        "Generative direction: the cross-family law "
        "(@claim_law_cross_family_transfer) predicts a positive "
        "gain on each cross-family base; qwen-3.6-plus +6.3 "
        "(@claim_qwen_transfer) realizes this for the Qwen family."
    ),
    prior=0.92,
)

s_xfam_predicts_gemini = support(
    [claim_law_cross_family_transfer],
    claim_gemini_transfer,
    reason=(
        "Generative direction: the law predicts a positive cross-"
        "family gain; gemini-3.1-flash-lite-preview +5.1 "
        "(@claim_gemini_transfer) realizes this for the Gemini "
        "family."
    ),
    prior=0.92,
)

s_xfam_predicts_deepseek = support(
    [claim_law_cross_family_transfer],
    claim_deepseek_transfer,
    reason=(
        "Generative direction: the law predicts a positive cross-"
        "family gain; deepseek-v4-flash +10.1 "
        "(@claim_deepseek_transfer) realizes this for the DeepSeek "
        "family, the largest cross-family gain."
    ),
    prior=0.92,
)

ind_xfam_qg = induction(
    s_xfam_predicts_qwen,
    s_xfam_predicts_gemini,
    law=claim_law_cross_family_transfer,
    reason=(
        "Qwen and Gemini are independent base-model families with "
        "different architectures, training regimes, and capability "
        "ceilings. Both yield positive gains (+6.3 and +5.1 pp), "
        "jointly inducing the cross-family law."
    ),
)

ind_xfam_qgd = induction(
    ind_xfam_qg,
    s_xfam_predicts_deepseek,
    law=claim_law_cross_family_transfer,
    reason=(
        "DeepSeek-v4-flash adds a third independent family with "
        "the largest cross-family gain (+10.1 pp). The three "
        "confirmations span Qwen / Gemini / DeepSeek with gains "
        "+5.1 to +10.1 pp, robustifying the cross-family law and "
        "confirming the 'distance from saturation' interpretation."
    ),
)

# ============================================================================
# CENTRAL ABDUCTION: 3-pillar design vs trivial alternatives
# ============================================================================

# Hypothesis: 3-pillar observability design causes the gain
# Alternative: bigger LM / more iterations / benchmark overfitting
# Discriminating observation: 3-fold conjunction (main result + transfer +
# factual-structure localization)

s_h_explains = support(
    [claim_pred_3pillar_explains],
    claim_obs_3pillar_pattern,
    reason=(
        "Under the 3-pillar hypothesis (@claim_pred_3pillar_explains), "
        "the conjunction (main result + cross-target transfer + "
        "factual-structure localization) is exactly the predicted "
        "fingerprint: component observability gives the action space, "
        "experience observability gives the signal, decision "
        "observability gives the rollback, and the gain lives in "
        "factual structure because that is what the substrate "
        "exposes for editing. The observed pattern (@claim_obs_"
        "3pillar_pattern) is exactly this fingerprint."
    ),
    prior=0.94,
)

s_alt_explains = support(
    [claim_pred_alt_explains],
    claim_obs_3pillar_pattern,
    reason=(
        "Under the trivial alternatives (@claim_pred_alt_explains), "
        "each predicts only a strict subset of the observed pattern: "
        "bigger LM / more iterations cannot explain the cross-family "
        "transfer (no LM access on the alternate bases at evolution "
        "time), and benchmark overfitting predicts the OPPOSITE of "
        "the SWE-bench-verified +0.4 pp transfer and the OPPOSITE of "
        "the all-five-positive cross-family pattern. The trivial "
        "alternatives cannot jointly explain the conjunction."
    ),
    prior=0.2,
)

comp_3pillar_vs_trivial = compare(
    claim_pred_3pillar_explains,
    claim_pred_alt_explains,
    claim_obs_3pillar_pattern,
    reason=(
        "The 3-pillar prediction (@claim_pred_3pillar_explains) "
        "uniquely explains the 3-element conjunction: main result + "
        "cross-target transfer + factual-structure localization. "
        "The trivial-alternatives prediction (@claim_pred_alt_"
        "explains) explains only subsets and predicts the opposite "
        "of the transfer measurements. The discriminating "
        "observation (@claim_obs_3pillar_pattern) is the ablation "
        "table localizing gains to factual structure (tools / "
        "middleware / memory) -- which trivial alternatives cannot "
        "explain at all. The discrimination is decisive."
    ),
    prior=0.95,
)

abd_3pillar_explains_pattern = abduction(
    s_h_explains,
    s_alt_explains,
    comp_3pillar_vs_trivial,
    reason=(
        "Both hypotheses attempt to explain the same observation "
        "pattern: main result + cross-benchmark transfer + cross-"
        "family transfer + factual-structure component-localization. "
        "The 3-pillar hypothesis (@claim_pred_3pillar_explains) "
        "predicts all four observations as a coherent fingerprint. "
        "The trivial alternatives (@claim_pred_alt_explains) -- "
        "bigger LM, more iterations, benchmark-specific overfitting "
        "-- explain only subsets and contradict the transfer "
        "measurements. The conjunction of (a) +5.1 to +10.1 pp on "
        "alternate model families *not seen during evolution* and "
        "(b) the system-prompt-only regression in the ablation "
        "discriminates strongly in favor of the 3-pillar account."
    ),
)

# ============================================================================
# CONTRADICTION 1: manual-only foil vs autonomous AHE demonstration
# ============================================================================

strat_alt_manual_only = support(
    [
        claim_manual_harness_practice,
        claim_optimal_harness_model_specific,
    ],
    claim_alt_manual_only,
    reason=(
        "The manual-only foil (@claim_alt_manual_only) is the "
        "literal extension of the prevailing manual practice "
        "(@claim_manual_harness_practice) plus the model-"
        "specificity argument (@claim_optimal_harness_model_"
        "specific) -- under the foil, model-specificity is taken "
        "as proof that only humans can make the per-model trade-"
        "offs."
    ),
    prior=0.85,
)

contra_manual_vs_ahe = contradiction(
    claim_alt_manual_only,
    claim_main_terminal_headline,
    reason=(
        "The manual-only foil (@claim_alt_manual_only: harness "
        "engineering must remain manual; autonomous evolution "
        "cannot stably converge or beat human harnesses) and the "
        "main result (@claim_main_terminal_headline: 10 iterations "
        "of autonomous AHE reach 77.0% pass@1, surpassing every "
        "human-designed harness on the panel) cannot both be true. "
        "If autonomous evolution cannot beat humans, the +5.1 pp "
        "AHE-vs-Codex margin must be wrong; conversely, if the "
        "margin holds, the foil must be wrong."
    ),
    prior=0.95,
)

# ============================================================================
# CONTRADICTION 2: prompt-is-main-lever vs ablation result
# ============================================================================

strat_alt_prompt_main_lever = support(
    [
        claim_prompt_instruction_methods,
        claim_self_critique_methods,
    ],
    claim_alt_prompt_is_main_lever,
    reason=(
        "The prompt-is-main-lever foil (@claim_alt_prompt_is_main_"
        "lever) is the literal claim implicit in the prompt-only "
        "optimizer literature (@claim_prompt_instruction_methods, "
        "DSPy / ACE / TF-GRPO / MIPRO / GEPA) and the self-critique "
        "literature (@claim_self_critique_methods, Self-Refine / "
        "Reflexion / Critiq), all of which target the prompt "
        "surface as their primary editable lever."
    ),
    prior=0.7,
)

contra_prompt_vs_ablation = contradiction(
    claim_alt_prompt_is_main_lever,
    claim_factual_structure_transfers,
    reason=(
        "The prompt-is-main-lever foil (@claim_alt_prompt_is_main_"
        "lever: prompt is primary; tool/middleware/memory are "
        "second-order) and the factual-structure-localization "
        "finding (@claim_factual_structure_transfers: tools "
        "+3.3, middleware +2.2, memory +5.6 pp; prompt -2.3 pp) "
        "cannot both be true. The system-prompt-only swap actively "
        "regressing while each of the other three components "
        "carries the gain alone is incompatible with prompt being "
        "the main lever."
    ),
    prior=0.95,
)

# ============================================================================
# Setup-anchor strategies for orphan prevention
# ============================================================================

strat_pillars_anchor_setting = support(
    [claim_design_principle_observability],
    claim_attribute_before_distill,
    reason=(
        "The attribute-before-distill ordering "
        "(@claim_attribute_before_distill) is a consequence of the "
        "outer loop's phase ordering (@setup_ahe_outer_loop, Phase 3 "
        "before Phase 4) plus the design principle that every phase "
        "must be observable (@claim_design_principle_observability). "
        "The role agents (@setup_role_agents) -- in particular the "
        "separation between Code Agent rollouts and Evolve Agent "
        "manifests -- make this ordering load-bearing."
    ),
    prior=0.93,
    background=[setup_ahe_outer_loop, setup_role_agents],
)

strat_explore_seeds = support(
    [claim_ahe_minimal_human_prior],
    claim_explore_agent_seed_skills,
    reason=(
        "The one-shot explore agent (@claim_explore_agent_seed_"
        "skills) runs in parallel with iteration 1 of the outer loop "
        "(@setup_ahe_outer_loop) starting from the minimal seed "
        "(@setup_seed_nexau0). The minimal-human-prior design "
        "(@claim_ahe_minimal_human_prior) requires that its skills "
        "receive no special protection so they must earn their "
        "place in subsequent iterations."
    ),
    prior=0.9,
    background=[setup_ahe_outer_loop, setup_seed_nexau0],
)

strat_iteration_traj_supported_by_loop = support(
    [claim_design_principle_observability],
    claim_law_ahe_stable_optimizer,
    reason=(
        "The 'AHE is a stable harness optimizer' law "
        "(@claim_law_ahe_stable_optimizer) is supported in the "
        "structural sense by (a) the outer-loop algorithm "
        "(@setup_ahe_outer_loop), (b) the k=2 rollout discipline "
        "(@setup_k_rollouts), and (c) the shared-model role-agent "
        "setup (@setup_models_used) ensuring gains are attributable "
        "to harness rather than analyzer or editor capability. The "
        "design principle that every phase must be observable "
        "(@claim_design_principle_observability) is what makes the "
        "loop optimize stably rather than degenerate to trial-and-"
        "error."
    ),
    prior=0.85,
    background=[
        setup_ahe_outer_loop,
        setup_k_rollouts,
        setup_models_used,
        setup_role_agents,
        setup_runtime_infrastructure,
    ],
)

# ============================================================================
# Setup-anchored fallback strategies for orphan prevention
# ============================================================================

strat_harness_central_observed = support(
    [
        claim_evaluation_horizons,
        claim_harness_engineering_definition,
    ],
    claim_harness_central_to_perf,
    reason=(
        "The harness-is-central premise (@claim_harness_central_to_"
        "perf) follows from (a) harness engineering as a research "
        "practice with documented impact "
        "(@claim_harness_engineering_definition) and (b) the broad "
        "coverage of coding-agent benchmarks "
        "(@claim_evaluation_horizons) where harness differences are "
        "measurable."
    ),
    prior=0.9,
    background=[setup_coding_agent_regime],
)

strat_optimal_model_specific = support(
    [claim_evaluation_horizons],
    claim_optimal_harness_model_specific,
    reason=(
        "The model-specificity of optimal harnesses "
        "(@claim_optimal_harness_model_specific) is observable in "
        "the practitioner literature: each new base model release "
        "ships its own preferred harness configuration; this is "
        "consistent with the broad benchmark coverage of "
        "@claim_evaluation_horizons showing harnesses tuned per "
        "model and per benchmark."
    ),
    prior=0.85,
)

strat_existing_evolution = support(
    [
        claim_self_critique_methods,
        claim_prompt_instruction_methods,
        claim_program_structure_methods,
        claim_meta_harness,
    ],
    claim_existing_evolution_partial,
    reason=(
        "The state-of-literature claim (@claim_existing_evolution_"
        "partial) summarizes the three optimizer dimensions: "
        "self-critique (@claim_self_critique_methods), "
        "prompt-instruction (@claim_prompt_instruction_methods), "
        "and program-structure (@claim_program_structure_methods); "
        "Meta-Harness (@claim_meta_harness) is the only attempt at "
        "joint multi-component optimization."
    ),
    prior=0.92,
)

strat_combinatorial_whole = support(
    [claim_existing_evolution_partial],
    claim_ahe_combinatorial_whole,
    reason=(
        "AHE's combinatorial-whole distinction "
        "(@claim_ahe_combinatorial_whole) follows from (a) the "
        "single-surface orientation of existing optimizers "
        "(@claim_existing_evolution_partial) versus (b) the seven-"
        "component editable substrate of AHE "
        "(@setup_seven_component_types)."
    ),
    prior=0.95,
    background=[setup_seven_component_types],
)

strat_minimal_human_prior_dist = support(
    [claim_minimal_seed_attribution],
    claim_ahe_minimal_human_prior,
    reason=(
        "The minimal-human-prior distinction "
        "(@claim_ahe_minimal_human_prior) restates the seed "
        "definition (@setup_seed_nexau0) and its attribution "
        "implication (@claim_minimal_seed_attribution): a bash-only "
        "seed leaves methodology for the optimizer to discover and "
        "keeps every gain attributable to the loop rather than the "
        "seed."
    ),
    prior=0.95,
    background=[setup_seed_nexau0],
)


# Failure-surface claims connect to the per-component ablation deltas
strat_memory_surface = support(
    [claim_memory_only_delta],
    claim_memory_failure_surface,
    reason=(
        "The memory failure-surface description "
        "(@claim_memory_failure_surface, 12 boundary-case lessons) "
        "is the qualitative correlate of the memory-only ablation "
        "result (@claim_memory_only_delta): the +11.6 pp Hard-tier "
        "lift is exactly what factual contract-pattern lessons "
        "predict, while the Easy regression is what re-verification "
        "overhead predicts."
    ),
    prior=0.85,
)

strat_tool_surface = support(
    [claim_tool_only_delta],
    claim_tool_failure_surface,
    reason=(
        "The tools failure-surface description "
        "(@claim_tool_failure_surface, contract surfacing + 1364-"
        "line shell) is the qualitative correlate of the tool-only "
        "ablation result (@claim_tool_only_delta): +9.1 pp on "
        "Medium (matching the surface) and -5.0 pp on Hard "
        "(early-closing publish guard)."
    ),
    prior=0.85,
)

strat_middleware_surface = support(
    [claim_middleware_only_delta],
    claim_middleware_failure_surface,
    reason=(
        "The middleware failure-surface description "
        "(@claim_middleware_failure_surface, finish-hook closure "
        "check) is the qualitative correlate of the middleware-only "
        "ablation result (@claim_middleware_only_delta): +12.5 pp "
        "on Easy (closure check clears them) and -1.7 pp on Hard "
        "(turn-count inflation)."
    ),
    prior=0.85,
)

strat_prompt_surface = support(
    [claim_prompt_only_regression, claim_factual_structure_transfers],
    claim_prompt_failure_surface,
    reason=(
        "The prompt failure-surface description "
        "(@claim_prompt_failure_surface, 79 lines of advisory "
        "discipline) is the qualitative explanation of why the "
        "prompt-only swap regresses (@claim_prompt_only_regression): "
        "without execution-time backing from the other three "
        "components, advisory text becomes ignored, consistent with "
        "the factual-structure localization finding "
        "(@claim_factual_structure_transfers)."
    ),
    prior=0.88,
)

# ============================================================================
# Limitations connecting back to discussion
# ============================================================================

strat_lim_benchmark_anchor = support(
    [claim_evolved_components_general],
    claim_lim_benchmark_scope,
    reason=(
        "The benchmark-scope limitation "
        "(@claim_lim_benchmark_scope) is anchored in the two "
        "evaluation surfaces used: Terminal-Bench 2 "
        "(@setup_terminal_bench_2) and SWE-bench-verified "
        "(@setup_swebench_verified). Beyond these, broader "
        "languages and human-in-the-loop workflows are untested by "
        "construction. Even though evolved components encode "
        "general experience (@claim_evolved_components_general) on "
        "the evaluated surfaces, the scope of 'general' is bounded "
        "to those surfaces."
    ),
    prior=0.95,
    background=[setup_terminal_bench_2, setup_swebench_verified],
)

strat_lim_operating_point = support(
    [claim_non_monotone_within_family],
    claim_lim_operating_point,
    reason=(
        "The operating-point limitation "
        "(@claim_lim_operating_point) is anchored in the within-"
        "family non-monotonicity (@claim_non_monotone_within_"
        "family, GPT-5.4 medium +2.3 / high +7.3 / xhigh +2.3) "
        "and the model lineup (@setup_models_used) showing the "
        "step budget and timeout fitted to GPT-5.4 high."
    ),
    prior=0.95,
    background=[setup_models_used],
)

strat_codex_human_anchor = support(
    [claim_codex_human_baseline],
    claim_codex_pass1,
    reason=(
        "The Codex CLI 71.9% measurement (@claim_codex_pass1) is "
        "the panel-position realization of the human-designed "
        "baseline (@claim_codex_human_baseline) on Terminal-Bench "
        "2: Codex CLI is the strongest of the three human-designed "
        "harnesses on the comparison panel."
    ),
    prior=0.94,
    background=[setup_terminal_bench_2],
)

strat_eval_infra = support(
    [claim_eval_infrastructure],
    claim_design_principle_observability,
    reason=(
        "AHE's design principle that every loop phase must produce "
        "structured artifacts (@claim_design_principle_observability) "
        "is grounded in the broader reproducible-execution "
        "infrastructure tradition (@claim_eval_infrastructure, "
        "SWE-Gym / R2E-Gym / SWE-Hub). Without reproducible, "
        "traceable, verifiable execution as a substrate, layered "
        "observability could not be built."
    ),
    prior=0.85,
)

strat_lim_self_mod = support(
    [claim_controllability_blocks_shortcuts],
    claim_lim_self_modification_governance,
    reason=(
        "The self-modification-governance limitation "
        "(@claim_lim_self_modification_governance) is anchored in "
        "the existing constraint set (@setup_two_hard_constraints, "
        "@setup_attribution_check) which is non-trivial "
        "(@claim_controllability_blocks_shortcuts) but incomplete: "
        "the read-only restrictions cover infrastructure shortcuts "
        "but do not provide misuse prevention, and the rollback "
        "granularity is file-level rather than semantic."
    ),
    prior=0.9,
    background=[setup_two_hard_constraints, setup_attribution_check],
)


__all__ = [
    "claim_law_ahe_stable_optimizer",
    "claim_law_cross_family_transfer",
    "s_law_predicts_iter2",
    "s_law_predicts_iter5",
    "s_law_predicts_iter6",
    "s_law_predicts_iter8",
    "ind_iter25",
    "ind_iter256",
    "ind_iter2568",
    "s_xfam_predicts_qwen",
    "s_xfam_predicts_gemini",
    "s_xfam_predicts_deepseek",
    "ind_xfam_qg",
    "ind_xfam_qgd",
    "s_h_explains",
    "s_alt_explains",
    "comp_3pillar_vs_trivial",
    "abd_3pillar_explains_pattern",
    "strat_alt_manual_only",
    "contra_manual_vs_ahe",
    "strat_alt_prompt_main_lever",
    "contra_prompt_vs_ablation",
    "strat_decoupling_from_components",
    "strat_action_space_from_git_history",
    "strat_minimal_seed_supports_attribution",
    "strat_token_compression_from_setup",
    "strat_distillation_realizes_pillar2",
    "strat_per_task_pass_fail_grounding",
    "strat_partial_pass_from_k",
    "strat_falsifiable_contract",
    "strat_controllability_blocks",
    "strat_decision_solves_o3",
    "strat_evidence_driven_from_metrics",
    "strat_regression_blindness_from_metrics",
    "strat_margin_vs_seed",
    "strat_margin_vs_codex",
    "strat_margin_vs_ace",
    "strat_margin_vs_tfgrpo",
    "strat_terminal_results_table",
    "strat_beats_human",
    "strat_beats_self_evolution",
    "strat_layer_mismatch",
    "strat_iteration_trajectory",
    "strat_main_terminal_headline",
    "strat_hard_tier_exception",
    "strat_swe_table",
    "strat_succ_per_mtok",
    "strat_swe_transfer_headline",
    "strat_swe_concentration",
    "strat_cross_model_table",
    "strat_all_five_positive",
    "strat_non_monotone_within",
    "strat_cross_family_dominate",
    "strat_cross_family_headline",
    "strat_evolved_general",
    "strat_ablation_table",
    "strat_factual_structure",
    "strat_non_additive",
    "strat_ablation_headline",
    "strat_attribution_asymmetric",
    "strat_per_round_fix",
    "strat_regression_explains_non_monotone",
    "strat_obs_3pillar_pattern",
    "strat_synthesis",
    "strat_complementary",
    "strat_three_contributions",
    "strat_lim_two_evolution_limits",
    "strat_three_pillars_synth",
    "strat_observability_bottleneck_supports_3pillar",
    "strat_alt_predicts_subsets",
    "strat_two_obstacles_motivation",
    "strat_observability_insight",
    "strat_manual_practice",
    "strat_pillars_anchor_setting",
    "strat_explore_seeds",
    "strat_iteration_traj_supported_by_loop",
    "strat_harness_central_observed",
    "strat_optimal_model_specific",
    "strat_existing_evolution",
    "strat_combinatorial_whole",
    "strat_minimal_human_prior_dist",
    "strat_component_type_table_anchor",
    "strat_memory_surface",
    "strat_tool_surface",
    "strat_middleware_surface",
    "strat_prompt_surface",
    "strat_lim_benchmark_anchor",
    "strat_lim_operating_point",
    "strat_lim_self_mod",
    "strat_codex_human_anchor",
    "strat_eval_infra",
]
