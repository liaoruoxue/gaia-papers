"""Section 5: Main Experimental Results"""

from gaia.lang import claim, setting, support, abduction
from .motivation import claim_prm_fails_on_analysis
from .s2_architecture import (
    claim_env_interaction_critical, claim_ternary_reward_benefit,
    claim_prm_mirrors_agent,
)
from .s3_data import claim_diversity_over_purity
from .s4_training import claim_process_beats_outcome, claim_no_entropy_collapse

# ── Settings: experimental setup ──────────────────────────────────────────────

setup_benchmarks = setting(
    "DataPRM is evaluated on ScienceAgentBench (Success Rate metric, visualization "
    "assessed by Qwen3-VL-235B) and DABStep (accuracy, with Easy and Hard subsets). "
    "For RL, evaluation uses DABench and TableBench. DataPRM is trained on "
    "Qwen3-4B-Instruct with learning rate 1e-5, batch size 32, 3 epochs, on "
    "8×H20 GPUs.",
    title="Experimental setup"
)

setup_baselines = setting(
    "Baselines include: discriminative PRMs (Math-Shepherd-7B, Qwen2.5-Math-PRM-7B/72B, "
    "ReasonFlux-PRM-7B), generative PRMs (ThinkPRM-14B, GenPRM-32B), majority voting, "
    "LLM-as-a-judge (DeepSeek-V3.2), and self-rewarding (Qwen3-235B-A22B-Instruct). "
    "All use Qwen3-235B-A22B-Instruct as the base policy model for Best-of-N evaluation.",
    title="Baseline methods"
)

# ── Claims: main results ──────────────────────────────────────────────────────

claim_4b_beats_72b = claim(
    "DataPRM (4B parameters) outperforms all baselines including Qwen2.5-Math-PRM-72B "
    "(72B) and GenPRM-32B (32B). On DABStep average at N=16: DataPRM achieves 40.89% "
    "vs GenPRM 34.22% and Qwen2.5-Math-PRM-72B 29.11%. DataPRM also surpasses "
    "self-rewarding with Qwen3-235B (39.77%) despite 58× parameter efficiency.",
    title="4B DataPRM beats 72B baselines",
    metadata={"source_table": "artifacts/2604.24198.pdf, Table 2"}
)

claim_effective_scaling = claim(
    "DataPRM achieves effective scaling: performance consistently improves as N "
    "increases from 4 to 8 to 16 (37.11% → 39.77% → 40.89% on DABStep average). "
    "In contrast, existing PRMs exhibit negative scaling — Qwen2.5-Math-PRM-72B "
    "degrades from 33.33% (N=8) to 31.33% (N=16).",
    title="DataPRM scales effectively with candidate pool",
    metadata={"source_table": "artifacts/2604.24198.pdf, Table 2"}
)

claim_resists_reward_hacking = claim(
    "DataPRM resists reward hacking under beam search. While Qwen2.5-Math-PRM-72B "
    "exhibits performance degradation as beam search budget increases (33.56% → "
    "30.89% → 32.44%), DataPRM maintains consistent improvement (35.33% → 38.00% "
    "→ 38.89%). This indicates robustness against exploitative search policies.",
    title="DataPRM resists reward hacking",
    metadata={"figure": "artifacts/2604.24198.pdf, Figure 4"}
)

claim_58x_efficiency = claim(
    "DataPRM achieves 58× parameter efficiency compared to self-rewarding with "
    "Qwen3-235B-A22B-Instruct: the 4B DataPRM outperforms the 235B model's "
    "self-rewarding strategy on DABStep Hard (33.86% vs 32.80% at N=16).",
    title="58× parameter efficiency over self-rewarding"
)

# ── Connect claims ────────────────────────────────────────────────────────────

strat_4b_beats = support(
    [claim_env_interaction_critical, claim_ternary_reward_benefit,
     claim_diversity_over_purity],
    claim_4b_beats_72b,
    reason=(
        "DataPRM's superiority comes from three sources: (1) environment interaction "
        "enables detection of silent errors that text-only PRMs miss "
        "(@claim_env_interaction_critical), (2) ternary rewards correctly handle "
        "exploratory steps (@claim_ternary_reward_benefit), and (3) diversity-driven "
        "training data provides richer error patterns than filtered datasets "
        "(@claim_diversity_over_purity). These architectural and data advantages "
        "overcome the parameter gap with larger general PRMs."
    ),
    prior=0.90
)

strat_scaling = support(
    [claim_4b_beats_72b, claim_prm_fails_on_analysis],
    claim_effective_scaling,
    reason=(
        "DataPRM's effective scaling (@claim_4b_beats_72b) demonstrates it can "
        "distinguish correct trajectories even as the pool grows. In contrast, "
        "general PRMs' negative scaling (@claim_prm_fails_on_analysis) confirms "
        "they cannot — larger pools introduce more confusable trajectories. "
        "Task-specific training enables the discrimination that general PRMs lack."
    ),
    prior=0.88
)

strat_robustness = support(
    [claim_prm_mirrors_agent, claim_env_interaction_critical],
    claim_resists_reward_hacking,
    reason=(
        "DataPRM's robustness to reward hacking stems from environment-grounded "
        "verification (@claim_env_interaction_critical). Unlike text-only PRMs "
        "that can be fooled by superficially correct code, DataPRM executes the "
        "code and verifies outputs. The principle that verifier must mirror agent "
        "capabilities (@claim_prm_mirrors_agent) ensures the verification is as deep "
        "as the generation."
    ),
    prior=0.85
)

strat_efficiency = support(
    [claim_4b_beats_72b],
    claim_58x_efficiency,
    reason=(
        "The 4B model outperforms 235B self-rewarding (@claim_4b_beats_72b) because "
        "task-specific PRM training + environment interaction is more parameter-"
        "efficient than scaling a general-purpose model for self-evaluation. "
        "Self-rewarding inherits the same blind spots as the policy model, while "
        "a specialized PRM learns to detect errors the policy model cannot."
    ),
    prior=0.87
)
