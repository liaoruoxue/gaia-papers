"""Pass 2 wiring: strategies, abductions, inductions, contradictions for the
CRAFT formalization.

Conventions
-----------

* `support` -- soft deduction with author-specified prior. The default for
  "premises imply conclusion" with empirical or interpretive uncertainty.
* `deduction` -- rigid logical entailment. Used for the formal Theorem 5.1
  step from {SSA definition + assumptions} to {policy is not locally
  optimal}.
* `compare` -- two predictions vs an observation; sub-strategy of `abduction`.
* `abduction` -- inference to best explanation. Used once: the central
  hypothesis "hidden-representation alignment is the mechanism behind
  CRAFT's empirical gain", versus the alternative "compute / data / prompts
  explain the gain". The discriminating observation is cross-model
  consistency + the catastrophic LCLR ablation.
* `induction` -- chained binary composite. Used once: the population law
  "CRAFT consistently outperforms SOTA defenses across LRM families and
  benchmarks" inducted over (i) DeepSeek-R1-Distill-Llama-8B and (ii)
  Qwen3-4B-Thinking model families.
* `contradiction` -- two contradictions:
    (i) the prevailing assumption "output-level alignment is sufficient for
        jailbreak robustness" vs the empirical demonstration that
        hidden-space alignment is needed (Tables 1, 3);
    (ii) "vanilla GRPO with output-only reward produces robustly aligned
         policies" vs Theorem 5.1 ruling out SSA only with R_cons.
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
    claim_contribution_empirical,
    claim_contribution_framework,
    claim_contribution_method,
    claim_contribution_theory,
    claim_craft_proposal,
    claim_implication_latent_alignment,
    claim_latent_separation_observation,
    claim_lrm_safety_underexplored,
    claim_output_level_insufficient,
    claim_ssa_phenomenon,
    setup_alignment_baselines,
    setup_jailbreak_threat_model,
    setup_lrm_regime,
)
from .s2_related_work import (
    claim_guard_models,
    claim_inference_time_defenses,
    claim_ipo_method,
    claim_lrm_attack_surface_growing,
    claim_lrm_strong_reasoning,
    claim_other_training_methods,
    claim_prior_work_gap,
    claim_realsafe_method,
    claim_reasoningshield_method,
    claim_safechain_method,
    claim_safekey_method,
    claim_star_method,
    setup_defense_taxonomy,
    setup_lrm_taxonomy,
)
from .s3_setup import (
    claim_rethink_at_boundary,
    claim_safe_unsafe_separation,
    claim_separation_model_agnostic,
    claim_separation_motivates_design,
    setup_probe_protocol,
    setup_projection_head,
    setup_prototypes,
    setup_reasoning_trace_notation,
    setup_semantic_labels,
)
from .s4_method import (
    claim_craft_framework_contribution,
    claim_craft_overall_pipeline,
    claim_lclr_design_rationale,
    claim_rcons_targets_ssa,
    claim_three_rewards_address_distinct_objectives,
    setup_cal_loss,
    setup_consistency_reward,
    setup_inst_loss,
    setup_lclr_total_objective,
    setup_latent_semantic_reward,
    setup_proto_loss,
    setup_r2l_objective_form,
    setup_textual_safety_reward,
    setup_two_phase_pipeline,
)
from .s5_theory import (
    claim_assumption_continuity,
    claim_assumption_fixed_evaluator,
    claim_assumption_grpo_local_opt,
    claim_assumptions_mild,
    claim_epsilon_depends_on_variance_and_entropy,
    claim_ssa_definition,
    claim_theorem_5p1_statement,
    claim_theorem_implies_grpo_alone_insufficient,
    claim_theorem_rcons_essential,
    setup_theorem_setup,
)
from .s6_main_results import (
    claim_craft_best_average_safety,
    claim_craft_preserves_reasoning,
    claim_craft_qwen_best_overall,
    claim_craft_r1distill_competitive,
    claim_craft_vs_baselines_summary,
    claim_table1_full,
    claim_table2_full,
    setup_compute_environment,
    setup_evaluation_protocol,
    setup_metrics,
)
from .s7_avg_improvements import (
    claim_advanced_jailbreaks_robustness,
    claim_cross_model_consistent_gain,
    claim_per_model_safety_breakdown,
    claim_reasoning_perf_4p7,
    claim_reasoning_safety_79p0,
    claim_response_safety_87p7,
)
from .s8_ablations import (
    claim_ablation_full_table,
    claim_ablation_validates_design,
    claim_all_components_essential,
    claim_lclr_removal_largest_drop,
    claim_rcons_removal_283,
    claim_rls_removal_271,
)
from .s9_discussion_limitations import (
    claim_foil_grpo_alone_sufficient,
    claim_foil_output_alignment_sufficient,
    claim_future_adaptive_signals,
    claim_impact_intent,
    claim_lim_fixed_evaluator,
    claim_lim_misuse_potential,
    claim_lim_pca_visualization_evidence,
    claim_lim_training_budget,
    claim_lim_two_models,
    claim_obs_cross_model_plus_ablations,
    claim_pred_alt_compute,
    claim_pred_latent_explains,
    claim_synthesis_main,
)


# ===========================================================================
# Section 1 (Motivation): SSA phenomenon and the case for latent alignment
# ===========================================================================

strat_ssa_from_lrm_attack_surface = support(
    [claim_lrm_attack_surface_growing, claim_lrm_safety_underexplored],
    claim_ssa_phenomenon,
    reason=(
        "The SSA phenomenon claim (@claim_ssa_phenomenon) is supported "
        "by two related observations: long reasoning traces expand the "
        "jailbreak attack surface (@claim_lrm_attack_surface_growing) "
        "and LRM safety is comparatively underexplored "
        "(@claim_lrm_safety_underexplored). Together these imply that "
        "even pipeline-aligned LRMs can leak harmful content in "
        "intermediate reasoning while presenting a safe final answer."
    ),
    prior=0.9,
    background=[setup_lrm_regime, setup_alignment_baselines],
)

strat_output_insufficient_from_ssa = support(
    [claim_ssa_phenomenon],
    claim_output_level_insufficient,
    reason=(
        "Given that SSA is empirically attested (@claim_ssa_phenomenon), "
        "and that standard output-level alignment pipelines (RLHF, DPO, "
        "SFT) are precisely the methods used to align the models that "
        "exhibit SSA, it follows that output-level alignment "
        "(@claim_output_level_insufficient) is *insufficient* on its "
        "own to prevent SSA: were it sufficient, SSA would not be "
        "observed in pipeline-aligned models."
    ),
    prior=0.92,
    background=[setup_alignment_baselines, setup_jailbreak_threat_model],
)

# ===========================================================================
# Section 2 (related work): identifying the gap
# ===========================================================================

strat_prior_work_gap_from_baselines = support(
    [
        claim_safechain_method,
        claim_realsafe_method,
        claim_star_method,
        claim_safekey_method,
        claim_ipo_method,
        claim_reasoningshield_method,
        claim_other_training_methods,
        claim_inference_time_defenses,
        claim_guard_models,
    ],
    claim_prior_work_gap,
    reason=(
        "The prior-work gap (@claim_prior_work_gap) is the conjunction "
        "of: (i) all six directly-evaluated training-time baselines "
        "(@claim_safechain_method, @claim_realsafe_method, "
        "@claim_star_method, @claim_safekey_method, @claim_ipo_method, "
        "@claim_reasoningshield_method) operate over textual reasoning "
        "traces; (ii) other training-time methods "
        "(@claim_other_training_methods) similarly operate at the text "
        "level; (iii) inference-time defenses "
        "(@claim_inference_time_defenses) are reactive rather than "
        "training-time aligning; (iv) guard models (@claim_guard_models) "
        "are post-hoc detectors. The conjunction implies no method "
        "directly aligns the *latent geometry* of reasoning traces "
        "during training -- which is the gap CRAFT addresses."
    ),
    prior=0.93,
    background=[setup_defense_taxonomy, setup_lrm_taxonomy],
)

# ===========================================================================
# Section 3 (setup): the latent separation observation motivates the design
# ===========================================================================

strat_separation_obs_to_motivation = support(
    [
        claim_safe_unsafe_separation,
        claim_rethink_at_boundary,
        claim_separation_model_agnostic,
    ],
    claim_separation_motivates_design,
    reason=(
        "The design-motivation claim (@claim_separation_motivates_design) "
        "follows from three Section-3 observations: safe and unsafe "
        "traces are clearly separated in latent space "
        "(@claim_safe_unsafe_separation); rethink traces concentrate at "
        "the boundary (@claim_rethink_at_boundary); and the pattern is "
        "model-agnostic across two LRMs (@claim_separation_model_agnostic). "
        "Together they show the latent space already encodes safety "
        "structure that contrastive + RL alignment can exploit."
    ),
    prior=0.92,
    background=[setup_probe_protocol, setup_projection_head, setup_prototypes],
)

strat_separation_to_motivation_observation = support(
    [claim_safe_unsafe_separation, claim_separation_model_agnostic],
    claim_latent_separation_observation,
    reason=(
        "The motivation-section latent-separation observation "
        "(@claim_latent_separation_observation) is the abstract-level "
        "statement of the Section-3 empirical observations: clear "
        "separation in PCA (@claim_safe_unsafe_separation) and "
        "model-agnostic structure (@claim_separation_model_agnostic). "
        "Identical empirical content; this strategy connects the "
        "abstract-level claim to its in-paper realization."
    ),
    prior=0.96,
    background=[setup_reasoning_trace_notation, setup_semantic_labels],
)

# ===========================================================================
# Section 4 (method): wire LCLR and R2L design claims
# ===========================================================================

strat_pipeline_from_phases = support(
    [claim_lclr_design_rationale, claim_three_rewards_address_distinct_objectives],
    claim_craft_overall_pipeline,
    reason=(
        "The end-to-end pipeline (@claim_craft_overall_pipeline) is the "
        "composition of the LCLR phase (@claim_lclr_design_rationale -- "
        "three contrastive losses) followed by the R2L phase "
        "(@claim_three_rewards_address_distinct_objectives -- three "
        "GRPO rewards). The pipeline diagram in Fig. 3 sequentially "
        "applies LCLR then R2L; both phases are essential for the "
        "framework to function."
    ),
    prior=0.93,
    background=[
        setup_two_phase_pipeline,
        setup_lclr_total_objective,
        setup_r2l_objective_form,
    ],
)

strat_framework_from_pipeline = support(
    [claim_craft_overall_pipeline, claim_craft_proposal],
    claim_craft_framework_contribution,
    reason=(
        "The framework-contribution claim (@claim_craft_framework_contribution) "
        "follows from the overall pipeline (@claim_craft_overall_pipeline) "
        "instantiating CRAFT's headline proposal "
        "(@claim_craft_proposal): integrating contrastive learning "
        "(LCLR) with reinforcement learning (R2L) over latent "
        "representations is precisely what the pipeline does."
    ),
    prior=0.94,
)

strat_contribution_method_from_pipeline = support(
    [claim_craft_overall_pipeline, claim_lclr_design_rationale],
    claim_contribution_method,
    reason=(
        "Contribution 3 (@claim_contribution_method, methodology) is "
        "supported by the pipeline (@claim_craft_overall_pipeline) "
        "instantiating each component, and the LCLR design rationale "
        "(@claim_lclr_design_rationale) explaining why each contrastive "
        "loss is needed. The latent-RL objective with "
        "$R_{ls}, R_{cons}$ enforces alignment at both intermediate "
        "and output levels."
    ),
    prior=0.93,
    background=[
        setup_proto_loss,
        setup_inst_loss,
        setup_cal_loss,
        setup_latent_semantic_reward,
        setup_consistency_reward,
        setup_textual_safety_reward,
    ],
)

strat_contribution_framework_from_overall = support(
    [claim_craft_framework_contribution],
    claim_contribution_framework,
    reason=(
        "Contribution 1 (@claim_contribution_framework, framework) is "
        "the abstract-level statement of CRAFT's framework integration "
        "(@claim_craft_framework_contribution). Identical content; "
        "this strategy connects the abstract claim to its in-paper "
        "realization."
    ),
    prior=0.96,
)

strat_rcons_targets_ssa_from_design = support(
    [claim_three_rewards_address_distinct_objectives],
    claim_rcons_targets_ssa,
    reason=(
        "The claim that $R_{cons}$ specifically targets SSA "
        "(@claim_rcons_targets_ssa) follows from the three-reward "
        "design (@claim_three_rewards_address_distinct_objectives): "
        "$R_{cons}$ is precisely the term that punishes "
        "$|p_z - p_y|$, which is by definition the SSA failure "
        "signature ($p_y \\approx 1$ but $|p_z - p_y| \\geq \\delta$)."
    ),
    prior=0.95,
    background=[setup_consistency_reward],
)

# ===========================================================================
# Section 5 (theory): Theorem 5.1
# ===========================================================================

# The theorem is a deductive derivation: under the SSA definition + the three
# assumptions, the policy cannot be locally optimal. Inside the proof there
# is a perturbation argument; once granted Assumption 5.1's local
# controllability, the conclusion follows deterministically via the
# perturbation contradicting the local-optimum assumption.
strat_theorem_5p1_deduction = deduction(
    [
        claim_ssa_definition,
        claim_assumption_continuity,
        claim_assumption_grpo_local_opt,
        claim_assumption_fixed_evaluator,
        claim_rcons_targets_ssa,
    ],
    claim_theorem_5p1_statement,
    background=[setup_theorem_setup, setup_consistency_reward],
)

strat_rcons_essential_from_theorem = support(
    [claim_theorem_5p1_statement, claim_rcons_targets_ssa],
    claim_theorem_rcons_essential,
    reason=(
        "The 'theorem essentially relies on $R_{cons}$' claim "
        "(@claim_theorem_rcons_essential) is the natural reading of "
        "the proof structure: the SSA-reducing perturbation only "
        "*strictly* improves the total reward through the "
        "$R_{cons}$ term (@claim_rcons_targets_ssa). Without "
        "$R_{cons}$, the perturbation would be reward-neutral and "
        "the local-optimality contradiction would not arise."
    ),
    prior=0.95,
)

strat_grpo_alone_insufficient_from_theorem = support(
    [claim_theorem_rcons_essential],
    claim_theorem_implies_grpo_alone_insufficient,
    reason=(
        "If $R_{cons}$ is essential to the theorem "
        "(@claim_theorem_rcons_essential), then GRPO without it "
        "(i.e., output-only reward) cannot use the same argument to "
        "rule out SSA. Therefore @claim_theorem_implies_grpo_alone_"
        "insufficient: vanilla GRPO with only $R_{txt}$ does not "
        "enjoy the SSA-elimination guarantee."
    ),
    prior=0.95,
)

strat_contribution_theory_from_thm = support(
    [claim_theorem_5p1_statement],
    claim_contribution_theory,
    reason=(
        "Contribution 2 (@claim_contribution_theory, theory) is the "
        "abstract-level statement of Theorem 5.1 "
        "(@claim_theorem_5p1_statement). Identical content; this "
        "connects the abstract claim to its in-paper realization."
    ),
    prior=0.96,
)

# ===========================================================================
# Section 6 (main results): Tables 1 & 2 -> headline numbers
# ===========================================================================

strat_qwen_best_avg_from_table1 = support(
    [claim_table1_full],
    claim_craft_qwen_best_overall,
    reason=(
        "The Qwen3-4B-Thinking best-average claim "
        "(@claim_craft_qwen_best_overall, CRAFT 0.117) is the "
        "row-arithmetic on the Qwen3-4B-Thinking section of Table 1 "
        "(@claim_table1_full): CRAFT achieves the lowest avg column "
        "across the eight methods evaluated."
    ),
    prior=0.97,
    background=[setup_evaluation_protocol, setup_metrics],
)

strat_r1distill_avg_from_table1 = support(
    [claim_table1_full],
    claim_craft_r1distill_competitive,
    reason=(
        "The R1-Distill-Llama-8B best-average claim "
        "(@claim_craft_r1distill_competitive, CRAFT 0.074) is "
        "row-arithmetic on the R1-Distill-Llama-8B section of "
        "Table 1 (@claim_table1_full): CRAFT achieves the lowest "
        "avg column."
    ),
    prior=0.97,
    background=[setup_evaluation_protocol, setup_metrics],
)

strat_best_avg_safety_from_table1 = support(
    [
        claim_craft_qwen_best_overall,
        claim_craft_r1distill_competitive,
    ],
    claim_craft_best_average_safety,
    reason=(
        "The cross-model best-average claim "
        "(@claim_craft_best_average_safety, CRAFT 0.096 cross-LRM "
        "avg) is the mean of the two per-model averages "
        "(@claim_craft_qwen_best_overall = 0.117 and "
        "@claim_craft_r1distill_competitive = 0.074): "
        "(0.117 + 0.074)/2 = 0.0955 ~ 0.096."
    ),
    prior=0.97,
)

strat_vs_baselines_from_table1 = support(
    [claim_table1_full],
    claim_craft_vs_baselines_summary,
    reason=(
        "The 'CRAFT +5.0% reasoning / +22.1% response vs strongest "
        "baselines' claim (@claim_craft_vs_baselines_summary) is "
        "row-by-row arithmetic on Table 1 (@claim_table1_full): "
        "comparing CRAFT to IPO/SafeKey on reasoning and response "
        "axes; the per-cell relative gaps average to those two "
        "headlines."
    ),
    prior=0.95,
    background=[setup_metrics],
)

strat_preserves_reasoning_from_table2 = support(
    [claim_table2_full],
    claim_craft_preserves_reasoning,
    reason=(
        "The reasoning-preservation claim (@claim_craft_preserves_reasoning, "
        "+4.7% avg Pass@1 over base) is row-arithmetic on Table 2 "
        "(@claim_table2_full): R1-Distill goes 0.437 -> 0.468 (+7.1%); "
        "Qwen3 goes 0.569 -> 0.585 (+2.8%); average +4.7%."
    ),
    prior=0.96,
    background=[setup_evaluation_protocol],
)

# ===========================================================================
# Section 6 (avg improvements): the 79.0% / 87.7% headline numbers
# ===========================================================================

strat_79p0_from_table1 = support(
    [claim_table1_full],
    claim_reasoning_safety_79p0,
    reason=(
        "The 79.0% reasoning-safety headline "
        "(@claim_reasoning_safety_79p0) is computed from Table 1 "
        "(@claim_table1_full): for each (model, benchmark) pair, "
        "compute (base - CRAFT) / base on the reasoning column; "
        "average across the four pairs yields ~79.0%."
    ),
    prior=0.96,
    background=[setup_metrics],
)

strat_87p7_from_table1 = support(
    [claim_table1_full],
    claim_response_safety_87p7,
    reason=(
        "The 87.7% response-safety headline "
        "(@claim_response_safety_87p7) is computed from Table 1 "
        "(@claim_table1_full) on the response column: average "
        "(base - CRAFT) / base across the four (model, benchmark) "
        "pairs yields ~87.7%."
    ),
    prior=0.96,
    background=[setup_metrics],
)

strat_4p7_from_table2 = support(
    [claim_table2_full],
    claim_reasoning_perf_4p7,
    reason=(
        "The +4.7% Pass@1 headline (@claim_reasoning_perf_4p7) is "
        "computed from Table 2 (@claim_table2_full) avg columns: "
        "(0.468 - 0.437)/0.437 = +7.1% on R1-Distill, "
        "(0.585 - 0.569)/0.569 = +2.8% on Qwen3; average = +4.7%."
    ),
    prior=0.96,
    background=[setup_metrics],
)

strat_per_model_breakdown_from_79_87 = support(
    [claim_reasoning_safety_79p0, claim_response_safety_87p7],
    claim_per_model_safety_breakdown,
    reason=(
        "The per-model safety breakdown "
        "(@claim_per_model_safety_breakdown) is the within-model "
        "decomposition of the cross-model 79.0% reasoning "
        "(@claim_reasoning_safety_79p0) and 87.7% response "
        "(@claim_response_safety_87p7) headlines. Per-model the "
        "improvements are 81.7%/76.1% reasoning and 94.1%/80.5% "
        "response on R1-Distill / Qwen3 respectively."
    ),
    prior=0.95,
)

strat_cross_model_consistent = support(
    [claim_per_model_safety_breakdown, claim_craft_preserves_reasoning],
    claim_cross_model_consistent_gain,
    reason=(
        "The cross-model consistency claim "
        "(@claim_cross_model_consistent_gain) follows from the "
        "per-model breakdown (@claim_per_model_safety_breakdown -- "
        "both LRMs see safety gains in the 76-94% range) and the "
        "preservation of reasoning across both LRMs "
        "(@claim_craft_preserves_reasoning -- both improve over "
        "base). Two LRM families with different architectures and "
        "training data both confirm the law."
    ),
    prior=0.92,
)

strat_advanced_jailbreaks_consistency = support(
    [claim_advanced_jailbreaks_robustness],
    claim_cross_model_consistent_gain,
    reason=(
        "The robustness under advanced jailbreaks "
        "(@claim_advanced_jailbreaks_robustness, GPTFuzzer + AutoDAN) "
        "further reinforces the cross-model consistency claim "
        "(@claim_cross_model_consistent_gain): the gains are not "
        "specific to one attack distribution -- they generalize to "
        "adversarial-prompt-optimization attacks too."
    ),
    prior=0.9,
)

# ===========================================================================
# Section 6 (ablations): per-component contributions
# ===========================================================================

strat_lclr_largest_drop_from_table3 = support(
    [claim_ablation_full_table],
    claim_lclr_removal_largest_drop,
    reason=(
        "The 'LCLR removal is most catastrophic' claim "
        "(@claim_lclr_removal_largest_drop) is row-arithmetic on "
        "Table 3 (@claim_ablation_full_table): full CRAFT 0.082, "
        "w/o LCLR 0.423; the +0.341 absolute / +416% relative gap "
        "is the largest among the three ablations."
    ),
    prior=0.97,
)

strat_rcons_drop_from_table3 = support(
    [claim_ablation_full_table],
    claim_rcons_removal_283,
    reason=(
        "The R_cons-removal claim (@claim_rcons_removal_283, "
        "+0.289 absolute increase) is row-arithmetic on Table 3 "
        "(@claim_ablation_full_table): 0.082 -> 0.371 = +0.289 "
        "absolute, +352% relative."
    ),
    prior=0.97,
)

strat_rls_drop_from_table3 = support(
    [claim_ablation_full_table],
    claim_rls_removal_271,
    reason=(
        "The R_ls-removal claim (@claim_rls_removal_271, +0.271 "
        "absolute) is row-arithmetic on Table 3 "
        "(@claim_ablation_full_table): 0.082 -> 0.353."
    ),
    prior=0.97,
)

strat_components_essential_from_ablations = support(
    [
        claim_lclr_removal_largest_drop,
        claim_rcons_removal_283,
        claim_rls_removal_271,
    ],
    claim_all_components_essential,
    reason=(
        "All three components being essential "
        "(@claim_all_components_essential) is the conjunction of "
        "the three per-component degradations: removing LCLR "
        "(@claim_lclr_removal_largest_drop), R_cons "
        "(@claim_rcons_removal_283), or R_ls "
        "(@claim_rls_removal_271) each causes a >27% absolute "
        "score increase. None is redundant."
    ),
    prior=0.95,
)

strat_ablation_validates_design = support(
    [
        claim_all_components_essential,
        claim_lclr_design_rationale,
        claim_three_rewards_address_distinct_objectives,
    ],
    claim_ablation_validates_design,
    reason=(
        "The empirical-validates-design synthesis "
        "(@claim_ablation_validates_design) follows from: "
        "(i) the ablations show all three components essential "
        "(@claim_all_components_essential); (ii) the LCLR design "
        "rationale (@claim_lclr_design_rationale) predicted each "
        "loss is necessary; (iii) the three R2L rewards target "
        "distinct objectives (@claim_three_rewards_address_distinct_"
        "objectives). Theory + design + empirics agree."
    ),
    prior=0.93,
)

# ===========================================================================
# Headline empirical claim (motivation 4) is supported by the headlines
# ===========================================================================

strat_contribution_empirical_from_headlines = support(
    [
        claim_reasoning_safety_79p0,
        claim_response_safety_87p7,
        claim_reasoning_perf_4p7,
        claim_cross_model_consistent_gain,
    ],
    claim_contribution_empirical,
    reason=(
        "Contribution 4 (@claim_contribution_empirical, empirical) "
        "is the conjunction of the three headline numbers "
        "(@claim_reasoning_safety_79p0, @claim_response_safety_87p7, "
        "@claim_reasoning_perf_4p7) and the cross-model consistency "
        "(@claim_cross_model_consistent_gain)."
    ),
    prior=0.95,
)

# ===========================================================================
# Synthesis (Section 7)
# ===========================================================================

strat_synthesis_main = support(
    [
        claim_contribution_framework,
        claim_contribution_theory,
        claim_contribution_method,
        claim_contribution_empirical,
    ],
    claim_synthesis_main,
    reason=(
        "The Section 7 synthesis (@claim_synthesis_main) is the "
        "joint statement of the four contributions: framework "
        "(@claim_contribution_framework), theory "
        "(@claim_contribution_theory), method (@claim_contribution_method), "
        "and empirical (@claim_contribution_empirical). All four "
        "support the conclusion that latent-space CRAFT eliminates "
        "SSA both empirically and theoretically."
    ),
    prior=0.94,
)

strat_implication_from_synthesis = support(
    [
        claim_synthesis_main,
        claim_theorem_5p1_statement,
        claim_separation_motivates_design,
        claim_all_components_essential,
    ],
    claim_implication_latent_alignment,
    reason=(
        "The motivation-section implication (@claim_implication_"
        "latent_alignment, latent-space alignment is feasible + "
        "necessary) is the conjunction of: synthesis "
        "(@claim_synthesis_main), the theorem ruling out SSA at "
        "local optima (@claim_theorem_5p1_statement), the latent "
        "structure being amenable (@claim_separation_motivates_design), "
        "and the ablation showing all components essential "
        "(@claim_all_components_essential)."
    ),
    prior=0.93,
)

# ===========================================================================
# INDUCTION: cross-LRM, cross-benchmark population law
# ===========================================================================

claim_population_law = claim(
    "**Population law: CRAFT consistently outperforms state-of-the-art "
    "reasoning-safety defenses (best or co-best average jailbreak "
    "score) across multiple LRM families and multiple safety "
    "benchmarks.** This is the paper's central empirical "
    "generalization, supported by the Qwen3-4B-Thinking result "
    "(CRAFT lowest avg) and the DeepSeek-R1-Distill-Llama-8B result "
    "(CRAFT lowest avg) on JailbreakBench + StrongReject "
    "[@Luo2026CRAFT, Sec. 6].",
    title="Population law: CRAFT consistently outperforms SOTA defenses across LRMs + benchmarks",
)

# Generative direction: the law predicts each per-LRM headline result.
s_law_predicts_qwen = support(
    [claim_population_law],
    claim_craft_qwen_best_overall,
    reason=(
        "Generative direction: the population law (@claim_population_law) "
        "predicts that CRAFT achieves the lowest average jailbreak "
        "score on Qwen3-4B-Thinking; the empirical 0.117 avg "
        "(@claim_craft_qwen_best_overall) is the realization for "
        "the Qwen LRM family."
    ),
    prior=0.92,
)

s_law_predicts_r1distill = support(
    [claim_population_law],
    claim_craft_r1distill_competitive,
    reason=(
        "Generative direction: the population law (@claim_population_law) "
        "predicts that CRAFT achieves the lowest average jailbreak "
        "score on DeepSeek-R1-Distill-Llama-8B; the empirical 0.074 "
        "avg (@claim_craft_r1distill_competitive) is the realization "
        "for the R1-Distill LRM family."
    ),
    prior=0.92,
)

induction_population_law = induction(
    s_law_predicts_qwen,
    s_law_predicts_r1distill,
    law=claim_population_law,
    reason=(
        "The two LRM families test the law in *independent* regimes: "
        "Qwen3-4B-Thinking (4B parameters, Qwen3 architecture, "
        "@claim_craft_qwen_best_overall) and DeepSeek-R1-Distill-"
        "Llama-8B (8B parameters, Llama-3 architecture distilled "
        "from R1, @claim_craft_r1distill_competitive). Both confirm "
        "the law -- CRAFT achieves the lowest avg jailbreak score -- "
        "which jointly induces the population law to higher "
        "confidence than either single observation alone would "
        "warrant."
    ),
)

# ===========================================================================
# CENTRAL ABDUCTION: latent-alignment H vs compute / data Alt
# ===========================================================================

# Hypothesis: the hidden-representation alignment mechanism explains the gain
# (@claim_pred_latent_explains)
# Alternative: compute / SFT data / better prompts explain the gain
# (@claim_pred_alt_compute)
# Discriminating observation: cross-LRM consistency + catastrophic
# LCLR ablation (@claim_obs_cross_model_plus_ablations)

s_latent_supports_obs = support(
    [claim_pred_latent_explains],
    claim_obs_cross_model_plus_ablations,
    reason=(
        "Under the latent-alignment hypothesis "
        "(@claim_pred_latent_explains), we expect (i) cross-LRM "
        "consistency on a fixed compute budget (the algorithmic "
        "mechanism is the same across LRMs), and (ii) catastrophic "
        "failure when the latent component (LCLR) is removed (the "
        "algorithm collapses without its latent-shaping primitive). "
        "Both are observed (@claim_obs_cross_model_plus_ablations). "
        "The latent-alignment hypothesis predicts both signals."
    ),
    prior=0.95,
)

s_alt_supports_obs = support(
    [claim_pred_alt_compute],
    claim_obs_cross_model_plus_ablations,
    reason=(
        "Under the compute / data alternative "
        "(@claim_pred_alt_compute), the cross-LRM consistency would "
        "be at most weakly predicted (compute / data effects are "
        "model-specific), and the catastrophic LCLR ablation would "
        "be unexplained -- removing one specific algorithmic "
        "component does not alter the compute consumed nor the "
        "training data. The alternative cannot easily explain the "
        "joint signal (@claim_obs_cross_model_plus_ablations); its "
        "explanatory power for this observation is low."
    ),
    prior=0.25,
)

comp_latent_vs_alt = compare(
    claim_pred_latent_explains,
    claim_pred_alt_compute,
    claim_obs_cross_model_plus_ablations,
    reason=(
        "The latent-alignment prediction (@claim_pred_latent_explains) "
        "expects both cross-LRM consistency and catastrophic LCLR "
        "ablation. The compute / data alternative "
        "(@claim_pred_alt_compute) does not predict either: "
        "compute / data effects vary across LRMs (so cross-LRM "
        "consistency is weakly predicted at best), and removing one "
        "algorithmic component does not alter the compute budget "
        "(so the catastrophic ablation is unexplained). The joint "
        "observation (@claim_obs_cross_model_plus_ablations) "
        "discriminates strongly in favor of the latent-alignment "
        "hypothesis."
    ),
    prior=0.95,
)

abd_latent_explains = abduction(
    s_latent_supports_obs,
    s_alt_supports_obs,
    comp_latent_vs_alt,
    reason=(
        "Both hypotheses attempt to explain the same empirical "
        "pattern: CRAFT's substantial safety gain across LRMs while "
        "preserving reasoning ability. The latent-alignment "
        "hypothesis (@claim_pred_latent_explains) predicts the gain "
        "comes from the explicit hidden-state objectives -- and "
        "specifically predicts both cross-LRM consistency and "
        "ablation-fragility on the latent component. The compute / "
        "data alternative (@claim_pred_alt_compute) predicts neither "
        "of these signatures crisply. The discriminating "
        "observation (@claim_obs_cross_model_plus_ablations) is "
        "consistent with the hypothesis and awkward for the "
        "alternative."
    ),
)

# ===========================================================================
# CONTRADICTION 1: output-level alignment sufficiency vs hidden-space need
# ===========================================================================

strat_foil_output_alignment_from_baselines = support(
    [
        claim_ipo_method,
        claim_safekey_method,
        claim_other_training_methods,
    ],
    claim_foil_output_alignment_sufficient,
    reason=(
        "The output-level-sufficiency foil "
        "(@claim_foil_output_alignment_sufficient) is the implicit "
        "position taken by methods that operate solely over textual "
        "reasoning traces / output tokens: IPO (@claim_ipo_method), "
        "SafeKey (@claim_safekey_method), and the other "
        "training-time methods (@claim_other_training_methods). "
        "These methods presume that aligning at the textual / "
        "output level suffices."
    ),
    prior=0.85,
)

contra_output_vs_hidden = contradiction(
    claim_foil_output_alignment_sufficient,
    claim_lclr_removal_largest_drop,
    reason=(
        "The output-level-sufficiency foil "
        "(@claim_foil_output_alignment_sufficient: aligning at the "
        "output level is sufficient) and the LCLR-removal "
        "catastrophic-degradation finding "
        "(@claim_lclr_removal_largest_drop: removing the "
        "latent-space component pushes the average jailbreak score "
        "from 0.082 to 0.423, a 416% relative degradation) cannot "
        "both be true. If output-level alignment were sufficient, "
        "removing LCLR (which leaves $R_{txt}$ intact -- still an "
        "output-level reward) should not catastrophically hurt "
        "safety. The +0.341 absolute degradation when only the "
        "*latent* component is removed directly refutes the foil."
    ),
    prior=0.95,
)

# ===========================================================================
# CONTRADICTION 2: GRPO-alone-suffices vs Theorem 5.1
# ===========================================================================

strat_foil_grpo_alone_from_motivation = support(
    [claim_foil_output_alignment_sufficient],
    claim_foil_grpo_alone_sufficient,
    reason=(
        "The 'GRPO with output-only reward suffices' foil "
        "(@claim_foil_grpo_alone_sufficient) is a specialization "
        "of the broader output-level-sufficiency position "
        "(@claim_foil_output_alignment_sufficient) to the GRPO "
        "algorithm specifically: GRPO + output-only reward should "
        "produce robustly aligned policies."
    ),
    prior=0.85,
)

contra_grpo_alone_vs_theorem = contradiction(
    claim_foil_grpo_alone_sufficient,
    claim_theorem_implies_grpo_alone_insufficient,
    reason=(
        "The GRPO-alone-suffices foil "
        "(@claim_foil_grpo_alone_sufficient: GRPO with output-only "
        "reward produces robustly aligned policies) and the "
        "theorem's implication "
        "(@claim_theorem_implies_grpo_alone_insufficient: GRPO with "
        "output-only reward does not rule out SSA at local optima) "
        "cannot both be true. The theorem's perturbation argument "
        "shows that without $R_{cons}$ in $R_{total}$, locally-"
        "optimal policies *can* exhibit SSA, contradicting the "
        "robustness claim."
    ),
    prior=0.95,
)

# ===========================================================================
# Other supporting strategies (settings/limitations -> implications)
# ===========================================================================

strat_lim_two_models_caveat = support(
    [claim_lim_two_models, claim_lim_training_budget],
    claim_synthesis_main,
    reason=(
        "The two-model limitation (@claim_lim_two_models) and "
        "training-budget limitation (@claim_lim_training_budget) "
        "qualify but do not invalidate the Section 7 synthesis "
        "(@claim_synthesis_main): the strong empirical claims hold "
        "for the two evaluated open-weight LRMs, with extrapolation "
        "to larger / closed-source LRMs an open question."
    ),
    prior=0.85,
)

strat_fixed_evaluator_to_future = support(
    [claim_lim_fixed_evaluator],
    claim_future_adaptive_signals,
    reason=(
        "The fixed-evaluator limitation "
        "(@claim_lim_fixed_evaluator) directly motivates the "
        "future-work direction (@claim_future_adaptive_signals): "
        "adaptive safety signals are explicitly framed as a "
        "mitigation for the StrongReject + GPT-4o reliance."
    ),
    prior=0.92,
)

strat_pca_caveat_to_separation = support(
    [claim_lim_pca_visualization_evidence, claim_safe_unsafe_separation],
    claim_separation_model_agnostic,
    reason=(
        "The PCA caveat (@claim_lim_pca_visualization_evidence) "
        "qualifies but does not invalidate the model-agnostic "
        "separation claim (@claim_separation_model_agnostic): the "
        "qualitative separation pattern "
        "(@claim_safe_unsafe_separation) is observed via 2D PCA on "
        "two models; while higher-dimensional structure may differ, "
        "the consistency across two models is preserved at the PCA "
        "level."
    ),
    prior=0.85,
)

strat_misuse_to_intent = support(
    [claim_lim_misuse_potential],
    claim_impact_intent,
    reason=(
        "The dual-use limitation (@claim_lim_misuse_potential) is "
        "what the impact statement (@claim_impact_intent) "
        "acknowledges. The defensive-intent framing is precisely "
        "the authors' response to the dual-use concern."
    ),
    prior=0.9,
)

# ===========================================================================
# CRAFT proposal (motivation) -> framework realization (s4)
# ===========================================================================

strat_craft_proposal_from_observations = support(
    [
        claim_ssa_phenomenon,
        claim_output_level_insufficient,
        claim_separation_motivates_design,
    ],
    claim_craft_proposal,
    reason=(
        "The CRAFT proposal (@claim_craft_proposal) is motivated by "
        "(i) the SSA phenomenon (@claim_ssa_phenomenon), (ii) the "
        "insufficiency of output-level alignment "
        "(@claim_output_level_insufficient), and (iii) the latent "
        "separation that makes hidden-state alignment well-posed "
        "(@claim_separation_motivates_design). Together these "
        "warrant a framework that aligns at the latent level."
    ),
    prior=0.93,
)

# Contribution 1 framework already wired upstream. Tie LCLR design rationale
# to method contribution.
strat_lclr_to_method = support(
    [claim_lclr_design_rationale],
    claim_contribution_method,
    reason=(
        "The LCLR design rationale (@claim_lclr_design_rationale) "
        "is part of Contribution 3 (@claim_contribution_method): "
        "the methodology contribution explicitly includes the "
        "contrastive latent-representation learning scheme."
    ),
    prior=0.92,
    background=[setup_lclr_total_objective],
)

# Wire LRM landscape -> SSA-related claims
strat_lrm_strong_to_attack_surface = support(
    [claim_lrm_strong_reasoning],
    claim_lrm_attack_surface_growing,
    reason=(
        "Stronger LRM reasoning (@claim_lrm_strong_reasoning) "
        "enables longer / more capable chains-of-thought, which "
        "in turn expands the attack surface "
        "(@claim_lrm_attack_surface_growing) -- adversaries have "
        "more reasoning steps to exploit / optimize."
    ),
    prior=0.85,
    background=[setup_lrm_taxonomy],
)

# Theorem assumptions are mild
strat_assumptions_mild_to_theorem = support(
    [
        claim_assumption_continuity,
        claim_assumption_grpo_local_opt,
        claim_assumption_fixed_evaluator,
    ],
    claim_assumptions_mild,
    reason=(
        "The 'assumptions are mild' claim (@claim_assumptions_mild) "
        "is a meta-claim about the three assumptions: continuity / "
        "Lipschitz (@claim_assumption_continuity, holds for any "
        "finite-weight network), GRPO local optimality "
        "(@claim_assumption_grpo_local_opt, standard convergence "
        "assumption), and fixed evaluator "
        "(@claim_assumption_fixed_evaluator, standard practice in "
        "alignment training)."
    ),
    prior=0.9,
)

# Epsilon caveat is a property of the theorem
strat_epsilon_from_theorem = support(
    [claim_theorem_5p1_statement],
    claim_epsilon_depends_on_variance_and_entropy,
    reason=(
        "The epsilon-depends-on-variance-and-entropy caveat "
        "(@claim_epsilon_depends_on_variance_and_entropy) is part "
        "of the theorem statement (@claim_theorem_5p1_statement) "
        "itself -- it explains why the bound is non-zero and why "
        "empirical SSA reduction is substantial but not perfect."
    ),
    prior=0.95,
)

# ===========================================================================
# Adv-jailbreaks robustness wired through to the empirical contribution
# ===========================================================================

strat_advanced_to_empirical_contribution = support(
    [claim_advanced_jailbreaks_robustness],
    claim_contribution_empirical,
    reason=(
        "The advanced-jailbreak robustness "
        "(@claim_advanced_jailbreaks_robustness) further supports "
        "the empirical contribution (@claim_contribution_empirical): "
        "the safety gains generalize to GPTFuzzer / AutoDAN attacks, "
        "indicating CRAFT is robust beyond the in-distribution "
        "JailbreakBench / StrongReject evaluation."
    ),
    prior=0.9,
)


__all__ = [
    "claim_population_law",
    "s_law_predicts_qwen",
    "s_law_predicts_r1distill",
    "induction_population_law",
    "strat_ssa_from_lrm_attack_surface",
    "strat_output_insufficient_from_ssa",
    "strat_prior_work_gap_from_baselines",
    "strat_separation_obs_to_motivation",
    "strat_separation_to_motivation_observation",
    "strat_pipeline_from_phases",
    "strat_framework_from_pipeline",
    "strat_contribution_method_from_pipeline",
    "strat_contribution_framework_from_overall",
    "strat_rcons_targets_ssa_from_design",
    "strat_theorem_5p1_deduction",
    "strat_rcons_essential_from_theorem",
    "strat_grpo_alone_insufficient_from_theorem",
    "strat_contribution_theory_from_thm",
    "strat_qwen_best_avg_from_table1",
    "strat_r1distill_avg_from_table1",
    "strat_best_avg_safety_from_table1",
    "strat_vs_baselines_from_table1",
    "strat_preserves_reasoning_from_table2",
    "strat_79p0_from_table1",
    "strat_87p7_from_table1",
    "strat_4p7_from_table2",
    "strat_per_model_breakdown_from_79_87",
    "strat_cross_model_consistent",
    "strat_advanced_jailbreaks_consistency",
    "strat_lclr_largest_drop_from_table3",
    "strat_rcons_drop_from_table3",
    "strat_rls_drop_from_table3",
    "strat_components_essential_from_ablations",
    "strat_ablation_validates_design",
    "strat_contribution_empirical_from_headlines",
    "strat_synthesis_main",
    "strat_implication_from_synthesis",
    "s_latent_supports_obs",
    "s_alt_supports_obs",
    "comp_latent_vs_alt",
    "abd_latent_explains",
    "strat_foil_output_alignment_from_baselines",
    "contra_output_vs_hidden",
    "strat_foil_grpo_alone_from_motivation",
    "contra_grpo_alone_vs_theorem",
    "strat_lim_two_models_caveat",
    "strat_fixed_evaluator_to_future",
    "strat_pca_caveat_to_separation",
    "strat_misuse_to_intent",
    "strat_craft_proposal_from_observations",
    "strat_lclr_to_method",
    "strat_lrm_strong_to_attack_surface",
    "strat_assumptions_mild_to_theorem",
    "strat_epsilon_from_theorem",
    "strat_advanced_to_empirical_contribution",
]
