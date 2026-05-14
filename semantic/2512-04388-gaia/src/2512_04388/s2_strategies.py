"""Layer 2 strategies and judgment nodes for Conductor (2512.04388).

Strategy chains connect semantic claims via support/deduction.
Judgment nodes (surprise/elegant/weak/boundary/negative) are gaia claim objects.
"""

from gaia.lang import claim, support, deduction

from .motivation import (
    conductor_rl_emergent_coordination,
    conductor_sota_cost_efficient,
    conductor_cross_pool_generalization,
    conductor_recursive_scaling,
    conductor_broader_thesis_rl_sufficient,
)

# ===========================================================================
# Strategy chain — 4 premises converge on broader thesis (1 deduction)
# ===========================================================================

strat_broader_thesis = deduction(
    [
        conductor_sota_cost_efficient,
        conductor_rl_emergent_coordination,
        conductor_cross_pool_generalization,
        conductor_recursive_scaling,
    ],
    conductor_broader_thesis_rl_sufficient,
    reason=(
        "Four independent lines of evidence converge: (1) SOTA on 7 benchmarks "
        "at lower cost — empirical anchor; (2) two emergent RL-discovered skills "
        "(topology design + prompt engineering) — mechanistic account; "
        "(3) cross-pool generalization (open-only beats Claude ~10%, closed-only "
        "matches pretrained SOTA) — rules out free-riding on GPT-5; "
        "(4) recursive self-referential topology as new test-time scaling axis "
        "(+2.2 pp on BCB via adaptive redistribution). If any premise weakens, "
        "BP back-propagates penalty to that premise."
    ),
    prior=0.82,
)

# ===========================================================================
# Surprising Points
# ===========================================================================

surprise_ood_few_shot_better = claim(
    "OOD few-shot examples produce better Conductor performance than "
    "in-distribution examples. All-OOD few-shot yields +5.97 pp on "
    "LiveCodeBench vs all-in-distribution. The posited mechanism: OOD "
    "examples prevent exploitation of provided strategies and incentivize "
    "exploration of the coordination strategy space — an anti-reward-hacking "
    "effect from the conditioning distribution.",
    title="Surprising: OOD few-shot outperforms in-distribution (anti-reward-hacking via conditioning)",
    aggregated_from=[
        "claim_ood_few_shot_finding",
        "claim_ood_few_shot_explanation",
    ],
    semantic_refs=["conductor_rl_emergent_coordination"],
    novelty_vs_kb="new",
    kb_anchor="chunks/rl-training.md",
)

strat_surprise_ood = support(
    [surprise_ood_few_shot_better],
    conductor_rl_emergent_coordination,
    reason="OOD few-shot effect is direct evidence that the emergent coordination is genuine exploration, not lazy pattern reuse.",
    prior=0.82,
)

surprise_3b_same_agent_but_worse = claim(
    "A 3B Conductor converges to the same agent-selection distribution as "
    "the 7B Conductor, yet the 7B substantially outperforms via better "
    "prompt engineering. Agent selection (picking which model) is learnable "
    "at small scale; prompt engineering (what to tell each model) needs "
    "larger models. The two emergent skills have different scaling laws.",
    title="Surprising: agent-selection and prompt-engineering have different scaling laws (3B vs 7B)",
    aggregated_from=[
        "claim_3b_same_agent_dist",
        "claim_7b_better_prompt_engineering",
    ],
    semantic_refs=["conductor_rl_emergent_coordination"],
    novelty_vs_kb="new",
    kb_anchor="chunks/multi-agent.md",
)

strat_surprise_scale = support(
    [surprise_3b_same_agent_but_worse],
    conductor_rl_emergent_coordination,
    reason="Differential scaling of the two emergent skills reveals that prompt engineering is the harder capability, supporting the natural-language-medium design choice.",
    prior=0.85,
)

surprise_small_coordinator_beats_frontier = claim(
    "A 7B coordinator lifts frontier workers (GPT-5, Gemini 2.5 Pro, Claude "
    "Sonnet 4) past their individual ceilings — overturning the intuition "
    "that a small model cannot outperform much larger models. The key is "
    "reframing: the Conductor doesn't solve tasks itself; it orchestrates "
    "workers that are individually 5-50x larger. The untrained frontier-LLM-"
    "as-Conductor fails to match the 7B RL-trained Conductor by 4-16 pp.",
    title="Surprising: 7B coordinator lifts frontier workers past individual ceilings",
    aggregated_from=[
        "claim_headline_sota",
        "claim_table11_conductor_replacement",
        "claim_conductor_training_essential",
        "claim_foil_7b_cannot_beat_frontier",
    ],
    semantic_refs=["conductor_broader_thesis_rl_sufficient"],
    novelty_vs_kb="refine",
    kb_anchor="chunks/multi-agent.md",
)

