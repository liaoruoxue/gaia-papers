"""Layer 2 strategies — TPO (2604.06159)"""

from gaia.lang import support, induction, abduction, contradiction
from 2604_06159.motivation import (
    tpo_decouples_rl, tpo_excels_on_sparse_reward,
    tpo_matches_on_dense_reward, tpo_simplicity_advantage,
    bandit_and_single_task,
)

strat_decouple_enables_sparse = support(
    [tpo_decouples_rl],
    tpo_excels_on_sparse_reward,
    reason=(
        "The decoupling is the mechanism: PG methods fail on sparse reward "
        "because the gradient is a product of policy gradient and reward — "
        "zero reward → zero gradient. TPO's target distribution q incorporates "
        "all feedback (including zero-reward trajectories) and the cross-entropy "
        "fit provides a dense learning signal. Decoupling breaks the dependency "
        "between reward density and learning signal. The sparse-reward result "
        "is not just empirical — it follows from the architecture."
    ),
    prior=0.88,
)

strat_sparse_generalization = induction(
    [
        "claim_fig1_sparse_outperform",  # token reversal
        "claim_neural_bandit_sparse",    # neural bandit
        "claim_sequence_sparse",         # sequence task
    ],
    tpo_excels_on_sparse_reward,
    reason=(
        "TPO's sparse-reward advantage generalizes across three task types: "
        "token reversal (symbolic), neural bandit (statistical), and sequence "
        "tasks (temporal). This covers the main sparse-reward regimes. "
        "Gap: no compositional multi-step tasks tested."
    ),
    prior=0.82,
)

alt_critic_could_work = claim(
    "Critic-based methods with better exploration (e.g., RND, curiosity) "
    "might match TPO on sparse rewards if the critic can learn a dense "
    "pseudo-reward. TPO's advantage may reflect under-tuned PG baselines "
    "rather than a fundamental architectural superiority.",
    title="Alternative: better PG tuning may close the gap",
)

strat_tpo_abduction = abduction(
    tpo_excels_on_sparse_reward,
    [tpo_decouples_rl, alt_critic_could_work],
    reason=(
        "TPO's mechanism-based explanation (decoupling → dense learning signal) "
        "is more parsimonious than the alternative (PG methods need better "
        "tuning) because: (1) the gap is solve-vs-not-learn, not a small delta, "
        "(2) the same PG methods work well on dense tasks (Fig 1a), confirming "
        "implementations are correct, (3) TPO has fewer hyperparameters to tune. "
        "However, the PG baselines used default hyperparameters — a dedicated "
        "PG tuning study on sparse tasks hasn't been done."
    ),
    prior=0.75,
)

strat_dense_match = support(
    [tpo_decouples_rl],
    tpo_matches_on_dense_reward,
    reason=(
        "The dense-reward result is the complement to the sparse-reward result: "
        "TPO doesn't sacrifice anything to gain sparse-reward robustness. "
        "This is a 'no-regret' property — TPO is at least as good as PG methods "
        "everywhere, and decisively better in the sparse regime."
    ),
    prior=0.85,
)
