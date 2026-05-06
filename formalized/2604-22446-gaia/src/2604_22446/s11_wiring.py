"""Pass 2-5 wiring: strategies, deductions, inductions, abductions,
contradictions linking the propositions extracted across the per-section
modules into the reasoning graph.

Key wiring blocks:
* Motivation: skills + existing-MAS landscape => missing-organisation diagnosis
* Section 2.1: typed-interface architecture => identity-substrate decoupling
* Section 2.2-2.2.4: AND-tree + FSM + circuit breakers => termination + deadlock-freedom (deductions)
* Section 3.2: Table 2 panel => OMC > all 12 baselines (induction over baselines)
* Section 3.3: 4 case studies => cross-domain generality (induction over domains)
* Central abduction: organisational-decoupling vs bigger-LM/more-compute alternative
* Two contradictions: fixed-team-sufficient vs OMC's dynamic-organisational gain;
  tightly-coupled-coordination-required vs the typed-interface deployment
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
# Imports
# ---------------------------------------------------------------------------

from .motivation import (
    setup_individual_skills_advances,
    setup_existing_mas_paradigm,
    claim_skills_within_agent_only,
    claim_existing_mas_three_limits,
    claim_dynamic_workflow_still_bounded,
    claim_missing_organisation_layer,
    setup_ai_organisation_definition,
    claim_omc_proposal,
    claim_three_pillars,
    claim_organisation_decoupling_thesis,
    claim_headline_prdbench,
    claim_three_design_aspects_drive_result,
    claim_three_stated_contributions,
)
from .s2_related_work import (
    setup_three_related_work_dimensions,
    claim_heterogeneity_only_at_model_level,
    claim_protocol_and_marketplace_landscape,
    claim_team_composition_spectrum,
    claim_omc_fills_heterogeneity_gap,
    claim_dynamic_decomposition_landscape,
    claim_omc_fills_coordination_gap,
    claim_individual_evolution_landscape,
    claim_organisation_evolution_underdeveloped,
    claim_omc_fills_evolution_gap,
    claim_table_4_architectural_comparison,
    claim_three_structural_gaps_summary,
    claim_lit_fixed_team_assumption,
    claim_lit_tightly_coupled_coordination,
)
from .s3_setup import (
    setup_employee_definition,
    setup_talent_definition,
    setup_container_definition,
    setup_talent_market_definition,
    setup_three_pillars_architecture,
    claim_radical_heterogeneity_challenge,
    claim_typed_layer_solves_heterogeneity,
)
from .s4_talent_abstraction import (
    setup_six_typed_interfaces,
    setup_algorithm_1_talent_assembly,
    claim_property_1_identity_substrate_separation,
    claim_property_2_multi_tenancy_isolation,
    claim_property_3_extensibility,
    claim_os_kernel_correspondence,
    claim_talent_market_grounding,
    claim_three_sourcing_channels,
    claim_human_in_loop_recruitment,
    claim_table_1_skills_vs_talents,
    claim_typed_interface_decoupling_demonstration,
)
from .s5_e2r_tree_search import (
    setup_organisational_search_space,
    setup_e2r_mcts_analogy,
    setup_tree_definition,
    setup_two_edge_types,
    setup_five_action_types,
    setup_strategy_and_transition,
    setup_policy_pi,
    claim_stage_1_explore,
    claim_stage_2_execute,
    claim_stage_3_review,
    claim_top_down_bottom_up_unification,
    setup_policy_update_function,
    claim_external_oracle_role,
    setup_three_circuit_breakers,
    claim_circuit_breakers_imply_bounded_termination,
    setup_iteration_function_iter,
)
from .s6_dag_and_guarantees import (
    setup_and_tree_dag_dependency,
    setup_and_semantics,
    setup_task_lifecycle_fsm,
    setup_scheduling_predicate,
    setup_bottom_up_propagation,
    setup_deadlock_detector,
    claim_invariant_1_dag,
    claim_invariant_2_mutual_exclusion,
    claim_invariant_3_schedule_idempotency,
    claim_invariant_4_review_termination,
    claim_invariant_5_cascade_completeness,
    claim_invariant_6_dependency_completeness,
    claim_invariant_7_recovery_correctness,
    claim_theorem_termination,
    claim_theorem_deadlock_freedom,
    claim_crash_recovery_property,
    claim_mirrors_human_enterprise,
)
from .s7_self_evolution import (
    setup_two_individual_triggers,
    claim_individual_evolution_modifies_talent_artefacts,
    setup_project_retrospective,
    claim_org_knowledge_accumulates_across_projects,
    setup_hr_performance_pipeline,
    claim_hr_pipeline_closes_market_loop,
    claim_three_level_evolution_summary,
)
from .s8_evaluation_setup import (
    setup_prdbench_benchmark,
    setup_each_prdbench_is_wild_dynamic,
    setup_omc_agent_setup,
    setup_dev_mode,
    setup_baseline_panel,
    setup_four_case_studies,
)
from .s9_main_results import (
    claim_table_2_prdbench,
    claim_omc_beats_minimal_best,
    claim_omc_beats_codex,
    claim_omc_beats_claude_code,
    claim_omc_beats_gemini_minimal,
    claim_omc_beats_gemini_cli,
    claim_omc_beats_all_baselines,
    claim_design_aspect_dynamic_decomposition,
    claim_design_aspect_review_gate,
    claim_design_aspect_cross_family,
    claim_case_content_generation_result,
    claim_case_game_development_result,
    claim_case_audiobook_result,
    claim_case_research_survey_result,
    claim_cross_case_pattern,
)
from .s10_discussion import (
    claim_limitation_only_prdbench_quant,
    claim_limitation_self_evolution_not_ablated,
    claim_cost_performance_tradeoff,
    claim_human_enterprise_analogy_general,
    claim_open_questions,
    claim_pred_h_organisational_decoupling_drives,
    claim_pred_alt_bigger_lm_or_more_compute,
    claim_observed_fingerprint,
    claim_omc_demonstration_dynamic_org_works,
    claim_omc_typed_interfaces_demonstration,
    claim_conclusion_synthesis,
)


# ============================================================================
# SECTION 1 (Motivation): three-limits diagnosis -> missing-organisation gap
# ============================================================================

strat_existing_mas_three_limits_imply_missing_layer = support(
    [
        claim_existing_mas_three_limits,
        claim_dynamic_workflow_still_bounded,
        claim_skills_within_agent_only,
    ],
    claim_missing_organisation_layer,
    background=[setup_existing_mas_paradigm, setup_individual_skills_advances],
    reason=(
        "The diagnosis that an organisation-level abstraction is "
        "missing (@claim_missing_organisation_layer) follows from "
        "(i) skills only operate inside one agent "
        "(@claim_skills_within_agent_only), (ii) existing MAS face "
        "fixed-team brittleness, runtime lock-in, and session-bound "
        "learning (@claim_existing_mas_three_limits), and (iii) "
        "even dynamic agentic workflows remain pre-configured "
        "(team / runtime / template fixed before execution) "
        "(@claim_dynamic_workflow_still_bounded). Together these "
        "exhaust the candidate places where the organisation layer "
        "could otherwise live."
    ),
    prior=0.92,
)


# ============================================================================
# SECTION 2.1 (Talent abstraction): typed interfaces -> three properties
# ============================================================================

strat_six_interfaces_yield_p1 = support(
    [claim_radical_heterogeneity_challenge],
    claim_property_1_identity_substrate_separation,
    background=[setup_six_typed_interfaces, setup_algorithm_1_talent_assembly],
    reason=(
        "Identity-substrate separation "
        "(@claim_property_1_identity_substrate_separation) follows "
        "from the typed interfaces (@setup_six_typed_interfaces): "
        "all agent-platform interaction routes through "
        "Execution / Task / Event / Storage / Context / Lifecycle, "
        "so identity (the Talent) is fixed by data (prompts + "
        "principles + tools + skills) and substrate (the Container) "
        "is fixed by code implementing the six contracts -- "
        "orthogonal axes by construction. Algorithm 1 "
        "(@setup_algorithm_1_talent_assembly) realises the "
        "composition during one task execution."
    ),
    prior=0.92,
)

strat_six_interfaces_yield_p2 = support(
    [claim_radical_heterogeneity_challenge],
    claim_property_2_multi_tenancy_isolation,
    background=[setup_six_typed_interfaces],
    reason=(
        "Multi-tenancy with isolation "
        "(@claim_property_2_multi_tenancy_isolation) follows from "
        "the six typed interfaces being the only communication "
        "channel: pre-hooks (@setup_six_typed_interfaces) gate "
        "validation; post-hooks gate audit/self-improvement; the "
        "Task interface gates queue access; the Storage interface "
        "gates memory. There is no API outside the six contracts, "
        "so no Container can bypass organisational policies."
    ),
    prior=0.93,
)

strat_six_interfaces_yield_p3 = support(
    [claim_radical_heterogeneity_challenge],
    claim_property_3_extensibility,
    background=[setup_six_typed_interfaces],
    reason=(
        "Extensibility without platform modification "
        "(@claim_property_3_extensibility) follows from the typed "
        "contracts: a new runtime needs only to implement the six "
        "interfaces -- no platform code changes elsewhere. The "
        "lifecycle hooks let self-improvement (working-principle "
        "refinement, skill accumulation) live entirely at the "
        "organisational layer."
    ),
    prior=0.92,
)

strat_typed_interfaces_demonstration = support(
    [
        claim_property_1_identity_substrate_separation,
        claim_property_2_multi_tenancy_isolation,
        claim_property_3_extensibility,
        claim_os_kernel_correspondence,
    ],
    claim_typed_interface_decoupling_demonstration,
    reason=(
        "The deployment claim "
        "(@claim_typed_interface_decoupling_demonstration) is "
        "underwritten by the three architectural properties "
        "(@claim_property_1_identity_substrate_separation; "
        "@claim_property_2_multi_tenancy_isolation; "
        "@claim_property_3_extensibility) plus the OS-kernel "
        "correspondence (@claim_os_kernel_correspondence) "
        "demonstrating the design has the same structural shape as "
        "well-understood OS abstractions [@TanenbaumOS; "
        "@SilberschatzOS]."
    ),
    prior=0.92,
)

strat_typed_layer_solves_challenge = support(
    [claim_typed_interface_decoupling_demonstration, claim_radical_heterogeneity_challenge],
    claim_typed_layer_solves_heterogeneity,
    reason=(
        "The typed organisational layer claim "
        "(@claim_typed_layer_solves_heterogeneity) follows from "
        "the demonstration that decoupling identity from runtime "
        "is feasible "
        "(@claim_typed_interface_decoupling_demonstration) "
        "addressing the radical heterogeneity challenge "
        "(@claim_radical_heterogeneity_challenge). The OS-kernel "
        "analogy makes the structural correspondence explicit."
    ),
    prior=0.92,
)

strat_omc_fills_het_gap_from_landscape = support(
    [
        claim_heterogeneity_only_at_model_level,
        claim_protocol_and_marketplace_landscape,
        claim_team_composition_spectrum,
        claim_typed_interface_decoupling_demonstration,
        claim_three_sourcing_channels,
        claim_table_4_architectural_comparison,
        claim_table_1_skills_vs_talents,
        claim_talent_market_grounding,
        claim_human_in_loop_recruitment,
    ],
    claim_omc_fills_heterogeneity_gap,
    reason=(
        "OMC fills the three heterogeneity gaps "
        "(@claim_omc_fills_heterogeneity_gap) because (i) prior "
        "work supports model-level heterogeneity only "
        "(@claim_heterogeneity_only_at_model_level); (ii) prior "
        "marketplaces handle tools but not full agent packages "
        "(@claim_protocol_and_marketplace_landscape); (iii) prior "
        "team-composition designs do not bootstrap with a founding "
        "team (@claim_team_composition_spectrum); and OMC supplies "
        "(a) typed-interface decoupling "
        "(@claim_typed_interface_decoupling_demonstration), (b) "
        "three Talent-sourcing channels "
        "(@claim_three_sourcing_channels), and (c) a founding "
        "C-suite per Section 2 setup."
    ),
    prior=0.9,
)


# ============================================================================
# SECTION 2.2.4 (DAG layer): seven invariants -> formal theorems
# ============================================================================

deduct_termination = deduction(
    [
        claim_invariant_4_review_termination,
        claim_circuit_breakers_imply_bounded_termination,
        claim_invariant_2_mutual_exclusion,
    ],
    claim_theorem_termination,
    background=[
        setup_task_lifecycle_fsm,
        setup_and_semantics,
        setup_three_circuit_breakers,
    ],
    reason=(
        "Termination (@claim_theorem_termination) follows by "
        "composition: (i) the FSM (@setup_task_lifecycle_fsm) "
        "bounds retries via $k_{retry}$; (ii) review-round "
        "termination (@claim_invariant_4_review_termination) "
        "bounds review escalations via $k_{rev}$; (iii) the three "
        "circuit breakers "
        "(@claim_circuit_breakers_imply_bounded_termination, "
        "@setup_three_circuit_breakers) bound wall-clock per node "
        "and total cost. Under the executor-respects-timeout "
        "assumption every task node reaches a terminal state in "
        "$F = \\{finished, cancelled\\}$ in bounded time/cost; the "
        "AND-semantics (@setup_and_semantics) then propagate "
        "completion bottom-up so the project root reaches a "
        "terminal state under the same bounds. Pure deduction from "
        "the FSM + breakers + AND-semantics."
    ),
    prior=0.99,
)

deduct_deadlock_freedom = deduction(
    [
        claim_invariant_1_dag,
        claim_invariant_6_dependency_completeness,
        claim_invariant_5_cascade_completeness,
    ],
    claim_theorem_deadlock_freedom,
    background=[
        setup_and_tree_dag_dependency,
        setup_scheduling_predicate,
        setup_deadlock_detector,
    ],
    reason=(
        "Deadlock-freedom (@claim_theorem_deadlock_freedom) "
        "follows from: (i) DAG invariant I1 "
        "(@claim_invariant_1_dag) so the dependency graph admits a "
        "topological order; (ii) dependency completeness I6 "
        "(@claim_invariant_6_dependency_completeness) ensuring "
        "every resolved-state transition triggers forward "
        "resolution -- so no node with all dependencies resolved "
        "is left permanently pending; (iii) the deadlock detector "
        "(@setup_deadlock_detector) converts any reachable state "
        "where every non-root is terminal/blocked but the root "
        "remains unresolved into a `failed` terminal state, "
        "eliminating silent stalls. Pure deduction from the DAG "
        "structure + scheduling rules + safety net."
    ),
    prior=0.99,
)

strat_crash_recovery = support(
    [
        claim_invariant_3_schedule_idempotency,
        claim_invariant_7_recovery_correctness,
    ],
    claim_crash_recovery_property,
    reason=(
        "Crash recovery (@claim_crash_recovery_property) follows "
        "from idempotency I3 "
        "(@claim_invariant_3_schedule_idempotency) -- so "
        "re-scheduling never duplicates execution -- and recovery "
        "correctness I7 (@claim_invariant_7_recovery_correctness) "
        "-- so processing nodes reset to pending and dependent-"
        "ready nodes are re-scheduled. Together they yield a "
        "consistent post-crash resumption."
    ),
    prior=0.95,
)

strat_e2r_unifies_loop = support(
    [
        claim_stage_1_explore,
        claim_stage_2_execute,
        claim_stage_3_review,
    ],
    claim_top_down_bottom_up_unification,
    background=[setup_iteration_function_iter],
    reason=(
        "The unification claim "
        "(@claim_top_down_bottom_up_unification) follows from the "
        "three stages: Explore decomposes top-down "
        "(@claim_stage_1_explore), Execute carries out the work "
        "(@claim_stage_2_execute), and Review aggregates results "
        "bottom-up (@claim_stage_3_review). The composite "
        "iteration function $\\mathcal{I}$ "
        "(@setup_iteration_function_iter) wires them into one loop."
    ),
    prior=0.94,
)

strat_omc_fills_coord_gap = support(
    [
        claim_dynamic_decomposition_landscape,
        claim_theorem_termination,
        claim_theorem_deadlock_freedom,
    ],
    claim_omc_fills_coordination_gap,
    reason=(
        "OMC fills the coordination gap "
        "(@claim_omc_fills_coordination_gap) because prior dynamic "
        "decomposition systems lack formal completion guarantees "
        "(@claim_dynamic_decomposition_landscape), while OMC "
        "supplies both termination "
        "(@claim_theorem_termination) and deadlock-freedom "
        "(@claim_theorem_deadlock_freedom) under dynamic task-tree "
        "expansion."
    ),
    prior=0.93,
)

strat_mirrors_human_enterprise = support(
    [
        claim_top_down_bottom_up_unification,
        claim_theorem_termination,
        claim_theorem_deadlock_freedom,
    ],
    claim_mirrors_human_enterprise,
    reason=(
        "The mirrors-human-enterprise claim "
        "(@claim_mirrors_human_enterprise) follows from the "
        "structural correspondence: top-down decomposition + "
        "bottom-up review (@claim_top_down_bottom_up_unification) "
        "matches manage-plan-deliver-review; termination and "
        "deadlock-freedom (@claim_theorem_termination, "
        "@claim_theorem_deadlock_freedom) provide the formal "
        "guarantees human enterprises rely on but rarely formalise."
    ),
    prior=0.88,
)


# ============================================================================
# SECTION 2.3 (Self-evolution): three-level synthesis
# ============================================================================

strat_three_level_evolution = support(
    [
        claim_individual_evolution_modifies_talent_artefacts,
        claim_org_knowledge_accumulates_across_projects,
        claim_hr_pipeline_closes_market_loop,
    ],
    claim_three_level_evolution_summary,
    background=[
        setup_two_individual_triggers,
        setup_project_retrospective,
        setup_hr_performance_pipeline,
    ],
    reason=(
        "The three-level synthesis "
        "(@claim_three_level_evolution_summary) is the conjunction "
        "of: (L1) individual Talent-artefact updates "
        "(@claim_individual_evolution_modifies_talent_artefacts) "
        "via CEO one-on-ones + post-task reflection "
        "(@setup_two_individual_triggers); (L2) organisational SOP "
        "accumulation "
        "(@claim_org_knowledge_accumulates_across_projects) via "
        "project retrospectives (@setup_project_retrospective); "
        "(L3) HR pipeline closing the market loop "
        "(@claim_hr_pipeline_closes_market_loop) via periodic "
        "review + PIP + offboarding "
        "(@setup_hr_performance_pipeline)."
    ),
    prior=0.92,
)

strat_omc_fills_evolution_gap = support(
    [
        claim_individual_evolution_landscape,
        claim_organisation_evolution_underdeveloped,
        claim_three_level_evolution_summary,
        claim_individual_evolution_modifies_talent_artefacts,
        claim_org_knowledge_accumulates_across_projects,
        claim_hr_pipeline_closes_market_loop,
    ],
    claim_omc_fills_evolution_gap,
    reason=(
        "OMC fills the evolution gap "
        "(@claim_omc_fills_evolution_gap) because (i) prior work "
        "develops individual self-improvement well "
        "(@claim_individual_evolution_landscape) but (ii) "
        "organisation-level evolution is underdeveloped "
        "(@claim_organisation_evolution_underdeveloped), while "
        "OMC implements all three levels "
        "(@claim_three_level_evolution_summary) including the "
        "novel HR-pipeline-driven systemic level."
    ),
    prior=0.92,
)


# ============================================================================
# Three-pillar OMC proposal aggregates
# ============================================================================

strat_three_pillars_aggregate = support(
    [
        claim_typed_interface_decoupling_demonstration,
        claim_top_down_bottom_up_unification,
        claim_three_level_evolution_summary,
    ],
    claim_three_pillars,
    background=[setup_three_pillars_architecture],
    reason=(
        "The three-pillar architecture (@claim_three_pillars) is "
        "the conjunction of: Pillar 1 (typed Talent-Container "
        "demonstration, "
        "@claim_typed_interface_decoupling_demonstration); Pillar "
        "2 (E2R unification, "
        "@claim_top_down_bottom_up_unification); Pillar 3 "
        "(three-level evolution, "
        "@claim_three_level_evolution_summary). Each pillar is "
        "individually established by Sections 2.1-2.3."
    ),
    prior=0.94,
)

strat_omc_proposal_from_pillars = support(
    [claim_three_pillars],
    claim_omc_proposal,
    background=[
        setup_employee_definition,
        setup_talent_definition,
        setup_container_definition,
        setup_talent_market_definition,
    ],
    reason=(
        "The OMC proposal (@claim_omc_proposal) is the union of "
        "the three core abstractions (Employee = Talent + "
        "Container, plus the Talent Market) operating under the "
        "three pillars (@claim_three_pillars). The proposal is the "
        "engineering instantiation of the three-pillar design."
    ),
    prior=0.95,
)

strat_decoupling_thesis_from_proposal = support(
    [claim_omc_proposal, claim_typed_interface_decoupling_demonstration],
    claim_organisation_decoupling_thesis,
    background=[setup_ai_organisation_definition],
    reason=(
        "The decoupling thesis "
        "(@claim_organisation_decoupling_thesis) follows from "
        "(i) the OMC proposal (@claim_omc_proposal) realises the "
        "decoupling concretely; (ii) the typed-interface "
        "demonstration "
        "(@claim_typed_interface_decoupling_demonstration) shows "
        "the decoupling is *practical* (deployed across three "
        "Container families)."
    ),
    prior=0.9,
)


# ============================================================================
# SECTION 3.2 (Main results): induction over per-baseline contrasts
# ============================================================================

# Each per-baseline gap is an observation that the panel-wide law predicts;
# induction direction: support([law], observation), then law confirmed by
# observation conjunction.
sup_minimal_best = support(
    [claim_omc_beats_all_baselines],
    claim_omc_beats_minimal_best,
    reason=(
        "Under the panel-wide law (@claim_omc_beats_all_baselines), "
        "the per-baseline observation against the strongest Minimal "
        "baseline (Claude-4.5: 84.67% - 69.19% = +15.48 pp) "
        "(@claim_omc_beats_minimal_best) is the minimum-gap "
        "instance of the law. Generative direction: law -> "
        "observation."
    ),
    prior=0.94,
)

sup_codex = support(
    [claim_omc_beats_all_baselines],
    claim_omc_beats_codex,
    reason=(
        "Under the panel-wide law, the +22.58 pp gap vs CodeX "
        "(@claim_omc_beats_codex) is the per-baseline instance "
        "for the strongest Commercial agent."
    ),
    prior=0.94,
)

sup_claude_code = support(
    [claim_omc_beats_all_baselines],
    claim_omc_beats_claude_code,
    reason=(
        "Under the panel-wide law, the +28.02 pp same-substrate "
        "gap vs Claude Code (@claim_omc_beats_claude_code) is the "
        "per-baseline instance for the same-LLM-family Commercial "
        "agent."
    ),
    prior=0.94,
)

sup_gemini_minimal = support(
    [claim_omc_beats_all_baselines],
    claim_omc_beats_gemini_minimal,
    reason=(
        "Under the panel-wide law, the +61.91 pp gap vs "
        "Gemini-3-Pro Minimal (@claim_omc_beats_gemini_minimal) "
        "is the per-baseline instance for a different Minimal "
        "family."
    ),
    prior=0.94,
)

sup_gemini_cli = support(
    [claim_omc_beats_all_baselines],
    claim_omc_beats_gemini_cli,
    reason=(
        "Under the panel-wide law, the +73.38 pp gap vs Gemini "
        "CLI Commercial (@claim_omc_beats_gemini_cli) is the "
        "widest per-baseline instance, completing cross-family "
        "coverage."
    ),
    prior=0.94,
)

ind_baselines_12 = induction(
    sup_minimal_best,
    sup_codex,
    law=claim_omc_beats_all_baselines,
    reason=(
        "Combined induction across two baselines (Claude-4.5 "
        "Minimal best and CodeX Commercial best) -- the gap holds "
        "in both categories, so the panel-wide generalisation is "
        "strengthened."
    ),
)

ind_baselines_123 = induction(
    ind_baselines_12,
    sup_claude_code,
    law=claim_omc_beats_all_baselines,
    reason=(
        "Adding the same-substrate Claude Code datapoint: the gap "
        "(+28 pp) is wider than the Minimal best gap (+15 pp) "
        "*despite* sharing the Claude family substrate. Three "
        "independent measurement points support the cross-baseline "
        "generalisation."
    ),
)

ind_baselines_1234 = induction(
    ind_baselines_123,
    sup_gemini_minimal,
    law=claim_omc_beats_all_baselines,
    reason=(
        "Adding Gemini-3-Pro Minimal (+61.91 pp) widens the "
        "model-family coverage; four independent datapoints "
        "support the generalisation."
    ),
)

ind_baselines_full = induction(
    ind_baselines_1234,
    sup_gemini_cli,
    law=claim_omc_beats_all_baselines,
    reason=(
        "Adding Gemini CLI Commercial (+73.38 pp); the five "
        "datapoints span both Minimal and Commercial categories "
        "and three model families (Claude, Gemini, others) -- "
        "supporting the cross-baseline generalisation that OMC > "
        "all 12 baselines."
    ),
)

# Headline derives from the panel + design aspects
strat_three_design_aspects = support(
    [
        claim_design_aspect_dynamic_decomposition,
        claim_design_aspect_review_gate,
        claim_design_aspect_cross_family,
    ],
    claim_three_design_aspects_drive_result,
    reason=(
        "The three-design-aspects claim "
        "(@claim_three_design_aspects_drive_result) is the "
        "conjunction of (D1) dynamic decomposition "
        "(@claim_design_aspect_dynamic_decomposition), (D2) "
        "review gate (@claim_design_aspect_review_gate), and (D3) "
        "cross-family recruitment "
        "(@claim_design_aspect_cross_family). Each is read off "
        "Section 3.2's design-aspect attribution."
    ),
    prior=0.9,
)

strat_headline_from_table = support(
    [claim_table_2_prdbench, claim_omc_beats_all_baselines],
    claim_headline_prdbench,
    background=[
        setup_prdbench_benchmark,
        setup_each_prdbench_is_wild_dynamic,
        setup_omc_agent_setup,
        setup_dev_mode,
        setup_baseline_panel,
    ],
    reason=(
        "The headline 84.67% / +15.48 pp claim "
        "(@claim_headline_prdbench) is read directly from Table 2 "
        "(@claim_table_2_prdbench) under the cross-baseline "
        "generalisation (@claim_omc_beats_all_baselines), with "
        "PRDBench DEV-mode setup (@setup_prdbench_benchmark, "
        "@setup_dev_mode, @setup_baseline_panel) controlling for "
        "agent-stack differences."
    ),
    prior=0.95,
)


# ============================================================================
# SECTION 3.3 (Case studies): induction over four cross-domain successes
# ============================================================================

sup_case_content = support(
    [claim_cross_case_pattern],
    claim_case_content_generation_result,
    reason=(
        "Under the cross-case generality pattern "
        "(@claim_cross_case_pattern), Case 1 (content generation) "
        "succeeds with no framework change "
        "(@claim_case_content_generation_result). Generative "
        "direction: pattern -> observation."
    ),
    prior=0.92,
)

sup_case_game = support(
    [claim_cross_case_pattern],
    claim_case_game_development_result,
    reason=(
        "Under the cross-case generality pattern, Case 2 (game "
        "development with rejection-driven mid-project skill "
        "creation, @claim_case_game_development_result) succeeds "
        "with no framework change."
    ),
    prior=0.92,
)

sup_case_audiobook = support(
    [claim_cross_case_pattern],
    claim_case_audiobook_result,
    reason=(
        "Under the cross-case generality pattern, Case 3 "
        "(audiobook, @claim_case_audiobook_result) succeeds across "
        "cross-modal text + audio + visual coordination on "
        "different LLM backends."
    ),
    prior=0.92,
)

sup_case_research = support(
    [claim_cross_case_pattern],
    claim_case_research_survey_result,
    reason=(
        "Under the cross-case generality pattern, Case 4 "
        "(research survey, @claim_case_research_survey_result) "
        "succeeds with 17 documents + 3 novel research ideas."
    ),
    prior=0.92,
)

ind_cases_12 = induction(
    sup_case_content,
    sup_case_game,
    law=claim_cross_case_pattern,
    reason=(
        "Cases 1 and 2 cover content and software/game domains "
        "with distinct LLM backends and execution modes."
    ),
)

ind_cases_123 = induction(
    ind_cases_12,
    sup_case_audiobook,
    law=claim_cross_case_pattern,
    reason=(
        "Adding Case 3 covers cross-modal coordination "
        "(text + audio + visual) on a different LLM backend mix."
    ),
)

ind_cases_full = induction(
    ind_cases_123,
    sup_case_research,
    law=claim_cross_case_pattern,
    reason=(
        "Adding Case 4 covers academic research, exercising "
        "another distinct skill profile and Talent-Market "
        "recruitment path. Four independent domain successes with "
        "no framework modification support the cross-case "
        "generality pattern."
    ),
)


# ============================================================================
# Central abduction: organisational-decoupling vs bigger-LM/more-compute
# ============================================================================

s_h_organisational = support(
    [claim_pred_h_organisational_decoupling_drives],
    claim_observed_fingerprint,
    reason=(
        "Under the organisational-decoupling hypothesis "
        "(@claim_organisation_decoupling_thesis + "
        "@claim_three_pillars + "
        "@claim_three_design_aspects_drive_result), the predicted "
        "fingerprint matches: same-substrate Commercial gap is *wider* "
        "than the Minimal gap (because the organisational layer "
        "amplifies whatever the substrate provides), the gap is "
        "broad across model families, cross-domain case studies "
        "succeed without framework changes, and mid-project skill "
        "creation occurs (a behaviour reachable only via the "
        "typed organisational layer). All four observation "
        "components match by direct prediction."
    ),
    prior=0.85,
)

s_alt_bigger_lm = support(
    [claim_pred_alt_bigger_lm_or_more_compute],
    claim_observed_fingerprint,
    reason=(
        "Under the bigger-LM / better-tools / more-compute "
        "alternative, the fingerprint should differ: same-substrate "
        "gap should converge (Claude OMC vs Claude Minimal), gap "
        "against tooled Commercial agents should be *narrower* "
        "than against Minimal LLMs, cross-domain case studies "
        "should require domain scaffolding, and mid-project skill "
        "creation should not arise from 'more compute' alone. The "
        "observed pattern *contradicts* these predictions on at "
        "least three of four dimensions."
    ),
    prior=0.2,
)

comp_central = compare(
    claim_pred_h_organisational_decoupling_drives,
    claim_pred_alt_bigger_lm_or_more_compute,
    claim_observed_fingerprint,
    reason=(
        "The observed fingerprint "
        "(@claim_observed_fingerprint) -- same-substrate "
        "Commercial gap +28 pp wider than +15 pp Minimal gap, "
        "cross-family generality, framework-invariant cross-domain "
        "success, mid-project skill creation -- matches the "
        "organisational-decoupling prediction "
        "(@claim_pred_h_organisational_decoupling_drives) on all "
        "four dimensions, while violating the bigger-LM "
        "alternative's predictions "
        "(@claim_pred_alt_bigger_lm_or_more_compute) on at least "
        "three of four. Inferential ordering strongly favours H "
        "over Alt."
    ),
    prior=0.9,
)

abd_central = abduction(
    s_h_organisational,
    s_alt_bigger_lm,
    comp_central,
    reason=(
        "Inference to the best explanation: the organisational-"
        "decoupling hypothesis predicts the observed fingerprint "
        "directly while the bigger-LM/more-compute alternative "
        "violates it on the same-substrate datapoint, the "
        "Commercial-vs-Minimal-gap-direction datapoint, the "
        "cross-domain framework-invariance datapoint, and the "
        "mid-project skill-creation datapoint. The "
        "organisational-decoupling hypothesis is therefore the "
        "best available explanation for the headline gain."
    ),
)


# ============================================================================
# Two contradictions
# ============================================================================

# (1) Fixed-team-sufficient vs OMC's dynamic-organisational gain

strat_omc_demonstration_dynamic = support(
    [
        claim_headline_prdbench,
        claim_cross_case_pattern,
        claim_omc_beats_all_baselines,
    ],
    claim_omc_demonstration_dynamic_org_works,
    reason=(
        "OMC's empirical demonstration "
        "(@claim_omc_demonstration_dynamic_org_works) follows "
        "from the headline PRDBench gain "
        "(@claim_headline_prdbench), the cross-baseline lead "
        "across all 12 systems (@claim_omc_beats_all_baselines), "
        "and the cross-domain case-study generality "
        "(@claim_cross_case_pattern)."
    ),
    prior=0.95,
)

contradiction_fixed_team = contradiction(
    claim_lit_fixed_team_assumption,
    claim_omc_demonstration_dynamic_org_works,
    reason=(
        "The implicit literature assumption that fixed team "
        "structure is sufficient for production-grade MAS "
        "(@claim_lit_fixed_team_assumption) cannot coexist with "
        "OMC's empirical demonstration "
        "(@claim_omc_demonstration_dynamic_org_works) that "
        "*on-demand recruitment + dynamic decomposition* "
        "outperforms fixed-team baselines on the same task panel. "
        "Both cannot be true: either fixed teams are sufficient "
        "(contradicted by 84.67% > 69.19% with on-demand "
        "specialists), or on-demand organisational dynamics matter."
    ),
    prior=0.95,
)

# (2) Tightly-coupled-coordination-required vs typed-interface deployment

contradiction_tight_coupling = contradiction(
    claim_lit_tightly_coupled_coordination,
    claim_omc_typed_interfaces_demonstration,
    reason=(
        "The implicit literature assumption that MAS coordination "
        "requires tightly coupled bespoke logic "
        "(@claim_lit_tightly_coupled_coordination) cannot coexist "
        "with OMC's deployed typed-interface architecture "
        "(@claim_omc_typed_interfaces_demonstration), which "
        "successfully orchestrates three Container families "
        "(LangGraph / Claude CLI / script-based) under six typed "
        "contracts on PRDBench plus four cross-domain case studies. "
        "Decoupling identity from runtime is not impractical -- it "
        "is a deployed engineering feature."
    ),
    prior=0.95,
)

strat_omc_typed_demonstration = support(
    [
        claim_typed_interface_decoupling_demonstration,
        claim_cross_case_pattern,
    ],
    claim_omc_typed_interfaces_demonstration,
    reason=(
        "The deployment claim "
        "(@claim_omc_typed_interfaces_demonstration) follows from "
        "the architectural demonstration "
        "(@claim_typed_interface_decoupling_demonstration) plus "
        "the cross-case framework-invariance "
        "(@claim_cross_case_pattern) showing the typed interfaces "
        "carry across content / game / audiobook / research "
        "domains with multiple model families."
    ),
    prior=0.95,
)


# ============================================================================
# Stated contributions aggregate
# ============================================================================

strat_three_structural_gaps = support(
    [
        claim_omc_fills_heterogeneity_gap,
        claim_omc_fills_coordination_gap,
        claim_omc_fills_evolution_gap,
    ],
    claim_three_structural_gaps_summary,
    reason=(
        "The three-structural-gaps summary "
        "(@claim_three_structural_gaps_summary) is the conjunction "
        "of OMC's filling of the heterogeneity gap "
        "(@claim_omc_fills_heterogeneity_gap), the coordination "
        "gap (@claim_omc_fills_coordination_gap), and the evolution "
        "gap (@claim_omc_fills_evolution_gap)."
    ),
    prior=0.93,
)

strat_e2r_explore_with_oracle = support(
    [claim_external_oracle_role],
    claim_stage_1_explore,
    reason=(
        "The Explore stage's exploration-exploitation tradeoff and "
        "branching-factor-decided-at-runtime behaviour "
        "(@claim_stage_1_explore) is influenced by the external "
        "oracle (CEO) intervention modes "
        "(@claim_external_oracle_role) -- policy override, "
        "requirement injection, iteration triggering -- which "
        "shape what strategies $\\pi$ explores under bounded "
        "rationality."
    ),
    prior=0.85,
)

strat_limitations_to_open_questions = support(
    [
        claim_limitation_only_prdbench_quant,
        claim_limitation_self_evolution_not_ablated,
    ],
    claim_open_questions,
    reason=(
        "The open questions stated in Section 6 "
        "(@claim_open_questions) follow from the limitations "
        "(@claim_limitation_only_prdbench_quant -- only PRDBench "
        "quantitatively evaluated; "
        "@claim_limitation_self_evolution_not_ablated -- no "
        "per-component ablation). The acknowledged limitations "
        "directly motivate the open questions on scaling, "
        "per-component contribution, and Talent Market growth."
    ),
    prior=0.94,
)

strat_cost_tradeoff = support(
    [claim_headline_prdbench, claim_cross_case_pattern],
    claim_cost_performance_tradeoff,
    reason=(
        "The cost-performance trade-off "
        "(@claim_cost_performance_tradeoff) follows from the "
        "headline cost ($6.91/task across 50 PRDBench tasks "
        "@claim_headline_prdbench) and the cross-domain case "
        "studies (with cost figures, "
        "@claim_cross_case_pattern) -- the trade-off is "
        "reasonable above a complexity threshold but the adaptive "
        "dispatch mode is required for simple queries."
    ),
    prior=0.9,
)

strat_human_enterprise_analogy = support(
    [
        claim_organisation_decoupling_thesis,
        claim_cross_case_pattern,
        claim_mirrors_human_enterprise,
    ],
    claim_human_enterprise_analogy_general,
    reason=(
        "The general human-enterprise analogy "
        "(@claim_human_enterprise_analogy_general) follows from "
        "(i) the decoupling thesis "
        "(@claim_organisation_decoupling_thesis); (ii) the "
        "cross-domain pattern of success "
        "(@claim_cross_case_pattern); (iii) the structural "
        "mirroring of human-enterprise feedback mechanisms "
        "(@claim_mirrors_human_enterprise). The OS-kernel "
        "scaling argument follows the same pattern (more agent "
        "diversity -> more value of the abstraction layer)."
    ),
    prior=0.88,
)

strat_four_contributions = support(
    [
        claim_missing_organisation_layer,
        claim_three_pillars,
        claim_theorem_termination,
        claim_theorem_deadlock_freedom,
        claim_headline_prdbench,
        claim_cross_case_pattern,
    ],
    claim_three_stated_contributions,
    reason=(
        "The four stated contributions "
        "(@claim_three_stated_contributions) are the conjunction "
        "of: (C1) diagnosis of the missing organisation layer "
        "(@claim_missing_organisation_layer); (C2) the OMC method "
        "via three pillars (@claim_three_pillars); (C3) formal "
        "guarantees -- termination (@claim_theorem_termination) "
        "and deadlock-freedom "
        "(@claim_theorem_deadlock_freedom); (C4) empirical "
        "validation via PRDBench (@claim_headline_prdbench) and "
        "four cross-domain case studies "
        "(@claim_cross_case_pattern)."
    ),
    prior=0.94,
)

strat_conclusion_synthesis = support(
    [
        claim_three_pillars,
        claim_headline_prdbench,
        claim_theorem_termination,
        claim_theorem_deadlock_freedom,
        claim_cross_case_pattern,
    ],
    claim_conclusion_synthesis,
    reason=(
        "The conclusion synthesis "
        "(@claim_conclusion_synthesis) integrates the three "
        "pillars (@claim_three_pillars), the headline empirical "
        "result (@claim_headline_prdbench), the formal guarantees "
        "(@claim_theorem_termination, "
        "@claim_theorem_deadlock_freedom), and cross-domain "
        "generality (@claim_cross_case_pattern) into the closing "
        "argument that organisation-machinery transfers from human "
        "companies to AI."
    ),
    prior=0.92,
)


__all__ = [
    "claim_observed_fingerprint",
    "claim_omc_demonstration_dynamic_org_works",
    "claim_omc_typed_interfaces_demonstration",
]
