"""Layer 2 — Target Policy Optimization (2604.06159)

TPO decouples RL for agents: build target distribution from environment
feedback, then cross-entropy-fit policy to target. No critic, no value
function, no off-policy data.
"""

from gaia.lang import claim, setting

tpo_decouples_rl = claim(
    "TPO decouples RL-based agent optimization into two independent steps: "
    "(1) build a target distribution q from environment feedback (solving Q1: "
    "what should the agent do?), (2) cross-entropy-fit the policy to q (solving "
    "Q2: how to update the agent?). This eliminates the critic, value function, "
    "and off-policy correction that make PPO/GRPO/DG fragile.",
    title="TPO decouples Q1 (target) from Q2 (update) — no critic needed",
    aggregated_from=[
        "claim_tpo_decouples", "claim_pg_entangles_two_questions",
        "claim_entanglement_makes_pg_fragile",
    ],
)

tpo_excels_on_sparse_reward = claim(
    "PG/PPO/GRPO/DG fail to learn on sparse-reward tasks because the policy "
    "gradient vanishes when most trajectories earn zero reward. TPO's decoupled "
    "design avoids this: the target distribution is built from all available "
    "feedback (including zeros), and the cross-entropy fit provides a dense "
    "learning signal regardless of reward sparsity. On token reversal (sparse "
    "reward), TPO solves the task while GRPO/DG fail to leave random baseline. "
    "This is a 'solve vs not-learn' gap, not a small delta.",
    title="TPO excels where PG methods fail: sparse-reward tasks",
    aggregated_from=[
        "claim_fig1_sparse_outperform", "claim_fig1_sparse_qualitative_gap",
        "claim_fig1_dense_match", "claim_entanglement_makes_pg_fragile",
    ],
)

tpo_matches_on_dense_reward = claim(
    "On dense-reward tasks (MNIST bandit, WebArena-Turbo), TPO matches or "
    "slightly exceeds PG-based methods (PPO, GRPO, DG). It achieves 59.2% "
    "on WebArena-Turbo (+16.2pp over prompt engineering SPA's 43%). The key "
    "insight is that TPO's design loses nothing on easy tasks while gaining "
    "decisively on hard ones.",
    title="TPO matches PG methods on dense reward, dominates on sparse",
    aggregated_from=[
        "claim_fig1_dense_match", "claim_tpo_webarena_result",
        "claim_headline_contribution",
    ],
)

tpo_simplicity_advantage = claim(
    "TPO requires no critic network, no value function, no GAE, no off-policy "
    "correction, and no KL penalty tuning. The core loop is: sample trajectories "
    "→ score with environment → build target q → cross-entropy step. This "
    "simplicity eliminates multiple hyperparameters and failure modes that "
    "make PG-based agent training brittle in practice.",
    title="TPO eliminates critic, GAE, KL penalty — simpler and more robust",
    aggregated_from=[
        "claim_tpo_decouples", "claim_pg_entangles_two_questions",
    ],
)

# ── Boundary ──

bandit_and_single_task = claim(
    "TPO experiments span tabular bandits, neural bandits, sequence tasks, "
    "and WebArena-Turbo. However, it has not been tested on multi-turn, "
    "multi-step agent tasks (e.g., SWE-bench, multi-hop web navigation) "
    "where the action space is compositional and the credit assignment "
    "problem is harder.",
    title="Limitation: single-step or simple multi-step tasks only",
)

no_rlhf_comparison = claim(
    "TPO compares against PPO, GRPO, DG, and prompt engineering baselines "
    "but not against RLHF/DPO-based methods that use preference data. This "
    "is appropriate for the paper's scope (online RL for agents) but limits "
    "claims about TPO vs the broader RL optimization landscape.",
    title="Limitation: no comparison with preference-based methods",
)