strat_surprise_7b = support(
    [surprise_small_coordinator_beats_frontier],
    conductor_sota_cost_efficient,
    reason="The meta-agent design point (small coordinator + large workers) is validated by the frontier-LLM replacement ablation showing trained 7B beats untrained frontier LLM orchestrators.",
    prior=0.84,
)

# ===========================================================================
# Elegant Points (islands — metadata only, no BP)
# ===========================================================================

elegant_nl_workflow_medium = claim(
    "The Conductor's core design choice — natural language as the workflow "
    "specification medium — gives it an unrestricted instruction surface over "
    "workers. Unlike prior routing frameworks constrained to fixed topology "
    "vocabularies or pre-specified role templates, natural-language subtask "
    "specification removes the expressivity bottleneck. This single design "
    "choice unifies what were previously separate systems: router, subtask "
    "decomposer, and prompt engineer.",
    title="Elegant: natural-language workflow as unrestricted instruction surface",
    aggregated_from=[
        "claim_conductor_proposal",
        "claim_prior_routing_inexpressive",
    ],
    semantic_refs=["conductor_rl_emergent_coordination"],
    portability="high",
    reusable_primitive=True,
)

elegant_ordinal_naming = claim(
    "Workers are presented to the Conductor as ordinal numbers (Model 0..k) "
    "rather than by name. This eliminates prior-association bias — the "
    "Conductor cannot fall back on 'GPT-5 is good at math' from pretraining "
    "and must learn per-worker capabilities from empirical feedback. A simple "
    "anti-bias mechanism with zero additional cost.",
    title="Elegant: ordinal model naming eliminates prior-association bias",
    aggregated_from=["setup_ordinal_model_names"],
    semantic_refs=["conductor_rl_emergent_coordination"],
    portability="high",
    reusable_primitive=True,
)

elegant_recursion_pass_through = claim(
    "The recursive Conductor's pass-through decision (emit three empty lists "
    "to return the previous response unchanged) elegantly handles the 'already "
    "optimal' case. On AIME25 the Conductor correctly passes through with 0 "
    "gain — recursion doesn't waste compute on already-good strategies. The "
    "decision is made by the Conductor itself, not by an external budget "
    "heuristic.",
    title="Elegant: recursion pass-through decision avoids wasting compute on already-optimal strategies",
    aggregated_from=[
        "claim_recursion_aime25",
        "claim_recursion_decision_protocol",
    ],
    semantic_refs=["conductor_recursive_scaling"],
    portability="medium",
    reusable_primitive=False,
)

# ===========================================================================
# Weak Points
# ===========================================================================

weak_no_standard_error_tables_1_2_10 = claim(
    "Standard error is reported only for Table 7. Tables 1, 2, and 10 report "
    "point estimates without error bars. Close-margin deltas — MATH500 +0.4, "
    "MMLU +0.6, BCB +0.35 — lack statistical separation quantification. The "
    "headline 'won every column' claim on close margins may not survive "
    "proper confidence intervals.",
    title="Weak: no standard error on Tables 1/2/10 — close-margin deltas unquantified",
    aggregated_from=[
        "claim_table1_full",
        "claim_table2_recursion_full",
        "claim_table10_agent_selection_ablation",
    ],
    semantic_refs=["conductor_sota_cost_efficient"],
    issue_type="weak_evidence",
    what_would_falsify="Compute 95% CI on MATH500/MMLU/BCB deltas; if any CI crosses zero, the 'all-columns-won' claim is overstated for that benchmark.",
)

weak_only_7b_conductor_tested = claim(
    "Only 3B and 7B Conductor sizes tested. The marginal benefit curve at "
    "13B/30B/70B is unmeasured. The frontier-LLM-as-Conductor ablation "
    "(Table 11) is a proxy but uses no Conductor-specific training — it "
    "doesn't answer how a trained 13B+ Conductor would perform. If prompt-"
    "engineering quality scales with Conductor size (as 3B→7B suggests), "
    "the optimal Conductor size is unknown.",
    title="Weak: only 3B/7B Conductor sizes tested; optimal scale unknown",
    aggregated_from=[
        "claim_7b_better_prompt_engineering",
        "claim_scale_thesis",
    ],
    semantic_refs=["conductor_rl_emergent_coordination"],
    issue_type="scope_limit",
    what_would_falsify="Train 13B/30B/70B Conductors; if gains plateau at 7B, the scaling thesis is falsified.",
)

