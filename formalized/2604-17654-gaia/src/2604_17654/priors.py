"""
Prior assignments for independent (leaf) claims in the Poly-EPO knowledge package.

These priors reflect the epistemological status of each independent premise:
- Well-established empirical findings from prior literature get high priors (0.85-0.92)
- Mathematical definitions and formal constructs get high priors (0.90-0.95)
- Algorithmic claims that are the paper's own contributions start at moderate priors (0.75-0.85)
"""

from . import (
    rl_diversity_collapse,
    standard_rl_limitation,
    reward_shaping_limitation,
    set_rl_definition,
    set_rl_gradient,
    policy_gradient_identity,
    combinatorial_set_construction,
    set_advantage_definition,
    marginal_set_advantage,
    polychromic_objective_def,
    diversity_function_def,
    standard_rl_logit_shift,
)

PRIORS = {
    rl_diversity_collapse: (
        0.88,
        "Well-documented empirical phenomenon with multiple confirming papers (YCL+25, CZC+25). "
        "The observation that RL fine-tuning collapses generation diversity has strong empirical "
        "support across different base models and tasks.",
    ),
    standard_rl_limitation: (
        0.92,
        "Follows directly from the design of PPO and GRPO: neither algorithm contains an explicit "
        "diversity or exploration term in its objective. The claim is essentially definitional — "
        "these algorithms optimize per-generation advantage without set-level coupling.",
    ),
    reward_shaping_limitation: (
        0.85,
        "Well-known limitation of additive reward shaping: the lambda weighting creates a linear "
        "tradeoff rather than synergy, and requires tuning. Supported by the theoretical analysis "
        "in Section 5.2 of the paper showing the threshold p/lambda becomes unsatisfiable.",
    ),
    set_rl_definition: (
        0.95,
        "Mathematical definition from Hamid et al. [HOX+26]. The definition is formally precise "
        "and the irreducibility condition is carefully stated. High prior as it is a definitional "
        "claim about the set RL framework.",
    ),
    set_rl_gradient: (
        0.93,
        "The set RL policy gradient follows from applying the score-function identity to the joint "
        "density. Standard result in policy gradient theory. The constraint on admissible baselines "
        "follows from the requirement that the baseline be independent of the sampled set.",
    ),
    policy_gradient_identity: (
        0.99,
        "The REINFORCE/score-function identity is a foundational result in stochastic optimization "
        "with decades of theoretical backing. Essentially a mathematical identity.",
    ),
    combinatorial_set_construction: (
        0.92,
        "The combinatorial construction of subsets from i.i.d. samples is a well-defined procedure. "
        "The claim accurately describes the algorithm's set construction step.",
    ),
    set_advantage_definition: (
        0.95,
        "Definition of the set advantage as deviation from mean baseline — a direct instantiation "
        "of the standard RL advantage concept applied at the set level.",
    ),
    marginal_set_advantage: (
        0.90,
        "The marginal set advantage is defined as the sum of set advantages over all sets "
        "containing a given generation. This is a design choice whose correctness is established "
        "by Proposition 3.1 (unbiasedness). Moderate-high prior since it is a novel construct.",
    ),
    polychromic_objective_def: (
        0.92,
        "The polychromic objective (product of average reward and diversity) is adapted from "
        "Hamid et al. [HOX+26]. The definition is formally clear and the multiplicative structure "
        "for enforcing joint optimization of both goals is mathematically sound.",
    ),
    diversity_function_def: (
        0.88,
        "The cluster-based diversity function using an LM-judge is a design choice. While the "
        "mathematical formulation is clear, the effectiveness depends on judge quality. "
        "Slightly lower prior due to potential judge noise in cluster assignments.",
    ),
    standard_rl_logit_shift: (
        0.92,
        "Result from Cui et al. [CZC+25] on logit shifts for softmax policies after one gradient "
        "step. Established analytical result that the paper cites and builds upon.",
    ),
}
