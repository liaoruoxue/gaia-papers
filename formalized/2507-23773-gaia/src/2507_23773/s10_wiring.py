"""Pass 2 wiring: strategies, abductions, inductions, contradictions
linking propositions extracted in motivation/s2-s9 into the reasoning
graph.

The wiring module collects all reasoning connections in one place so the
per-section modules remain pure content extraction.
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
    setup_fm_agents,
    setup_autoregressive_reasoning_definition,
    setup_human_mental_simulation,
    q_central,
    claim_one_task_one_agent_limit,
    claim_autoregressive_planning_limit,
    claim_simura_intro,
    claim_natural_language_substrate,
    claim_headline_flightqa,
    claim_headline_124_pct,
    claim_open_source_release,
    claim_contributions,
)
from .s2_related_work import (
    claim_llm_agents_two_lines,
    claim_world_model_history,
    claim_existing_wm_continuous_embedding_limit,
    claim_existing_web_agents_react_limited,
    claim_existing_benchmarks_limit,
    claim_generalist_two_lines,
)
from .s3_optimal_agent_formulation import (
    setup_agent_environment_model,
    setup_reward_and_value,
    setup_value_recursion,
    setup_optimal_agent_def,
    claim_optimal_decision_rule,
    claim_three_required_capabilities,
    claim_ground_truth_unavailable,
    setup_world_model_definition,
    claim_simulative_decision_rule,
    claim_continuous_embedding_brittle,
    claim_human_concept_categorization,
    setup_natural_language_state_def,
    claim_concept_state_helps_policy,
    claim_atomic_action_rollout_limits,
    claim_hierarchical_action_proposal,
    claim_natural_language_action_empirical,
    claim_simura_decision_process,
)
from .s4_simura_architecture import (
    setup_simura_modules,
    claim_planner_loop,
    claim_design_is_environment_agnostic,
    claim_design_is_model_agnostic,
    claim_llm_pretraining_is_world_modeling,
    setup_search_algorithms,
    claim_architecture_addresses_diagnosis,
)
from .s5_world_model_implementation import (
    setup_web_browser_environment,
    setup_observation_format,
    setup_action_space,
    setup_llm_encoder_actor,
    setup_llm_policy,
    setup_llm_world_model,
    setup_llm_critic,
    setup_memory_update,
    setup_autoregressive_planning_baseline,
    setup_browsingagent_baseline,
    claim_prototype_summary,
    claim_natural_language_actions_in_prototype,
)
from .s6_main_results import (
    setup_three_task_families,
    setup_baselines_overall,
    setup_environment_and_budget,
    claim_overview_three_task_panel,
    claim_simura_beats_browsingagent_across_tasks,
    claim_wm_beats_ar_across_tasks,
    claim_124pct_max_relative_improvement,
    claim_o1_o3mini_close_to_zero,
    claim_temporal_repeatability_caveat,
)
from .s7_per_task_results import (
    setup_flightqa_dataset,
    claim_flightqa_motivates_counterfactual,
    setup_flightqa_evaluation,
    claim_flightqa_table1,
    claim_flightqa_browsing_action_error,
    claim_flightqa_repetition_reduction,
    claim_flightqa_browsingagent_no_o_models,
    claim_flightqa_constraint_scaling,
    claim_chatgpt_4o_hallucination_example,
    setup_fanoutqa_eval,
    claim_fanoutqa_table2,
    claim_fanoutqa_response_rate_jump,
    claim_fanoutqa_action_error_reduction,
    claim_fanoutqa_browsing_partial_success,
    setup_webarena_eval,
    claim_webarena_table3,
    claim_webarena_setup_caveat,
)
from .s8_generality_and_ablations import (
    claim_law_simulative_reasoning_advantage,
    claim_law_simura_beats_open_baseline,
    claim_structured_pipeline_helps_independently,
    claim_world_model_adds_planning_advantage,
    claim_components_combine_multiplicatively,
    claim_law_generality_across_constraint_complexity,
    claim_statistical_significance,
)
from .s9_discussion_limitations import (
    claim_limit_runtime,
    claim_limit_tooling,
    claim_limit_modality,
    claim_conclusion_synthesis,
    claim_future_work_breadth,
)


# ============================================================================
# SECTION 3 -- THEORY: deductive chain from agent-environment model to the
# optimal decision rule and its world-model-based counterpart.
# ============================================================================

# (Eq. 4) optimal decision rule follows deductively from the agent-env model
# + value recursion + optimal-agent definition. Premise of deduction must
# be non-empty; we use the optimal-agent definition (Eq. 3) as the principal
# premise, with the trajectory distribution and value recursion as background.
strat_optimal_decision_rule = deduction(
    [setup_value_recursion],
    claim_optimal_decision_rule,
    reason=(
        "The optimal decision rule (@claim_optimal_decision_rule, Eq. 4) "
        "follows by direct algebraic manipulation from: "
        "the recursive Bellman-style value decomposition "
        "(@setup_value_recursion, Eq. 2), the definition of the "
        "optimal agent as the value-maximizing policy "
        "(@setup_optimal_agent_def, Eq. 3), and the agent-environment "
        "factored trajectory distribution (@setup_agent_environment_"
        "model, Eq. 1). Substituting (1) and (2) into (3) and "
        "grouping the action and state sums yields the arg-max "
        "decision rule directly. This is mathematical deduction: no "
        "empirical content is introduced beyond the definitions."
    ),
    background=[
        setup_agent_environment_model,
        setup_reward_and_value,
        setup_optimal_agent_def,
    ],
    prior=0.99,
)

# Three required capabilities follow deductively from Eq. 4 (the rule
# explicitly contains a 'propose actions / predict trajectories /
# evaluate goal progress' structure).
strat_three_capabilities = deduction(
    [claim_optimal_decision_rule],
    claim_three_required_capabilities,
    reason=(
        "The three required capabilities (@claim_three_required_"
        "capabilities) -- (i) propose actions, (ii) predict trajectories "
        "via mu, (iii) evaluate goal progress -- are read off the three "
        "factors of the optimal decision rule (@claim_optimal_decision_"
        "rule): the arg-max over a_{t:T-1} (proposing), the product of "
        "mu(s_{i+1} | s_i, a_i) (predicting), and the sum of gamma^k "
        "r(g, s_k) + gamma^T V(s_T) (evaluating). The System-1 / "
        "System-2 reading [@Kahneman2011] is the natural cognitive "
        "interpretation of taking only the first sample from pi-tilde "
        "vs the full deliberative loop."
    ),
    background=[setup_reward_and_value],
    prior=0.97,
)

# Simulation-based decision rule (Eq. 5) is deduced from Eq. 4 by
# substitution of (s_t, mu) -> (s_hat_t, f).
strat_simulative_decision_rule = deduction(
    [
        claim_optimal_decision_rule,
        claim_ground_truth_unavailable,
    ],
    claim_simulative_decision_rule,
    reason=(
        "The simulation-based decision rule (@claim_simulative_decision_"
        "rule, Eq. 5) is obtained from the optimal decision rule "
        "(@claim_optimal_decision_rule, Eq. 4) by substituting the "
        "ground-truth state s_t with the belief state s_hat_t and the "
        "ground-truth environment p_mu(s_{i+1} | s_i, a_i) with the "
        "world-model simulator p_f(s_hat_{i+1} | s_hat_i, a_i). The "
        "substitution is forced by the unavailability of (s, mu) in "
        "general environments (@claim_ground_truth_unavailable). The "
        "world model and belief state are formally defined in "
        "@setup_world_model_definition."
    ),
    background=[setup_world_model_definition],
    prior=0.97,
)

# Hierarchical action proposal is the design solution to the atomic-action
# rollout limits.
strat_hierarchical_action_proposal = support(
    [claim_atomic_action_rollout_limits],
    claim_hierarchical_action_proposal,
    reason=(
        "The hierarchical-action design (@claim_hierarchical_action_"
        "proposal) is the architectural response to the limits of "
        "rolling out at the concrete-action level (@claim_atomic_action_"
        "rollout_limits): transferability is recovered by reasoning in "
        "an action space A' decoupled from the environment-specific A; "
        "richer intentions are expressible at the abstract level; and "
        "rollouts shrink (one a' = many a) to reduce error accumulation "
        "[@Dyna]."
    ),
    prior=0.9,
)

# SIMURA decision process Eq. 8 is the integrated specification combining
# encoding (h), planning (Eq. 5 with the hierarchical action proposal),
# and acting (alpha).
strat_simura_decision_process = deduction(
    [
        claim_simulative_decision_rule,
        setup_natural_language_state_def,
        claim_hierarchical_action_proposal,
    ],
    claim_simura_decision_process,
    reason=(
        "SIMURA's three-level decision process (@claim_simura_decision_"
        "process, Eq. 8) is the combination of: the simulation-based "
        "decision rule (@claim_simulative_decision_rule, replacing s_t, "
        "mu with s_hat_t, f); the natural-language state factorization "
        "(@setup_natural_language_state_def, Eqs. 6-7) defining how "
        "p_h and p_f are realized; and the hierarchical-action "
        "decomposition (@claim_hierarchical_action_proposal, splitting "
        "a' for planning from a for execution). Each level (Perception, "
        "Planning, Acting) maps to one factor in Eq. 8."
    ),
    prior=0.97,
)


# ============================================================================
# SECTION 3.4 -- ARGUMENT: discrete natural-language representation
# ============================================================================

# Concept-categorization argument: continuous-embedding brittleness +
# human concept-categorization -> SIMURA's natural-language design choice.
strat_nl_state_argument = support(
    [
        claim_continuous_embedding_brittle,
        claim_human_concept_categorization,
    ],
    setup_natural_language_state_def,
    reason=(
        "SIMURA's natural-language belief-state representation "
        "(@setup_natural_language_state_def) is motivated by two "
        "complementary arguments: (1) continuous-embedding "
        "observation encoding is brittle to real-world noise/"
        "variability (@claim_continuous_embedding_brittle); "
        "(2) human cognition categorizes raw perception into discrete "
        "concepts, which language efficiently encodes hierarchically, "
        "and discrete representations are formally complete in general "
        "(@claim_human_concept_categorization, [@CritiquesWorldModels]). "
        "Together these motivate the discrete, hierarchical, language-"
        "based latent space."
    ),
    prior=0.85,
)

# Concept-state empirical observation supports the natural-language design.
strat_concept_state_helps = support(
    [setup_natural_language_state_def],
    claim_concept_state_helps_policy,
    reason=(
        "The empirical observation that concept-based natural-language "
        "states reduce hallucination and improve planning robustness "
        "(@claim_concept_state_helps_policy) is the predicted "
        "consequence of operating downstream modules on a structured "
        "(@setup_natural_language_state_def) rather than a noisy "
        "high-dimensional latent space. The paper reports it as an "
        "empirical finding observed in the web-browsing prototype."
    ),
    prior=0.7,
)

# Natural-language simulated-action observation supports the hierarchical
# design.
strat_nl_action_helps = support(
    [claim_hierarchical_action_proposal],
    claim_natural_language_action_empirical,
    reason=(
        "Empirical observation that natural-language simulated actions "
        "yield more diverse, grounded action proposals (@claim_natural_"
        "language_action_empirical) is the practical realization of the "
        "hierarchical-action design (@claim_hierarchical_action_"
        "proposal): expressing a' as language phrases lets the policy "
        "exploit pretrained-LLM diversity and grounding capabilities. "
        "The paper reports this as an in-prototype observation."
    ),
    prior=0.7,
)


# ============================================================================
# SECTION 4 -- ARCHITECTURE: SIMURA pipeline addresses the diagnosed limits
# ============================================================================

strat_simura_intro_from_simura_decision_process = support(
    [claim_simura_decision_process],
    claim_simura_intro,
    reason=(
        "SIMURA (@claim_simura_intro) is the architectural realization "
        "of the three-level decision process (@claim_simura_decision_"
        "process, Eq. 8): the policy module, world model, and critic "
        "instantiate the Planning level; the encoder instantiates "
        "Perception; the actor instantiates Acting. The 'world model "
        "as the engine for planning via simulation' framing comes "
        "directly from substituting f for mu in the optimal rule "
        "(@claim_simulative_decision_rule)."
    ),
    background=[setup_simura_modules],
    prior=0.95,
)

strat_simura_modules_from_intro = deduction(
    [claim_simura_intro],
    setup_simura_modules,
    reason=(
        "The five-module decomposition (@setup_simura_modules: encoder, "
        "policy, world model, critic, actor) is the structural "
        "definition implied by the SIMURA proposal (@claim_simura_"
        "intro): the proposal names exactly these modules, and the "
        "decision process (Eq. 8) references each of them. This is "
        "definitional unpacking, not an empirical claim."
    ),
    prior=0.99,
)

strat_natural_language_substrate_from_args = support(
    [
        setup_natural_language_state_def,
        claim_natural_language_action_empirical,
    ],
    claim_natural_language_substrate,
    reason=(
        "The natural-language belief-state-and-action substrate "
        "(@claim_natural_language_substrate) combines the natural-"
        "language state representation (@setup_natural_language_state_"
        "def, Eqs. 6-7) with the natural-language simulated-action "
        "representation observed empirically (@claim_natural_language_"
        "action_empirical). The 'model-agnostic' property follows "
        "because no specific LLM architecture is required to read/"
        "write natural language."
    ),
    prior=0.92,
)

strat_planner_loop_from_modules = deduction(
    [setup_simura_modules],
    claim_planner_loop,
    reason=(
        "The planner inner loop (@claim_planner_loop -- propose / "
        "simulate / evaluate / select) is the operational reading of "
        "the SIMURA modules (@setup_simura_modules): policy proposes, "
        "world model simulates, critic evaluates, planner selects "
        "the first step a'^*_t for execution. This unpacks the named "
        "modules into their per-step interaction."
    ),
    prior=0.99,
)

strat_environment_agnostic = support(
    [claim_planner_loop, setup_simura_modules],
    claim_design_is_environment_agnostic,
    reason=(
        "SIMURA's environment-agnosticism (@claim_design_is_"
        "environment_agnostic) follows from its planning loop "
        "(@claim_planner_loop) operating entirely on natural-language "
        "belief states and natural-language simulated actions: only "
        "the encoder h and actor alpha (@setup_simura_modules) bind "
        "to environment-specific observation/action APIs. Swapping "
        "environments only requires swapping these two modules."
    ),
    prior=0.9,
)

strat_model_agnostic = support(
    [claim_natural_language_substrate, setup_simura_modules],
    claim_design_is_model_agnostic,
    reason=(
        "SIMURA's model-agnosticism (@claim_design_is_model_agnostic) "
        "follows from the natural-language substrate (@claim_natural_"
        "language_substrate): each module (@setup_simura_modules) "
        "specifies only an input/output type defined over natural "
        "language, so any LLM, VLM, or trained world model "
        "[@Chae2024WMA; @LeCunOpenReview2022] can in principle "
        "instantiate it. The paper's prototype uses gpt-4o, but the "
        "specification does not require it."
    ),
    prior=0.9,
)

strat_llm_pretraining_wm_substrate = support(
    [claim_llm_pretraining_is_world_modeling],
    claim_prototype_summary,
    reason=(
        "The viability of an LLM-only prototype (@claim_prototype_"
        "summary) rests on the conceptual link between LLM next-token "
        "pretraining and world modeling (@claim_llm_pretraining_is_"
        "world_modeling): pretrained LLMs already encode large "
        "amounts of latent world knowledge usable as a generative "
        "model of futures over natural-language states "
        "[@RAP; @HuShu2023]. This justifies using off-the-shelf "
        "gpt-4o for every module."
    ),
    prior=0.85,
    background=[
        setup_llm_encoder_actor,
        setup_llm_policy,
        setup_llm_world_model,
        setup_llm_critic,
        setup_memory_update,
        setup_search_algorithms,
        setup_web_browser_environment,
        setup_observation_format,
        setup_action_space,
    ],
)

strat_natural_language_actions_in_prototype = support(
    [claim_prototype_summary, claim_hierarchical_action_proposal],
    claim_natural_language_actions_in_prototype,
    reason=(
        "The prototype's split between natural-language simulated "
        "actions a'_t and concrete browser API calls a_t "
        "(@claim_natural_language_actions_in_prototype) is the direct "
        "instantiation of the hierarchical-action design "
        "(@claim_hierarchical_action_proposal) inside the LLM-based "
        "prototype (@claim_prototype_summary): the policy/world "
        "model/critic/clustering operate on NL phrases; the actor "
        "grounds the chosen phrase to a click()/fill()/etc. browser "
        "call."
    ),
    prior=0.95,
)

strat_architecture_addresses_diagnosis = support(
    [
        claim_design_is_environment_agnostic,
        claim_planner_loop,
    ],
    claim_architecture_addresses_diagnosis,
    reason=(
        "SIMURA's architecture structurally addresses the two "
        "diagnosed limits (@claim_architecture_addresses_diagnosis): "
        "(1) one-task-one-agent scalability (D1) is addressed because "
        "the planner is environment-agnostic (@claim_design_is_"
        "environment_agnostic); (2) black-box autoregressive reasoning "
        "(D2) is addressed because the planner explicitly simulates "
        "and evaluates futures via the world model and critic "
        "(@claim_planner_loop). This is a design-level claim that "
        "must still be verified empirically in Section 4."
    ),
    prior=0.85,
)


# ============================================================================
# SECTION 4 -- HEADLINE CLAIMS: anchor headline empirical claims to the
# per-task tables that produce them.
# ============================================================================

strat_headline_flightqa = deduction(
    [claim_flightqa_table1],
    claim_headline_flightqa,
    reason=(
        "The headline FlightQA claim (@claim_headline_flightqa, "
        "0.0% -> 32.2%) is read directly from Table 1 (@claim_"
        "flightqa_table1): BrowsingAgent row Correct = 0.0%, SIMURA + "
        "World Model row Correct = 32.2%. This is a transcription "
        "of two cells of Table 1; deduction is appropriate."
    ),
    prior=0.99,
)

strat_headline_124_pct_from_flightqa = deduction(
    [claim_flightqa_table1, claim_124pct_max_relative_improvement],
    claim_headline_124_pct,
    reason=(
        "The headline +124% claim (@claim_headline_124_pct) is the "
        "ratio computation 32.2 / 14.4 - 1 ~ 1.236 read off Table 1 "
        "(@claim_flightqa_table1, SIMURA + Autoregressive Correct "
        "= 14.4%, SIMURA + World Model Correct = 32.2%). The 'up "
        "to 124%' framing as the cross-task maximum is established "
        "in @claim_124pct_max_relative_improvement."
    ),
    prior=0.99,
)

strat_124_max_relative = deduction(
    [
        claim_flightqa_table1,
        claim_fanoutqa_table2,
        claim_webarena_table3,
    ],
    claim_124pct_max_relative_improvement,
    reason=(
        "The cross-task maximum relative gain of +124% "
        "(@claim_124pct_max_relative_improvement) is derived by "
        "computing WM/AR - 1 across the three task tables: "
        "FlightQA (@claim_flightqa_table1) 32.2/14.4 - 1 = +124%; "
        "FanOutQA (@claim_fanoutqa_table2) 29.8/20.2 - 1 = +47.5% "
        "(or 55.0/37.0 - 1 = +48.6% on response rate); "
        "WebArena (@claim_webarena_table3) 23.0/19.0 - 1 = +21.1%. "
        "The maximum is on FlightQA."
    ),
    prior=0.99,
)


# ============================================================================
# SECTION 4 -- PER-TABLE CLAIM ATTRIBUTION
# ============================================================================

# Action-error reduction on FlightQA -> Table 1 ratios.
strat_flightqa_action_error_from_table1 = deduction(
    [claim_flightqa_table1],
    claim_flightqa_browsing_action_error,
    reason=(
        "The 93.3% -> 1.1% action-error reduction (@claim_flightqa_"
        "browsing_action_error) is read directly from Table 1 "
        "(@claim_flightqa_table1): BrowsingAgent Action Err column = "
        "93.3%, SIMURA + World Model Action Err column = 1.1%. The "
        "ratio 93.3 / 1.1 ~ 84.8 supports the ~85x framing."
    ),
    prior=0.99,
)

strat_flightqa_repetition_from_table1 = deduction(
    [claim_flightqa_table1],
    claim_flightqa_repetition_reduction,
    reason=(
        "The 44.4% -> 18.9% repetitive-action reduction "
        "(@claim_flightqa_repetition_reduction) is read directly "
        "from Table 1 (@claim_flightqa_table1): SIMURA + AR Repeat "
        "= 44.4%, SIMURA + WM Repeat = 18.9%. The 'world-model "
        "spots loops before committing' interpretation is the "
        "paper's own gloss; the numerical facts are direct "
        "transcriptions."
    ),
    prior=0.97,
)

strat_temporal_caveat_from_table1 = support(
    [claim_flightqa_table1],
    claim_temporal_repeatability_caveat,
    reason=(
        "The temporal-repeatability caveat (@claim_temporal_repeatability_"
        "caveat) is the methodological qualifier on the empirical "
        "panels (@claim_flightqa_table1 and the related per-task "
        "tables): all main experiments ran Nov-Dec 2024, the o1/"
        "o3-mini autoregressive-planner experiments ran Feb 2025, "
        "and absolute scores depend on then-available models and "
        "browser tooling. The repeatable claim is the WM-vs-AR "
        "advantage under matched conditions, not the absolute "
        "score levels."
    ),
    prior=0.95,
)

strat_browsing_no_o_models_from_table1 = support(
    [claim_flightqa_table1],
    claim_flightqa_browsingagent_no_o_models,
    reason=(
        "The exclusion of BrowsingAgent + o1/o3-mini from FlightQA "
        "(@claim_flightqa_browsingagent_no_o_models) is the paper's "
        "stated methodological choice when running the variants "
        "documented in Table 1 (@claim_flightqa_table1): under o1/"
        "o3-mini, BrowsingAgent hallucinates without browser "
        "interaction, which precludes valid agent evaluation. The "
        "footnote $\\dagger$ in Table 1 marks the autoregressive-"
        "planner-only variants for o1 and o3-mini accordingly."
    ),
    prior=0.95,
)

strat_fanoutqa_browsing_partial = support(
    [claim_fanoutqa_table2],
    claim_fanoutqa_browsing_partial_success,
    reason=(
        "BrowsingAgent's 17.0% accuracy on FanOutQA "
        "(@claim_fanoutqa_browsing_partial_success) is read directly "
        "from the BrowsingAgent row of Table 2 (@claim_fanoutqa_"
        "table2). The 'single-Wikipedia-page-answerable' "
        "interpretation is the paper's narrative explanation for "
        "why a non-memory-bearing agent achieves any partial "
        "success on a multi-hop multi-website benchmark."
    ),
    prior=0.9,
)

strat_o1_o3mini_close_to_zero = deduction(
    [claim_flightqa_table1],
    claim_o1_o3mini_close_to_zero,
    reason=(
        "The 1.1% / 3.3% close-to-zero correct rates for o1 and "
        "o3-mini autoregressive planners (@claim_o1_o3mini_close_to_"
        "zero) are read directly from Table 1 (@claim_flightqa_"
        "table1): SIMURA + Autoregressive (o1) Correct = 1.1%, "
        "SIMURA + Autoregressive (o3-mini) Correct = 3.3%. Compared "
        "to gpt-4o autoregressive 14.4% and SIMURA-WM 32.2%."
    ),
    prior=0.99,
)

# FanOutQA derived claims
strat_fanoutqa_response_rate_from_table2 = deduction(
    [claim_fanoutqa_table2],
    claim_fanoutqa_response_rate_jump,
    reason=(
        "FanOutQA response-rate jump 37.0% -> 55.0% "
        "(@claim_fanoutqa_response_rate_jump) is read off Table 2 "
        "(@claim_fanoutqa_table2): SIMURA + AR Response = 37.0%, "
        "SIMURA + WM Response = 55.0%. Relative gain 55/37 - 1 "
        "= 48.6%."
    ),
    prior=0.99,
)

strat_fanoutqa_action_error_from_table2 = deduction(
    [claim_fanoutqa_table2],
    claim_fanoutqa_action_error_reduction,
    reason=(
        "FanOutQA action-error reduction 43% -> 10% -> 1% "
        "(@claim_fanoutqa_action_error_reduction) and 24% browser-"
        "crash rate are read directly from Table 2 (@claim_"
        "fanoutqa_table2)."
    ),
    prior=0.99,
)

# WebArena setup caveat must be carried forward
strat_webarena_caveat_from_setup = support(
    [setup_webarena_eval],
    claim_webarena_setup_caveat,
    reason=(
        "The non-comparability of WebArena absolute scores to prior "
        "work (@claim_webarena_setup_caveat) is a direct consequence "
        "of using the OpenHands-mediated environment "
        "(@setup_webarena_eval) rather than the standard "
        "[@WebArena] setup; the same setup also accounts for the "
        "100-sample random subset and the rewritten agent description."
    ),
    prior=0.95,
)


# ============================================================================
# SECTION 4 -- INDUCTION 1: world-model planning > autoregressive planning
# across 3 task panels (consistent direction). Generative direction:
# the law (WM > AR) predicts each per-task gap.
# ============================================================================

s_wm_predicts_flightqa = support(
    [claim_law_simulative_reasoning_advantage],
    claim_flightqa_table1,
    reason=(
        "If world-model-based simulative reasoning genuinely yields "
        "an advantage over matched autoregressive reasoning across "
        "diverse web-browsing tasks (@claim_law_simulative_reasoning_"
        "advantage), the FlightQA panel (@claim_flightqa_table1) "
        "should show SIMURA-WM > SIMURA-AR. The observed +17.8 pp "
        "(14.4 -> 32.2) gap, significant at p<0.01, is the predicted "
        "consequence on the deepest-navigation task family."
    ),
    prior=0.9,
)

s_wm_predicts_fanoutqa = support(
    [claim_law_simulative_reasoning_advantage],
    claim_fanoutqa_table2,
    reason=(
        "If world-model planning genuinely outperforms autoregressive "
        "planning across web tasks (@claim_law_simulative_reasoning_"
        "advantage), FanOutQA (@claim_fanoutqa_table2, multi-hop "
        "multi-website QA) should show the same direction. The "
        "observed +9.6 pp (20.2 -> 29.8) accuracy gap and +18 pp "
        "(37.0 -> 55.0) response-rate gap, significant at p=0.011, "
        "are the predicted consequences on the breadth-stressing "
        "task family."
    ),
    prior=0.9,
)

s_wm_predicts_webarena = support(
    [claim_law_simulative_reasoning_advantage],
    claim_webarena_table3,
    reason=(
        "If world-model planning genuinely outperforms autoregressive "
        "planning across web tasks (@claim_law_simulative_reasoning_"
        "advantage), WebArena (@claim_webarena_table3, general "
        "automation) should also show the same direction. The "
        "observed +4.0 pp (19.0 -> 23.0) success-rate gap is the "
        "predicted consequence on the generality-stressing task "
        "family."
    ),
    prior=0.9,
)

ind_wm_advantage_flight_fan = induction(
    s_wm_predicts_flightqa,
    s_wm_predicts_fanoutqa,
    law=claim_law_simulative_reasoning_advantage,
    reason=(
        "FlightQA and FanOutQA are independent web-browsing task "
        "families with different structure (deep complex-site "
        "navigation vs broad multi-hop multi-website QA), different "
        "datasets, different evaluation protocols (LLM-judge "
        "groundedness/relevance vs answer-accuracy match), and "
        "different gpt-4o backbone versions. Both show WM > AR with "
        "statistical significance, supporting the cross-task law."
    ),
)

ind_wm_advantage_full = induction(
    ind_wm_advantage_flight_fan,
    s_wm_predicts_webarena,
    law=claim_law_simulative_reasoning_advantage,
    reason=(
        "WebArena adds a third independent task family (general web "
        "automation across simulated Reddit/shopping/GitLab/map/wiki "
        "sites). The observed WM > AR direction on WebArena, combined "
        "with the FlightQA-FanOutQA induction, completes the cross-"
        "task induction over the three families evaluated in the "
        "paper."
    ),
)


# ============================================================================
# SECTION 4 -- INDUCTION 2: SIMURA full > BrowsingAgent across 3 panels.
# ============================================================================

s_simura_predicts_flightqa = support(
    [claim_law_simura_beats_open_baseline],
    claim_flightqa_table1,
    reason=(
        "If SIMURA's full architecture genuinely outperforms the "
        "OpenHands BrowsingAgent baseline across web-browsing tasks "
        "(@claim_law_simura_beats_open_baseline), FlightQA "
        "(@claim_flightqa_table1) should show SIMURA-WM > "
        "BrowsingAgent. The observed +32.2 pp (0.0 -> 32.2) gap is "
        "the predicted consequence."
    ),
    prior=0.92,
)

s_simura_predicts_fanoutqa = support(
    [claim_law_simura_beats_open_baseline],
    claim_fanoutqa_table2,
    reason=(
        "Cross-architecture: if SIMURA generally beats BrowsingAgent "
        "(@claim_law_simura_beats_open_baseline), FanOutQA "
        "(@claim_fanoutqa_table2) should show the same direction. "
        "Observed +12.8 pp (17.0 -> 29.8) gap confirms."
    ),
    prior=0.92,
)

s_simura_predicts_webarena = support(
    [claim_law_simura_beats_open_baseline],
    claim_webarena_table3,
    reason=(
        "Cross-architecture: if SIMURA generally beats BrowsingAgent "
        "(@claim_law_simura_beats_open_baseline), WebArena "
        "(@claim_webarena_table3) should show the same direction. "
        "Observed +11.0 pp (12.0 -> 23.0) gap confirms."
    ),
    prior=0.92,
)

ind_simura_beats_open_flight_fan = induction(
    s_simura_predicts_flightqa,
    s_simura_predicts_fanoutqa,
    law=claim_law_simura_beats_open_baseline,
    reason=(
        "FlightQA and FanOutQA independently confirm SIMURA-full > "
        "BrowsingAgent under the same gpt-4o backbone but different "
        "tasks/datasets/eval protocols."
    ),
)

ind_simura_beats_open_full = induction(
    ind_simura_beats_open_flight_fan,
    s_simura_predicts_webarena,
    law=claim_law_simura_beats_open_baseline,
    reason=(
        "WebArena adds the third independent panel completing the "
        "cross-task generality induction for SIMURA-full > "
        "BrowsingAgent."
    ),
)


# ============================================================================
# SECTION 4 -- INDUCTION 3 (within FlightQA): WM > AR across constraint
# counts 3-8 -> the within-task constraint-scaling generality law.
# ============================================================================

# Group constraint counts into two endpoints since per-bucket sub-tables
# are not separately tabulated; treat the Fig. 9 plot as the overall
# observation. Use per-end induction with the law as the conclusion.

claim_wm_gap_low_constraints = claim(
    "**Within FlightQA: WM > AR at low constraint counts (3-5).** "
    "The Fig. 9 curves at constraint counts 3, 4, 5 each show "
    "a positive gap (WM > AR), albeit with moderate magnitude.",
    title="Within FlightQA: WM > AR at constraint counts 3-5 (Fig. 9 left segment)",
)

claim_wm_gap_high_constraints = claim(
    "**Within FlightQA: WM > AR at high constraint counts (6-8).** "
    "The Fig. 9 curves at constraint counts 6, 7, 8 each show a "
    "positive gap (WM > AR), with the 7-constraint point exhibiting "
    "the sharp uptick described in the paper.",
    title="Within FlightQA: WM > AR at constraint counts 6-8 (Fig. 9 right segment)",
)

s_wm_predicts_low_constraints = support(
    [claim_law_generality_across_constraint_complexity],
    claim_wm_gap_low_constraints,
    reason=(
        "If WM consistently beats AR across constraint counts "
        "(@claim_law_generality_across_constraint_complexity), "
        "constraint counts 3-5 should show a positive gap "
        "(@claim_wm_gap_low_constraints). Fig. 9 confirms."
    ),
    prior=0.85,
)

s_wm_predicts_high_constraints = support(
    [claim_law_generality_across_constraint_complexity],
    claim_wm_gap_high_constraints,
    reason=(
        "If WM consistently beats AR across constraint counts "
        "(@claim_law_generality_across_constraint_complexity), "
        "constraint counts 6-8 should also show a positive gap "
        "(@claim_wm_gap_high_constraints). Fig. 9 confirms; the 7-"
        "constraint uptick is a separate phenomenon attributed to "
        "memorization/implicit constraints, not to the WM/AR gap."
    ),
    prior=0.85,
)

ind_constraint_scaling = induction(
    s_wm_predicts_low_constraints,
    s_wm_predicts_high_constraints,
    law=claim_law_generality_across_constraint_complexity,
    reason=(
        "Low-constraint and high-constraint endpoints of Fig. 9 "
        "are separate sub-populations of FlightQA questions "
        "(constraint counts 3-5 vs 6-8). Both show positive WM-AR "
        "gaps, supporting the within-task constraint-scaling "
        "generality law and the broader 'reasoning ability' "
        "interpretation (@claim_flightqa_constraint_scaling)."
    ),
)

# Anchor the Fig. 9 observation to a data leaf via FlightQA Table 1.
# The constraint-scaling figure is presented adjacent to Table 1 in the
# paper and is read directly off the same per-question evaluation runs.
strat_fig9_from_flightqa_data = deduction(
    [claim_flightqa_table1],
    claim_flightqa_constraint_scaling,
    reason=(
        "The constraint-scaling Fig. 9 observation "
        "(@claim_flightqa_constraint_scaling) is computed from the "
        "same set of FlightQA runs that produced Table 1 "
        "(@claim_flightqa_table1), grouped by constraint count "
        "rather than method. The 'WM > AR at every constraint "
        "count' reading is the per-bucket disaggregation of the "
        "aggregate WM-vs-AR gap reported in Table 1."
    ),
    prior=0.95,
)

# Anchor the per-segment WM-gap claims to Fig. 9 observation so they
# inherit empirical signal.
strat_low_seg_from_fig9 = deduction(
    [claim_flightqa_constraint_scaling],
    claim_wm_gap_low_constraints,
    reason=(
        "The low-constraint segment WM-vs-AR gap "
        "(@claim_wm_gap_low_constraints, counts 3-5) is read from "
        "the left segment of Fig. 9 (@claim_flightqa_constraint_"
        "scaling): each constraint count from 3 to 5 shows a "
        "positive WM-AR gap on the plotted curves."
    ),
    prior=0.95,
)

strat_high_seg_from_fig9 = deduction(
    [claim_flightqa_constraint_scaling],
    claim_wm_gap_high_constraints,
    reason=(
        "The high-constraint segment WM-vs-AR gap "
        "(@claim_wm_gap_high_constraints, counts 6-8) is read from "
        "the right segment of Fig. 9 (@claim_flightqa_constraint_"
        "scaling): each constraint count from 6 to 8 shows a "
        "positive WM-AR gap on the plotted curves, with the 7-"
        "constraint uptick attributed separately to memorization/"
        "implicit constraints."
    ),
    prior=0.95,
)


# ============================================================================
# SECTION 4 -- COMPONENT ATTRIBUTION (ablation reading)
# ============================================================================

strat_structured_pipeline_helps = deduction(
    [
        claim_flightqa_table1,
        claim_fanoutqa_table2,
        claim_webarena_table3,
    ],
    claim_structured_pipeline_helps_independently,
    reason=(
        "Comparing BrowsingAgent vs SIMURA-AR rows of each table "
        "(@claim_flightqa_table1: 0.0 -> 14.4; @claim_fanoutqa_"
        "table2: 17.0 -> 20.2; @claim_webarena_table3: 12.0 -> "
        "19.0) shows the structured-NL pipeline alone (encoder + "
        "memory + actor + clustering) produces a measurable "
        "improvement on every panel. The action-error reduction "
        "(93.3% -> 1.1% on FlightQA; 43% -> 10% on FanOutQA) "
        "explains most of this gap. The structured-pipeline-only "
        "claim (@claim_structured_pipeline_helps_independently) "
        "is read directly from these row pairs."
    ),
    prior=0.97,
)

strat_world_model_adds_planning = deduction(
    [
        claim_flightqa_table1,
        claim_fanoutqa_table2,
        claim_webarena_table3,
        claim_flightqa_repetition_reduction,
    ],
    claim_world_model_adds_planning_advantage,
    reason=(
        "Comparing SIMURA-AR vs SIMURA-WM rows isolates the world-"
        "model planner's contribution holding the structured pipeline "
        "fixed: @claim_flightqa_table1 14.4 -> 32.2 (+17.8 pp); "
        "@claim_fanoutqa_table2 20.2 -> 29.8 (+9.6 pp); "
        "@claim_webarena_table3 19.0 -> 23.0 (+4.0 pp). The "
        "operational mechanism on FlightQA is repetition reduction "
        "44.4% -> 18.9% (@claim_flightqa_repetition_reduction). "
        "@claim_world_model_adds_planning_advantage is the synthesis."
    ),
    prior=0.97,
)

strat_combine_multiplicatively = deduction(
    [
        claim_flightqa_table1,
        claim_structured_pipeline_helps_independently,
        claim_world_model_adds_planning_advantage,
    ],
    claim_components_combine_multiplicatively,
    reason=(
        "On FlightQA, BrowsingAgent achieves 0.0% (@claim_flightqa_"
        "table1), SIMURA-AR achieves 14.4% (structured pipeline "
        "alone, @claim_structured_pipeline_helps_independently), and "
        "SIMURA-WM achieves 32.2% (combined, @claim_world_model_"
        "adds_planning_advantage). The combined gain (+32.2 pp) "
        "exceeds neither component's solo gain alone, and the "
        "structured-pipeline gain (+14.4 pp from 0) plus the WM "
        "increment (+17.8 pp) shows that the components are "
        "complementary rather than redundant."
    ),
    prior=0.95,
)


# ============================================================================
# SECTION 4 -- HEADLINE PANEL CLAIM AGGREGATION
# ============================================================================

strat_overview_panel_aggregation = deduction(
    [
        claim_flightqa_table1,
        claim_fanoutqa_table2,
        claim_webarena_table3,
    ],
    claim_overview_three_task_panel,
    reason=(
        "The cross-task overview claim (@claim_overview_three_task_"
        "panel) is the table-aggregation of the three per-task "
        "tables: @claim_flightqa_table1 (Table 1), @claim_fanoutqa_"
        "table2 (Table 2), @claim_webarena_table3 (Table 3). Each "
        "row is a direct transcription."
    ),
    prior=0.99,
)

strat_simura_beats_browsing_aggregate = deduction(
    [
        claim_law_simura_beats_open_baseline,
        claim_overview_three_task_panel,
    ],
    claim_simura_beats_browsingagent_across_tasks,
    reason=(
        "The cross-task synthesis (@claim_simura_beats_browsingagent_"
        "across_tasks) follows from the cross-task generality law "
        "(@claim_law_simura_beats_open_baseline) plus the per-panel "
        "transcriptions in @claim_overview_three_task_panel. The "
        "specific pp deltas (32.2/12.8/11.0) and relative gains "
        "(unbounded/+75.3%/+91.7%) are arithmetic readings of the "
        "panel."
    ),
    prior=0.97,
)

strat_wm_beats_ar_aggregate = deduction(
    [
        claim_law_simulative_reasoning_advantage,
        claim_overview_three_task_panel,
        claim_statistical_significance,
    ],
    claim_wm_beats_ar_across_tasks,
    reason=(
        "The cross-task synthesis WM > AR (@claim_wm_beats_ar_"
        "across_tasks) follows from the cross-task generality law "
        "(@claim_law_simulative_reasoning_advantage), the panel "
        "transcriptions (@claim_overview_three_task_panel), and the "
        "statistical-significance summary (@claim_statistical_"
        "significance, p<0.01 FlightQA / p=0.011 FanOutQA)."
    ),
    prior=0.97,
)

strat_significance_from_per_table = deduction(
    [claim_flightqa_table1, claim_fanoutqa_table2],
    claim_statistical_significance,
    reason=(
        "Statistical significance levels (@claim_statistical_"
        "significance) are reported in the per-table footnotes: "
        "** = p<0.01 in @claim_flightqa_table1; * = p<0.05 (with "
        "narrative p=0.011) in @claim_fanoutqa_table2."
    ),
    prior=0.99,
)


# ============================================================================
# RELATED-WORK ANCHORING
# ============================================================================

strat_one_task_one_agent_from_lit = support(
    [claim_existing_web_agents_react_limited, claim_llm_agents_two_lines],
    claim_one_task_one_agent_limit,
    reason=(
        "The one-task-one-agent diagnosis (@claim_one_task_one_agent_"
        "limit) is supported by the existing-agents literature "
        "characterization: web-browsing agents are typically domain-"
        "specialized ReAct-based systems (@claim_existing_web_agents_"
        "react_limited), and the two main LLM-agent design lines "
        "(data-collection-then-training; prompt-based workflows; "
        "@claim_llm_agents_two_lines) are both implemented as task-"
        "specialized pipelines. The cross-task transferability "
        "limitation is widely recognized in this literature."
    ),
    prior=0.85,
    background=[setup_fm_agents],
)

strat_autoregressive_limit_from_definition = support(
    [claim_existing_web_agents_react_limited],
    claim_autoregressive_planning_limit,
    reason=(
        "The autoregressive-planning limitation (@claim_autoregressive_"
        "planning_limit, no explicit counterfactual simulation) is the "
        "inherent operational consequence of the paper's definition "
        "of autoregressive reasoning (@setup_autoregressive_reasoning_"
        "definition, p(z_t | z_{<t}, x) without explicit modeling/"
        "simulation of future outcomes), and is empirically observed "
        "in existing ReAct-style web agents "
        "(@claim_existing_web_agents_react_limited) which routinely "
        "fail to recover from previous mistakes. The 'myopia + error "
        "accumulation' pathology is documented in [@Andreas2022; "
        "@ReAct]."
    ),
    background=[setup_autoregressive_reasoning_definition],
    prior=0.9,
)

strat_continuous_embedding_brittle_from_lit = support(
    [claim_existing_wm_continuous_embedding_limit],
    claim_continuous_embedding_brittle,
    reason=(
        "The continuous-embedding brittleness argument "
        "(@claim_continuous_embedding_brittle) recapitulates the "
        "characterization in the world-model literature "
        "(@claim_existing_wm_continuous_embedding_limit) -- existing "
        "world models that use holistic continuous embeddings suffer "
        "from noise/variability problems [@Barrett2017]."
    ),
    prior=0.85,
)

strat_human_concept_from_psych = support(
    [claim_continuous_embedding_brittle],
    claim_human_concept_categorization,
    reason=(
        "The human-concept-categorization argument "
        "(@claim_human_concept_categorization) follows the "
        "psychological literature on emotion/perception construction "
        "[@Barrett2017] and inherits the same brittleness/variability "
        "diagnosis applied to AI world models "
        "(@claim_continuous_embedding_brittle): if continuous "
        "perceptual encoding is brittle, biological cognition's "
        "evolved response is to categorize raw perception into "
        "discrete concepts. The human-mental-simulation baseline "
        "(@setup_human_mental_simulation) supplies the supporting "
        "evidence from cognitive psychology [@Ball2020; "
        "@LeCunWorldModel]."
    ),
    background=[setup_human_mental_simulation],
    prior=0.85,
)

strat_world_model_history_anchor = support(
    [claim_world_model_history],
    claim_simura_intro,
    reason=(
        "SIMURA's proposal (@claim_simura_intro) extends the long "
        "trajectory of world-model-based planning research "
        "(@claim_world_model_history -- games -> control -> math/"
        "Minecraft/web) to a unified, generalized goal-oriented "
        "agent architecture. The paper situates SIMURA as the "
        "natural next step after web-browsing work like [@WebDreamer] "
        "and math-reasoning work like [@RAP]."
    ),
    prior=0.8,
)

strat_existing_benchmarks_motivates_flightqa = support(
    [claim_existing_benchmarks_limit],
    setup_flightqa_dataset,
    reason=(
        "The FlightQA construction (@setup_flightqa_dataset) is "
        "designed to address the documented gaps in existing web-"
        "agent benchmarks (@claim_existing_benchmarks_limit, "
        "simulated/outdated/weakly-evaluated): live flight data, "
        "controlled iterative-extension structure, automatic "
        "verifiability via groundedness-relevance LLM judging."
    ),
    prior=0.9,
)

strat_flightqa_motivates_counterfactual = support(
    [setup_flightqa_dataset],
    claim_flightqa_motivates_counterfactual,
    reason=(
        "The counterfactual-analysis affordance of FlightQA "
        "(@claim_flightqa_motivates_counterfactual) follows directly "
        "from its construction (@setup_flightqa_dataset): each "
        "sequence shares its initial constraints and adds one "
        "constraint per step, isolating constraint count as the "
        "controllable variable."
    ),
    prior=0.95,
)

strat_chatgpt_hallucination_motivates = support(
    [claim_chatgpt_4o_hallucination_example, claim_existing_benchmarks_limit],
    setup_flightqa_evaluation,
    reason=(
        "The FlightQA evaluation design (@setup_flightqa_evaluation, "
        "groundedness-relevance LLM judge) is motivated by both the "
        "live-data-grounding gap of existing benchmarks "
        "(@claim_existing_benchmarks_limit) and the documented "
        "LLM hallucination pathology on time-sensitive queries "
        "(@claim_chatgpt_4o_hallucination_example, [@AssistantBench])."
    ),
    prior=0.9,
)


# ============================================================================
# OPEN-SOURCE RELEASE / CONTRIBUTIONS / CONCLUSION SYNTHESIS
# ============================================================================

strat_open_source_from_prototype = support(
    [claim_prototype_summary],
    claim_open_source_release,
    reason=(
        "The REASONERAGENT-WEB open-source release "
        "(@claim_open_source_release) is the public artifact of the "
        "LLM-based prototype (@claim_prototype_summary), made "
        "available via LLM-Reasoners [@LLMReasoners] and the project "
        "demo URL [@ReasonerAgent]."
    ),
    prior=0.95,
)

strat_contributions_from_six_components = support(
    [
        claim_simura_intro,
        claim_simura_decision_process,
        claim_prototype_summary,
        setup_flightqa_dataset,
        claim_overview_three_task_panel,
        claim_one_task_one_agent_limit,
    ],
    claim_contributions,
    reason=(
        "The six stated contributions (@claim_contributions) are "
        "the union of the diagnosis (@claim_one_task_one_agent_"
        "limit), the formulation (@claim_simura_decision_process), "
        "the architecture (@claim_simura_intro), the prototype "
        "(@claim_prototype_summary), the FlightQA benchmark "
        "(@setup_flightqa_dataset), and the cross-task empirical "
        "results (@claim_overview_three_task_panel)."
    ),
    prior=0.95,
)

strat_conclusion_from_full_panel = support(
    [
        claim_law_simulative_reasoning_advantage,
        claim_law_simura_beats_open_baseline,
        claim_overview_three_task_panel,
    ],
    claim_conclusion_synthesis,
    reason=(
        "The conclusion synthesis (@claim_conclusion_synthesis) is "
        "the high-level summary of the cross-task generality findings "
        "(@claim_law_simulative_reasoning_advantage, @claim_law_simura"
        "_beats_open_baseline) anchored in the three-panel evidence "
        "(@claim_overview_three_task_panel)."
    ),
    prior=0.92,
)

strat_future_work_from_limits = support(
    [claim_limit_runtime, claim_limit_tooling, claim_limit_modality],
    claim_future_work_breadth,
    reason=(
        "The future-work breadth (@claim_future_work_breadth) is "
        "the explicit response to the three identified limitations "
        "(@claim_limit_runtime, @claim_limit_tooling, "
        "@claim_limit_modality), plus the cross-environment / multi-"
        "agent extensions enabled by the model-agnostic design."
    ),
    prior=0.85,
)


# ============================================================================
# ABDUCTION: world-model simulation hypothesis vs alternative explanations
# of SIMURA's empirical gap.
# ============================================================================

# --- Component claims for abduction ---------------------------------------

claim_obs_simura_full_pattern = claim(
    "**Observation: SIMURA's joint empirical fingerprint.** Under "
    "matched gpt-4o backbone, BrowserGym environment, and identical "
    "prompts, SIMURA's full architecture produces a five-fact "
    "fingerprint vs SIMURA + autoregressive planning: "
    "(i) FlightQA correct rate 14.4% -> 32.2% (+124% relative, p<0.01); "
    "(ii) FanOutQA accuracy 20.2% -> 29.8% (+47.5% rel, p=0.011); "
    "(iii) WebArena success 19.0% -> 23.0% (+21.1% rel); "
    "(iv) FlightQA repetitive-action failures 44.4% -> 18.9% (loop "
    "avoidance is a specifically planning-attributable mechanism); "
    "(v) WM > AR at every constraint count (Fig. 9), confirming "
    "task-difficulty-independent advantage. The pattern is observed "
    "while the encoder/memory/actor/prompts/backbone/environment "
    "are all held fixed.",
    title="Observation: 5-fact joint fingerprint -- WM-vs-AR gap on 3 panels + repetition reduction + constraint-scaling",
)

claim_h_world_model_explains = claim(
    "**Hypothesis prediction: explicit simulation-and-evaluation in "
    "the world model + critic explains the joint fingerprint.** "
    "If SIMURA's gain is genuinely produced by the world-model + "
    "critic doing explicit counterfactual simulation and evaluation "
    "of candidate actions before commitment, the predicted "
    "consequences are: (i)-(iii) cross-task accuracy gains; "
    "(iv) loop avoidance because predicted next-state under a "
    "repeated action equals current state -> low value -> not "
    "selected; (v) advantage scaling with reasoning difficulty "
    "(constraint count) because more candidate paths benefit more "
    "from explicit evaluation. All five facts are predicted "
    "qualitatively by this single mechanism.",
    title="Hypothesis: world-model simulation-and-evaluation predicts the 5-fact fingerprint",
)

claim_alt_lm_capability_explains = claim(
    "**Alternative prediction: trivial confounds (bigger LM / more "
    "prompt engineering / more inference compute) explain the "
    "joint fingerprint.** Under the foil that the gain is "
    "attributable to (a) better LM capabilities exposed by SIMURA's "
    "richer prompt structure, (b) more total inference compute "
    "(N=20 critic calls, M=20 policy calls per step), or (c) better "
    "tool-use elicited by structured prompts, the predicted "
    "consequences are at most a uniform accuracy lift. CRUCIALLY, "
    "this alternative cannot explain: "
    "(iv) the *specific* repetition reduction (44.4% -> 18.9%) -- "
    "more compute by itself does not implement loop detection; "
    "(v) the consistent gap across constraint counts -- if the "
    "advantage were just 'more LM capability', it would saturate "
    "at low difficulty rather than persist at high difficulty; "
    "and notably, the o1/o3-mini autoregressive-planner result "
    "(1.1%/3.3% on FlightQA) shows that *more LM reasoning power "
    "alone does not rescue autoregressive planning*. Trivial "
    "confounds explain at most fact (i) at face value.",
    title="Alternative: trivial confounds (bigger LM / more compute / better prompt) explain the 5-fact fingerprint",
)

# Anchor the joint observation to the per-table empirical evidence so it
# carries the data signal into the abduction.
strat_obs_pattern_from_data = deduction(
    [
        claim_flightqa_table1,
        claim_fanoutqa_table2,
        claim_webarena_table3,
        claim_flightqa_repetition_reduction,
        claim_flightqa_constraint_scaling,
    ],
    claim_obs_simura_full_pattern,
    reason=(
        "The 5-fact joint fingerprint (@claim_obs_simura_full_"
        "pattern) is the literal aggregation of: "
        "(i) FlightQA correct rate gap (@claim_flightqa_table1, "
        "14.4 -> 32.2); "
        "(ii) FanOutQA accuracy gap (@claim_fanoutqa_table2, 20.2 "
        "-> 29.8); "
        "(iii) WebArena success gap (@claim_webarena_table3, 19.0 "
        "-> 23.0); "
        "(iv) FlightQA repetition-failure reduction "
        "(@claim_flightqa_repetition_reduction, 44.4 -> 18.9); "
        "(v) WM > AR at every constraint count "
        "(@claim_flightqa_constraint_scaling, Fig. 9). "
        "All five are direct readings of cited tables/figures."
    ),
    prior=0.97,
)

# --- Build the three component strategies ---------------------------------

s_h_explains_obs = support(
    [claim_h_world_model_explains],
    claim_obs_simura_full_pattern,
    reason=(
        "Under the world-model-simulation hypothesis "
        "(@claim_h_world_model_explains), all five observed facts "
        "(@claim_obs_simura_full_pattern) are coherent predicted "
        "consequences of a single mechanism: explicit simulation + "
        "evaluation lifts accuracy ((i)-(iii)), filters loops "
        "((iv)), and benefits more on difficult cases ((v))."
    ),
    prior=0.7,
)

s_alt_explains_obs = support(
    [claim_alt_lm_capability_explains],
    claim_obs_simura_full_pattern,
    reason=(
        "Under trivial confounds (@claim_alt_lm_capability_explains), "
        "the 5-fact joint fingerprint cannot be jointly explained: "
        "more LM capability alone does not implement loop detection "
        "((iv)), nor does it preserve a constant gap across "
        "constraint complexity ((v)), nor does it explain why o1/"
        "o3-mini autoregressive planning collapses to 1.1%/3.3% "
        "(@claim_o1_o3mini_close_to_zero) -- a more capable LM "
        "should help if 'more LM capability' were the true "
        "mechanism. The trivial confounds can explain at most "
        "fact (i) in isolation."
    ),
    prior=0.2,
)

comp_h_vs_alt = compare(
    claim_h_world_model_explains,
    claim_alt_lm_capability_explains,
    claim_obs_simura_full_pattern,
    reason=(
        "The world-model hypothesis (@claim_h_world_model_explains) "
        "uniquely explains the joint 5-fact pattern (@claim_obs_"
        "simura_full_pattern), with the strongest discriminating "
        "signals being: "
        "(A) The o1/o3-mini autoregressive-planner result -- "
        "swapping in a more powerful reasoning LLM *worsens* "
        "autoregressive planning rather than helping it, ruling "
        "out 'more LM capability' as the mechanism. "
        "(B) The repetition-reduction gap (44.4% -> 18.9%) -- a "
        "specifically planning-attributable mechanism that 'more "
        "compute' cannot produce. "
        "(C) The constraint-count consistency (Fig. 9) -- the "
        "advantage persists across difficulty levels, inconsistent "
        "with a saturating LM-capability effect. "
        "(D) The matched-pipeline within-architecture comparison -- "
        "all non-planner modules are identical, so only the planner "
        "swap can explain the gap."
    ),
    prior=0.93,
)

abd_world_model_vs_lm_capability = abduction(
    s_h_explains_obs,
    s_alt_explains_obs,
    comp_h_vs_alt,
    reason=(
        "Both hypotheses attempt to explain the same observation: "
        "the 5-fact SIMURA-vs-AR fingerprint (@claim_obs_simura_"
        "full_pattern). The world-model-simulation hypothesis "
        "(@claim_h_world_model_explains) predicts exactly this "
        "fingerprint as a coherent signature. Trivial confounds "
        "(@claim_alt_lm_capability_explains) predict at most fact "
        "(i) and contradict the o1/o3-mini result. The "
        "discriminating signal is decisive on at least four axes "
        "simultaneously."
    ),
)


# ============================================================================
# CONTRADICTIONS
# ============================================================================

# CONTRADICTION 1: one-task-one-agent paradigm assumption vs SIMURA's
# demonstrated cross-task generality.

claim_one_task_one_agent_assumption = claim(
    "**Foil: agent design must be one-task-one-agent.** The "
    "prevailing pattern in foundation-model agent practice "
    "(@setup_fm_agents) is to design a domain-specialized agent for "
    "each task (web automation, internet research, social "
    "simulation, software engineering, scientific research, etc.). "
    "Under this foil, a *single* generalized architecture cannot "
    "match domain-specialized agents on diverse tasks; cross-task "
    "transfer is achievable only by composing specialists.",
    title="Foil: one-task-one-agent is necessary for competitive performance across tasks",
)

strat_one_task_one_agent_assumption_from_lit = support(
    [
        claim_one_task_one_agent_limit,
        claim_generalist_two_lines,
    ],
    claim_one_task_one_agent_assumption,
    reason=(
        "The one-task-one-agent assumption (@claim_one_task_one_"
        "agent_assumption) is the implicit premise behind both the "
        "documented diagnosis (@claim_one_task_one_agent_limit) and "
        "the multi-agent-workflow generalist line "
        "(@claim_generalist_two_lines, G1) which composes "
        "specialists rather than building a unified architecture."
    ),
    prior=0.6,
)

contra_one_task_vs_simura_generality = contradiction(
    claim_one_task_one_agent_assumption,
    claim_law_simura_beats_open_baseline,
    reason=(
        "The one-task-one-agent foil (@claim_one_task_one_agent_"
        "assumption: a single generalized architecture cannot match "
        "domain-specialized agents) and SIMURA's cross-task "
        "generality (@claim_law_simura_beats_open_baseline: SIMURA "
        "full > BrowsingAgent on 3 different task families with the "
        "same architecture and backbone) cannot both be true. If "
        "one-task-one-agent is necessary, a single SIMURA "
        "configuration cannot consistently outperform a "
        "representative open-web specialist across structurally "
        "different task families. If the cross-task generality "
        "result holds (with statistical significance on FlightQA "
        "and FanOutQA), the foil must be wrong."
    ),
    prior=0.92,
)

# CONTRADICTION 2: 'autoregressive reasoning is sufficient for complex
# planning' vs SIMURA's empirical gap on the same backbone.

claim_autoregressive_sufficient_assumption = claim(
    "**Foil: autoregressive reasoning is sufficient for complex "
    "agentic planning.** Under the prevailing practice of building "
    "agents on autoregressive backbones (@setup_autoregressive_"
    "reasoning_definition; ReAct [@ReAct], CoT-style chain-of-"
    "thought) and the rise of RL-trained reasoning LLMs (o1 "
    "[@OpenAIo1], DeepSeek-R1 [@DeepSeekR1]) -- which exhibit some "
    "emergent planning -- the implicit assumption is that "
    "autoregressive reasoning *alone* (with sufficiently strong "
    "models) is enough for complex agentic planning, without "
    "requiring an explicit world-model + critic.",
    title="Foil: autoregressive reasoning is sufficient for complex planning (no explicit WM needed)",
)

strat_autoregressive_sufficient_from_lit = support(
    [
        claim_existing_web_agents_react_limited,
    ],
    claim_autoregressive_sufficient_assumption,
    background=[setup_autoregressive_reasoning_definition],
    reason=(
        "The autoregressive-sufficiency foil "
        "(@claim_autoregressive_sufficient_assumption) is the "
        "implicit operational premise of existing ReAct-style web "
        "agents (@claim_existing_web_agents_react_limited) and "
        "RL-trained reasoning LLMs (@setup_autoregressive_reasoning_"
        "definition discusses the procedural mode). The hope is "
        "that strong-enough autoregressive models alone solve "
        "complex agentic tasks without explicit simulation."
    ),
    prior=0.55,
)

contra_autoregressive_vs_simura_gap = contradiction(
    claim_autoregressive_sufficient_assumption,
    claim_law_simulative_reasoning_advantage,
    reason=(
        "The autoregressive-sufficiency foil "
        "(@claim_autoregressive_sufficient_assumption: AR alone with "
        "strong-enough models is enough for complex agentic "
        "planning) and SIMURA's cross-task WM > AR finding "
        "(@claim_law_simulative_reasoning_advantage: holding the "
        "backbone and pipeline fixed, swapping in a world-model + "
        "critic planner improves task-completion rate by up to "
        "+124% on FlightQA, with consistent direction across "
        "FanOutQA and WebArena, and o1/o3-mini autoregressive "
        "planners collapse to 1.1%/3.3% on FlightQA) cannot both "
        "be true. If AR alone were sufficient, neither the WM-vs-AR "
        "gap nor the o1/o3-mini collapse should occur."
    ),
    prior=0.93,
)


__all__ = [
    # New auxiliary claims introduced in wiring
    "claim_wm_gap_low_constraints",
    "claim_wm_gap_high_constraints",
    "claim_obs_simura_full_pattern",
    "claim_h_world_model_explains",
    "claim_alt_lm_capability_explains",
    "claim_one_task_one_agent_assumption",
    "claim_autoregressive_sufficient_assumption",
    # Inductions
    "ind_wm_advantage_flight_fan",
    "ind_wm_advantage_full",
    "ind_simura_beats_open_flight_fan",
    "ind_simura_beats_open_full",
    "ind_constraint_scaling",
    # Abduction
    "abd_world_model_vs_lm_capability",
    # Contradictions
    "contra_one_task_vs_simura_generality",
    "contra_autoregressive_vs_simura_gap",
]
