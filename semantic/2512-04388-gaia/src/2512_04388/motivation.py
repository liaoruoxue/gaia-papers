"""Layer 2 semantic claims for Nielsen et al. 2026 — Conductor.

Aggregated from Layer 1's 90 user-visible claims across 12 modules.
Each semantic claim carries aggregated_from references back to L1.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Settings (operational context for the semantic analysis)
# ---------------------------------------------------------------------------

setup_7_worker_pool = setting(
    "7-worker pool: Gemini 2.5 Pro, Claude Sonnet 4, GPT-5, "
    "DeepSeek-R1-Distill-Qwen-32B, Gemma3-27B-it, Qwen3-32B (thinking + direct). "
    "3 closed-source + 4 open-source frontier models.",
    title="Setup: 7-worker heterogeneous pool (3 closed + 4 open)",
)

setup_base_7b = setting(
    "Base Conductor: Qwen2.5-7B, trained 200 GRPO iterations, 960 problems "
    "from MATH500/MMLU/RLPR/LiveCodeBench V1, no KL penalty, no ref-model sync.",
    title="Setup: Qwen2.5-7B trained 200 GRPO iters with no KL regularization",
)

setup_in_dist_ood_eval = setting(
    "Evaluation: 4 in-domain (MATH500/MMLU/RLPR/LCBv6) + 3 OOD "
    "(GPQA-Diamond/BigCodeBench/AIME25), 16 repeats each.",
    title="Setup: 7-benchmark evaluation (4 in-dist + 3 OOD)",
)

# ---------------------------------------------------------------------------
# Semantic claim 1: RL training produces emergent coordination skills
# ---------------------------------------------------------------------------

conductor_rl_emergent_coordination = claim(
    "A 7B language model trained end-to-end with GRPO on verifiable "
    "task rewards — without supervised coordination demonstrations, "
    "hand-engineered scaffolds, or pre-specified topology vocabularies — "
    "learns two emergent coordination skills: (a) targeted communication "
    "topology design (chain / tree / independent-then-aggregate / abdication "
    "modes), and (b) focused prompt engineering (worker-tailored subtask "
    "instructions). The agent-selection skill converges at 3B scale; "
    "prompt-engineering quality scales with Conductor size. Training converges "
    "in only 200 iterations without KL regularization — the powerful worker "
    "pool sidesteps the exploration bottleneck that plagues small-model RL.",
    title="Conductor RL produces emergent prompt-engineering + topology-design skills",
    aggregated_from=[
        "claim_conductor_two_emergent_skills",
        "claim_emergent_prompt_engineering",
        "claim_emergent_topology_design",
        "claim_emergent_task_adaptivity",
        "claim_exploration_sidestep",
        "claim_3b_same_agent_dist",
        "claim_7b_better_prompt_engineering",
        "claim_scale_thesis",
    ],
)

# ---------------------------------------------------------------------------
# Semantic claim 2: SOTA on 7 benchmarks at lower cost
# ---------------------------------------------------------------------------

conductor_sota_cost_efficient = claim(
    "The 7B Conductor attains state-of-the-art on all 7 evaluated benchmarks "
    "(avg 77.27 unconstrained, +2.49 pp over GPT-5), outperforms 5x-self-"
    "reflection, 5x-context, and 4 prior multi-agent baselines (MASRouter/MoA/"
    "RouterDC/Smoothie) in the controlled setting (avg 72.35 vs best worker "
    "64.14, +8.21 pp), with strictly better cost-vs-accuracy Pareto position: "
    "3 average workflow steps, 1,820 tokens/sample, ~$0.024 cost — 1.56x the "
    "cost-adjusted performance of the best 5x-consensus baseline. Gains are "
    "generational in magnitude (+2.5 pp AIME25 ≈ o3→GPT-5 jump, +2.7 pp "
    "GPQA-D), not incremental.",
    title="Conductor achieves SOTA on 7 benchmarks with better cost-efficiency than all baselines",
    aggregated_from=[
        "claim_headline_sota",
        "claim_headline_beats_baselines",
        "claim_table1_full",
        "claim_avg_unconstrained",
        "claim_table7_full",
        "claim_conductor_avg_controlled",
        "claim_controlled_summary",
        "claim_table5_efficiency_consensus",
        "claim_table6_efficiency_baselines",
        "claim_avg_workflow_steps",
        "claim_long_tail_difficulty",
        "claim_aime25_unconstrained",
        "claim_gpqa_unconstrained",
    ],
)

# ---------------------------------------------------------------------------
# Semantic claim 3: Cross-pool generalization
# ---------------------------------------------------------------------------

conductor_cross_pool_generalization = claim(
    "A short randomized-pool finetuning phase (k-of-n random subsets, no new "
    "data) makes the Conductor generalize to arbitrary user-specified worker "
    "subsets. Open-source-only pool: outperforms Claude Sonnet 4 by ~10%. "
    "Closed-source-only pool: matches original pretrained SOTA (no compromise). "
    "The gain is larger when the worker pool has more headroom — the Conductor "
    "amplifies complementary capabilities rather than free-riding on a single "
    "dominant worker. This enables cost-preferred or API-constrained deployment "
    "without expensive paid-API calls.",
    title="Randomized-pool finetuning generalizes Conductor to arbitrary worker subsets",
    aggregated_from=[
        "claim_headline_pool_generality",
        "claim_open_pool_finetuned",
        "claim_closed_pool_finetuned",
        "claim_pool_generalization_thesis",
        "claim_extension_dynamic_pool",
        "claim_dynamic_pool_design_aim",
    ],
)

# ---------------------------------------------------------------------------
# Semantic claim 4: Recursive self-referential topology
# ---------------------------------------------------------------------------

conductor_recursive_scaling = claim(
    "A second short finetuning phase (20 iters, 350 samples) enables the "
    "Conductor to specify itself as a worker, creating recursive topologies. "
    "In recursive calls, the Conductor receives its parent output + previous "
    "agent response, then decides to (a) instantiate a revision workflow or "
    "(b) pass through unchanged. Recursive Conductor adds +1.07 pp avg on OOD "
    "tasks (63.00 vs 61.93), with the largest gain on BigCodeBench (+2.2 pp) "
    "where GPT-5 underperforms — the Conductor adaptively redistributes from "
    "GPT-5 to Claude/Gemini. On AIME25 gain = 0 (correct pass-through when "
    "initial strategy is already optimal). Recursion depth is a tunable "
    "test-time hyperparameter, creating a new test-time scaling axis distinct "
    "from open-ended chain-of-thought.",
    title="Recursive self-referential topology enables dynamic test-time scaling",
    aggregated_from=[
        "claim_headline_recursive_scaling",
        "claim_table2_recursion_full",
        "claim_recursion_bcb",
        "claim_recursion_gpqa",
        "claim_recursion_aime25",
        "claim_recursion_bcb_redistribution",
        "claim_recursion_dynamic_scaling_thesis",
        "claim_extension_recursive",
        "claim_recursive_scaling_aim",
        "claim_recursion_decision_protocol",
    ],
)

# ---------------------------------------------------------------------------
# Semantic claim 5: Broader thesis — RL alone sufficient for emergent coordination
# ---------------------------------------------------------------------------

conductor_broader_thesis_rl_sufficient = claim(
    "The Conductor is among the early demonstrations that end-to-end RL on "
    "verifiable rewards alone is sufficient to discover sophisticated "
    "multi-agent prompt-engineering and coordination behaviors in language "
    "models — without supervised coordination demonstrations. The RL-trained "
    "7B Conductor beats untrained frontier LLMs (GPT-5, Gemini 2.5 Pro) as "
    "conductors by +4 to +16 pp: untrained LLMs rely on prior biases about "
    "which model is best for which task, while RL provides the empirical "
    "feedback mechanism to correct these biases. The Conductor establishes "
    "a new meta-agent design point: a small learned coordinator that lifts "
    "much larger frontier workers past their individual ceilings.",
    title="Broader thesis: end-to-end RL on verifiable rewards alone unlocks emergent LLM coordination",
    aggregated_from=[
        "claim_broader_thesis",
        "claim_meta_orchestrator_thesis",
        "claim_table11_conductor_replacement",
        "claim_frontier_orchestrator_evidence",
        "claim_conductor_training_essential",
        "claim_subtask_alone_matters",
        "claim_three_contributions",
        "claim_foil_7b_cannot_beat_frontier",
        "claim_foil_manual_best",
    ],
)

__all__ = [
    "setup_7_worker_pool",
    "setup_base_7b",
    "setup_in_dist_ood_eval",
    "conductor_rl_emergent_coordination",
    "conductor_sota_cost_efficient",
    "conductor_cross_pool_generalization",
    "conductor_recursive_scaling",
    "conductor_broader_thesis_rl_sufficient",
]
