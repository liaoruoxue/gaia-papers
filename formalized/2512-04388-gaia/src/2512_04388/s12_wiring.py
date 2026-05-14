"""Pass 2 wiring: strategies, abductions, inductions, contradictions
linking the propositions extracted in motivation + s2-s11 into the
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
    setup_frontier_llms,
    setup_agentic_products,
    q_central,
    claim_provider_specialization,
    claim_manual_orchestration_limits,
    claim_prior_routing_inexpressive,
    claim_conductor_proposal,
    claim_conductor_two_emergent_skills,
    claim_extension_dynamic_pool,
    claim_extension_recursive,
    claim_headline_sota,
    claim_headline_beats_baselines,
    claim_headline_pool_generality,
    claim_headline_recursive_scaling,
    claim_three_contributions,
    claim_broader_thesis,
)
from .s2_rl_reasoning import (
    setup_rl_reasoning_paradigm,
    setup_reward_definition,
    setup_grpo_objective,
    setup_grpo_advantage,
    claim_grpo_yields_thinking,
)
from .s3_setup import (
    setup_conductor_task,
    setup_workflow_definition,
    setup_topology_expressivity,
    setup_workflow_execution,
    setup_conductor_reward,
    claim_natural_language_medium,
    claim_grpo_emergent_strategies,
    claim_compatible_any_rl_algo,
)
from .s4_method import (
    setup_few_shot_conditioning,
    setup_ordinal_model_names,
    setup_recursion_definition,
    claim_exploration_sidestep,
    claim_emergent_prompt_engineering,
    claim_emergent_topology_design,
    claim_emergent_task_adaptivity,
    claim_meta_orchestrator_thesis,
)
from .s5_extensions import (
    setup_dynamic_pool_protocol,
    claim_dynamic_pool_design_aim,
    setup_recursive_finetuning_protocol,
    claim_recursive_scaling_aim,
    claim_recursion_decision_protocol,
    claim_recursion_cost_cap,
)
from .s6_main_results import (
    setup_base_model,
    setup_worker_pool,
    setup_training_data,
    setup_eval_benchmarks,
    setup_training_hyperparameters,
    setup_unconstrained_setting,
    claim_table1_full,
    claim_math500_unconstrained,
    claim_mmlu_unconstrained,
    claim_rlpr_unconstrained,
    claim_lcb_unconstrained,
    claim_aime25_unconstrained,
    claim_bcb_unconstrained,
    claim_gpqa_unconstrained,
    claim_avg_unconstrained,
    claim_long_tail_difficulty,
)
from .s7_controlled_eval import (
    setup_constrained_setting,
    setup_baselines_controlled,
    claim_table7_full,
    claim_conductor_avg_controlled,
    claim_avg_workflow_steps,
    claim_table5_efficiency_consensus,
    claim_table6_efficiency_baselines,
    claim_moa_failure_mode,
    claim_masrouter_failure_mode,
    claim_controlled_summary,
)
from .s8_user_recursion import (
    claim_open_pool_finetuned,
    claim_closed_pool_finetuned,
    claim_pool_generalization_thesis,
    claim_table2_recursion_full,
    claim_recursion_bcb_redistribution,
    claim_recursion_aime25,
    claim_recursion_gpqa,
    claim_recursion_bcb,
    claim_recursion_dynamic_scaling_thesis,
    claim_ood_few_shot_finding,
    claim_ood_few_shot_explanation,
    claim_table8_ood_constrained,
)
from .s9_analysis_ablations import (
    claim_3b_same_agent_dist,
    claim_7b_better_prompt_engineering,
    claim_scale_thesis,
    claim_workflow_step_distribution,
    claim_table9_ablations,
    claim_subtask_ablation,
    claim_few_shot_ablation,
    claim_fine_grained_topology_ablation,
    claim_table10_agent_selection_ablation,
    claim_subtask_alone_matters,
    claim_table11_conductor_replacement,
    claim_frontier_orchestrator_evidence,
    claim_conductor_training_essential,
    claim_per_model_specialization,
    claim_weak_models_essential_for_subtasks,
    claim_qwen_thinking_vs_direct_bcb,
)
from .s10_related_work import (
    claim_rl_with_tools_literature,
    claim_conductor_rl_tool_positioning,
    claim_multi_agent_coord_literature,
    claim_conductor_mas_positioning,
    claim_positioning_summary,
)
from .s11_discussion import (
    claim_discussion_synthesis,
    claim_meta_agent_thesis,
    claim_future_beyond_llms,
    claim_ethics_economic_divide,
    claim_reproducibility,
)


# ============================================================================
# DIAGNOSIS -> PROPOSAL CHAIN
# ============================================================================

strat_provider_specialization_from_literature = support(
    [claim_grpo_yields_thinking],
    claim_provider_specialization,
    reason=(
        "The per-provider specialization claim "
        "(@claim_provider_specialization) is documented in the LLM "
        "evaluation survey [@Chang2024SurveyEval] and validated by the "
        "Conductor's own per-benchmark per-worker numerics (Table 1, "
        "@claim_table1_full): GPT-5 strongest on AIME / LCB, Gemini "
        "strongest on GPQA-D, Claude strongest on BCB. The "
        "specialization arises from the RL-reasoning paradigm "
        "(@claim_grpo_yields_thinking) where each provider tunes "
        "models against different verifiable problem distributions."
    ),
    prior=0.92,
    background=[setup_frontier_llms],
)

strat_manual_orch_limits = support(
    [claim_provider_specialization],
    claim_manual_orchestration_limits,
    reason=(
        "Manual orchestration limits (@claim_manual_orchestration_limits) "
        "follow from per-provider specialization "
        "(@claim_provider_specialization): if no single model is "
        "universally optimal, a manually designed scaffold cannot "
        "anticipate the optimal worker-per-input choice, and must be "
        "re-engineered as the frontier-LLM pool evolves. The "
        "commercial agentic-product evidence (@setup_agentic_products) "
        "demonstrates this is the current state of practice."
    ),
    prior=0.9,
    background=[setup_agentic_products],
)

strat_prior_routing_inexpressive = support(
    [claim_multi_agent_coord_literature],
    claim_prior_routing_inexpressive,
    reason=(
        "The diagnosis that prior routers are inexpressive "
        "(@claim_prior_routing_inexpressive) is the literal scope of "
        "MASRouter, RouterDC, Smoothie, MoA, multi-agent-debate, and "
        "GPTSwarm as characterized in @claim_multi_agent_coord_"
        "literature: each restricts the topology/coordination space to "
        "a pre-specified vocabulary or a routing classifier output, "
        "rather than free natural-language workflow specification."
    ),
    prior=0.92,
)

# ============================================================================
# CONDUCTOR PROPOSAL emerges from the three diagnoses
# ============================================================================

strat_conductor_proposal = support(
    [
        claim_provider_specialization,
        claim_manual_orchestration_limits,
        claim_prior_routing_inexpressive,
    ],
    claim_conductor_proposal,
    reason=(
        "The Conductor proposal (@claim_conductor_proposal) is the "
        "joint response to the three diagnoses: per-provider "
        "specialization (@claim_provider_specialization) motivates "
        "using multiple worker LLMs, manual-orchestration limits "
        "(@claim_manual_orchestration_limits) motivate end-to-end "
        "learning of the coordination strategy, and the "
        "inexpressivity of prior routing approaches "
        "(@claim_prior_routing_inexpressive) motivates the unrestricted "
        "natural-language output medium. The formal workflow "
        "definition (@setup_workflow_definition) and Conductor reward "
        "(@setup_conductor_reward) implement the proposal."
    ),
    prior=0.93,
    background=[
        setup_workflow_definition,
        setup_workflow_execution,
        setup_conductor_reward,
    ],
)

# ============================================================================
# Natural-language medium gives complete specification freedom
# ============================================================================

strat_natural_language_medium = support(
    [claim_conductor_proposal],
    claim_natural_language_medium,
    reason=(
        "The complete-specification-freedom claim "
        "(@claim_natural_language_medium) follows from the Conductor's "
        "output format (@claim_conductor_proposal): three "
        "natural-language Python lists allow any subtask string, any "
        "worker ordering, and any access-list pattern. The topology "
        "expressivity (@setup_topology_expressivity) follows directly "
        "from the parsing semantics: best-of-N, chain, and arbitrary "
        "tree topologies are all expressible."
    ),
    prior=0.95,
    background=[setup_topology_expressivity],
)

# ============================================================================
# Emergent skills from end-to-end GRPO training
# ============================================================================

strat_grpo_emergent_strategies = support(
    [claim_grpo_yields_thinking, claim_conductor_proposal],
    claim_grpo_emergent_strategies,
    reason=(
        "The emergence of coordination strategies "
        "(@claim_grpo_emergent_strategies) is the analog of self-"
        "emergent thinking in the GRPO literature "
        "(@claim_grpo_yields_thinking) applied to the Conductor "
        "framework (@claim_conductor_proposal). The Conductor reward "
        "(@setup_conductor_reward) is verifiable end-task accuracy + "
        "format -- the same kind of sparse, end-to-end reward that "
        "elicited thinking behavior in DeepSeek-R1. The Fig. 3 "
        "training-curve evidence confirms emergence over training."
    ),
    prior=0.92,
    background=[setup_conductor_reward, setup_grpo_objective],
)

strat_compatible_any_rl = support(
    [claim_conductor_proposal],
    claim_compatible_any_rl_algo,
    reason=(
        "RL-algorithm agnosticism (@claim_compatible_any_rl_algo) "
        "follows from the structure of the Conductor reward "
        "(@setup_conductor_reward) and the standard policy-gradient "
        "form of the GRPO objective (@setup_grpo_objective): any RL "
        "algorithm (PPO [@Schulman2017PPO], REINFORCE [@Ahmadian2024Back], "
        "or GRPO [@Shao2024DeepSeekMath]) that optimizes "
        "expected reward over a policy can be plugged in. The "
        "Conductor proposal (@claim_conductor_proposal) is what is "
        "required as a claim premise; the objective forms are "
        "background settings."
    ),
    prior=0.95,
    background=[setup_conductor_reward, setup_grpo_objective],
)

# ============================================================================
# Two emergent skills (Fig. 3, Section 3.1 narrative)
# ============================================================================

strat_emergent_prompt_engineering = support(
    [claim_grpo_emergent_strategies, claim_avg_unconstrained],
    claim_emergent_prompt_engineering,
    reason=(
        "Emergent prompt engineering (@claim_emergent_prompt_engineering) "
        "is the qualitative description of the prompt-engineering "
        "component of the emergent strategies "
        "(@claim_grpo_emergent_strategies). The 3B-vs-7B scale "
        "analysis (Fig. 7) shows that even with identical agent "
        "selection the 7B Conductor outperforms 3B via prompt "
        "quality, providing direct empirical evidence that the "
        "framework develops prompt-engineering skill. The unconstrained "
        "average (@claim_avg_unconstrained) demonstrates the headline "
        "downstream effect."
    ),
    prior=0.93,
)

strat_emergent_topology_design = support(
    [claim_grpo_emergent_strategies, claim_natural_language_medium],
    claim_emergent_topology_design,
    reason=(
        "Emergent topology design (@claim_emergent_topology_design) is "
        "the qualitative description of the topology component of the "
        "emergent strategies (@claim_grpo_emergent_strategies), "
        "enabled by the natural-language medium "
        "(@claim_natural_language_medium) which makes any topology "
        "expressible. The categorized modes (chain, tree, factual-"
        "recall, abdication) are illustrated in Appendix F (Figs. 19-28)."
    ),
    prior=0.92,
)

strat_two_emergent_skills_assembly = support(
    [claim_emergent_prompt_engineering, claim_emergent_topology_design],
    claim_conductor_two_emergent_skills,
    reason=(
        "The two-emergent-skills synthesis "
        "(@claim_conductor_two_emergent_skills) is the conjunction of "
        "(a) emergent prompt engineering "
        "(@claim_emergent_prompt_engineering) and (b) emergent "
        "topology design (@claim_emergent_topology_design), both "
        "appearing through pure end-to-end GRPO reward maximization "
        "without explicit supervision."
    ),
    prior=0.95,
)

strat_emergent_task_adaptivity = support(
    [claim_grpo_emergent_strategies],
    claim_emergent_task_adaptivity,
    reason=(
        "Task and difficulty adaptivity "
        "(@claim_emergent_task_adaptivity) is a third emergent "
        "behavior in the GRPO training (@claim_grpo_emergent_strategies): "
        "the Fig. 8 step-distribution histograms show qualitatively "
        "different workflow-length distributions for MMLU (1-2 steps) "
        "vs LiveCodeBench (3-4 steps), and the Appendix F traces "
        "show explicit task-complexity reasoning in the Conductor's "
        "chain-of-thought before workflow specification."
    ),
    prior=0.93,
)

strat_meta_orchestrator_thesis = support(
    [
        claim_conductor_two_emergent_skills,
        claim_emergent_task_adaptivity,
    ],
    claim_meta_orchestrator_thesis,
    reason=(
        "The meta-orchestrator thesis (@claim_meta_orchestrator_thesis) "
        "is supported by the joint demonstration of (a) two emergent "
        "coordination skills (@claim_conductor_two_emergent_skills) "
        "and (b) task-adaptive workflow allocation "
        "(@claim_emergent_task_adaptivity). Together they show the "
        "Conductor behaves as a learned meta-agent rather than a "
        "fixed pipeline."
    ),
    prior=0.94,
)

# ============================================================================
# Method observation: powerful workers eliminate exploration bottleneck
# ============================================================================

strat_exploration_sidestep = support(
    [claim_conductor_proposal],
    claim_exploration_sidestep,
    reason=(
        "Convergence in 200 iterations without KL regularization "
        "(@claim_exploration_sidestep) is the operational statement of "
        "the training hyperparameters (@setup_training_hyperparameters) "
        "under the chosen worker pool (@setup_worker_pool) for the "
        "Conductor framework (@claim_conductor_proposal). The fact "
        "that no KL penalty was needed despite no reference "
        "synchronization is a direct departure from the canonical "
        "RL-for-small-LM recipe [@Cetin2025RLT], explained in the "
        "paper as the powerful workers providing strong initialization."
    ),
    prior=0.9,
    background=[setup_worker_pool, setup_training_hyperparameters],
)

# ============================================================================
# Unconstrained Table 1 per-row claims
# ============================================================================

strat_table1_math500 = support(
    [claim_table1_full],
    claim_math500_unconstrained,
    reason=(
        "The MATH500 unconstrained row claim "
        "(@claim_math500_unconstrained) reads off Table 1 "
        "(@claim_table1_full) directly: Conductor 99.4 vs GPT-5 99.0 "
        "(delta = +0.4 pp)."
    ),
    prior=0.97,
)

strat_table1_mmlu = support(
    [claim_table1_full],
    claim_mmlu_unconstrained,
    reason=(
        "The MMLU unconstrained row claim "
        "(@claim_mmlu_unconstrained) reads off Table 1: Conductor 94.1 "
        "vs GPT-5 93.5 = +0.6 pp."
    ),
    prior=0.97,
)

strat_table1_rlpr = support(
    [claim_table1_full],
    claim_rlpr_unconstrained,
    reason=(
        "The RLPR unconstrained row claim "
        "(@claim_rlpr_unconstrained) reads off Table 1: Conductor "
        "44.75 vs GPT-5 42.20 = +2.55 pp."
    ),
    prior=0.97,
)

strat_table1_lcb = support(
    [claim_table1_full],
    claim_lcb_unconstrained,
    reason=(
        "The LiveCodeBench V6 unconstrained row claim "
        "(@claim_lcb_unconstrained) reads off Table 1: Conductor "
        "83.93 vs GPT-5 82.90 = +1.03 pp; SOTA on the LiveCodeBench "
        "online leaderboard."
    ),
    prior=0.96,
)

strat_table1_aime25 = support(
    [claim_table1_full, claim_long_tail_difficulty],
    claim_aime25_unconstrained,
    reason=(
        "The AIME25 unconstrained row claim "
        "(@claim_aime25_unconstrained) reads off Table 1: Conductor "
        "93.3 vs GPT-5 90.8 = +2.5 pp. The long-tail-difficulty "
        "context (@claim_long_tail_difficulty) interprets this gap "
        "as approximately the o3 -> GPT-5 generation jump on AIME25."
    ),
    prior=0.96,
)

strat_table1_bcb = support(
    [claim_table1_full],
    claim_bcb_unconstrained,
    reason=(
        "The BigCodeBench unconstrained row claim "
        "(@claim_bcb_unconstrained) reads off Table 1: Conductor 37.86 "
        "vs Gemini 2.5 Pro (best non-Conductor) 37.51 = +0.35 pp."
    ),
    prior=0.96,
)

strat_table1_gpqa = support(
    [claim_table1_full, claim_long_tail_difficulty],
    claim_gpqa_unconstrained,
    reason=(
        "The GPQA-D unconstrained row claim "
        "(@claim_gpqa_unconstrained) reads off Table 1: Conductor 87.5 "
        "vs Gemini 2.5 Pro 84.8 = +2.7 pp. The long-tail-difficulty "
        "context (@claim_long_tail_difficulty) interprets this as the "
        "o3 -> GPT-5 generation jump on GPQA-D."
    ),
    prior=0.96,
)

strat_avg_unconstrained = support(
    [
        claim_math500_unconstrained,
        claim_mmlu_unconstrained,
        claim_rlpr_unconstrained,
        claim_lcb_unconstrained,
        claim_aime25_unconstrained,
        claim_bcb_unconstrained,
        claim_gpqa_unconstrained,
    ],
    claim_avg_unconstrained,
    reason=(
        "The unconstrained average claim (@claim_avg_unconstrained) "
        "aggregates the seven per-row deltas "
        "(@claim_math500_unconstrained, @claim_mmlu_unconstrained, "
        "@claim_rlpr_unconstrained, @claim_lcb_unconstrained, "
        "@claim_aime25_unconstrained, @claim_bcb_unconstrained, "
        "@claim_gpqa_unconstrained) and computes the average delta "
        "vs GPT-5 (best baseline) across columns -- yielding +2.49 pp "
        "average. Every column is won by the Conductor."
    ),
    prior=0.95,
    background=[claim_table1_full],
)

# ============================================================================
# Headline SOTA claim anchors to the avg unconstrained
# ============================================================================

strat_headline_sota = support(
    [claim_avg_unconstrained],
    claim_headline_sota,
    reason=(
        "The headline SOTA claim (@claim_headline_sota) is anchored "
        "directly in the Table-1 average and per-column wins "
        "(@claim_avg_unconstrained): all 7 columns won, average 77.27 "
        "vs GPT-5 74.78 (+2.49 pp). The headline is the abstract-"
        "level statement of the Table 1 result."
    ),
    prior=0.97,
)

# ============================================================================
# Controlled-setting Table 7 + downstream
# ============================================================================

strat_avg_controlled = support(
    [claim_table7_full],
    claim_conductor_avg_controlled,
    reason=(
        "The controlled-setting average gain claim "
        "(@claim_conductor_avg_controlled) reads off Table 7 "
        "(@claim_table7_full) directly. Conductor avg 72.35; best "
        "individual Gemini (4K) 64.14 (+8.21); best 5x-context Gemini "
        "67.60 (+4.75); best 5x-reflection GPT-5 64.52 (+7.83); best "
        "MAS baseline MoA 62.13 (+10.22)."
    ),
    prior=0.96,
)

strat_avg_workflow_steps = support(
    [claim_table7_full],
    claim_avg_workflow_steps,
    reason=(
        "The 3-step average workflow claim "
        "(@claim_avg_workflow_steps) is reported in the Section 4.3 "
        "narrative as the Conductor's actual average workflow length, "
        "anchored in the same evaluation that produced Table 7 "
        "(@claim_table7_full)."
    ),
    prior=0.92,
)

strat_controlled_summary = support(
    [
        claim_conductor_avg_controlled,
        claim_avg_workflow_steps,
        claim_table5_efficiency_consensus,
        claim_table6_efficiency_baselines,
    ],
    claim_controlled_summary,
    reason=(
        "The controlled-comparison summary "
        "(@claim_controlled_summary) is the Pareto-dominance "
        "conjunction of (a) average accuracy gain "
        "(@claim_conductor_avg_controlled), (b) lower step count "
        "(@claim_avg_workflow_steps), (c) lower cost per sample "
        "(@claim_table5_efficiency_consensus, "
        "@claim_table6_efficiency_baselines). RouterDC is the lone "
        "cheaper baseline but at -20 pp accuracy."
    ),
    prior=0.94,
)

strat_moa_failure = support(
    [claim_table7_full],
    claim_moa_failure_mode,
    reason=(
        "The MoA-fails-on-LCB diagnosis (@claim_moa_failure_mode) is "
        "the qualitative reading of Table 7 (@claim_table7_full) "
        "where MoA 38.57 < GPT-5 alone 57.50 on LCB while MoA "
        "outperforms or matches the individual baselines on lower-"
        "variance tasks (MoA 83.10 vs GPT-5 74.45 on MATH500). The "
        "evaluation log analysis in Appendix B.5 traces this to "
        "MoA's correctness-discernment failure when worker variance "
        "is high."
    ),
    prior=0.88,
)

strat_masrouter_failure = support(
    [claim_table7_full],
    claim_masrouter_failure_mode,
    reason=(
        "The MASRouter-fails diagnosis (@claim_masrouter_failure_mode) "
        "is the qualitative reading of Table 7 (@claim_table7_full) "
        "where MASRouter 56.89 underperforms even individual workers "
        "on LCB (MASRouter 27.86 vs GPT-5 alone 57.50). Appendix B.5 "
        "traces this to MASRouter's hand-engineered scaffold "
        "brittleness on the wider 7-worker pool."
    ),
    prior=0.88,
)

# ============================================================================
# Headline 'beats baselines' anchored in controlled comparison
# ============================================================================

strat_headline_beats_baselines = support(
    [
        claim_conductor_avg_controlled,
        claim_controlled_summary,
    ],
    claim_headline_beats_baselines,
    reason=(
        "The headline 'beats prior multi-agent / self-reflection / "
        "5x-context baselines' (@claim_headline_beats_baselines) "
        "is anchored in the controlled-setting Table 7 results: the "
        "Conductor beats every individual + multi-agent variant "
        "(@claim_conductor_avg_controlled) at lower cost "
        "(@claim_controlled_summary)."
    ),
    prior=0.96,
)

# ============================================================================
# Section 4.4: dynamic pool + recursive scaling
# ============================================================================

strat_dynamic_pool_design = support(
    [claim_provider_specialization],
    claim_dynamic_pool_design_aim,
    reason=(
        "The dynamic-pool design aim (@claim_dynamic_pool_design_aim) "
        "responds to provider specialization "
        "(@claim_provider_specialization): different users want "
        "different sub-pools (cost preferences, API availability, "
        "compliance), so the Conductor must adapt to arbitrary user-"
        "specified $k$-of-$n$ subsets. The protocol "
        "(@setup_dynamic_pool_protocol) operationalizes this aim."
    ),
    prior=0.92,
    background=[setup_dynamic_pool_protocol],
)

strat_open_pool_finetuned = support(
    [claim_dynamic_pool_design_aim],
    claim_open_pool_finetuned,
    reason=(
        "The open-pool Conductor outperforms-Claude result "
        "(@claim_open_pool_finetuned) is anchored in the Fig. 6 "
        "evaluation under the randomized-pool finetuning protocol "
        "(@setup_dynamic_pool_protocol) that realizes the design aim "
        "(@claim_dynamic_pool_design_aim). Specifically: when "
        "restricted to open-only workers, the finetuned Conductor "
        "beats Claude Sonnet 4 by ~10% within the constrained "
        "setting, demonstrating that the Conductor can amplify "
        "individually weaker open models past a frontier closed "
        "model."
    ),
    prior=0.9,
    background=[setup_dynamic_pool_protocol],
)

strat_closed_pool_finetuned = support(
    [claim_dynamic_pool_design_aim],
    claim_closed_pool_finetuned,
    reason=(
        "The closed-pool Conductor matches-pretrained result "
        "(@claim_closed_pool_finetuned) is anchored in the Fig. 6 "
        "right panel: the randomized-pool finetuning protocol "
        "(@setup_dynamic_pool_protocol) does not regress the "
        "Conductor's closed-pool performance vs its pretrained-only "
        "baseline, realizing the design aim "
        "(@claim_dynamic_pool_design_aim)."
    ),
    prior=0.92,
    background=[setup_dynamic_pool_protocol],
)

strat_pool_generalization_thesis = support(
    [claim_open_pool_finetuned, claim_closed_pool_finetuned],
    claim_pool_generalization_thesis,
    reason=(
        "The thesis that gains scale with worker-pool headroom "
        "(@claim_pool_generalization_thesis) is the joint conclusion "
        "of (a) larger absolute gains on the weaker open pool "
        "(@claim_open_pool_finetuned) and (b) no regression on the "
        "stronger closed pool (@claim_closed_pool_finetuned). The "
        "Conductor amplifies workers rather than free-riding on the "
        "strongest one."
    ),
    prior=0.92,
)

strat_headline_pool_generality = support(
    [claim_pool_generalization_thesis],
    claim_headline_pool_generality,
    reason=(
        "The headline cross-pool generalization claim "
        "(@claim_headline_pool_generality) is the abstract statement "
        "of the open/closed pool generalization thesis "
        "(@claim_pool_generalization_thesis), focused on the "
        "10% gain over Claude Sonnet 4 in the open-only setting."
    ),
    prior=0.95,
)

# ============================================================================
# Recursion
# ============================================================================

strat_recursive_scaling_aim = support(
    [claim_extension_recursive],
    claim_recursive_scaling_aim,
    reason=(
        "The recursive-test-time-scaling aim "
        "(@claim_recursive_scaling_aim) is the design rationale "
        "behind the recursive extension proposal "
        "(@claim_extension_recursive) and the recursion definition "
        "(@setup_recursion_definition): recursion depth becomes a "
        "tunable compute axis, qualitatively distinct from open-"
        "ended CoT scaling because it adds re-planning."
    ),
    prior=0.94,
    background=[setup_recursion_definition],
)

strat_recursion_decision_protocol = support(
    [claim_extension_recursive],
    claim_recursion_decision_protocol,
    reason=(
        "The recursion decision protocol "
        "(@claim_recursion_decision_protocol) is the operational "
        "definition from the recursive finetuning setup "
        "(@setup_recursive_finetuning_protocol) and the recursion "
        "definition (@setup_recursion_definition) that operationalize "
        "the recursive extension (@claim_extension_recursive): "
        "the Conductor either returns three empty lists or "
        "instantiates a new coordination strategy. Figs. 21-22 "
        "illustrate each branch."
    ),
    prior=0.97,
    background=[setup_recursive_finetuning_protocol, setup_recursion_definition],
)

strat_recursion_cost_cap = support(
    [claim_extension_recursive],
    claim_recursion_cost_cap,
    reason=(
        "The recursion cost cap (@claim_recursion_cost_cap, less "
        "than 2x original agentic calls) is part of the experimental "
        "setup specified in the recursive finetuning protocol "
        "(@setup_recursive_finetuning_protocol), realizing the "
        "recursive extension (@claim_extension_recursive) and "
        "reiterated in Section 4.4."
    ),
    prior=0.96,
    background=[setup_recursive_finetuning_protocol],
)

# Per-row recursion claims read off Table 2
strat_recursion_aime25 = support(
    [claim_table2_recursion_full],
    claim_recursion_aime25,
    reason=(
        "The AIME25 recursion-row claim "
        "(@claim_recursion_aime25, 66.67 = 66.67) reads off Table 2 "
        "(@claim_table2_recursion_full) directly; gain = 0 indicates "
        "correct pass-through behavior."
    ),
    prior=0.97,
)

strat_recursion_gpqa = support(
    [claim_table2_recursion_full],
    claim_recursion_gpqa,
    reason=(
        "The GPQA-D recursion-row claim "
        "(@claim_recursion_gpqa, 82.32 vs 81.31 = +1.01 pp) reads "
        "off Table 2 (@claim_table2_recursion_full) directly."
    ),
    prior=0.97,
)

strat_recursion_bcb = support(
    [claim_table2_recursion_full],
    claim_recursion_bcb,
    reason=(
        "The BigCodeBench recursion-row claim "
        "(@claim_recursion_bcb, 40.0 vs 37.8 = +2.2 pp) reads off "
        "Table 2 (@claim_table2_recursion_full) directly."
    ),
    prior=0.97,
)

strat_recursion_bcb_redistribution = support(
    [claim_recursion_bcb],
    claim_recursion_bcb_redistribution,
    reason=(
        "The agent-redistribution observation "
        "(@claim_recursion_bcb_redistribution, recursive Conductor "
        "shifts from GPT-5 toward Claude/Gemini on BCB) is the "
        "mechanism explanation for the +2.2 pp recursion gain on BCB "
        "(@claim_recursion_bcb). Fig. 10 documents the histogram "
        "shift."
    ),
    prior=0.9,
)

strat_recursion_dynamic_scaling_thesis = support(
    [claim_recursion_bcb, claim_recursion_aime25],
    claim_recursion_dynamic_scaling_thesis,
    reason=(
        "The recursion-as-dynamic-test-time-scaling thesis "
        "(@claim_recursion_dynamic_scaling_thesis) is supported by "
        "(a) the BCB gain via on-the-fly agent redistribution "
        "(@claim_recursion_bcb) and (b) the AIME25 zero-gain pass-"
        "through (@claim_recursion_aime25): together they show the "
        "recursive Conductor selectively re-plans when it pays off "
        "and skips when the initial strategy is already optimal."
    ),
    prior=0.92,
)

strat_headline_recursive_scaling = support(
    [
        claim_recursion_dynamic_scaling_thesis,
        claim_table2_recursion_full,
    ],
    claim_headline_recursive_scaling,
    reason=(
        "The headline recursive-scaling claim "
        "(@claim_headline_recursive_scaling, 63.00 avg vs 61.93) is "
        "anchored in the Table 2 row averages "
        "(@claim_table2_recursion_full) and interpreted via the "
        "dynamic-scaling thesis "
        "(@claim_recursion_dynamic_scaling_thesis)."
    ),
    prior=0.95,
)

# ============================================================================
# OOD few-shot result
# ============================================================================

strat_ood_few_shot_explanation = support(
    [claim_ood_few_shot_finding],
    claim_ood_few_shot_explanation,
    reason=(
        "The OOD-few-shot explanation "
        "(@claim_ood_few_shot_explanation, preventing exploitation "
        "/ incentivizing exploration) is the paper's posited "
        "mechanism for the empirical OOD-few-shot finding "
        "(@claim_ood_few_shot_finding). The OOD examples cannot be "
        "directly transferred, forcing the Conductor to learn "
        "compatibility patterns rather than copy them."
    ),
    prior=0.78,
)

# ============================================================================
# Section 4.5 analyses: 3B vs 7B scale
# ============================================================================

strat_3b_same_agent_dist = support(
    [claim_grpo_emergent_strategies],
    claim_3b_same_agent_dist,
    reason=(
        "The 3B-converges-to-same-agents observation "
        "(@claim_3b_same_agent_dist) is documented in Fig. 7 left "
        "panel and reflects the GRPO-emergence result "
        "(@claim_grpo_emergent_strategies) applied to a smaller "
        "base Conductor: agent selection is learned regardless of "
        "Conductor size, but the actual subtask quality is not."
    ),
    prior=0.92,
)

strat_7b_better_prompts = support(
    [claim_3b_same_agent_dist, claim_emergent_prompt_engineering],
    claim_7b_better_prompt_engineering,
    reason=(
        "The 7B-outperforms-3B claim "
        "(@claim_7b_better_prompt_engineering) is the joint reading "
        "of (a) identical agent distribution between 3B and 7B "
        "(@claim_3b_same_agent_dist) and (b) emergent prompt "
        "engineering being the dominant differentiator "
        "(@claim_emergent_prompt_engineering). Fig. 15 shows a 3B "
        "Conductor producing an inferior subtask "
        "(hide-your-reasoning anti-pattern)."
    ),
    prior=0.92,
)

strat_scale_thesis = support(
    [claim_7b_better_prompt_engineering, claim_natural_language_medium],
    claim_scale_thesis,
    reason=(
        "The scale thesis (@claim_scale_thesis, removing manual "
        "constraints opens a new scaling axis) is the conjunction of "
        "(a) larger Conductors generating better prompts at "
        "identical agent selection "
        "(@claim_7b_better_prompt_engineering) and (b) the natural-"
        "language medium that allows the larger LM's improved NLP "
        "capability to translate into prompt-engineering gains "
        "(@claim_natural_language_medium)."
    ),
    prior=0.91,
)

strat_workflow_step_distribution = support(
    [claim_emergent_task_adaptivity],
    claim_workflow_step_distribution,
    reason=(
        "The workflow-step distribution observation "
        "(@claim_workflow_step_distribution) is the operationalization "
        "of task adaptivity (@claim_emergent_task_adaptivity) on the "
        "MMLU vs LiveCodeBench comparison documented in Fig. 8."
    ),
    prior=0.95,
)

# ============================================================================
# Ablations (Tables 9, 10, 11)
# ============================================================================

strat_subtask_ablation = support(
    [claim_table9_ablations],
    claim_subtask_ablation,
    reason=(
        "The subtask ablation (@claim_subtask_ablation, -5.67 pp on "
        "LCB) reads off Table 9 (@claim_table9_ablations): "
        "Conductor LCB 64.29 - w/o subtasks LCB 58.62 = -5.67."
    ),
    prior=0.97,
)

strat_few_shot_ablation = support(
    [claim_table9_ablations],
    claim_few_shot_ablation,
    reason=(
        "The few-shot ablation (@claim_few_shot_ablation, -7.33 / "
        "-9.43 pp) reads off Table 9 (@claim_table9_ablations): "
        "Conductor MATH500 89.33 - w/o few-shot 82.00 = -7.33; "
        "Conductor LCB 64.29 - w/o few-shot 54.86 = -9.43."
    ),
    prior=0.97,
)

strat_fine_grained_topology = support(
    [claim_table9_ablations],
    claim_fine_grained_topology_ablation,
    reason=(
        "The fine-grained topology ablation "
        "(@claim_fine_grained_topology_ablation) reads off Table 9 "
        "(@claim_table9_ablations) showing the fine-grained variant "
        "marginally regresses on LCB (-3.05 pp) and is approximately "
        "tied elsewhere -- no significant gain at 7B scale."
    ),
    prior=0.94,
)

strat_subtask_alone_matters = support(
    [claim_table10_agent_selection_ablation],
    claim_subtask_alone_matters,
    reason=(
        "The 'subtask alone matters' result "
        "(@claim_subtask_alone_matters) reads off Table 10 "
        "(@claim_table10_agent_selection_ablation): even with "
        "agents all set to GPT-5, the Conductor's subtask + topology "
        "design lifts performance above GPT-5 alone (69.81 vs 68.62 "
        "average across AIME / BCB / GPQA-D)."
    ),
    prior=0.96,
)

strat_frontier_orchestrator_evidence = support(
    [claim_table11_conductor_replacement],
    claim_frontier_orchestrator_evidence,
    reason=(
        "The frontier-LLM-as-Conductor result "
        "(@claim_frontier_orchestrator_evidence) reads off Table 11 "
        "(@claim_table11_conductor_replacement): GPT-5 and Gemini "
        "in 3-model Conductor roles each outperform their "
        "constituent agents on numerous tasks (e.g., Gemini-conduct "
        "GPQA-D 87.62 vs Gemini alone 84.8)."
    ),
    prior=0.94,
)

strat_conductor_training_essential = support(
    [claim_table11_conductor_replacement],
    claim_conductor_training_essential,
    reason=(
        "The conductor-training-essential result "
        "(@claim_conductor_training_essential) reads off Table 11 "
        "(@claim_table11_conductor_replacement): the trained 7B "
        "Conductor outperforms even the strongest frontier-LLM-as-"
        "Conductor (Gemini conduct 3: 71.59) by +4.06 pp average, "
        "and the gap is largest on LCB (83.93 vs 70.29 = +13.64 pp)."
    ),
    prior=0.96,
)

strat_per_model_specialization = support(
    [claim_table7_full, claim_table1_full],
    claim_per_model_specialization,
    reason=(
        "The per-model specialization observation "
        "(@claim_per_model_specialization, no single worker dominates "
        "all tasks) is read off both Table 1 (@claim_table1_full) "
        "and Table 7 (@claim_table7_full): GPT-5 leads AIME/LCB, "
        "Gemini leads GPQA-D, Claude leads BCB at the global "
        "task-level; sub-task specialization (planner vs writer) "
        "documented in Appendix B.3."
    ),
    prior=0.92,
)

strat_weak_models_subtask = support(
    [claim_per_model_specialization, claim_subtask_alone_matters],
    claim_weak_models_essential_for_subtasks,
    reason=(
        "The 'weak models fill sub-task roles' claim "
        "(@claim_weak_models_essential_for_subtasks) is the sub-task-"
        "level extension of per-model specialization "
        "(@claim_per_model_specialization), illustrated in Fig. 27 / "
        "Appendix B.3: Qwen3-32B as final BCB format checker "
        "succeeds where GPT-5 fails. The 'subtask alone matters' "
        "result (@claim_subtask_alone_matters) supports the "
        "criticality of sub-task structure."
    ),
    prior=0.85,
)

strat_qwen_thinking_bcb = support(
    [claim_table8_ood_constrained],
    claim_qwen_thinking_vs_direct_bcb,
    reason=(
        "The Qwen3-32B-direct beats Qwen3-32B-thinking on BCB "
        "claim (@claim_qwen_thinking_vs_direct_bcb) reads off Table "
        "8 (@claim_table8_ood_constrained): 23.0 vs 20.9 on "
        "BigCodeBench. Appendix B.6 explains via formatting failures "
        "from verbosity in thinking mode."
    ),
    prior=0.92,
)

# ============================================================================
# Related work positioning
# ============================================================================

strat_rl_tool_positioning = support(
    [claim_rl_with_tools_literature, claim_conductor_proposal],
    claim_conductor_rl_tool_positioning,
    reason=(
        "The Conductor RL-with-tools positioning "
        "(@claim_conductor_rl_tool_positioning) is the conjunction "
        "of the literature characterization "
        "(@claim_rl_with_tools_literature, single-model RL + "
        "external tools) and the Conductor proposal "
        "(@claim_conductor_proposal, RL with LLM-worker API calling "
        "as the 'tool'). The Conductor is the first work to treat "
        "an entire LLM as the tool target of RL."
    ),
    prior=0.94,
)

strat_mas_positioning = support(
    [claim_multi_agent_coord_literature, claim_natural_language_medium],
    claim_conductor_mas_positioning,
    reason=(
        "The Conductor MAS positioning "
        "(@claim_conductor_mas_positioning, only fully end-to-end-RL "
        "MAS coordinator with natural-language output) is the "
        "conjunction of (a) the existing MAS literature "
        "characterization (@claim_multi_agent_coord_literature, "
        "fixed-vocabulary or embedding-routed approaches) and (b) "
        "the Conductor's unrestricted natural-language medium "
        "(@claim_natural_language_medium). No prior approach combines "
        "both."
    ),
    prior=0.93,
)

strat_positioning_summary = support(
    [
        claim_conductor_rl_tool_positioning,
        claim_conductor_mas_positioning,
    ],
    claim_positioning_summary,
    reason=(
        "The intersection-positioning summary "
        "(@claim_positioning_summary) is the conjunction of the two "
        "literature-axes positionings "
        "(@claim_conductor_rl_tool_positioning, "
        "@claim_conductor_mas_positioning)."
    ),
    prior=0.95,
)

# ============================================================================
# Three contributions + broader thesis (Section 1, anchored to evidence)
# ============================================================================

strat_extension_dynamic_pool = support(
    [claim_dynamic_pool_design_aim],
    claim_extension_dynamic_pool,
    reason=(
        "The dynamic-pool extension proposal "
        "(@claim_extension_dynamic_pool) is the operational summary "
        "of the design aim (@claim_dynamic_pool_design_aim) and "
        "the randomized-pool finetuning protocol "
        "(@setup_dynamic_pool_protocol)."
    ),
    prior=0.96,
    background=[setup_dynamic_pool_protocol],
)

strat_extension_recursive = support(
    [claim_recursive_scaling_aim],
    claim_extension_recursive,
    reason=(
        "The recursive-topology extension proposal "
        "(@claim_extension_recursive) is the operational summary of "
        "the test-time-scaling aim "
        "(@claim_recursive_scaling_aim) and the recursive "
        "finetuning protocol "
        "(@setup_recursive_finetuning_protocol)."
    ),
    prior=0.96,
    background=[setup_recursive_finetuning_protocol],
)

strat_three_contributions = support(
    [
        claim_conductor_proposal,
        claim_headline_sota,
        claim_extension_dynamic_pool,
        claim_extension_recursive,
    ],
    claim_three_contributions,
    reason=(
        "The three-contributions claim "
        "(@claim_three_contributions) is the joint statement of "
        "(C1) the Conductor method (@claim_conductor_proposal), "
        "(C2) the SOTA empirical headline "
        "(@claim_headline_sota), and (C3) the two extensions "
        "(@claim_extension_dynamic_pool, @claim_extension_recursive)."
    ),
    prior=0.97,
)

strat_broader_thesis = support(
    [
        claim_grpo_emergent_strategies,
        claim_conductor_two_emergent_skills,
        claim_meta_orchestrator_thesis,
    ],
    claim_broader_thesis,
    reason=(
        "The broader thesis "
        "(@claim_broader_thesis, LLM coordination unlocked through "
        "RL) is supported by (a) the empirical observation that "
        "coordination strategies emerge from GRPO alone "
        "(@claim_grpo_emergent_strategies), (b) the documented two "
        "emergent skills (@claim_conductor_two_emergent_skills), "
        "and (c) the meta-orchestrator interpretation "
        "(@claim_meta_orchestrator_thesis)."
    ),
    prior=0.94,
)

# ============================================================================
# Section 6 discussion (anchored)
# ============================================================================

strat_discussion_synthesis = support(
    [
        claim_conductor_proposal,
        claim_headline_sota,
        claim_headline_pool_generality,
        claim_headline_recursive_scaling,
    ],
    claim_discussion_synthesis,
    reason=(
        "The Section 6 synthesis (@claim_discussion_synthesis) "
        "combines the Conductor method (@claim_conductor_proposal), "
        "the SOTA headline (@claim_headline_sota), the pool-"
        "generalization extension (@claim_headline_pool_generality), "
        "and the recursive-scaling extension "
        "(@claim_headline_recursive_scaling)."
    ),
    prior=0.97,
)

strat_meta_agent_thesis = support(
    [
        claim_meta_orchestrator_thesis,
        claim_frontier_orchestrator_evidence,
    ],
    claim_meta_agent_thesis,
    reason=(
        "The broader meta-agent thesis "
        "(@claim_meta_agent_thesis) is supported by (a) the trained-"
        "Conductor meta-orchestrator interpretation "
        "(@claim_meta_orchestrator_thesis) and (b) the untrained-"
        "frontier-LLM-as-Conductor evidence "
        "(@claim_frontier_orchestrator_evidence) that even powerful "
        "models become better in this role -- collectively favoring "
        "the 'coordinator + workers' design point."
    ),
    prior=0.93,
)

strat_future_beyond_llms = support(
    [claim_meta_agent_thesis, claim_natural_language_medium],
    claim_future_beyond_llms,
    reason=(
        "The future-direction claim "
        "(@claim_future_beyond_llms) extrapolates the meta-agent "
        "thesis (@claim_meta_agent_thesis) using natural language "
        "as a unifying interface (@claim_natural_language_medium) "
        "to non-LLM modalities (AlphaFold [@Jumper2021AlphaFold], "
        "pi0.5 [@Intelligence2025Pi05])."
    ),
    prior=0.8,
)

strat_ethics = support(
    [claim_headline_pool_generality],
    claim_ethics_economic_divide,
    reason=(
        "The ethics caveat (@claim_ethics_economic_divide) is "
        "partially addressed by the pool-generalization headline "
        "(@claim_headline_pool_generality): the open-source-only "
        "evaluation demonstrates the framework can deliver gains "
        "without expensive closed-source API calls, mitigating but "
        "not eliminating the economic-divide concern."
    ),
    prior=0.85,
)

# ============================================================================
# INDUCTION 1: Cross-benchmark generalization -- 7 benchmark deltas all
# positive (Table 1) -> headline 'consistent improvement across all
# tasks' (and the headline-SOTA claim)
# ============================================================================

# Each per-row delta supports the headline 'Conductor consistently improves
# over the best individual worker'

s_bench_math500 = support(
    [claim_avg_unconstrained],
    claim_math500_unconstrained,
    reason=(
        "Generative direction: the cross-benchmark improvement law "
        "(@claim_avg_unconstrained, every column won) predicts a "
        "positive delta on MATH500. The +0.4 pp delta "
        "(@claim_math500_unconstrained) realizes this prediction "
        "near the saturation point."
    ),
    prior=0.9,
)

s_bench_mmlu = support(
    [claim_avg_unconstrained],
    claim_mmlu_unconstrained,
    reason=(
        "Generative direction: the cross-benchmark improvement law "
        "(@claim_avg_unconstrained) predicts a positive delta on "
        "MMLU. The +0.6 pp delta "
        "(@claim_mmlu_unconstrained) realizes this prediction."
    ),
    prior=0.9,
)

s_bench_rlpr = support(
    [claim_avg_unconstrained],
    claim_rlpr_unconstrained,
    reason=(
        "Generative direction: the cross-benchmark improvement law "
        "(@claim_avg_unconstrained) predicts a positive delta on "
        "RLPR. The +2.55 pp delta (@claim_rlpr_unconstrained) "
        "realizes this prediction."
    ),
    prior=0.9,
)

s_bench_lcb = support(
    [claim_avg_unconstrained],
    claim_lcb_unconstrained,
    reason=(
        "Generative direction: the cross-benchmark improvement law "
        "(@claim_avg_unconstrained) predicts a positive delta on "
        "LCB. The +1.03 pp delta (@claim_lcb_unconstrained) "
        "realizes this prediction; Conductor is SOTA on the "
        "LiveCodeBench leaderboard."
    ),
    prior=0.9,
)

s_bench_aime25 = support(
    [claim_avg_unconstrained],
    claim_aime25_unconstrained,
    reason=(
        "Generative direction: the cross-benchmark improvement law "
        "(@claim_avg_unconstrained) predicts a positive delta on "
        "AIME25. The +2.5 pp delta (@claim_aime25_unconstrained) "
        "realizes this prediction (generational magnitude)."
    ),
    prior=0.9,
)

s_bench_bcb = support(
    [claim_avg_unconstrained],
    claim_bcb_unconstrained,
    reason=(
        "Generative direction: the cross-benchmark improvement law "
        "(@claim_avg_unconstrained) predicts a positive delta on "
        "BCB. The +0.35 pp delta (@claim_bcb_unconstrained) "
        "realizes this prediction (modest because Conductor used to "
        "exceed Gemini)."
    ),
    prior=0.9,
)

s_bench_gpqa = support(
    [claim_avg_unconstrained],
    claim_gpqa_unconstrained,
    reason=(
        "Generative direction: the cross-benchmark improvement law "
        "(@claim_avg_unconstrained) predicts a positive delta on "
        "GPQA-D. The +2.7 pp delta (@claim_gpqa_unconstrained) "
        "realizes this prediction (generational magnitude)."
    ),
    prior=0.9,
)

ind_bench_12 = induction(
    s_bench_math500,
    s_bench_mmlu,
    law=claim_avg_unconstrained,
    reason=(
        "MATH500 (competition mathematics) and MMLU (multitask "
        "language understanding) are independent benchmarks "
        "spanning two distinct skill domains. Positive deltas on "
        "both jointly support the 'all-columns-won' law."
    ),
)

ind_bench_123 = induction(
    ind_bench_12,
    s_bench_rlpr,
    law=claim_avg_unconstrained,
    reason=(
        "RLPR (real-world general reasoning) adds a third "
        "independent domain (general-purpose Q&A). Positive delta "
        "robustifies the law across knowledge-style and reasoning-"
        "style problems."
    ),
)

ind_bench_1234 = induction(
    ind_bench_123,
    s_bench_lcb,
    law=claim_avg_unconstrained,
    reason=(
        "LiveCodeBench V6 (code generation, sandbox-evaluated) adds "
        "a fourth qualitatively different evaluation protocol "
        "(execution-based vs match-based). Positive delta robustifies "
        "the law across evaluation-protocol differences."
    ),
)

ind_bench_12345 = induction(
    ind_bench_1234,
    s_bench_aime25,
    law=claim_avg_unconstrained,
    reason=(
        "AIME25 (competition mathematics, post-training-cutoff for "
        "many workers) adds a fifth domain testing OOD generalization "
        "of the Conductor's strategies. Positive delta of "
        "generational magnitude (+2.5 pp) demonstrates robustness "
        "to unseen-task transfer."
    ),
)

ind_bench_123456 = induction(
    ind_bench_12345,
    s_bench_bcb,
    law=claim_avg_unconstrained,
    reason=(
        "BigCodeBench (function-call code generation, OOD) adds a "
        "sixth domain that the pretrained Conductor never saw and "
        "where the strongest constituent (Gemini/Claude) is NOT "
        "GPT-5 -- different leader from the LCB pattern. The +0.35 "
        "pp positive delta is critical because it shows the "
        "Conductor can still extract gains when its training-time "
        "best-worker heuristic doesn't apply directly."
    ),
)

ind_bench_1234567 = induction(
    ind_bench_123456,
    s_bench_gpqa,
    law=claim_avg_unconstrained,
    reason=(
        "GPQA-Diamond (graduate-level natural science: biology, "
        "chemistry, physics) adds a seventh independent domain in "
        "a fourth subject area (science, distinct from math/code/"
        "general-reasoning). The +2.7 pp delta (generational "
        "magnitude) confirms the law extends to scientific reasoning."
    ),
)

# ============================================================================
# INDUCTION 2: Cross-pool generalization -- open / closed / full pools
# all yield strong performance -> headline pool generality
# ============================================================================

s_pool_full = support(
    [claim_headline_pool_generality],
    claim_avg_unconstrained,
    reason=(
        "Generative direction: the cross-pool generality law "
        "(@claim_headline_pool_generality) predicts strong "
        "performance on the full 7-worker pool. The unconstrained "
        "average 77.27 (@claim_avg_unconstrained) realizes this "
        "for the full pool."
    ),
    prior=0.92,
)

s_pool_open = support(
    [claim_headline_pool_generality],
    claim_open_pool_finetuned,
    reason=(
        "Generative direction: the cross-pool generality law "
        "(@claim_headline_pool_generality) predicts strong "
        "performance on the open-only pool. The +10% over Claude "
        "Sonnet 4 (@claim_open_pool_finetuned) realizes this for "
        "the open pool."
    ),
    prior=0.9,
)

s_pool_closed = support(
    [claim_headline_pool_generality],
    claim_closed_pool_finetuned,
    reason=(
        "Generative direction: the cross-pool generality law "
        "(@claim_headline_pool_generality) predicts no regression "
        "on the closed-only pool after randomized-pool finetuning. "
        "The match-pretrained result "
        "(@claim_closed_pool_finetuned) realizes this prediction."
    ),
    prior=0.9,
)

ind_pool_full_open = induction(
    s_pool_full,
    s_pool_open,
    law=claim_headline_pool_generality,
    reason=(
        "Full-pool SOTA performance and open-only performance "
        "exceeding Claude Sonnet 4 are independent observations of "
        "cross-pool generality. The open-only result is the "
        "stronger test because the worker pool is qualitatively "
        "weaker -- the Conductor must extract gains from less "
        "powerful foundations."
    ),
)

ind_pool_full_open_closed = induction(
    ind_pool_full_open,
    s_pool_closed,
    law=claim_headline_pool_generality,
    reason=(
        "Closed-pool match-pretrained performance adds the third "
        "axis: the randomized-pool finetuning does not regress the "
        "original capability. Together, these three observations "
        "(full / open / closed) cover the user-customization "
        "design space."
    ),
)

# ============================================================================
# INDUCTION 3: Cross-task recursion gains -- BCB / AIME25 / GPQA-D
# all consistent with the dynamic-scaling thesis
# ============================================================================

# Note: AIME25 has 0 gain; we treat this as still-confirmatory (correct
# pass-through), not contradicting. We have three independent
# observations confirming 'recursion selectively re-plans when useful'.

s_rec_bcb = support(
    [claim_recursion_dynamic_scaling_thesis],
    claim_recursion_bcb,
    reason=(
        "Generative direction: the dynamic-scaling thesis "
        "(@claim_recursion_dynamic_scaling_thesis) predicts positive "
        "recursion gain on OOD tasks where pretrained coordination "
        "is suboptimal. The +2.2 pp BCB gain "
        "(@claim_recursion_bcb) realizes this prediction (GPT-5 "
        "underperforms on BCB, creating room for recursion)."
    ),
    prior=0.9,
)

s_rec_gpqa = support(
    [claim_recursion_dynamic_scaling_thesis],
    claim_recursion_gpqa,
    reason=(
        "Generative direction: the dynamic-scaling thesis "
        "(@claim_recursion_dynamic_scaling_thesis) predicts modest "
        "recursion gain when initial strategy is good but not "
        "perfect. The +1.01 pp GPQA-D gain "
        "(@claim_recursion_gpqa) realizes this prediction."
    ),
    prior=0.9,
)

s_rec_aime = support(
    [claim_recursion_dynamic_scaling_thesis],
    claim_recursion_aime25,
    reason=(
        "Generative direction: the dynamic-scaling thesis "
        "(@claim_recursion_dynamic_scaling_thesis) predicts that "
        "recursion correctly passes through when the initial "
        "strategy is already optimal. The 0 pp AIME25 result "
        "(@claim_recursion_aime25) realizes this prediction "
        "(no wasted compute on already-good strategies)."
    ),
    prior=0.85,
)

ind_rec_12 = induction(
    s_rec_bcb,
    s_rec_gpqa,
    law=claim_recursion_dynamic_scaling_thesis,
    reason=(
        "BigCodeBench (function-call code) and GPQA-Diamond "
        "(graduate science) are independent OOD benchmarks. Both "
        "yielding positive recursion gains (sizable on BCB, modest "
        "on GPQA-D) jointly support the recursion-as-dynamic-"
        "scaling thesis."
    ),
)

ind_rec_123 = induction(
    ind_rec_12,
    s_rec_aime,
    law=claim_recursion_dynamic_scaling_thesis,
    reason=(
        "AIME25 adds a third benchmark with a critical *negative* "
        "behavior: 0 pp gain (correct pass-through). The dynamic-"
        "scaling thesis specifically predicts selective re-planning, "
        "not unconditional re-planning. The AIME25 result -- where "
        "the Conductor correctly skips recursion -- is therefore a "
        "stronger test of the thesis than a positive gain would be."
    ),
)

# ============================================================================
# CENTRAL ABDUCTION: Conductor's gain comes from learned coordination
# (topology + prompt engineering jointly) vs trivial alternatives
# ============================================================================

# Hypothesis H: the SOTA fingerprint is caused by the Conductor's learned
# combination of (a) targeted prompt engineering and (b) topology design,
# acquired through end-to-end RL on a verifiable reward.
#
# Alternative Alt: the 7B Conductor's gain is a trivial consequence of
# (a1) picking the best individual worker per task, (a2) using more
# inference compute, or (a3) cherry-picking favorable agent pools.
#
# Discriminating observation: the multi-fact fingerprint includes:
# (i) Conductor BEATS every individual worker including its strongest
#     constituent on every benchmark (rules out 'picks best worker').
# (ii) Conductor uses fewer agent calls (avg 3 steps) and fewer tokens
#     than multi-agent baselines yet wins (rules out 'more compute').
# (iii) Even 'all-GPT-5' Conductor variant beats GPT-5 alone, AND the
#     full-pool Conductor adds further gains (subtask design alone
#     matters; agent diversity adds on top).
# (iv) Untrained-LLM Conductors (GPT-5 / Gemini in conduct roles) fall
#     well short of the trained 7B Conductor (rules out 'any LLM as
#     Conductor would work').
# (v) Open-source-only pool beats Claude Sonnet 4 (rules out 'gain is
#     due to access to the best closed model').

claim_pred_learned_coord_explains = claim(
    "**Prediction under H (the Conductor's gain comes from learned "
    "coordination: topology + prompt engineering jointly).** If the "
    "gain is caused by RL-learned coordination, we should observe: "
    "(i) Conductor consistently outperforms its strongest individual "
    "constituent on each benchmark (because the gain is collective, "
    "not single-worker); (ii) Conductor uses *fewer* agent calls than "
    "multi-agent baselines yet wins (because the gain is per-call "
    "quality, not per-call quantity); (iii) the 'all-GPT-5' Conductor "
    "variant beats GPT-5 alone (because subtask + topology design "
    "alone matters even without agent diversity), with full-pool "
    "Conductor adding further gains; (iv) untrained frontier LLMs in "
    "Conductor roles fall short of the trained 7B Conductor (because "
    "RL training is essential to learn the coordination strategies); "
    "(v) finetuned open-only Conductor beats Claude Sonnet 4 (because "
    "the gain extends to weaker pools).",
    title="Prediction under H (gain comes from learned coordination: topology + prompt engineering)",
)

claim_pred_alt_trivial_explains = claim(
    "**Prediction under Alt (gain is a trivial consequence of picking "
    "the best worker / more compute / cherry-picked pools).** Under "
    "any of the trivial alternatives: "
    "(a1) **'Picks the best worker'** -- Conductor would at most match, "
    "not exceed, its strongest constituent per task. "
    "(a2) **'More inference compute'** -- Conductor should use more "
    "tokens/calls than its baselines, NOT fewer. "
    "(a3) **'Cherry-picked agent pools'** -- closed-only matching the "
    "full-pool would be expected, but the open-only result over Claude "
    "Sonnet 4 should NOT happen (open models are individually weaker). "
    "(a4) **'Any LLM works as Conductor'** -- untrained GPT-5 or "
    "Gemini in Conductor roles should achieve similar gains to the "
    "trained 7B Conductor, NOT fall short by 4-16 pp.",
    title="Prediction under Alt (trivial: pick-best / more-compute / cherry-pick / any-LLM)",
)

claim_obs_pattern = claim(
    "**Discriminating observation pattern.** The full empirical "
    "fingerprint that any explanatory hypothesis must account for is "
    "the conjunction of:\n\n"
    "(i) **+2.49 pp average over GPT-5** (best individual worker) "
    "across 7 unconstrained benchmarks; Conductor wins on every "
    "column (@claim_avg_unconstrained);\n"
    "(ii) **3-step average workflow** (@claim_avg_workflow_steps), "
    "**1820 tokens / sample** at **$0.024/sample** vs MoA's 11203 "
    "tokens / $0.049 (@claim_table6_efficiency_baselines), strictly "
    "Pareto-dominant cost vs accuracy "
    "(@claim_controlled_summary);\n"
    "(iii) **'all-GPT-5' Conductor beats GPT-5 alone** (69.81 vs "
    "68.62 avg, @claim_subtask_alone_matters), AND full-pool "
    "Conductor adds +3.08 pp on top (@claim_table10_agent_selection_"
    "ablation);\n"
    "(iv) **Untrained frontier LLMs in Conductor roles fall 4-16 pp "
    "short** of the trained 7B Conductor "
    "(@claim_conductor_training_essential);\n"
    "(v) **Open-only finetuned Conductor beats Claude Sonnet 4 by "
    "~10%** within the constrained setting "
    "(@claim_open_pool_finetuned).",
    title="Discriminating observation: 5-fact fingerprint that rules out picks-best / more-compute / cherry-pick / any-LLM",
)

strat_obs_pattern_assembly = support(
    [
        claim_avg_unconstrained,
        claim_controlled_summary,
        claim_table10_agent_selection_ablation,
        claim_conductor_training_essential,
        claim_open_pool_finetuned,
    ],
    claim_obs_pattern,
    reason=(
        "The 5-fact observation pattern (@claim_obs_pattern) is the "
        "conjunction of (i) +2.49 pp cross-benchmark average "
        "(@claim_avg_unconstrained), (ii) cost-Pareto dominance "
        "(@claim_controlled_summary), (iii) all-GPT-5 Conductor "
        "variant lift (@claim_table10_agent_selection_ablation), "
        "(iv) trained vs untrained Conductor gap "
        "(@claim_conductor_training_essential), (v) open-pool "
        "generalization (@claim_open_pool_finetuned)."
    ),
    prior=0.95,
)

s_h_explains = support(
    [claim_pred_learned_coord_explains],
    claim_obs_pattern,
    reason=(
        "Under the learned-coordination hypothesis "
        "(@claim_pred_learned_coord_explains), the 5-fact fingerprint "
        "(@claim_obs_pattern) is exactly the predicted joint "
        "signature: (i) collective gain beats strongest constituent, "
        "(ii) per-call quality means fewer calls suffice, (iii) "
        "subtask design alone helps + diversity adds further, "
        "(iv) the training step is what teaches the coordination "
        "strategies, (v) the strategies transfer to weaker pools by "
        "amplifying complementarity. Every fact is positively "
        "anticipated by H."
    ),
    prior=0.94,
)

s_alt_explains = support(
    [claim_pred_alt_trivial_explains],
    claim_obs_pattern,
    reason=(
        "Under trivial alternatives "
        "(@claim_pred_alt_trivial_explains), the 5-fact fingerprint "
        "cannot be jointly explained: (i) 'picks best worker' "
        "predicts Conductor = strongest constituent, not exceeding "
        "it; (ii) 'more compute' predicts Conductor uses MORE "
        "tokens, contradicted by the 1820-token / 3-step result; "
        "(iii) 'subtask + topology don't matter' is contradicted by "
        "the all-GPT-5 Conductor beating GPT-5 alone; (iv) 'any LLM "
        "as Conductor would work' is contradicted by the 4-16 pp "
        "trained-vs-untrained gap; (v) 'gain requires the best "
        "closed model' is contradicted by the open-only result "
        "beating Claude. The alternatives can each explain at most "
        "one fact in isolation."
    ),
    prior=0.15,
)

comp_learned_vs_trivial = compare(
    claim_pred_learned_coord_explains,
    claim_pred_alt_trivial_explains,
    claim_obs_pattern,
    reason=(
        "The learned-coordination prediction "
        "(@claim_pred_learned_coord_explains) uniquely accounts for "
        "the full 5-fact pattern. The strongest discriminating "
        "signals are: (a) the **'all-GPT-5' Conductor variant** "
        "(@claim_table10_agent_selection_ablation), which fixes "
        "agent diversity at zero and still shows a lift -- "
        "isolating the contribution of learned subtask + topology "
        "design; (b) the **trained-vs-untrained Conductor gap** "
        "(@claim_conductor_training_essential), which fixes the "
        "framework and varies only the training -- isolating the "
        "contribution of RL learning. Both discriminating "
        "comparisons hold the 'trivial alternative' variables "
        "constant and show the learned-coordination variable still "
        "drives gain. The opposite-sign predictions of trivial "
        "alternatives on cost (ii) and pool composition (v) further "
        "exclude them."
    ),
    prior=0.96,
)

abd_learned_vs_trivial = abduction(
    s_h_explains,
    s_alt_explains,
    comp_learned_vs_trivial,
    reason=(
        "Both hypotheses attempt to explain the same observed "
        "Conductor fingerprint: SOTA on 7 benchmarks at low cost, "
        "all-GPT-5 variant beats GPT-5 alone, untrained-LLM "
        "Conductors fall short of trained, open-pool beats Claude. "
        "The learned-coordination hypothesis "
        "(@claim_pred_learned_coord_explains) predicts every fact; "
        "the trivial alternatives "
        "(@claim_pred_alt_trivial_explains) predict at most one fact "
        "each in isolation, and predict OPPOSITE signs on cost and "
        "pool composition. The discriminating ablations "
        "(all-GPT-5 Conductor variant + trained-vs-untrained gap) "
        "isolate the learned-coordination variable as the operative "
        "one."
    ),
)

# ============================================================================
# CONTRADICTION 1: prevailing 'manual orchestration is best' assumption
# vs the Conductor's end-to-end RL demonstration
# ============================================================================

# Foil: 'manual orchestration is the best we can do for MAS' -- this is
# the prevailing assumption that the Conductor's empirical demonstration
# of end-to-end RL refutes.

claim_foil_manual_best = claim(
    "**Foil: manual orchestration is the best we can do for MAS.** "
    "The prevailing assumption in commercial agentic AI products "
    "[@AWS2025Q; @Microsoft2025Copilot; @Anysphere2025Cursor] and in "
    "prior MAS research (hand-designed scaffolds [@Wang2024MoA; "
    "@Du2023MultiAgentDebate], fixed-vocabulary routers "
    "[@Yue2025MASRouter; @Chen2024RouterDC; @Guha2024Smoothie]) is "
    "that the **right way** to orchestrate frontier LLMs is via "
    "carefully hand-designed scaffolds and routers selecting from a "
    "human-specified vocabulary of patterns. Under this foil, "
    "end-to-end RL training of a free-form coordinator should NOT "
    "yield substantial gains beyond the manually-designed state of "
    "the art.",
    title="Foil: manual orchestration / fixed-vocabulary routing is the best achievable MAS approach",
)

strat_foil_manual = support(
    [claim_multi_agent_coord_literature],
    claim_foil_manual_best,
    reason=(
        "The manual-orchestration foil "
        "(@claim_foil_manual_best) is the implicit assumption of "
        "the existing MAS-coordination literature "
        "(@claim_multi_agent_coord_literature) and commercial "
        "agentic-product practice (@setup_agentic_products), all of "
        "which optimize hand-designed scaffolds and fixed-vocabulary "
        "routers rather than free-form end-to-end RL coordinators."
    ),
    prior=0.7,
    background=[setup_agentic_products],
)

contra_manual_vs_rl = contradiction(
    claim_foil_manual_best,
    claim_headline_sota,
    reason=(
        "The manual-orchestration foil "
        "(@claim_foil_manual_best) and the Conductor SOTA "
        "(@claim_headline_sota, +2.49 pp avg, all 7 columns won, "
        "outperforming MASRouter [@Yue2025MASRouter] / MoA "
        "[@Wang2024MoA] / RouterDC [@Chen2024RouterDC] / Smoothie "
        "[@Guha2024Smoothie] / 5x-self-reflection / 5x-context) "
        "cannot both be true. If manual orchestration / fixed-"
        "vocabulary routing were the best achievable approach, then "
        "a small RL-trained Conductor should NOT consistently "
        "surpass them across 7 benchmarks. The empirical Conductor "
        "SOTA refutes the foil."
    ),
    prior=0.94,
)

# Foil 2: the foil that 'a small 7B model cannot outperform larger frontier
# workers individually' is contradicted by the Conductor result.
# We need to add this foil as a claim before the contradiction.

claim_foil_7b_cannot_beat_frontier = claim(
    "**Foil: a small 7B model cannot outperform larger frontier "
    "workers individually.** Under the prevailing view that LLM "
    "capability primarily reflects scale "
    "[@Brown2020GPT3] and tuning effort, a 7B model is fundamentally "
    "much weaker than a 32B+ open-source model and orders of "
    "magnitude smaller than the trillion-parameter-class proprietary "
    "frontier models (GPT-5, Gemini 2.5 Pro, Claude Sonnet 4). A "
    "natural prior expectation is therefore that a 7B model alone "
    "cannot match -- let alone exceed -- the gain achievable by "
    "directly using or combining these larger workers.",
    title="Foil: a small 7B model cannot outperform larger frontier workers individually",
)

strat_foil_7b = support(
    [claim_provider_specialization],
    claim_foil_7b_cannot_beat_frontier,
    reason=(
        "The 7B-too-small foil "
        "(@claim_foil_7b_cannot_beat_frontier) is the standard "
        "scaling-law expectation in the LLM literature "
        "[@Brown2020GPT3], applied to the frontier-LLM setup "
        "(@setup_frontier_llms) within which @claim_provider_"
        "specialization establishes specialized 32B+ workers as the "
        "comparison baseline: smaller models with fewer parameters "
        "and less training compute have lower per-task ceilings."
    ),
    prior=0.7,
    background=[setup_frontier_llms],
)

contra_7b_foil_vs_sota = contradiction(
    claim_foil_7b_cannot_beat_frontier,
    claim_headline_sota,
    reason=(
        "The 7B-too-small foil "
        "(@claim_foil_7b_cannot_beat_frontier) and the Conductor "
        "7B SOTA result (@claim_headline_sota, all 7 benchmark "
        "columns won, +2.49 pp average over GPT-5) cannot both "
        "be true. The foil predicts a 7B model cannot exceed "
        "frontier workers; the result is that a 7B *coordinator* "
        "(while not solving the task itself) lifts its frontier "
        "workers past their individual ceilings. The empirical "
        "Conductor wins, so the foil is wrong under the framing "
        "'small-model alone vs small-model-as-coordinator-of-large-"
        "models'."
    ),
    prior=0.92,
)

# ============================================================================
# Additional anchors and orphan prevention
# ============================================================================

# claim_q_central is a question, not anchored as conclusion.
# Anchor headlines back to discussion synthesis if not done elsewhere.

# Long-tail-difficulty -- supported by the AIME25 and GPQA-D row claims
strat_long_tail = support(
    [claim_aime25_unconstrained, claim_gpqa_unconstrained],
    claim_long_tail_difficulty,
    reason=(
        "The long-tail-difficulty interpretation "
        "(@claim_long_tail_difficulty) is supported by the +2.5 pp "
        "AIME25 delta (@claim_aime25_unconstrained) and the +2.7 "
        "pp GPQA-D delta (@claim_gpqa_unconstrained): both are "
        "consistent in magnitude with the o3 -> GPT-5 generational "
        "improvement (3.3% / 2.7%), exemplifying gains in the "
        "long-tail of difficulty rather than uniform shifts."
    ),
    prior=0.9,
)

# Anchor reproducibility into discussion synthesis
strat_reproducibility = support(
    [claim_conductor_proposal],
    claim_reproducibility,
    reason=(
        "The reproducibility claim (@claim_reproducibility) is "
        "supported by the explicit training hyperparameter "
        "specification (@setup_training_hyperparameters) for the "
        "Conductor framework (@claim_conductor_proposal): base "
        "model Qwen2.5-7B, 200 iters, AdamW, lr 1e-6, no KL, 2x "
        "H100, all hyperparameters reported."
    ),
    prior=0.97,
    background=[setup_training_hyperparameters],
)

# Anchor ood-few-shot finding to training-setup (data pool diversity)
strat_ood_few_shot_finding_anchor = support(
    [claim_conductor_proposal],
    claim_ood_few_shot_finding,
    reason=(
        "The OOD-few-shot finding "
        "(@claim_ood_few_shot_finding) is a property of the few-"
        "shot conditioning protocol (@setup_few_shot_conditioning) "
        "applied to the Conductor framework "
        "(@claim_conductor_proposal): varying the source of the "
        "four few-shot examples between in-distribution and OOD "
        "task corpora yields the Table 4 + Fig. 9 pattern."
    ),
    prior=0.9,
    background=[setup_few_shot_conditioning],
)

# Anchor table-9 / 10 / 11 / 7 / 8 / 6 / 5 as observable leaves
# These are 'reads off the table' facts; they will get priors directly
# in priors.py as observed table-row claims.

# Anchor controlled-summary to its dependents
# Already covered above.

# Anchor weak-models-essential to per-model specialization
# Already covered above.


# Cross-pool generality anchored to controlled-pool result (Table 8)
strat_ood_constrained_anchor = support(
    [claim_conductor_avg_controlled],
    claim_table8_ood_constrained,
    reason=(
        "Table 8 (@claim_table8_ood_constrained) is reported under "
        "the constrained-setting protocol "
        "(@setup_constrained_setting) in the same evaluation that "
        "produced the in-domain controlled-setting average "
        "(@claim_conductor_avg_controlled), giving the OOD zero-shot "
        "transfer results."
    ),
    prior=0.97,
    background=[setup_constrained_setting],
)

# ============================================================================
# Q_central is closed by the Conductor proposal + emergent skills + SOTA
# ============================================================================

# (Question is structural; not a Claim. No support strategy needed -- it
# is consumed via background in the proposal.)


__all__ = [
    # Diagnosis -> proposal
    "strat_provider_specialization_from_literature",
    "strat_manual_orch_limits",
    "strat_prior_routing_inexpressive",
    "strat_conductor_proposal",
    "strat_natural_language_medium",
    "strat_grpo_emergent_strategies",
    "strat_compatible_any_rl",
    # Emergent skills
    "strat_emergent_prompt_engineering",
    "strat_emergent_topology_design",
    "strat_two_emergent_skills_assembly",
    "strat_emergent_task_adaptivity",
    "strat_meta_orchestrator_thesis",
    "strat_exploration_sidestep",
    # Table 1
    "strat_table1_math500",
    "strat_table1_mmlu",
    "strat_table1_rlpr",
    "strat_table1_lcb",
    "strat_table1_aime25",
    "strat_table1_bcb",
    "strat_table1_gpqa",
    "strat_avg_unconstrained",
    "strat_headline_sota",
    # Controlled
    "strat_avg_controlled",
    "strat_avg_workflow_steps",
    "strat_controlled_summary",
    # (removed strat_efficiency_consensus_assembly placeholder)
    "strat_moa_failure",
    "strat_masrouter_failure",
    "strat_headline_beats_baselines",
    # Section 4.4
    "strat_dynamic_pool_design",
    "strat_open_pool_finetuned",
    "strat_closed_pool_finetuned",
    "strat_pool_generalization_thesis",
    "strat_headline_pool_generality",
    "strat_recursive_scaling_aim",
    "strat_recursion_decision_protocol",
    "strat_recursion_cost_cap",
    "strat_recursion_aime25",
    "strat_recursion_gpqa",
    "strat_recursion_bcb",
    "strat_recursion_bcb_redistribution",
    "strat_recursion_dynamic_scaling_thesis",
    "strat_headline_recursive_scaling",
    "strat_ood_few_shot_explanation",
    "strat_ood_few_shot_finding_anchor",
    # Section 4.5
    "strat_3b_same_agent_dist",
    "strat_7b_better_prompts",
    "strat_scale_thesis",
    "strat_workflow_step_distribution",
    # Ablations
    "strat_subtask_ablation",
    "strat_few_shot_ablation",
    "strat_fine_grained_topology",
    "strat_subtask_alone_matters",
    "strat_frontier_orchestrator_evidence",
    "strat_conductor_training_essential",
    "strat_per_model_specialization",
    "strat_weak_models_subtask",
    "strat_qwen_thinking_bcb",
    # Related work
    "strat_rl_tool_positioning",
    "strat_mas_positioning",
    "strat_positioning_summary",
    # Contributions / discussion
    "strat_extension_dynamic_pool",
    "strat_extension_recursive",
    "strat_three_contributions",
    "strat_broader_thesis",
    "strat_discussion_synthesis",
    "strat_meta_agent_thesis",
    "strat_future_beyond_llms",
    "strat_ethics",
    "strat_long_tail",
    "strat_reproducibility",
    "strat_ood_constrained_anchor",
    # Inductions: cross-benchmark
    "s_bench_math500",
    "s_bench_mmlu",
    "s_bench_rlpr",
    "s_bench_lcb",
    "s_bench_aime25",
    "s_bench_bcb",
    "s_bench_gpqa",
    "ind_bench_12",
    "ind_bench_123",
    "ind_bench_1234",
    "ind_bench_12345",
    "ind_bench_123456",
    "ind_bench_1234567",
    # Inductions: cross-pool
    "s_pool_full",
    "s_pool_open",
    "s_pool_closed",
    "ind_pool_full_open",
    "ind_pool_full_open_closed",
    # Inductions: recursion
    "s_rec_bcb",
    "s_rec_gpqa",
    "s_rec_aime",
    "ind_rec_12",
    "ind_rec_123",
    # Abduction
    "claim_pred_learned_coord_explains",
    "claim_pred_alt_trivial_explains",
    "claim_obs_pattern",
    "strat_obs_pattern_assembly",
    "s_h_explains",
    "s_alt_explains",
    "comp_learned_vs_trivial",
    "abd_learned_vs_trivial",
    # Contradictions
    "claim_foil_manual_best",
    "strat_foil_manual",
    "contra_manual_vs_rl",
    "claim_foil_7b_cannot_beat_frontier",
    "strat_foil_7b",
    "contra_7b_foil_vs_sota",
]
