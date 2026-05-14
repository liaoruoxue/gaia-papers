"""Priors for the Conductor (2512.04388) Layer 2 semantic analysis.

Each prior includes justification with penalty decomposition.
Key must be a Knowledge object (not a string).
"""

from .motivation import (
    conductor_rl_emergent_coordination,
    conductor_sota_cost_efficient,
    conductor_cross_pool_generalization,
    conductor_recursive_scaling,
    conductor_broader_thesis_rl_sufficient,
)

from .s2_strategies import (
    surprise_ood_few_shot_better,
    surprise_3b_same_agent_but_worse,
    surprise_small_coordinator_beats_frontier,
    elegant_nl_workflow_medium,
    elegant_ordinal_naming,
    elegant_recursion_pass_through,
    weak_no_standard_error_tables_1_2_10,
    weak_only_7b_conductor_tested,
    weak_reasoning_only_domains,
    weak_few_shot_are_real_completions,
    bdry_qwen_base_only,
    bdry_max_5_steps,
    bdry_recursion_2x_budget_cap,
    bdry_verifiable_reward_assumption,
    neg_fine_grained_topology_no_gain,
    neg_recursion_zero_gain_aime25,
    neg_3b_worker_impairing_subtask,
    premise_skills_well_documented,
)

PRIORS = {
    # ---- Semantic claims ----
    conductor_rl_emergent_coordination: (
        0.88,
        "Two skills documented across multiple figures (3, 7, 8, 19-28). "
        "Agent-selection replicable at 3B. Prompt-engineering scales with "
        "Conductor size. Penalty -0.07: no >7B data; -0.05: emergent claims "
        "are qualitative (no metric for 'emergence')."
    ),
    conductor_sota_cost_efficient: (
        0.90,
        "Table 1 (unconstrained) + Table 7 (controlled) both show Conductor "
        "first on all columns. Efficiency is solid (Table 5: 1.56x cost-adjusted "
        "vs best baseline). Penalty -0.05: no SE on Tables 1/2/10; -0.05: "
        "close-margin deltas (MATH500 +0.4, MMLU +0.6) may not be statistically "
        "significant."
    ),
    conductor_cross_pool_generalization: (
        0.85,
        "Open-pool (+10% vs Claude) + closed-pool (matches pretrained SOTA) "
        "both positive. Randomized-pool finetuning protocol is clean (no new "
        "data). Penalty -0.05: pool sizes fixed at k=7; -0.05: only one round "
        "of finetuning tested; -0.05: extreme k=2 or k=15+ unmeasured."
    ),
    conductor_recursive_scaling: (
        0.83,
        "Table 2: +1.07 pp avg, +2.2 pp on BCB (largest gain). AIME25 "
        "pass-through is a clean negative control. Redistribution mechanism "
        "(Fig. 10) is documented. Penalty -0.05: <2x budget cap; -0.05: "
        "deeper recursion unmeasured; -0.07: only 3 OOD tasks tested."
    ),
    conductor_broader_thesis_rl_sufficient: (
        0.78,
        "The five semantic claims converge: SOTA + emergent skills + "
        "cross-pool + recursion + frontier-replacement all point to RL "
        "sufficiency. Penalty -0.07: all on Qwen2.5-7B base (one architecture); "
        "-0.05: reasoning-only domains; -0.05: single paper (no independent "
        "replication); -0.05: verifiable-reward assumption may not transfer."
    ),

    # ---- Surprising points ----
    surprise_ood_few_shot_better: (
        0.78,
        "Table 4 shows clear OOD > mixed > in-dist ordering. Proposed "
        "mechanism (prevent exploitation, incentivize exploration) is "
        "plausible but not directly tested. Penalty -0.07: could be selection "
        "effect; -0.05: alternative exemplar sources not tested; -0.10: "
        "single-paper finding."
    ),
    surprise_3b_same_agent_but_worse: (
        0.85,
        "Fig. 7 shows clear convergence of agent distribution. Fig. 15 "
        "provides concrete example of 3B producing inferior subtask. "
        "Penalty -0.05: only 3B/7B comparison; -0.05: agent-distribution "
        "metric is coarse (bin counts); -0.05: qualitative assessment of "
        "subtask quality."
    ),
    surprise_small_coordinator_beats_frontier: (
        0.88,
        "Table 11: 7B Conductor beats GPT-5/Gemini as conductors by +4 to "
        "+16 pp. Frontier-LLM-as-Conductor beats individuals (partial "
        "suitability confirmed). Penalty -0.05: frontier LLMs use 0-shot "
        "prompting vs Conductor's few-shot; -0.07: GPT-5/Gemini may improve "
        "with few-shot conditioning."
    ),

    # ---- Elegant points (standalone, no strategy in BP) ----
    elegant_nl_workflow_medium: (
        0.80,
        "Design choice is central to the framework's expressivity. Prior "
        "routing frameworks' fixed-vocabulary limitation is well-documented "
        "(MASRouter/RouterDC/Smoothie). Penalty -0.10: elegance is subjective; "
        "-0.10: no ablation directly comparing NL vs structured workflow spec."
    ),
    elegant_ordinal_naming: (
        0.85,
        "Simple, zero-cost anti-bias mechanism. The logic is sound: removing "
        "model names forces empirical learning. Penalty -0.10: no ablation "
        "comparing ordinal vs named models; -0.05: effect size unknown."
    ),
    elegant_recursion_pass_through: (
        0.88,
        "AIME25 pass-through (0 gain) is a clean demonstration. The three-"
        "empty-lists protocol is simple and elegant. Penalty -0.07: only one "
        "benchmark shows pass-through; -0.05: decision quality not directly "
        "evaluated."
    ),

    # ---- Weak points (deduction premises) ----
    weak_no_standard_error_tables_1_2_10: (
        0.85,
        "Table 7 does report SE; Tables 1/2/10 don't. Close-margin deltas "
        "(MATH500 +0.4, MMLU +0.6) without error bars are genuinely weak "
        "evidence for 'won every column'. Penalty -0.15: standard practice "
        "to report SE; omission is notable."
    ),
    weak_only_7b_conductor_tested: (
        0.90,
        "Only 3B/7B tested. Marginal benefit curve unknown. Frontier-LLM-"
        "as-Conductor is a proxy but doesn't answer the scaling question. "
        "Penalty -0.10: acknowledged limitation (Section 6)."
    ),
    weak_reasoning_only_domains: (
        0.92,
        "All 7 benchmarks are reasoning-heavy. This is a legitimate scope "
        "limit. Penalty -0.05: training data also reasoning-only; -0.03: "
        "paper acknowledges this in Section 6."
    ),
    weak_few_shot_are_real_completions: (
        0.80,
        "Few-shot examples are real Conductor completions. No test of "
        "alternative exemplar sources. OOD-better-than-ID could be selection "
        "effect. Penalty -0.15: this is a genuine alt-not-excluded gap; "
        "-0.05: the proposed mechanism is plausible but untested."
    ),

    # ---- Boundary conditions ----
    bdry_qwen_base_only: (
        0.95,
        "All experiments use Qwen2.5-7B base. No cross-architecture validation. "
        "This is a stated experimental choice, not a hidden assumption. "
        "Penalty -0.05: Qwen2.5 may have specific properties favoring the "
        "Conductor role."
    ),
    bdry_max_5_steps: (
        0.90,
        "Max 5 workflow steps during training. Conductor averages 3 steps "
        "in practice, so the cap may not bind. Penalty -0.10: whether "
        "longer workflows help on harder problems is unknown."
    ),
    bdry_recursion_2x_budget_cap: (
        0.95,
        "Explicitly stated in paper. Room for further improvement "
        "acknowledged. Penalty -0.05: deeper recursion scaling behavior "
        "is unknown but not hidden."
    ),
    bdry_verifiable_reward_assumption: (
        0.90,
        "GRPO requires verifiable reward. This is a fundamental boundary "
        "of the framework. Penalty -0.05: creative/open-ended tasks may "
        "admit learned reward models; -0.05: not discussed in paper."
    ),

    # ---- Negative results (support premises) ----
    neg_fine_grained_topology_no_gain: (
        0.88,
        "Table 9 shows fine-grained topology comparable or slightly worse. "
        "The finding is clean: more complex topology control doesn't help "
        "at 7B. Penalty -0.07: only tested at 7B; -0.05: might matter at "
        "larger Conductor scale."
    ),
    neg_recursion_zero_gain_aime25: (
        0.90,
        "Table 2 shows 66.67 = 66.67 on AIME25. Clean negative result. "
        "Penalty -0.10: only one benchmark shows pass-through; the decision "
        "mechanism is inferred, not directly verified."
    ),
    neg_3b_worker_impairing_subtask: (
        0.85,
        "Fig. 15 provides a concrete example. Bounds minimum viable "
        "Conductor scale. Penalty -0.10: single example, may not be "
        "representative of all 3B failures; -0.05: qualitative assessment."
    ),

    # ---- Deduction premises ----
    premise_skills_well_documented: (
        0.90,
        "Figs. 3, 7, 8, 19-28 document emergent behaviors across training "
        "and evaluation. Agent-selection replicable at 3B. Penalty -0.05: "
        "'emergence' is qualitative, no formal metric; -0.05: examples are "
        "cherry-picked for illustration."
    ),
}
