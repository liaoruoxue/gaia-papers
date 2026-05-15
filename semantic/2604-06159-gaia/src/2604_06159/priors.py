"""Layer 2 priors — TPO (2604.06159)."""

from .motivation import (
    tpo_decouples_rl,
    tpo_excels_on_sparse_reward,
    tpo_matches_on_dense_reward,
    tpo_simplicity_advantage,
    bandit_and_single_task,
    no_rlhf_comparison,
)
from .s2_strategies import (
    weak_pg_baselines_undertuned,
    weak_no_multistep,
    bdry_online_rl_only,
    bdry_7b_scale,
)


PRIORS: dict = {
    tpo_decouples_rl: (
        0.90,
        "Closed-form target distribution + supervised cross-entropy fit; "
        "mathematically precise. -0.05: η is a hyperparameter; -0.05: "
        "scalar feedback assumption."
    ),
    tpo_excels_on_sparse_reward: (
        0.85,
        "Token reversal qualitative 'solve vs not-learn' gap; replicated "
        "on neural bandit and sequence tasks. -0.08: PG baselines may be "
        "undertuned; -0.07: single-step only."
    ),
    tpo_matches_on_dense_reward: (
        0.82,
        "MNIST bandit + WebArena-Turbo show TPO ≈ PG on dense tasks. "
        "-0.10: WebArena-Turbo is a simplified split; -0.08: 7B scale only."
    ),
    tpo_simplicity_advantage: (
        0.88,
        "No critic / value / GAE / off-policy correction follows from the "
        "decoupled formulation — an engineering fact, not an empirical claim."
    ),
    bandit_and_single_task: (
        0.93,
        "Documented experimental scope; factual."
    ),
    no_rlhf_comparison: (
        0.95,
        "Paper's explicit scoping choice."
    ),
    weak_pg_baselines_undertuned: (
        0.85,
        "A factual observation about the baselines' tuning state."
    ),
    weak_no_multistep: (
        0.95,
        "Documented scope limit."
    ),
    bdry_online_rl_only: (
        0.97,
        "Stated explicitly in the paper."
    ),
    bdry_7b_scale: (
        0.95,
        "Direct reading of the experimental setup."
    ),
}