weak_reasoning_only_domains = claim(
    "All 7 benchmarks are reasoning-heavy (math/code/science/multi-task "
    "knowledge). Whether the Conductor framework benefits long-form "
    "generation, retrieval-heavy QA, vision-language tasks, or tool-use "
    "scenarios is unmeasured. The framework assumes a 'verifiable answer' "
    "reward structure — tasks without clear correctness signals may not "
    "admit the same RL training protocol.",
    title="Weak: only reasoning benchmarks tested; non-reasoning domains unmeasured",
    aggregated_from=[
        "setup_eval_benchmarks",
        "setup_training_data",
    ],
    semantic_refs=["conductor_broader_thesis_rl_sufficient"],
    issue_type="scope_limit",
    what_would_falsify="Test on long-form generation or retrieval QA; if gains disappear outside reasoning, the Conductor framework is reasoning-specific.",
)

weak_few_shot_are_real_completions = claim(
    "The few-shot examples are real Conductor completions from cold-start "
    "training runs. The ablation shows removing them costs -7 to -9 pp, but "
    "doesn't test whether any exemplar workflow (human-curated, random-"
    "baseline) yields the same effect. The OOD-better-than-ID finding could "
    "be a selection effect — the OOD examples happen to be qualitatively "
    "superior — rather than a causal anti-exploitation mechanism.",
    title="Weak: few-shot requirement untested against alternative exemplar sources",
    aggregated_from=[
        "claim_few_shot_ablation",
        "claim_ood_few_shot_explanation",
    ],
    semantic_refs=["conductor_rl_emergent_coordination"],
    issue_type="alt_not_excluded",
    what_would_falsify="Replace Conductor few-shots with human-curated workflows; if performance matches, the few-shot content matters more than the OOD property.",
)

# ===========================================================================
# Boundary Conditions
# ===========================================================================

bdry_qwen_base_only = claim(
    "All experiments use Qwen2.5-7B as the Conductor base model. No Llama, "
    "Mistral, DeepSeek, or other architecture tested as Conductor base. "
    "Qwen2.5 may have specific properties (instruction-following, reasoning "
    "pretraining) that make it particularly suitable for the Conductor role.",
    title="Boundary: Qwen2.5-7B base only — no cross-architecture Conductor validation",
    aggregated_from=["setup_base_model"],
    semantic_refs=["conductor_rl_emergent_coordination"],
    boundary_type="scope",
    stated_explicitly=False,
)

bdry_max_5_steps = claim(
    "The Conductor is trained with a maximum of 5 workflow steps. The impact "
    "of longer workflows (6+ steps) on task success and cost is unmeasured. "
    "The Conductor learns to average 3 steps — whether it would benefit from "
    "a higher cap on harder problems is unknown.",
    title="Boundary: max 5 workflow steps — longer workflows unmeasured",
    aggregated_from=[
        "claim_conductor_proposal",
        "claim_avg_workflow_steps",
    ],
    semantic_refs=["conductor_sota_cost_efficient"],
    boundary_type="implementation",
    stated_explicitly=True,
)

bdry_recursion_2x_budget_cap = claim(
    "Recursion experiments cap at <2x the original agentic-call budget. "
    "Deeper recursion (3x, 5x, 10x) is unmeasured. The paper acknowledges "
    "this leaves room for further improvement — whether gains compound with "
    "recursion depth (analogous to CoT scaling) or saturate quickly is "
    "unknown.",
    title="Boundary: recursion capped at <2x budget — deeper recursion unmeasured",
    aggregated_from=["claim_recursion_cost_cap"],
    semantic_refs=["conductor_recursive_scaling"],
    boundary_type="scope",
    stated_explicitly=True,
)

bdry_verifiable_reward_assumption = claim(
    "The GRPO training protocol requires a verifiable end-task reward "
    "(correct/incorrect answer). Tasks without clear binary or scalar "
    "correctness signals — creative writing, open-ended analysis, multi-"
    "turn dialogue — are outside the current framework's training scope. "
    "The 'RL alone is sufficient' thesis is conditioned on the existence "
    "of a verifiable reward signal.",
    title="Boundary: requires verifiable reward signal — open-ended tasks outside scope",
    aggregated_from=[
        "setup_training_data",
        "claim_broader_thesis",
    ],
    semantic_refs=["conductor_broader_thesis_rl_sufficient"],
    boundary_type="simplification",
    stated_explicitly=False,
)

# ===========================================================================
# Negative Results
# ===========================================================================

neg_fine_grained_topology_no_gain = claim(
    "Fine-grained topology specification (per-position access lists instead "
    "of binary all/none) produces no significant gain at 7B scale. The "
    "Conductor learns to use the more complex scheme effectively but "
    "performance is comparable or slightly worse (LCB -3.05 pp). The paper "
    "correctly opts for the simpler binary version. This negative result is "
    "useful: more complex topology control doesn't automatically help — the "
    "bottleneck at 7B is prompt engineering quality, not topology granularity.",
    title="Negative: fine-grained topology specification yields no significant gain at 7B",
    aggregated_from=[
        "claim_fine_grained_topology_ablation",
        "claim_table9_ablations",
    ],
    semantic_refs=["conductor_rl_emergent_coordination"],
)

