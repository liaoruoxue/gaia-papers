"""Pass 2 wiring: strategies, abductions, inductions, contradictions
linking the propositions extracted in motivation + s2-s7 into the
reasoning graph.
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

# ---------------------------------------------------------------------------
# Imports from per-section modules
# ---------------------------------------------------------------------------

from .motivation import (
    setup_mas_llm_regime,
    setup_artifact_refinement_task,
    claim_explicit_orchestration_paradigm,
    claim_orchestration_overhead_scales_poorly,
    claim_pressure_field_proposal,
    claim_foundation_models_enable,
    claim_headline_solve_rates,
    claim_headline_easy_problems,
    claim_headline_only_strategy_scales,
    claim_headline_decay_ablation,
    claim_headline_convergence_theorem,
    claim_fm_mas_mutually_enabling,
    claim_four_contributions,
)
from .s2_related_work import (
    claim_organizational_paradigms_assign_roles,
    claim_pressure_field_eliminates_three_dimensions,
    claim_malone_crowston_shared_resource,
    claim_gpgp_message_complexity,
    claim_pressure_field_o1_overhead,
    claim_sharedplans_joint_intentions_cost,
    claim_pressure_alignment_replaces_intention_alignment,
    setup_serugendo_four_mechanisms,
    setup_dewolf_holvoet_criteria,
    claim_pressure_field_instantiates_four_mechanisms,
    claim_pressure_field_satisfies_dewolf_holvoet,
    claim_fm_capability_1_domain_general_patches,
    claim_fm_capability_2_instruction_following,
    claim_fm_capability_3_zero_shot_quality,
    claim_fm_capability_4_in_context_pheromone,
    claim_fm_capability_5_generative_flexibility,
    claim_fm_enables_summary,
    claim_mas_llm_baselines_share_pattern,
    claim_explicit_orchestration_scaling_failures,
    setup_grasse_stigmergy,
    setup_aco_mechanisms,
    claim_pressure_field_inherits_aco,
    setup_potential_games,
    claim_distributed_gd_requires_protocols,
    claim_pressure_as_potential_function,
)
from .s3_problem_formulation import (
    setup_artifact_state_space,
    setup_signal_function,
    setup_pressure_function,
    setup_phase_1_decay,
    setup_phase_2_proposal,
    setup_phase_3_validation,
    setup_phase_4_reinforcement,
    setup_stability_definition,
    setup_locality_constraint,
    claim_central_design_questions,
)
from .s4_method import (
    setup_pressure_alignment,
    setup_bounded_coupling,
    claim_potential_game_connection,
    setup_finite_action_assumption,
    setup_algorithm_1,
    claim_algorithm_three_properties,
    claim_economic_termination,
)
from .s5_theoretical_analysis import (
    claim_per_tick_pressure_drop,
    claim_theorem_5_1_convergence,
    claim_convergence_bound_implication,
    claim_theorem_5_2_basin_quality,
    claim_theorem_5_3_basin_separation,
    claim_decay_necessity_argument,
    claim_theorem_5_4_linear_scaling,
    claim_theorem_5_5_parallel_convergence,
    claim_table_1_coordination_comparison,
    claim_centralized_complexity,
    claim_hierarchical_complexity,
    claim_message_passing_complexity,
)
from .s6_experiments_setup import (
    setup_task_meeting_scheduling,
    setup_difficulty_table,
    setup_meeting_pressure_function,
    claim_alignment_separability,
    claim_alignment_attendee_constraint_local,
    claim_alignment_empirical_zero_eps,
    setup_pressure_field_strategy,
    setup_conversation_strategy,
    setup_hierarchical_strategy,
    setup_sequential_random_strategies,
    setup_fairness_guarantees,
    setup_seeding_protocol,
    setup_metrics,
    setup_implementation,
    setup_band_escalation,
    setup_model_escalation,
    claim_model_choice_rationale,
    setup_negative_pheromones,
)
from .s6b_main_results import (
    claim_table_3_aggregate_solve_rates,
    claim_pressure_vs_conversation_4x,
    claim_pressure_vs_hierarchical_30x,
    claim_conversation_intermediate,
    claim_hierarchical_sequential_random_fail,
    claim_effect_sizes_large,
    claim_result_contradicts_explicit_orchestration_assumption,
    claim_table_9_convergence_speed,
    claim_solvability_is_limiting_factor_on_hard,
    claim_table_10_final_pressure,
    claim_table_11_token_per_trial,
    claim_table_12_token_per_solve,
    claim_table_13_solved_unsolved_split,
    claim_escalation_as_cost_control,
)
from .s6c_ablations import (
    claim_table_4_decay_ablation,
    claim_decay_ablation_mechanism,
    claim_table_5_full_ablation,
    claim_inhibition_no_effect_explanation,
    claim_table_6_scaling,
    claim_escalation_implements_exploitation_exploration,
    claim_escalation_demonstrates_fm_mas_symbiosis,
    claim_negative_pheromones_design,
)
from .s6d_difficulty_breakdown import (
    claim_table_8_difficulty_breakdown,
    claim_easy_pressure_field_86_7,
    claim_easy_conversation_33_3,
    claim_easy_hierarchical_4_4,
    claim_medium_pressure_field_43_3,
    claim_hard_pressure_field_15_6,
    claim_only_pressure_field_scales,
    claim_gap_widens_with_difficulty,
    claim_figure_1_visual,
)
from .s7_discussion import (
    claim_factor_1_coordination_overhead_harms,
    claim_factor_2_locality_makes_greedy_effective,
    claim_factor_3_parallel_validation_amplifies,
    claim_hierarchical_rejection_loop,
    claim_hierarchical_rejection_statistics,
    claim_architectural_lesson,
    claim_limitation_modest_hard_solve_rate,
    claim_limitation_domain_specificity,
    claim_other_practical_limitations,
    claim_limitation_trajectory_level_risks,
    claim_limitation_decay_miscalibration,
    claim_when_pressure_field,
    claim_when_hierarchical,
    claim_fm_solves_action_enumeration,
    claim_mas_solves_output_combination,
    claim_societal_accountability,
    claim_societal_goodhart,
    claim_societal_explainability,
    claim_conclusion_synthesis,
)


# ============================================================================
# SECTION 1 (Motivation): orchestration paradigm -> overhead diagnosis
# ============================================================================

strat_orchestration_paradigm_implies_overhead = support(
    [
        claim_explicit_orchestration_paradigm,
        claim_mas_llm_baselines_share_pattern,
        claim_explicit_orchestration_scaling_failures,
    ],
    claim_orchestration_overhead_scales_poorly,
    reason=(
        "The diagnostic claim that explicit-orchestration coordination "
        "overhead scales poorly with agent count and task complexity "
        "(@claim_orchestration_overhead_scales_poorly) follows from "
        "three premises: (i) the dominant MAS-LLM paradigm uses "
        "explicit orchestration through planners/managers/workers + "
        "message passing + hierarchical control "
        "(@claim_explicit_orchestration_paradigm); (ii) AutoGen, "
        "MetaGPT, CAMEL, and CrewAI all share this design pattern "
        "(@claim_mas_llm_baselines_share_pattern); (iii) the design "
        "pattern faces three concrete scaling failures -- coordinator "
        "bottlenecks, message-overhead growth ($O(n^2)$ pairwise / "
        "$O(n \\log n)$ tree), and manager-failure cascades "
        "(@claim_explicit_orchestration_scaling_failures). Combining "
        "(i)-(iii), the paradigm-level overhead claim follows."
    ),
    prior=0.92,
)

# ============================================================================
# SECTION 2: pressure-field eliminates organizational dimensions
# ============================================================================

strat_pressure_field_eliminates_three_dimensions = support(
    [claim_organizational_paradigms_assign_roles, claim_pressure_field_proposal],
    claim_pressure_field_eliminates_three_dimensions,
    reason=(
        "Dignum's three organizational dimensions (structure / norms "
        "/ dynamics) are eliminated "
        "(@claim_pressure_field_eliminates_three_dimensions) when "
        "(i) traditional paradigms require explicit role / norm / "
        "dynamics specification "
        "(@claim_organizational_paradigms_assign_roles), and (ii) "
        "the pressure-field proposal "
        "(@claim_pressure_field_proposal) replaces all three with "
        "gradient-based coordination -- roles dissolve via 'any "
        "agent may address any high-pressure region', norms become "
        "implicit (pressure function encodes goodness), dynamics "
        "emerge from temporal decay."
    ),
    prior=0.9,
)

strat_pressure_field_o1_overhead_from_proposal = support(
    [claim_pressure_field_proposal, claim_gpgp_message_complexity],
    claim_pressure_field_o1_overhead,
    reason=(
        "The $O(1)$ inter-agent communication-overhead claim "
        "(@claim_pressure_field_o1_overhead) follows from "
        "(i) the pressure-field proposal coordinating only through "
        "shared artifact reads/writes (@claim_pressure_field_proposal), "
        "in contrast to (ii) GPGP's $O(n \\log n)$ explicit messages "
        "(@claim_gpgp_message_complexity) and pairwise message-"
        "passing's $O(n^2)$ overhead. Eliminating the messages "
        "themselves yields $O(1)$ inter-agent overhead by "
        "construction."
    ),
    prior=0.95,
)

strat_pressure_alignment_replaces_intention_alignment = support(
    [claim_sharedplans_joint_intentions_cost, claim_pressure_field_proposal],
    claim_pressure_alignment_replaces_intention_alignment,
    reason=(
        "Pressure alignment replaces intention alignment "
        "(@claim_pressure_alignment_replaces_intention_alignment) "
        "because (i) SharedPlans / Joint Intentions require "
        "expensive recursive mutual-belief machinery "
        "(@claim_sharedplans_joint_intentions_cost), and (ii) the "
        "pressure-field proposal has all agents perceive the same "
        "pressure landscape via shared artifact state "
        "(@claim_pressure_field_proposal) -- so the shared artifact "
        "*is* the mutual belief, eliminating the 'I believe that "
        "you believe' regress."
    ),
    prior=0.9,
)

strat_pressure_field_instantiates_four_mechanisms = support(
    [claim_pressure_field_proposal],
    claim_pressure_field_instantiates_four_mechanisms,
    reason=(
        "The pressure-field design "
        "(@claim_pressure_field_proposal) instantiates Serugendo's "
        "four self-organization mechanisms "
        "(@setup_serugendo_four_mechanisms) directly: positive "
        "feedback via positive pheromones (few-shot examples), "
        "negative feedback via temporal decay + inhibition, "
        "randomness via stochastic sampling and band escalation, "
        "and multiple interactions via $K$ parallel patch "
        "proposals per tick."
    ),
    prior=0.92,
    background=[setup_serugendo_four_mechanisms],
)

strat_pressure_field_satisfies_dewolf_holvoet = support(
    [claim_pressure_field_proposal],
    claim_pressure_field_satisfies_dewolf_holvoet,
    reason=(
        "Pressure-field satisfies De Wolf-Holvoet self-organization "
        "criteria (@setup_dewolf_holvoet_criteria) -- absence of "
        "external control (autonomous local action), local-to-"
        "global pattern formation (regional pressure reduction "
        "yields global coordination), dynamic adaptation (continuous "
        "decay) -- because the proposal "
        "(@claim_pressure_field_proposal) realizes exactly these "
        "three properties through the gradient-fields design "
        "pattern explicitly named in De Wolf-Holvoet."
    ),
    prior=0.9,
    background=[setup_dewolf_holvoet_criteria],
)

# ============================================================================
# SECTION 2.1.5: FM-enablement -- 5 capabilities -> overall enablement
# ============================================================================

strat_fm_enables_summary = support(
    [
        claim_fm_capability_1_domain_general_patches,
        claim_fm_capability_2_instruction_following,
        claim_fm_capability_3_zero_shot_quality,
        claim_fm_capability_4_in_context_pheromone,
        claim_fm_capability_5_generative_flexibility,
    ],
    claim_fm_enables_summary,
    reason=(
        "The summary claim that five FM capabilities collectively "
        "enable stigmergic coordination on artifact refinement "
        "(@claim_fm_enables_summary) is the conjunction of: "
        "(1) broad-pretraining domain-general patch proposal "
        "(@claim_fm_capability_1_domain_general_patches), "
        "(2) instruction-following replacing action-space "
        "enumeration "
        "(@claim_fm_capability_2_instruction_following), "
        "(3) zero-shot reasoning interpreting quality signals "
        "(@claim_fm_capability_3_zero_shot_quality), "
        "(4) in-context learning implementing pheromone memory "
        "(@claim_fm_capability_4_in_context_pheromone), and "
        "(5) generative flexibility enabling unbounded solution "
        "spaces (@claim_fm_capability_5_generative_flexibility). "
        "Each capability addresses a specific limitation of "
        "traditional stigmergic systems."
    ),
    prior=0.92,
)

strat_foundation_models_enable_from_capabilities = support(
    [claim_fm_enables_summary],
    claim_foundation_models_enable,
    reason=(
        "The headline 'FMs enable stigmergic coordination' claim "
        "(@claim_foundation_models_enable) is the motivation-"
        "section restatement of the Section 2.1.5 capability "
        "summary (@claim_fm_enables_summary). Both express the "
        "'universal actor' synthesis: FMs solve the action-"
        "enumeration problem that previously blocked stigmergic "
        "approaches on open-ended artifact refinement."
    ),
    prior=0.95,
)

# ============================================================================
# SECTION 2.3-2.4: pressure-field inherits stigmergy + potential-game theory
# ============================================================================

strat_pressure_field_inherits_aco = support(
    [claim_pressure_field_proposal],
    claim_pressure_field_inherits_aco,
    reason=(
        "Pressure-field directly inherits stigmergic principles "
        "from ACO (@claim_pressure_field_inherits_aco) by analogy: "
        "the artifact serves as ACO's shared environment "
        "(@setup_grasse_stigmergy); regional pressures play the "
        "role of pheromone concentrations; temporal decay "
        "corresponds to pheromone evaporation "
        "(@setup_aco_mechanisms). The generalization beyond "
        "pathfinding -- to arbitrary artifact refinement with "
        "formal convergence guarantees -- is what the Section 4-5 "
        "potential-game framework provides."
    ),
    prior=0.9,
    background=[setup_grasse_stigmergy, setup_aco_mechanisms],
)

strat_pressure_as_potential_function = support(
    [claim_pressure_field_proposal, claim_alignment_separability],
    claim_pressure_as_potential_function,
    reason=(
        "The claim that pressure-field instantiates the potential-"
        "game framework with $\\Phi(s) = P(s)$ "
        "(@claim_pressure_as_potential_function) follows from: "
        "(i) the pressure-field proposal "
        "(@claim_pressure_field_proposal) defines local agents "
        "minimizing local pressure, and (ii) under separable / "
        "aligned pressure (@claim_alignment_separability), local "
        "improvement implies global improvement, satisfying "
        "Monderer-Shapley's potential-game alignment property "
        "(@setup_potential_games)."
    ),
    prior=0.92,
    background=[setup_potential_games],
)

# ============================================================================
# SECTION 4: alignment + potential-game theorem (deduction-style)
# ============================================================================

deduct_potential_game_connection = deduction(
    [claim_pressure_as_potential_function],
    claim_potential_game_connection,
    background=[setup_pressure_alignment, setup_potential_games],
    reason=(
        "Under pressure alignment (@setup_pressure_alignment), "
        "the pressure system has Monderer-Shapley's potential-game "
        "structure (@setup_potential_games) with $\\Phi(s) = P(s)$. "
        "By definition of a potential game, any sequence of "
        "improving moves converges to a Nash equilibrium "
        "(@claim_potential_game_connection). Nash equilibria "
        "correspond to stable basins (states where no local action "
        "can reduce pressure below activation threshold). The "
        "derivation is purely deductive from the two definitions."
    ),
    prior=0.99,
)

# ============================================================================
# SECTION 5: convergence theorems via deduction
# ============================================================================

deduct_per_tick_pressure_drop = deduction(
    [claim_pressure_as_potential_function],
    claim_per_tick_pressure_drop,
    background=[setup_bounded_coupling],
    reason=(
        "The per-tick pressure-drop lemma "
        "(@claim_per_tick_pressure_drop) follows directly from "
        "Definition 4.2 of $\\epsilon$-bounded coupling "
        "(@setup_bounded_coupling): for any patch reducing $P_i$ "
        "by $\\delta_i$, $|P_j(s') - P_j(s)| \\le \\epsilon$ for "
        "every $j \\ne i$, so $P_{t+1} - P_t \\le -\\delta_i + "
        "(n-1)\\epsilon$. With $\\delta_i \\ge \\delta_{\\min} > "
        "(n-1)\\epsilon$, the drop is at least $\\delta_{\\min} - "
        "(n-1)\\epsilon > 0$. Pure algebra from the definition."
    ),
    prior=0.99,
)

deduct_theorem_5_1 = deduction(
    [claim_per_tick_pressure_drop],
    claim_theorem_5_1_convergence,
    background=[
        setup_pressure_alignment,
        setup_bounded_coupling,
        setup_phase_1_decay,
        setup_phase_4_reinforcement,
        setup_stability_definition,
    ],
    reason=(
        "Theorem 5.1 (Convergence) "
        "(@claim_theorem_5_1_convergence) follows by composition: "
        "(i) under alignment (@setup_pressure_alignment) and "
        "$\\epsilon$-bounded coupling (@setup_bounded_coupling), "
        "the per-tick drop lemma "
        "(@claim_per_tick_pressure_drop) gives $P_{t+1} - P_t \\le "
        "-(\\delta_{\\min} - (n-1)\\epsilon) < 0$. (ii) Since "
        "$P(s) \\ge 0$ and decreases by a fixed minimum "
        "$\\Delta = \\delta_{\\min} - (n-1)\\epsilon$ per tick "
        "(when patches are applied), the system reaches a state "
        "where no region exceeds $\\tau_{act}$ within $T \\le "
        "P_0 / \\Delta$ ticks. (iii) The decay/reinforcement "
        "constraint "
        "$\\Delta_f > 1 - e^{-\\lambda_f \\cdot \\tau_{inh}}$ "
        "(combining @setup_phase_1_decay and "
        "@setup_phase_4_reinforcement) ensures stability is "
        "maintained once reached (per "
        "@setup_stability_definition). Pure deduction in "
        "Appendix C.1."
    ),
    prior=0.99,
)

strat_convergence_bound_implication = support(
    [claim_theorem_5_1_convergence],
    claim_convergence_bound_implication,
    reason=(
        "The implication that convergence time scales with $P_0$ "
        "rather than state-space or action-space size "
        "(@claim_convergence_bound_implication) is read directly "
        "from the bound in Theorem 5.1 "
        "(@claim_theorem_5_1_convergence): $T \\le P_0 / "
        "(\\delta_{\\min} - (n-1)\\epsilon)$ has $P_0$ as its "
        "only data-dependent term. The remaining quantities "
        "$\\delta_{\\min}, \\epsilon, n$ are fixed by the "
        "problem's pressure-function design, not by representation "
        "size."
    ),
    prior=0.97,
)

deduct_theorem_5_2 = deduction(
    [claim_central_design_questions],
    claim_theorem_5_2_basin_quality,
    background=[setup_stability_definition],
    reason=(
        "Theorem 5.2 (Basin Quality) "
        "(@claim_theorem_5_2_basin_quality) follows directly from "
        "Definition 3.1 of stability "
        "(@setup_stability_definition): in any stable basin "
        "$s^*$, $P_i(s^*) < \\tau_{act}$ for all $i$ by "
        "definition; summing over $n$ regions yields $P(s^*) = "
        "\\sum_i P_i(s^*) < n \\cdot \\tau_{act}$. One-line "
        "deduction in the main text."
    ),
    prior=0.99,
)

deduct_theorem_5_3 = deduction(
    [claim_pressure_as_potential_function],
    claim_theorem_5_3_basin_separation,
    background=[setup_stability_definition, setup_pressure_alignment],
    reason=(
        "Theorem 5.3 (Basin Separation) "
        "(@claim_theorem_5_3_basin_separation) follows from: "
        "(i) by Definition 3.1 (@setup_stability_definition), a "
        "stable basin $B$ requires every region to be below "
        "$\\tau_{act}$; (ii) under separable pressure "
        "(@setup_pressure_alignment with $\\epsilon = 0$), "
        "transitioning between two basins $B_1, B_2$ by "
        "continuity must pass through a state where some region "
        "exceeds $\\tau_{act}$. The minimum such exceedance "
        "defines the barrier height $\\ge \\tau_{act}$. "
        "Appendix C.2."
    ),
    prior=0.99,
)

strat_decay_necessity_argument = support(
    [claim_theorem_5_3_basin_separation],
    claim_decay_necessity_argument,
    background=[setup_phase_1_decay],
    reason=(
        "The decay-necessity argument "
        "(@claim_decay_necessity_argument) follows from Theorem "
        "5.3 (@claim_theorem_5_3_basin_separation): without "
        "decay, fitness in a basin remains high indefinitely so "
        "no region can exceed $\\tau_{act}$, trapping the system "
        "in the first basin reached even if a lower-pressure "
        "basin exists. Decay (@setup_phase_1_decay) erodes "
        "fitness, eventually allowing pressure to exceed "
        "$\\tau_{act}$ and enabling transition to a lower-"
        "pressure basin."
    ),
    prior=0.95,
)

deduct_theorem_5_4 = deduction(
    [claim_algorithm_three_properties],
    claim_theorem_5_4_linear_scaling,
    background=[setup_signal_function, setup_pressure_function, setup_algorithm_1],
    reason=(
        "Theorem 5.4 (Linear Scaling) "
        "(@claim_theorem_5_4_linear_scaling) tabulates the per-"
        "phase complexities of Algorithm 1 (@setup_algorithm_1): "
        "signal computation $O(m \\cdot d)$ (from "
        "@setup_signal_function), pressure computation "
        "$O(m \\cdot k)$ (from @setup_pressure_function), patch "
        "proposal $O(m \\cdot a)$, sorting $O(m \\cdot a \\cdot "
        "\\log(m \\cdot a))$, and $O(1)$ inter-agent coordination "
        "(no messages). Total $O(m \\cdot (d + k + a \\cdot "
        "\\log(ma)))$ is independent of agent count $n$. "
        "Appendix C.3."
    ),
    prior=0.99,
)

deduct_theorem_5_5 = deduction(
    [claim_theorem_5_1_convergence],
    claim_theorem_5_5_parallel_convergence,
    background=[setup_phase_3_validation],
    reason=(
        "Theorem 5.5 (Parallel Convergence) "
        "(@claim_theorem_5_5_parallel_convergence) extends "
        "Theorem 5.1 (@claim_theorem_5_1_convergence) to the "
        "parallel-validation setting (@setup_phase_3_validation): "
        "when $K$ patches target disjoint regions, each reduces "
        "global pressure by at least $\\delta_{\\min} - "
        "(n-1)\\epsilon$, and effects are additive on disjoint "
        "regions; combined drop is $K \\cdot (\\delta_{\\min} - "
        "(n-1)\\epsilon)$, yielding $T \\le P_0 / (K \\cdot "
        "(\\delta_{\\min} - (n-1)\\epsilon))$. Appendix C.4."
    ),
    prior=0.99,
)

deduct_table_1 = deduction(
    [
        claim_pressure_field_o1_overhead,
        claim_centralized_complexity,
        claim_hierarchical_complexity,
        claim_message_passing_complexity,
        claim_theorem_5_5_parallel_convergence,
    ],
    claim_table_1_coordination_comparison,
    reason=(
        "Table 1 "
        "(@claim_table_1_coordination_comparison) is the row-"
        "wise composition of: pressure-field $O(1)$ overhead "
        "(@claim_pressure_field_o1_overhead) and parallelism "
        "$\\min(n, m, K)$ (@claim_theorem_5_5_parallel_convergence); "
        "centralized $O(m \\cdot a)$ (@claim_centralized_complexity); "
        "hierarchical $O(n \\log n)$ "
        "(@claim_hierarchical_complexity); message-passing "
        "$O(n^2)$ (@claim_message_passing_complexity)."
    ),
    prior=0.99,
)

# ============================================================================
# Headline convergence-theorem -> textbook restatement
# ============================================================================

strat_headline_convergence_theorem = support(
    [claim_theorem_5_1_convergence, claim_theorem_5_5_parallel_convergence],
    claim_headline_convergence_theorem,
    reason=(
        "The motivation-section headline theoretical claim "
        "(@claim_headline_convergence_theorem) summarizes "
        "Theorems 5.1 (@claim_theorem_5_1_convergence) and 5.5 "
        "(@claim_theorem_5_5_parallel_convergence): convergence "
        "in $T \\le P_0 / (\\delta_{\\min} - (n-1)\\epsilon)$ "
        "ticks for sequential, improving by factor $K$ when $K$ "
        "patches are validated in parallel on disjoint regions."
    ),
    prior=0.97,
)

# ============================================================================
# SECTION 6: alignment-verification chain
# ============================================================================

strat_alignment_attendee_constraint_local = support(
    [claim_alignment_separability],
    claim_alignment_attendee_constraint_local,
    background=[setup_meeting_pressure_function],
    reason=(
        "The claim that attendee constraints don't create cross-"
        "region coupling "
        "(@claim_alignment_attendee_constraint_local) follows from: "
        "(i) the pressure function counts overlaps within a block "
        "only (@setup_meeting_pressure_function); (ii) per-region "
        "pressure is separable by design "
        "(@claim_alignment_separability). Moving a meeting between "
        "blocks creates only *local* effects on each block's "
        "pressure -- no indirect coupling through attendee "
        "identity."
    ),
    prior=0.93,
)

# NOTE: claim_alignment_separability is left as a leaf claim. Its
# justification is "read off the pressure function design"
# (@setup_meeting_pressure_function), but in Gaia we cannot use a
# setting as a strategy premise. The setting itself constitutes the
# warrant; the high prior in priors.py reflects this structural
# certainty.

strat_alignment_empirical_zero_eps = support(
    [
        claim_alignment_separability,
        claim_alignment_attendee_constraint_local,
    ],
    claim_alignment_empirical_zero_eps,
    reason=(
        "The empirical alignment-validation result "
        "(@claim_alignment_empirical_zero_eps) -- 9,873 "
        "transitions, 0 pressure-degradation events, $\\delta_{\\min} "
        "\\ge 1$ -- is the empirical confirmation expected from: "
        "(i) per-region pressure being structurally separable "
        "(@claim_alignment_separability); and (ii) attendee "
        "constraints not creating indirect coupling "
        "(@claim_alignment_attendee_constraint_local). Together "
        "these predict $\\epsilon = 0$, which the empirical record "
        "reproduces."
    ),
    prior=0.93,
)

# ============================================================================
# SECTION 6.2: per-strategy table -> headline pairwise gap claims
# ============================================================================

strat_pressure_vs_conversation_4x = support(
    [claim_table_3_aggregate_solve_rates],
    claim_pressure_vs_conversation_4x,
    reason=(
        "The 4x ratio claim (@claim_pressure_vs_conversation_4x) "
        "is read directly from Table 3 "
        "(@claim_table_3_aggregate_solve_rates): pressure-field "
        "131/270 = 48.5% versus conversation 30/270 = 11.1%, "
        "ratio $\\approx 4.4 \\times$. The pairwise $p < 0.001$ "
        "and Cohen's $h$ effect size are the same data."
    ),
    prior=0.97,
)

strat_pressure_vs_hierarchical_30x = support(
    [claim_table_3_aggregate_solve_rates],
    claim_pressure_vs_hierarchical_30x,
    reason=(
        "The 30x ratio claim (@claim_pressure_vs_hierarchical_30x) "
        "is read directly from Table 3 "
        "(@claim_table_3_aggregate_solve_rates): pressure-field "
        "131/270 = 48.5% versus hierarchical 4/270 = 1.5%, ratio "
        "$\\approx 32.3 \\times$, with $p < 0.001$."
    ),
    prior=0.97,
)

strat_conversation_intermediate_from_table = support(
    [claim_table_3_aggregate_solve_rates, claim_table_8_difficulty_breakdown],
    claim_conversation_intermediate,
    reason=(
        "Conversation's intermediate-performance characterization "
        "(@claim_conversation_intermediate) follows from "
        "(i) Table 3 (@claim_table_3_aggregate_solve_rates) "
        "showing 11.1% aggregate; and (ii) Table 8 "
        "(@claim_table_8_difficulty_breakdown) showing 33.3% on "
        "easy and 0% on medium / hard -- so conversation solves "
        "only easy problems."
    ),
    prior=0.96,
)

strat_hierarchical_sequential_random_fail = support(
    [claim_table_3_aggregate_solve_rates, claim_table_8_difficulty_breakdown],
    claim_hierarchical_sequential_random_fail,
    reason=(
        "Hierarchical / sequential / random failing on medium and "
        "hard (@claim_hierarchical_sequential_random_fail) is read "
        "directly from Table 3 (1.5% / 0.4% / 0.4% aggregate, "
        "@claim_table_3_aggregate_solve_rates) and Table 8 "
        "(0% / 0% / 0% on medium and hard, "
        "@claim_table_8_difficulty_breakdown)."
    ),
    prior=0.97,
)

# ============================================================================
# SECTION 6.6: per-difficulty observations -> aggregate "only scales" claim
# ============================================================================

# Each difficulty tier provides independent evidence that pressure-field is the
# only strategy with non-zero solve rate at that tier (medium and hard
# specifically). We use induction over the two tiers as separate observations
# of the cross-tier law.

s_only_scales_medium = support(
    [claim_only_pressure_field_scales],
    claim_medium_pressure_field_43_3,
    reason=(
        "If pressure-field is the only strategy that scales to "
        "harder problems (@claim_only_pressure_field_scales), "
        "then on medium difficulty, pressure-field should achieve "
        "non-zero solve rate while baselines achieve 0% -- which "
        "is exactly the medium-tier observation "
        "(@claim_medium_pressure_field_43_3): 43.3% / 0% / 0% / "
        "0% / 0% across the five strategies."
    ),
    prior=0.96,
)

s_only_scales_hard = support(
    [claim_only_pressure_field_scales],
    claim_hard_pressure_field_15_6,
    reason=(
        "If pressure-field is the only strategy that scales to "
        "harder problems (@claim_only_pressure_field_scales), "
        "then on hard difficulty, pressure-field should achieve "
        "non-zero solve rate while baselines achieve 0% -- which "
        "is exactly the hard-tier observation "
        "(@claim_hard_pressure_field_15_6): 15.6% / 0% / 0% / "
        "0% / 0% across the five strategies."
    ),
    prior=0.96,
)

induct_only_pressure_field_scales = induction(
    s_only_scales_medium,
    s_only_scales_hard,
    law=claim_only_pressure_field_scales,
    reason=(
        "The medium-tier observation (43.3% vs 0%, "
        "@claim_medium_pressure_field_43_3) and the hard-tier "
        "observation (15.6% vs 0%, "
        "@claim_hard_pressure_field_15_6) are independent panels "
        "(different problem-size configurations and different "
        "trial samples) that both confirm the cross-tier 'only "
        "pressure-field scales' law "
        "(@claim_only_pressure_field_scales). Each tier "
        "independently demonstrates the same population-level "
        "pattern."
    ),
)

strat_table_3_implies_only_pressure_scales = support(
    [claim_table_3_aggregate_solve_rates, claim_table_8_difficulty_breakdown],
    claim_only_pressure_field_scales,
    reason=(
        "The headline 'only pressure-field scales' claim "
        "(@claim_only_pressure_field_scales) is also a direct "
        "read of Table 3 (@claim_table_3_aggregate_solve_rates) "
        "and Table 8 (@claim_table_8_difficulty_breakdown), which "
        "show pressure-field as the only strategy with non-zero "
        "rate on medium and hard."
    ),
    prior=0.96,
)

strat_gap_widens_with_difficulty = support(
    [
        claim_table_8_difficulty_breakdown,
        claim_easy_pressure_field_86_7,
        claim_easy_conversation_33_3,
        claim_only_pressure_field_scales,
    ],
    claim_gap_widens_with_difficulty,
    reason=(
        "The gap-widens-with-difficulty claim "
        "(@claim_gap_widens_with_difficulty) follows from: "
        "(i) on easy, the gap is 53.4 pp (86.7% vs 33.3%, "
        "@claim_easy_pressure_field_86_7 and "
        "@claim_easy_conversation_33_3); "
        "(ii) on medium and hard, the gap is *absolute* "
        "(non-zero vs 0%, "
        "@claim_only_pressure_field_scales); (iii) Table 8 "
        "(@claim_table_8_difficulty_breakdown) shows the "
        "transition tier-by-tier."
    ),
    prior=0.96,
)

strat_figure_1_visual_from_table_8 = support(
    [claim_table_8_difficulty_breakdown],
    claim_figure_1_visual,
    reason=(
        "Figure 1's visual claim "
        "(@claim_figure_1_visual) -- pressure-field outperforms "
        "every baseline at every difficulty with non-overlapping "
        "Wilson 95% CIs -- is the bar-chart visualization of "
        "Table 8 (@claim_table_8_difficulty_breakdown). Same "
        "data, different presentation."
    ),
    prior=0.97,
)

# ============================================================================
# Easy-problems headline (motivation) <- Table 8 row + per-strategy values
# ============================================================================

strat_headline_easy_problems = support(
    [
        claim_easy_pressure_field_86_7,
        claim_easy_conversation_33_3,
        claim_easy_hierarchical_4_4,
        claim_table_8_difficulty_breakdown,
    ],
    claim_headline_easy_problems,
    reason=(
        "The motivation-section easy-problems headline "
        "(@claim_headline_easy_problems) -- 86.7% pressure-field "
        "vs 33.3% next-best, 4.4% hierarchical -- is the row-"
        "level read of Table 8 "
        "(@claim_table_8_difficulty_breakdown): the easy-tier "
        "values for pressure-field "
        "(@claim_easy_pressure_field_86_7), conversation "
        "(@claim_easy_conversation_33_3), and hierarchical "
        "(@claim_easy_hierarchical_4_4)."
    ),
    prior=0.97,
)

# ============================================================================
# Headline aggregate solve-rates claim: motivation <- Table 3
# ============================================================================

strat_headline_solve_rates = support(
    [claim_table_3_aggregate_solve_rates],
    claim_headline_solve_rates,
    reason=(
        "The motivation-section headline claim "
        "(@claim_headline_solve_rates) reproduces Table 3's "
        "aggregate row (@claim_table_3_aggregate_solve_rates) "
        "as the headline summary: 48.5% / 11.1% / 1.5% / 0.4% / "
        "0.4% across the five strategies, with $\\chi^2 > 200$ "
        "and $p < 0.001$."
    ),
    prior=0.97,
)

strat_headline_only_strategy_scales = support(
    [claim_only_pressure_field_scales, claim_table_8_difficulty_breakdown],
    claim_headline_only_strategy_scales,
    reason=(
        "The motivation-section headline that pressure-field is "
        "the only strategy with non-zero solve rate on medium "
        "(43.3%) and hard (15.6%) "
        "(@claim_headline_only_strategy_scales) is the same as "
        "the cross-tier law (@claim_only_pressure_field_scales) "
        "with the per-tier numbers attached, read off Table 8 "
        "(@claim_table_8_difficulty_breakdown)."
    ),
    prior=0.97,
)

# ============================================================================
# SECTION 6.3: ablation -- decay -> Theorem 5.3 connection
# ============================================================================

strat_decay_ablation_mechanism_from_theorem = support(
    [claim_decay_necessity_argument],
    claim_decay_ablation_mechanism,
    reason=(
        "The mechanistic explanation for the decay-ablation "
        "effect (@claim_decay_ablation_mechanism) -- without "
        "decay, agents are trapped in the first stable basin "
        "they reach -- is the empirical instantiation of the "
        "decay-necessity argument "
        "(@claim_decay_necessity_argument) following Theorem "
        "5.3 (@claim_theorem_5_3_basin_separation). Theory "
        "predicts the failure mode; ablation observes it."
    ),
    prior=0.92,
)

strat_table_4_decay_ablation_supports_decay_argument = support(
    [claim_table_4_decay_ablation, claim_decay_ablation_mechanism],
    claim_headline_decay_ablation,
    reason=(
        "The motivation-section headline decay-ablation claim "
        "(@claim_headline_decay_ablation) -- 96.7% with vs 86.7% "
        "without, $p = 0.35$ -- is the row-level read of Table 4 "
        "(@claim_table_4_decay_ablation) with the mechanistic "
        "interpretation (@claim_decay_ablation_mechanism) "
        "tying the directional effect to Theorem 5.3 (Basin "
        "Separation)."
    ),
    prior=0.95,
)

strat_table_5_supports_table_4 = support(
    [claim_table_5_full_ablation],
    claim_table_4_decay_ablation,
    reason=(
        "Table 4's decay ablation "
        "(@claim_table_4_decay_ablation) is the marginal cell "
        "of the full Table 5 ablation matrix "
        "(@claim_table_5_full_ablation): the 'Full' (96.7%) and "
        "'No Decay' (86.7%) rows of Table 5 *are* Table 4's two "
        "configurations, and the 10 pp single-feature "
        "contribution is read off both tables consistently."
    ),
    prior=0.97,
)

strat_inhibition_no_effect_explanation = support(
    [claim_table_5_full_ablation],
    claim_inhibition_no_effect_explanation,
    background=[setup_implementation],
    reason=(
        "The 50-tick-budget explanation for inhibition's 0pp "
        "effect (@claim_inhibition_no_effect_explanation) follows "
        "from Table 5 (@claim_table_5_full_ablation) showing 96.7% "
        "for both Full and No-Inhibition configurations, "
        "combined with the implementation detail "
        "(@setup_implementation) that all experiments use a "
        "50-tick budget."
    ),
    prior=0.85,
)

# ============================================================================
# SECTION 6.4 scaling -> Theorem 5.4
# ============================================================================

strat_table_6_scaling_validates_theorem_5_4 = support(
    [claim_table_6_scaling],
    claim_theorem_5_4_linear_scaling,
    reason=(
        "Table 6's scaling stability across 1/2/4 agents "
        "(@claim_table_6_scaling) is the empirical signature "
        "predicted by Theorem 5.4 "
        "(@claim_theorem_5_4_linear_scaling): per-tick "
        "complexity is independent of agent count $n$, so "
        "varying $n$ from 1 to 4 should not significantly "
        "change solve rates, which is what the table shows "
        "(83.3% / 93.3% / 83.3%, all CI-overlapping)."
    ),
    prior=0.9,
)

# ============================================================================
# SECTION 6.5 escalation
# ============================================================================

# NOTE: claim_escalation_implements_exploitation_exploration is left
# as a leaf-content claim. Its justification is "read off the band-
# and model-escalation design" (@setup_band_escalation,
# @setup_model_escalation), but Gaia does not allow settings as
# strategy premises.

strat_escalation_demonstrates_fm_mas_symbiosis = support(
    [
        claim_escalation_implements_exploitation_exploration,
        claim_fm_mas_mutually_enabling,
    ],
    claim_escalation_demonstrates_fm_mas_symbiosis,
    reason=(
        "Escalation as concrete FM-MAS symbiosis "
        "(@claim_escalation_demonstrates_fm_mas_symbiosis) "
        "follows from: (i) escalation implements exploit-explore "
        "balance via pressure signal "
        "(@claim_escalation_implements_exploitation_exploration); "
        "(ii) the bidirectional FM-MAS synthesis "
        "(@claim_fm_mas_mutually_enabling). The MAS coordination "
        "mechanism (pressure-field) provides the *when-to-"
        "escalate* criterion via pressure signal; FMs provide "
        "the broad-coverage substrate. Both directions of the "
        "synthesis are concretely realized in the escalation "
        "logic."
    ),
    prior=0.9,
)

# ============================================================================
# SECTION 6.7 / 6.8 / 6.9 minor results
# ============================================================================

strat_solvability_limiting = support(
    [claim_table_9_convergence_speed, claim_only_pressure_field_scales],
    claim_solvability_is_limiting_factor_on_hard,
    reason=(
        "The 'solvability is the limiting factor on hard "
        "problems' claim "
        "(@claim_solvability_is_limiting_factor_on_hard) "
        "follows from: (i) Table 9 "
        "(@claim_table_9_convergence_speed) showing similar "
        "convergence speeds (32.3 ticks on hard vs 34.6 on "
        "medium for the solved cases); (ii) the cross-tier 'only "
        "pressure-field scales' law "
        "(@claim_only_pressure_field_scales). Together these "
        "imply: when pressure-field can solve a hard problem, it "
        "does so quickly; when it cannot, it fails entirely."
    ),
    prior=0.9,
)

strat_table_12_token_per_solve = support(
    [claim_table_11_token_per_trial, claim_table_3_aggregate_solve_rates],
    claim_table_12_token_per_solve,
    reason=(
        "The tokens-per-solve table "
        "(@claim_table_12_token_per_solve) is computed by "
        "dividing total tokens (Table 11, "
        "@claim_table_11_token_per_trial, multiplied by 270 "
        "trials) by the number of successful solves (Table 3, "
        "@claim_table_3_aggregate_solve_rates: 131 for pressure-"
        "field, 30 for conversation). The arithmetic yields the "
        "12% efficiency reversal."
    ),
    prior=0.96,
)

strat_escalation_as_cost_control = support(
    [
        claim_escalation_implements_exploitation_exploration,
        claim_table_13_solved_unsolved_split,
    ],
    claim_escalation_as_cost_control,
    background=[setup_implementation],
    reason=(
        "Escalation as implicit cost control "
        "(@claim_escalation_as_cost_control) follows from: (i) "
        "the escalation mechanism only triggers on stagnated "
        "pressure velocity "
        "(@claim_escalation_implements_exploitation_exploration); "
        "(ii) Table 13 "
        "(@claim_table_13_solved_unsolved_split) shows solved "
        "trials use far fewer tokens (318K) than unsolved ones "
        "(900K) -- the 2.8x gap is the cost of escalation when "
        "needed. Together with the small-model-first design "
        "(@setup_implementation), the system scales cost with "
        "problem hardness."
    ),
    prior=0.9,
)

# ============================================================================
# SECTION 7.1: three factors explaining dominance
# ============================================================================

strat_factor_1_from_design = support(
    [claim_explicit_orchestration_scaling_failures],
    claim_factor_1_coordination_overhead_harms,
    reason=(
        "Factor 1 -- coordination overhead harms performance "
        "(@claim_factor_1_coordination_overhead_harms) -- follows "
        "from comparing strategy designs: hierarchical "
        "(@setup_hierarchical_strategy) requires multiple LLM "
        "calls per patch via a single sequential agent; "
        "conversation (@setup_conversation_strategy) requires "
        "4-12 LLM calls per region per tick; pressure-field "
        "(@setup_pressure_field_strategy) requires one LLM call "
        "per patch proposal in parallel. The same per-paradigm "
        "scaling-failure pattern is captured at the literature "
        "level by @claim_explicit_orchestration_scaling_failures."
    ),
    prior=0.92,
    background=[setup_pressure_field_strategy, setup_conversation_strategy, setup_hierarchical_strategy],
)

strat_factor_2_from_alignment = support(
    [claim_alignment_separability],
    claim_factor_2_locality_makes_greedy_effective,
    reason=(
        "Factor 2 -- locality makes greedy effective "
        "(@claim_factor_2_locality_makes_greedy_effective) -- "
        "follows from: (i) per-region pressure being "
        "structurally separable "
        "(@claim_alignment_separability) means fixing one region "
        "rarely creates conflicts elsewhere; (ii) the locality "
        "constraint (@setup_locality_constraint) makes greedy "
        "local optimization feasible without global state. Under "
        "these conditions, hierarchical's global planning offers "
        "no advantage."
    ),
    prior=0.9,
    background=[setup_locality_constraint],
)

strat_factor_3_from_theorem_5_5 = support(
    [claim_theorem_5_5_parallel_convergence],
    claim_factor_3_parallel_validation_amplifies,
    reason=(
        "Factor 3 -- parallel validation amplifies the advantage "
        "(@claim_factor_3_parallel_validation_amplifies) -- "
        "follows from Theorem 5.5 "
        "(@claim_theorem_5_5_parallel_convergence)'s factor-$K$ "
        "speedup, instantiated by the pressure-field strategy "
        "(@setup_pressure_field_strategy)'s parallel-validation "
        "phase. Hierarchical (@setup_hierarchical_strategy) "
        "validates one patch at a time; the resulting tick-"
        "budget difference is the empirical signature of the "
        "speedup."
    ),
    prior=0.92,
    background=[setup_pressure_field_strategy, setup_hierarchical_strategy],
)

# ============================================================================
# SECTION 7.2: rejection-loop failure mechanism
# ============================================================================

strat_hierarchical_rejection_loop_design = support(
    [claim_hierarchical_complexity],
    claim_hierarchical_rejection_loop,
    reason=(
        "The rejection-loop failure mechanism "
        "(@claim_hierarchical_rejection_loop) follows from the "
        "hierarchical strategy design "
        "(@setup_hierarchical_strategy): always selecting the "
        "single highest-pressure region + strict validation + "
        "sequential one-patch-per-tick produces a self-"
        "reinforcing cycle when the highest-pressure region is "
        "intractable -- the region remains highest-pressure "
        "after rejection, gets re-selected, etc. The general "
        "hierarchical-paradigm complexity claim "
        "(@claim_hierarchical_complexity) captures the same "
        "manager-bottleneck pattern."
    ),
    prior=0.95,
    background=[setup_hierarchical_strategy],
)

strat_hierarchical_rejection_statistics = support(
    [claim_hierarchical_rejection_loop],
    claim_hierarchical_rejection_statistics,
    reason=(
        "The 66.7% / 98.7% statistics "
        "(@claim_hierarchical_rejection_statistics) -- 180/270 "
        "runs applied 0 patches across 50 ticks; 173/13,460 "
        "patches accepted -- are direct measurements of the "
        "rejection-loop pattern "
        "(@claim_hierarchical_rejection_loop) playing out across "
        "the 270 hierarchical trials."
    ),
    prior=0.94,
)

strat_architectural_lesson = support(
    [claim_hierarchical_rejection_loop, claim_factor_3_parallel_validation_amplifies],
    claim_architectural_lesson,
    reason=(
        "The architectural lesson "
        "(@claim_architectural_lesson) -- focusing on worst-"
        "region + strict validation creates a coordination "
        "dead-end -- follows from: (i) the rejection-loop "
        "mechanism showing this trap concretely "
        "(@claim_hierarchical_rejection_loop); (ii) parallel "
        "exploration's amplifying effect "
        "(@claim_factor_3_parallel_validation_amplifies) "
        "providing the alternative that escapes the trap."
    ),
    prior=0.92,
)

# ============================================================================
# SECTION 7.7: FM-MAS synthesis
# ============================================================================

strat_fm_solves_action_enumeration = support(
    [claim_foundation_models_enable, claim_fm_capability_5_generative_flexibility],
    claim_fm_solves_action_enumeration,
    reason=(
        "FMs solving the MAS action-enumeration problem "
        "(@claim_fm_solves_action_enumeration) follows from: "
        "(i) the headline FM-enables claim "
        "(@claim_foundation_models_enable); (ii) FMs' "
        "generative flexibility "
        "(@claim_fm_capability_5_generative_flexibility) "
        "providing unbounded patch coverage. Traditional MAS "
        "coordination required explicit action enumeration; FMs "
        "remove that requirement by construction."
    ),
    prior=0.92,
)

strat_mas_solves_output_combination = support(
    [
        claim_pressure_as_potential_function,
        claim_pressure_vs_conversation_4x,
    ],
    claim_mas_solves_output_combination,
    reason=(
        "MAS coordination solving FM's output-combination "
        "problem (@claim_mas_solves_output_combination) follows "
        "from: (i) pressure being a *potential function* / "
        "objective criterion (@claim_pressure_as_potential_function); "
        "(ii) the empirical 4x advantage over conversation "
        "(@claim_pressure_vs_conversation_4x), which is exactly "
        "the prediction if dialogue is an ad-hoc combination "
        "strategy and pressure replaces it with an objective "
        "gradient."
    ),
    prior=0.9,
)

strat_fm_mas_synthesis = support(
    [
        claim_fm_solves_action_enumeration,
        claim_mas_solves_output_combination,
    ],
    claim_fm_mas_mutually_enabling,
    reason=(
        "The bidirectional FM-MAS synthesis claim "
        "(@claim_fm_mas_mutually_enabling) is the conjunction of: "
        "(i) FMs solve MAS's action-enumeration problem "
        "(@claim_fm_solves_action_enumeration); (ii) MAS solves "
        "FM's output-combination problem "
        "(@claim_mas_solves_output_combination). Both directions "
        "are essential: this is what 'mutually enabling, not "
        "merely additive' means."
    ),
    prior=0.92,
)

# ============================================================================
# CENTRAL ABDUCTION: pressure-field's gain over conversation/hierarchical
# is explained by FM + local-pressure-gradients (constraint-driven emergence),
# NOT by better-tuned LLM prompting / more compute / better evaluation.
# ============================================================================

# The 30x gap between pressure-field and hierarchical is on the SAME FM
# substrate and SAME 50-tick budget per problem -- the alternative
# explanations are explicitly controlled out by the fairness guarantees.

claim_pred_h_constraint_driven_emergence = claim(
    "**Hypothesis (H) prediction.** If 'constraint-driven "
    "emergence -- FM + local-pressure-gradients without explicit "
    "orchestration -- is the cause of the gain', the predicted "
    "fingerprint is: (i) order-of-magnitude gap (30x) between "
    "pressure-field and hierarchical *with identical FM substrate "
    "and identical tick budget*; (ii) the gap *widens* with "
    "difficulty (because explicit orchestration's overhead "
    "consumes a larger fraction of the budget on harder problems); "
    "(iii) decay ablation shows a directional benefit (because "
    "Theorem 5.3 predicts decay is necessary for basin escape); "
    "(iv) scaling agent count from 1 to 4 does not improve solve "
    "rates much (because $O(1)$ coordination overhead does not "
    "convert agents into linear throughput once base capability "
    "saturates).",
    title="Predicted fingerprint under H = 'constraint-driven emergence' (4 facts)",
)

claim_pred_alt_better_prompting = claim(
    "**Alternative (Alt) prediction.** If 'pressure-field is "
    "just better-tuned LLM prompting / more compute / better "
    "evaluation' is the cause, we'd expect: (i) the gap should "
    "*not* be 30x on identical substrate -- prompting "
    "differences typically produce 1.5-3x gaps; (ii) the gap "
    "should *narrow* with harder problems (because better "
    "prompting helps when the LLM is uncertain, but cannot "
    "overcome fundamental search-space scale); (iii) decay "
    "ablation should be meaningless (decay is not a prompting "
    "feature); (iv) scaling agent count from 1 to 4 should "
    "produce roughly 4x more compute and (at least slightly) "
    "more solves -- 'more compute' should manifest as "
    "throughput.",
    title="Predicted fingerprint under Alt = 'better-tuned prompting / more compute / better evaluation' (4 facts)",
)

claim_observed_fingerprint = claim(
    "**Observed empirical fingerprint (from Sections 6.2-6.6).** "
    "(i) The 30x gap *is* observed on identical FM substrate "
    "(same 0.5b/1.5b/3b qwen2.5 chain) with identical 50-tick "
    "budget; (ii) the gap *widens* with difficulty (53.4 pp on "
    "easy -> absolute (0%) on medium / hard); (iii) decay "
    "ablation shows the predicted directional benefit "
    "(96.7% -> 86.7%, $-10$ pp); (iv) scaling 1 -> 2 -> 4 agents "
    "yields 83.3% -> 93.3% -> 83.3% (CI-overlapping; *no* "
    "linear-throughput effect from added agents).",
    title="Observed fingerprint (Sections 6.2 / 6.4 / 6.6 / 6.3): 30x same-substrate gap, widens-with-difficulty, decay benefit, scaling-flat",
)

strat_observed_fingerprint_from_facts = support(
    [
        claim_pressure_vs_hierarchical_30x,
        claim_gap_widens_with_difficulty,
        claim_table_4_decay_ablation,
        claim_table_6_scaling,
    ],
    claim_observed_fingerprint,
    reason=(
        "The four-fact observed fingerprint "
        "(@claim_observed_fingerprint) is the package of: "
        "(i) the 30x same-substrate gap "
        "(@claim_pressure_vs_hierarchical_30x); "
        "(ii) the gap-widens-with-difficulty pattern "
        "(@claim_gap_widens_with_difficulty); "
        "(iii) the decay-ablation directional benefit "
        "(@claim_table_4_decay_ablation); "
        "(iv) the agent-count scaling pattern "
        "(@claim_table_6_scaling). All four are direct "
        "empirical readouts."
    ),
    prior=0.97,
)

s_h_explains = support(
    [claim_pred_h_constraint_driven_emergence],
    claim_observed_fingerprint,
    reason=(
        "Under the constraint-driven-emergence hypothesis "
        "(@claim_pred_h_constraint_driven_emergence), the four-"
        "fact fingerprint follows directly from the theory: same-"
        "substrate 30x gap is the FM-MAS synthesis effect; gap "
        "widens because explicit-orchestration overhead grows with "
        "problem complexity; decay benefit is a Theorem-5.3 "
        "prediction; scaling-flat is the $O(1)$ coordination-"
        "overhead signature of Theorem 5.4."
    ),
    prior=0.92,
)

s_alt_explains = support(
    [claim_pred_alt_better_prompting],
    claim_observed_fingerprint,
    reason=(
        "Under the better-prompting alternative "
        "(@claim_pred_alt_better_prompting), the observed "
        "fingerprint is hard to explain: prompting differences "
        "rarely produce 30x gaps on identical substrate; better "
        "prompting typically narrows the gap on harder problems "
        "(when LLM is most uncertain) rather than widens it; "
        "decay ablation has no prompting-side analog; flat "
        "scaling with agent count contradicts the 'more compute' "
        "story. Each fact is individually low-probability under "
        "Alt; their conjunction is far lower."
    ),
    prior=0.25,
)

comp_h_vs_alt = compare(
    claim_pred_h_constraint_driven_emergence,
    claim_pred_alt_better_prompting,
    claim_observed_fingerprint,
    reason=(
        "Comparison: H predicts the *signs and magnitudes* of "
        "all four facts (same-substrate 30x, gap-widens, decay-"
        "benefit, scaling-flat) by direct theoretical "
        "implication. Alt predicts the *opposite signs* on at "
        "least two facts (gap-widens-with-difficulty contradicts "
        "Alt's gap-narrowing prediction; scaling-flat "
        "contradicts Alt's more-compute prediction). H is "
        "decisively better at explaining the observed pattern."
    ),
    prior=0.93,
)

abd_central = abduction(
    s_h_explains,
    s_alt_explains,
    comp_h_vs_alt,
    reason=(
        "Both 'constraint-driven emergence' "
        "(@claim_pred_h_constraint_driven_emergence) and 'better "
        "prompting / more compute' "
        "(@claim_pred_alt_better_prompting) attempt to explain "
        "the observed empirical fingerprint "
        "(@claim_observed_fingerprint). The fairness guarantees "
        "(identical FM substrate, identical tick budget, "
        "identical prompts) discriminate sharply between them: "
        "the 30x same-substrate gap rules out 'better prompting' "
        "as a primary explanation; the gap-widens-with-"
        "difficulty pattern rules out 'more compute'; the "
        "scaling-flat pattern is a positive prediction of H "
        "(O(1) coordination overhead) and a negative prediction "
        "of Alt (more compute should help). Constraint-driven "
        "emergence is the better explanation."
    ),
)

# ============================================================================
# CONTRADICTIONS:
# (a) "explicit orchestration is necessary for MAS coordination" vs the
#     pressure-field demonstration of orchestration-free coordination
# (b) "coordination overhead is unavoidable in MAS" vs the convergence-
#     guarantee result with O(1) coordination overhead
# ============================================================================

claim_explicit_orchestration_is_necessary = claim(
    "**Contrarian (literature-implied) claim: explicit orchestration "
    "is necessary for MAS coordination.** The dominant MAS-LLM "
    "literature (AutoGen [@AutoGen], MetaGPT [@MetaGPT], CAMEL "
    "[@CAMEL], CrewAI [@CrewAI]) presupposes that effective multi-"
    "agent coordination *requires* a planner / coordinator / "
    "manager role and explicit message passing. Under this "
    "assumption, removing explicit orchestration should degrade "
    "coordination quality.",
    title="Literature-implied claim: 'explicit orchestration is necessary for MAS coordination'",
)

claim_pressure_field_demonstration = claim(
    "**Pressure-field demonstration: orchestration-free "
    "coordination outperforms explicit orchestration.** The "
    "empirical fact (Tables 3, 8): pressure-field -- *with no "
    "coordinator, no planner, no message passing, no role "
    "assignment* -- achieves 48.5% aggregate solve rate vs "
    "hierarchical's 1.5% (30x gap, $p < 0.001$) and "
    "conversation's 11.1% (4x gap, $p < 0.001$).",
    title="Empirical demonstration: orchestration-free coordination outperforms explicit orchestration (48.5% vs 1.5% / 11.1%)",
)

contra_explicit_necessity = contradiction(
    claim_explicit_orchestration_is_necessary,
    claim_pressure_field_demonstration,
    reason=(
        "If 'explicit orchestration is necessary for MAS "
        "coordination' (@claim_explicit_orchestration_is_necessary) "
        "is true, then orchestration-free coordination cannot "
        "*outperform* explicit orchestration. The pressure-field "
        "demonstration (@claim_pressure_field_demonstration) -- "
        "30x gap over hierarchical, 4x over conversation, with "
        "no coordinator / planner / message passing -- "
        "contradicts the necessity claim directly. Both cannot "
        "be true."
    ),
    prior=0.97,
)

claim_coordination_overhead_unavoidable = claim(
    "**Contrarian claim: coordination overhead is unavoidable in "
    "MAS.** A common assumption: $n$-agent MAS coordination "
    "*must* incur at least $\\Omega(n \\log n)$ communication "
    "cost (the GPGP [@GPGP] hierarchical-aggregation lower bound) "
    "-- or, in the pairwise-message-passing limit, $\\Omega(n^2)$. "
    "Under this assumption, $O(1)$ coordination overhead is "
    "infeasible.",
    title="Contrarian claim: 'coordination overhead is unavoidable in MAS' (>= O(n log n) communication)",
)

claim_o1_overhead_with_convergence = claim(
    "**Pressure-field result: $O(1)$ coordination overhead **plus** "
    "formal convergence guarantee.** Theorem 5.4 establishes "
    "$O(1)$ inter-agent coordination overhead (no messages); "
    "Theorems 5.1 and 5.5 establish convergence to a stable "
    "basin in $T \\le P_0 / (\\delta_{\\min} - (n-1)\\epsilon)$ "
    "ticks (sequentially) or $T \\le P_0 / (K \\cdot "
    "(\\delta_{\\min} - (n-1)\\epsilon))$ (parallel). "
    "Empirically, the 1350-trial study confirms the result on a "
    "constraint-satisfaction task.",
    title="Result: pressure-field achieves O(1) coordination overhead WITH formal convergence guarantee (theorems 5.1-5.5)",
)

contra_overhead_unavoidable = contradiction(
    claim_coordination_overhead_unavoidable,
    claim_o1_overhead_with_convergence,
    reason=(
        "If 'coordination overhead is unavoidable in MAS' "
        "(@claim_coordination_overhead_unavoidable) is true, "
        "$O(1)$ coordination overhead with formal convergence "
        "guarantees should be impossible. But Theorem 5.4 "
        "explicitly establishes $O(1)$ inter-agent overhead "
        "(@claim_o1_overhead_with_convergence) and Theorems "
        "5.1 / 5.5 establish convergence under that overhead. "
        "Both cannot be true. The literature claim assumed "
        "agents must exchange messages; pressure-field shows "
        "they can coordinate through *shared state* alone, "
        "evading the lower bound."
    ),
    prior=0.97,
)

# ============================================================================
# Conclusion synthesis
# ============================================================================

strat_conclusion_synthesis = support(
    [
        claim_table_3_aggregate_solve_rates,
        claim_table_8_difficulty_breakdown,
        claim_fm_mas_mutually_enabling,
        claim_only_pressure_field_scales,
    ],
    claim_conclusion_synthesis,
    reason=(
        "The conclusion synthesis "
        "(@claim_conclusion_synthesis) -- implicit coordination "
        "outperforms explicit coordination on constraint "
        "satisfaction with locality -- combines: (i) the "
        "aggregate solve-rate table "
        "(@claim_table_3_aggregate_solve_rates); (ii) the per-"
        "difficulty breakdown "
        "(@claim_table_8_difficulty_breakdown); (iii) the FM-MAS "
        "synthesis (@claim_fm_mas_mutually_enabling); (iv) the "
        "cross-tier 'only pressure-field scales' law "
        "(@claim_only_pressure_field_scales). Each piece "
        "contributes a different facet of the conclusion."
    ),
    prior=0.92,
)

# ============================================================================
# 4 stated contributions: composite of headline claims
# ============================================================================

strat_four_contributions = support(
    [
        claim_pressure_field_proposal,
        claim_decay_necessity_argument,
        claim_theorem_5_1_convergence,
        claim_table_3_aggregate_solve_rates,
    ],
    claim_four_contributions,
    reason=(
        "The four stated contributions "
        "(@claim_four_contributions) are the conjunction of: "
        "(C1) pressure-field as a method "
        "(@claim_pressure_field_proposal); "
        "(C2) temporal decay as a mechanism, justified by "
        "Theorem 5.3 (@claim_decay_necessity_argument); "
        "(C3) convergence theorem "
        "(@claim_theorem_5_1_convergence); "
        "(C4) 1350-trial empirical evidence "
        "(@claim_table_3_aggregate_solve_rates)."
    ),
    prior=0.95,
)


# ============================================================================
# Wire the remaining orphan claims (Pass 3 completeness fixes)
# ============================================================================

strat_result_contradicts_assumption = support(
    [claim_pressure_vs_hierarchical_30x],
    claim_result_contradicts_explicit_orchestration_assumption,
    reason=(
        "The result-contradicts-assumption claim "
        "(@claim_result_contradicts_explicit_orchestration_assumption) "
        "follows directly from the 30x pairwise gap "
        "(@claim_pressure_vs_hierarchical_30x): if explicit "
        "hierarchical coordination were necessary, no implicit "
        "alternative would beat it by 30x on the same substrate "
        "and same budget. The empirical 30x gap is the contradiction."
    ),
    prior=0.95,
)

strat_table_10_final_pressure_supports_only_scales = support(
    [claim_table_10_final_pressure],
    claim_only_pressure_field_scales,
    reason=(
        "Table 10 (@claim_table_10_final_pressure) provides an "
        "additional independent line of evidence for the cross-"
        "tier 'only pressure-field scales' law "
        "(@claim_only_pressure_field_scales): pressure-field's "
        "final pressure is 35-200x lower than baselines on every "
        "difficulty tier. Even when the binary solve metric reads "
        "0 / 0, pressure-field reaches a much higher-quality "
        "partial solution -- consistent with the cross-tier "
        "scaling pattern."
    ),
    prior=0.92,
)

strat_effect_sizes_large_supports_4x = support(
    [claim_effect_sizes_large],
    claim_pressure_vs_conversation_4x,
    reason=(
        "Cohen's $h = 1.16$ on easy versus conversation "
        "(@claim_effect_sizes_large) is part of the same "
        "evidence package as the 4x ratio "
        "(@claim_pressure_vs_conversation_4x): both come from "
        "the per-strategy aggregate / easy-tier solve-rate "
        "tables, and both express the same magnitude of "
        "advantage."
    ),
    prior=0.95,
)

strat_distributed_gd_supports_o1 = support(
    [claim_distributed_gd_requires_protocols],
    claim_pressure_field_o1_overhead,
    reason=(
        "Distributed gradient descent's protocol/synchronization "
        "requirement (@claim_distributed_gd_requires_protocols) "
        "is the foil for pressure-field's $O(1)$ overhead "
        "(@claim_pressure_field_o1_overhead): both methods solve "
        "decentralized optimization, but pressure-field eliminates "
        "the explicit communication that distributed GD requires."
    ),
    prior=0.85,
)

strat_malone_crowston_supports_potential = support(
    [claim_malone_crowston_shared_resource],
    claim_pressure_as_potential_function,
    reason=(
        "Pressure-field instantiating the Malone-Crowston shared-"
        "resource pattern (@claim_malone_crowston_shared_resource) "
        "is a precondition for treating $P(s)$ as a potential "
        "function (@claim_pressure_as_potential_function): the "
        "shared-resource pattern provides the multi-agent "
        "coordination semantics that the potential-game "
        "framework formalizes."
    ),
    prior=0.85,
)

strat_economic_termination_from_decay = support(
    [claim_algorithm_three_properties],
    claim_economic_termination,
    reason=(
        "Economic termination "
        "(@claim_economic_termination) follows from Phase 1 "
        "decay (@setup_phase_1_decay) plus the algorithm's "
        "three core properties "
        "(@claim_algorithm_three_properties): when decay is "
        "balanced by reinforcement and pressure gradients "
        "flatten, no patches are applied even though the system "
        "has not declared a goal -- the system stops because "
        "the cost of action exceeds benefit, not because of a "
        "logical termination condition."
    ),
    prior=0.9,
    background=[setup_phase_1_decay],
)

strat_negative_pheromones_design_from_setup = support(
    [claim_model_choice_rationale],
    claim_negative_pheromones_design,
    reason=(
        "Negative pheromones use positive language "
        "(@claim_negative_pheromones_design) because of the "
        "small-model choice (@claim_model_choice_rationale): "
        "small (1.5b parameter) models reportedly struggle with "
        "'AVOID X' instructions, so the design reframes them as "
        "'TIP: try Y instead' to fit the substrate."
    ),
    prior=0.9,
    background=[setup_negative_pheromones],
)

strat_when_pressure_field_from_results = support(
    [
        claim_table_3_aggregate_solve_rates,
        claim_alignment_separability,
        claim_pressure_field_o1_overhead,
    ],
    claim_when_pressure_field,
    reason=(
        "The when-to-prefer-pressure-field guidance "
        "(@claim_when_pressure_field) follows from: "
        "(i) the 3-30x performance advantage on the empirical "
        "table (@claim_table_3_aggregate_solve_rates) -- "
        "performance criterion; (ii) separable pressure / "
        "locality (@claim_alignment_separability) -- "
        "decomposability criterion; (iii) $O(1)$ coordination "
        "overhead (@claim_pressure_field_o1_overhead) -- "
        "fault-tolerance and simplicity criterion."
    ),
    prior=0.92,
)

strat_when_hierarchical_from_limitations = support(
    [claim_limitation_domain_specificity],
    claim_when_hierarchical,
    reason=(
        "The when-to-prefer-hierarchical guidance "
        "(@claim_when_hierarchical) follows from the domain-"
        "specificity limitation "
        "(@claim_limitation_domain_specificity): tasks lacking "
        "locality or requiring global planning -- and tasks "
        "where explicit control or interpretability is mandated "
        "-- fall outside pressure-field's regime, leaving "
        "hierarchical (or other explicit-orchestration) "
        "approaches as the appropriate choice."
    ),
    prior=0.85,
)

strat_limitations_implied_by_hard_solve_rate = support(
    [claim_hard_pressure_field_15_6],
    claim_limitation_modest_hard_solve_rate,
    reason=(
        "The limitation that absolute solve rates are modest on "
        "hard problems (@claim_limitation_modest_hard_solve_rate) "
        "is read directly from the hard-tier observation "
        "(@claim_hard_pressure_field_15_6): 15.6% is the "
        "absolute number that motivates the limitation."
    ),
    prior=0.97,
)

strat_decay_miscalibration_from_decay_argument = support(
    [claim_decay_necessity_argument, claim_table_4_decay_ablation],
    claim_limitation_decay_miscalibration,
    reason=(
        "The decay-miscalibration limitation "
        "(@claim_limitation_decay_miscalibration) follows from "
        "(i) the decay-necessity argument "
        "(@claim_decay_necessity_argument) showing too-slow "
        "decay traps in suboptimal basins; (ii) the ablation "
        "(@claim_table_4_decay_ablation) showing the directional "
        "effect. The mirror failure (too-fast decay producing "
        "perpetual oscillation) is symmetric."
    ),
    prior=0.85,
)

strat_trajectory_level_risks_from_validation = support(
    [claim_algorithm_three_properties],
    claim_limitation_trajectory_level_risks,
    reason=(
        "Trajectory-level risks "
        "(@claim_limitation_trajectory_level_risks) follow from "
        "the per-step nature of the validation phase "
        "(@setup_phase_3_validation) and the algorithm-three-"
        "properties description "
        "(@claim_algorithm_three_properties): validation tests "
        "each patch on its own fork, so coherence drift / "
        "emergent gaming / dependency accumulation patterns "
        "that span many patches escape per-step rejection."
    ),
    prior=0.9,
    background=[setup_phase_3_validation],
)

strat_other_practical_limitations_from_setup = support(
    [claim_algorithm_three_properties],
    claim_other_practical_limitations,
    reason=(
        "The additional practical limitations "
        "(@claim_other_practical_limitations) -- hand-designed "
        "pressure functions, decay-rate tuning, parallel-"
        "validation memory cost -- are direct corollaries of the "
        "pressure-function design "
        "(@setup_meeting_pressure_function) and the algorithm-"
        "three-properties description "
        "(@claim_algorithm_three_properties)."
    ),
    prior=0.9,
    background=[setup_meeting_pressure_function],
)

strat_societal_accountability_from_o1 = support(
    [claim_pressure_field_o1_overhead],
    claim_societal_accountability,
    reason=(
        "Accountability diffusion "
        "(@claim_societal_accountability) follows from the "
        "$O(1)$ inter-agent coordination overhead "
        "(@claim_pressure_field_o1_overhead): coordination "
        "without explicit delegation removes the natural "
        "accountability chain that hierarchical paradigms "
        "provide."
    ),
    prior=0.88,
)

strat_societal_goodhart_from_pressure = support(
    [claim_pressure_field_proposal],
    claim_societal_goodhart,
    reason=(
        "Goodhart-gaming risk "
        "(@claim_societal_goodhart) follows from the pressure-"
        "field proposal (@claim_pressure_field_proposal): if "
        "agents are optimized to reduce designer-specified "
        "pressure, any imperfection in the pressure function "
        "becomes a target. FMs amplify this concern via their "
        "internet-scale-text-based implicit knowledge of "
        "benchmark patterns."
    ),
    prior=0.9,
)

strat_societal_explainability_from_design = support(
    [claim_pressure_field_proposal],
    claim_societal_explainability,
    reason=(
        "The explainability concern "
        "(@claim_societal_explainability) follows from the "
        "pressure-field proposal "
        "(@claim_pressure_field_proposal): coordination through "
        "shared state rather than delegation chains makes "
        "explanations mechanistically transparent (what each "
        "agent did) but causally opaque (why it chose that "
        "patch)."
    ),
    prior=0.88,
)

strat_model_choice_rationale_from_proposal = support(
    [claim_pressure_field_proposal, claim_foundation_models_enable],
    claim_model_choice_rationale,
    reason=(
        "The model-choice rationale "
        "(@claim_model_choice_rationale) -- using small models to "
        "isolate coordination effects -- depends on (i) the "
        "pressure-field proposal "
        "(@claim_pressure_field_proposal) being orthogonal to "
        "model capability; and (ii) FMs of different scales all "
        "enabling stigmergic patches "
        "(@claim_foundation_models_enable). If any of these were "
        "false, small-model results would not support the "
        "general thesis."
    ),
    prior=0.88,
)

