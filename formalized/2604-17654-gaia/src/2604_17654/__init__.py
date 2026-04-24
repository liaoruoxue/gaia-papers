"""
Poly-EPO: Training Exploratory Reasoning Models.

Orney, Hamid, Ramanujam, Wu, Hu, Goodman, Sadigh, Finn. arXiv:2604.17654. 2026.

This package formalizes the Poly-EPO paper's knowledge structure: motivation for
exploration in LM post-training, the set reinforcement learning framework, the
scalable recipe for set RL on language models, the Polychromic Exploratory Policy
Optimization (Poly-EPO) algorithm, its theoretical analysis, and experimental results
on mathematical reasoning and synthetic domains.
"""

from .motivation import (
    rl_diversity_collapse,
    exploration_roles,
    standard_rl_limitation,
    reward_shaping_limitation,
    desideratum_optimism,
    desideratum_synergy,
    desideratum_scalability,
    rq_exploration,
    set_rl_scalable,
    poly_epo_claim,
)

from .s2_preliminaries import (
    standard_rl_objective,
    policy_gradient_identity,
    set_rl_definition,
    set_rl_irreducibility,
    set_rl_gradient,
    set_rl_practical_challenge,
)

from .s3_set_rl_recipe import (
    combinatorial_set_construction,
    set_advantage_definition,
    marginal_set_advantage,
    gradient_estimator,
    proposition_unbiasedness,
    recipe_scalable,
)

from .s4_poly_epo import (
    polychromic_objective_def,
    diversity_function_def,
    lm_judge_design,
    poly_epo_algorithm,
    poly_epo_optimism,
    poly_epo_synergy,
)

from .s5_analysis import (
    standard_rl_logit_shift,
    set_rl_logit_shift,
    marginal_advantage_interpretation,
    pass_at_n_analysis,
    polychromic_advantage_decomposition,
)

from .s6_experiments import (
    pass_at_k_result,
    pass_at_k_grpo_degradation,
    training_diversity_result,
    training_coverage_result,
    branching_result,
    majority_vote_result,
    synthetic_diversity_result,
)

__all__ = [
    # Motivation
    "rl_diversity_collapse",
    "exploration_roles",
    "standard_rl_limitation",
    "reward_shaping_limitation",
    "desideratum_optimism",
    "desideratum_synergy",
    "desideratum_scalability",
    "rq_exploration",
    "set_rl_scalable",
    "poly_epo_claim",
    # Preliminaries
    "standard_rl_objective",
    "policy_gradient_identity",
    "set_rl_definition",
    "set_rl_irreducibility",
    "set_rl_gradient",
    "set_rl_practical_challenge",
    # Set RL Recipe
    "combinatorial_set_construction",
    "set_advantage_definition",
    "marginal_set_advantage",
    "gradient_estimator",
    "proposition_unbiasedness",
    "recipe_scalable",
    # Poly-EPO
    "polychromic_objective_def",
    "diversity_function_def",
    "lm_judge_design",
    "poly_epo_algorithm",
    "poly_epo_optimism",
    "poly_epo_synergy",
    # Analysis
    "standard_rl_logit_shift",
    "set_rl_logit_shift",
    "marginal_advantage_interpretation",
    "pass_at_n_analysis",
    "polychromic_advantage_decomposition",
    # Experiments
    "pass_at_k_result",
    "pass_at_k_grpo_degradation",
    "training_diversity_result",
    "training_coverage_result",
    "branching_result",
    "majority_vote_result",
    "synthetic_diversity_result",
]
