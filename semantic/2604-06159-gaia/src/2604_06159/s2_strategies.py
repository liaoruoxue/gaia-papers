"""Layer 2 strategies — TPO (2604.06159)."""

from gaia.lang import claim, support, deduction
from .motivation import (
    tpo_decouples_rl,
    tpo_excels_on_sparse_reward,
    tpo_matches_on_dense_reward,
    tpo_simplicity_advantage,
    bandit_and_single_task,
)


# ── Weak / Boundary premises (enter deduction, not support) ──

weak_pg_baselines_undertuned = claim(
    "PG baselines used default hyperparameters; a dedicated PG tuning study "
    "on sparse-reward tasks has not been done. Critic-based methods with "
    "better exploration (RND, curiosity) might close the gap.",
    title="Weak: PG baselines may be undertuned",
    aggregated_from=["claim_fig1_sparse_outperform"],
    semantic_refs=["tpo_excels_on_sparse_reward"],
    issue_type="alt_not_excluded",
    what_would_falsify="dedicated PG hyperparameter sweep on sparse-reward tasks",
)

weak_no_multistep = claim(
    "Experiments cover bandit / single-task / sequence tasks but not "
    "multi-step multi-turn agent tasks (SWE-bench, WebArena-full, "
    "multi-hop web navigation).",
    title="Weak: no multi-step agent task validation",
    aggregated_from=["bandit_and_single_task"],
    semantic_refs=["tpo_excels_on_sparse_reward", "tpo_matches_on_dense_reward"],
    issue_type="scope_limit",
    what_would_falsify="multi-step agent benchmark; if PG methods catch up under long-horizon tasks, TPO advantage is task-bound",
)

bdry_online_rl_only = claim(
    "TPO is positioned in online RL for agents. It does not compare "
    "against RLHF/DPO-based methods that use preference data.",
    title="Boundary: online RL only, no preference-data comparison",
    aggregated_from=[],
    semantic_refs=["tpo_decouples_rl"],
    boundary_type="scope",
    stated_explicitly=True,
)

bdry_7b_scale = claim(
    "WebArena-Turbo results are on a 7B base model; large-scale (70B+) "
    "behavior is unverified.",
    title="Boundary: 7B scale only",
    aggregated_from=[],
    semantic_refs=["tpo_matches_on_dense_reward"],
    boundary_type="scope",
    stated_explicitly=False,
)


# ── Strategies ──

# Soft diagnostic: decoupling mechanism → sparse-reward advantage
strat_decouple_enables_sparse = support(
    [tpo_decouples_rl],
    tpo_excels_on_sparse_reward,
    reason=(
        "Decoupling breaks the reward-density / learning-signal dependency. "
        "Target distribution q incorporates zero-reward trajectories; "
        "cross-entropy fit gives a dense signal regardless of reward sparsity."
    ),
    prior=0.88,
)

# Rigid method claim: TPO's dense-reward parity is a method-level deduction
strat_tpo_dense_validity = deduction(
    [tpo_decouples_rl, bdry_7b_scale, weak_no_multistep],
    tpo_matches_on_dense_reward,
    reason=(
        "If decoupling yields unbiased gradient estimates and the 7B + bandit "
        "scope is respected, TPO matches PG methods on dense reward. If this "
        "fails at larger scale or longer horizon, BP flags bdry_7b_scale / "
        "weak_no_multistep as the premises to revisit."
    ),
    prior=0.90,
)

strat_tpo_simplicity_validity = deduction(
    [tpo_decouples_rl, bdry_online_rl_only],
    tpo_simplicity_advantage,
    reason=(
        "The simpler training loop follows from decoupling (no critic, value, "
        "GAE, off-policy correction). Scoped to online RL — the simplicity "
        "claim is not asserted vs preference-data methods."
    ),
    prior=0.92,
)

# Sparse-reward validity includes the alt-tuning caveat as deduction premise
strat_tpo_sparse_validity = deduction(
    [tpo_decouples_rl, weak_pg_baselines_undertuned, weak_no_multistep],
    tpo_excels_on_sparse_reward,
    reason=(
        "The sparse-reward advantage follows from decoupling, conditional on "
        "(a) the gap surviving dedicated PG tuning and (b) the result "
        "generalising to multi-step tasks. If PG catches up under dedicated "
        "tuning, BP flags weak_pg_baselines_undertuned."
    ),
    prior=0.80,
)
