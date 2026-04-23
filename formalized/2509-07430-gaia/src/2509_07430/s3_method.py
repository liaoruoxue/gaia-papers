"""Section 3: DPH-RL Method — Two-Stage Training with f-Divergence Regularization"""

from gaia.lang import claim, setting

from .motivation import (
    f_divergence_setting,
    rlvr_setting,
    pass_at_k_setting,
    mass_covering_preserves,
)
from .s2_background import (
    grpo_objective,
    dapo_objective,
    ppo_objective,
    forward_kl_mass_covering,
    js_mass_covering,
    trpo_bound,
)

# ── Settings ──────────────────────────────────────────────────────────────────

dphrl_objective = setting(
    "The DPH-RL (Diversity-Preserving Hybrid RL) optimization objective is: "
    "$\\max_{\\pi_\\theta} \\mathbb{E}_{q \\sim \\mathcal{D}} "
    "[\\mathbb{E}_{a \\sim \\pi_\\theta(\\cdot|q)}[r(a|q)] - \\eta D_f(\\pi_\\theta(\\cdot|q) \\| \\pi_{ref}(\\cdot|q))]$, "
    "where $\\eta > 0$ is a regularization weight, $D_f$ is an f-divergence, and "
    "$\\pi_{ref}$ is the fixed initial (reference) policy.",
    title="DPH-RL objective (definition)",
)

dataset_partition = setting(
    "The DPH-RL training dataset $\\mathcal{D}$ is partitioned into two disjoint subsets "
    "during pre-sampling: "
    "$\\mathcal{D}_{pef}$ (near-perfect set) contains queries where the base model consistently "
    "generates correct solutions (threshold: all 8/8 sampled rollouts are correct), and "
    "$\\mathcal{D}_{exp}$ (exploration set) contains the remaining queries where the model "
    "does not yet reliably succeed. The two subsets receive different training objectives.",
    title="Dataset partition into D_pef and D_exp (definition)",
)

exploration_loss = setting(
    "For queries in the exploration set $\\mathcal{D}_{exp}$, DPH-RL applies the standard "
    "PPO-clip objective without any KL or divergence penalty, enabling maximal exploration: "
    "$\\mathcal{L}_{DPH\\text{-}exp}(\\theta) = -\\mathbb{E}\\left[\\sum_t \\min\\!\\left("
    "\\rho_{i,t}(\\theta)\\hat{A}_{i,t},\\, \\text{clip}(\\rho_{i,t}(\\theta), 1-\\varepsilon, 1+\\varepsilon)\\hat{A}_{i,t}"
    "\\right)\\right]$, "
    "where $\\rho_{i,t}(\\theta) = \\pi_\\theta(a_{i,t}|s_{i,t})/\\pi_{old}(a_{i,t}|s_{i,t})$ "
    "and $\\hat{A}_{i,t}$ is the group-normalized advantage.",
    title="Exploration set loss (definition)",
)

preservation_loss = setting(
    "For queries in the preservation set $\\mathcal{D}_{pef}$, DPH-RL applies an "
    "f-divergence regularization loss to prevent forgetting: "
    "$\\mathcal{L}_{pef}(\\theta) = \\mathbb{E}_{q \\sim \\mathcal{D}_{pef}}[D_f(\\pi_\\theta(\\cdot|q) \\| \\pi_{ref}(\\cdot|q))]$. "
    "Two variants: "
    "DPH-F uses forward-KL: $D_{KL}(\\pi_{ref} \\| \\pi_\\theta) = \\sum_a \\pi_{ref}(a|q)\\log(\\pi_{ref}(a|q)/\\pi_\\theta(a|q))$; "
    "DPH-JS uses Jensen-Shannon divergence.",
    title="Preservation set loss (definition)",
)

generator_method = setting(
    "DPH-RL uses a generator-based approach to compute f-divergences without an online "
    "reference model: during the pre-sampling stage, a fixed set of rollout trajectories "
    "is sampled from $\\pi_{ref}$ (the initial policy). During training, divergences are "
    "computed against these pre-sampled trajectories, eliminating the need to query a "
    "reference model at each training step. This makes DPH-RL computationally comparable "
    "to GRPO.",
    title="Generator-based f-divergence computation (definition)",
)

# ── Claims ────────────────────────────────────────────────────────────────────

partition_rationale = claim(
    "Applying f-divergence regularization only to $\\mathcal{D}_{pef}$ (queries the base "
    "model already solves well) is principled because these queries represent existing "
    "capabilities that should be preserved. Applying no divergence constraint to "
    "$\\mathcal{D}_{exp}$ allows unconstrained exploration on hard queries where the model "
    "must learn new capabilities. This asymmetric treatment avoids applying a conservative "
    "constraint where aggressive exploration is needed.",
    title="Asymmetric partition rationale",
)

generator_efficiency = claim(
    "The generator-based pre-sampling approach in DPH-RL achieves computational efficiency "
    "comparable to GRPO/DAPO by avoiding online reference model inference during training. "
    "The divergence is computed against a static set of pre-sampled trajectories, adding "
    "only negligible overhead compared to methods that query a live reference model.",
    title="Generator approach is computationally efficient",
)

dphrl_handles_discrete = claim(
    "DPH-RL's generator-based computation effectively handles the challenge of computing "
    "f-divergences over discrete token sequences (LLM outputs) by approximating the "
    "divergence using the pre-sampled trajectories from $\\pi_{ref}$ as a Monte Carlo "
    "estimator, rather than requiring an intractable sum over all possible sequences.",
    title="Generator method handles discrete action space",
)

threshold_8_of_8_optimal = claim(
    "Using the strictest threshold (all 8/8 sampled rollouts correct) for partitioning "
    "into $\\mathcal{D}_{pef}$ yields the best performance, selecting approximately 8% of "
    "training data. This threshold provides a statistically unbiased subset of genuinely "
    "mastered queries, avoiding contamination with borderline queries. Looser thresholds "
    "(e.g., 6/8 or 7/8) provide broader coverage but dilute the diversity-preservation "
    "signal.",
    title="Strict 8/8 threshold optimal for D_pef",
    metadata={"source_table": "artifacts/2509.07430.pdf, Table 4"},
)

__all__ = [
    "partition_rationale",
    "generator_efficiency",
    "dphrl_handles_discrete",
    "threshold_8_of_8_optimal",
]