neg_recursion_zero_gain_aime25 = claim(
    "Recursive Conductor yields exactly 0 gain on AIME25 (66.67 = 66.67). "
    "This is a correct negative result — the Conductor's pretrained strategy "
    "on AIME25 is already optimal, and recursion correctly passes through. "
    "The zero gain is a stronger test of the recursion mechanism than a "
    "positive gain: it demonstrates selectivity rather than unconditional "
    "re-planning.",
    title="Negative: recursion zero gain on AIME25 — correct pass-through on already-optimal strategy",
    aggregated_from=["claim_recursion_aime25"],
    semantic_refs=["conductor_recursive_scaling"],
)

neg_3b_worker_impairing_subtask = claim(
    "The 3B Conductor sometimes produces subtasks that impair workers — e.g., "
    "instructing a model to hide its reasoning in XML tags due to a formatting "
    "constraint, degrading collaboration quality. The 7B Conductor avoids this. "
    "This negative result bounds the minimum viable Conductor scale: at 3B, "
    "prompt engineering is unreliable enough to occasionally harm performance.",
    title="Negative: 3B Conductor produces worker-impairing subtasks (hiding reasoning in tags)",
    aggregated_from=["claim_7b_better_prompt_engineering"],
    semantic_refs=["conductor_rl_emergent_coordination"],
)

# ===========================================================================
# Deduction chains — weak/bdry nodes as premises for method validity
# ===========================================================================

premise_skills_well_documented = claim(
    "The two emergent skills (topology design + prompt engineering) are "
    "consistently observed across training and documented in Figs. 3, 7, 8, "
    "19-28. The agent-selection skill is replicable at 3B; the prompt-"
    "engineering skill improves with Conductor size (3B→7B).",
    title="Premise: emergent skills are well-documented across multiple figures and scales",
)

strat_emergent_coordination_validity = deduction(
    [
        premise_skills_well_documented,
        weak_only_7b_conductor_tested,
        weak_reasoning_only_domains,
        weak_few_shot_are_real_completions,
        bdry_qwen_base_only,
        bdry_max_5_steps,
        bdry_verifiable_reward_assumption,
    ],
    conductor_rl_emergent_coordination,
    reason=(
        "The emergent coordination claim holds under the documented conditions "
        "(Qwen2.5-7B, reasoning tasks, verifiable reward, ≤5 steps). Three "
        "weakness flags (scale limit, domain limit, few-shot dependency) and "
        "three boundary conditions (Qwen base, step cap, reward type) bound "
        "the claim's scope. BP will back-propagate if the conclusion is "
        "weakened by other evidence."
    ),
    prior=0.88,
)

strat_sota_validity = deduction(
    [
        weak_no_standard_error_tables_1_2_10,
        bdry_max_5_steps,
    ],
    conductor_sota_cost_efficient,
    reason=(
        "The SOTA claim is empirically strong (Table 1, Table 7 both show "
        "Conductor first on all columns) but the close-margin deltas lack "
        "statistical separation. The 5-step cap bounds the efficiency claim."
    ),
    prior=0.85,
)

strat_recursion_validity = deduction(
    [
        bdry_recursion_2x_budget_cap,
    ],
    conductor_recursive_scaling,
    reason=(
        "The recursion claim is supported by Table 2 and the redistribution "
        "mechanism (Fig. 10), but the <2x budget cap bounds the scaling "
        "extrapolation."
    ),
    prior=0.83,
)

__all__ = [
    # Strategies
    "strat_broader_thesis",
    "strat_surprise_ood",
    "strat_surprise_scale",
    "strat_surprise_7b",
    "strat_emergent_coordination_validity",
    "strat_sota_validity",
    "strat_recursion_validity",
    # Surprising
    "surprise_ood_few_shot_better",
    "surprise_3b_same_agent_but_worse",
    "surprise_small_coordinator_beats_frontier",
    # Elegant
    "elegant_nl_workflow_medium",
    "elegant_ordinal_naming",
    "elegant_recursion_pass_through",
    # Weak
    "weak_no_standard_error_tables_1_2_10",
    "weak_only_7b_conductor_tested",
    "weak_reasoning_only_domains",
    "weak_few_shot_are_real_completions",
    # Boundary
    "bdry_qwen_base_only",
    "bdry_max_5_steps",
    "bdry_recursion_2x_budget_cap",
    "bdry_verifiable_reward_assumption",
    # Negative
    "neg_fine_grained_topology_no_gain",
    "neg_recursion_zero_gain_aime25",
    "neg_3b_worker_impairing_subtask",
    # Premise
    "premise_skills_well_documented",
]
