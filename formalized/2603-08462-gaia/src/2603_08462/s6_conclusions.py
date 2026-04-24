"""Section 6: Conclusions and Limitations"""

from gaia.lang import claim, setting, support

from .s3_methodology import (
    cib_resolves_paradox,
    rl_objective_formulation,
    semantic_cost_advantage,
)
from .s4_theory import cib_unifies_budget_forcing
from .s5_experiments import (
    cib_pareto_dominates_l1,
    larger_prior_more_compression,
    info_density_result,
)

# --- Conclusion claims ---

cib_principled_framework = claim(
    "The Conditional Information Bottleneck (CIB) framework provides a principled "
    "information-theoretic foundation for efficient LLM reasoning by: "
    "(1) identifying the Attention Paradox that invalidates standard IB for transformers, "
    "(2) deriving a semantically-grounded RL objective from CIB principles, "
    "(3) unifying existing budget-forcing methods as special cases with degenerate priors, "
    "and (4) empirically demonstrating Pareto improvements over token-count baselines "
    "across five math benchmarks.",
    title="CIB provides principled, theoretically-grounded efficient reasoning framework",
    metadata={"source_section": "Section 6"},
)

strat_cib_principled = support(
    [cib_resolves_paradox, cib_unifies_budget_forcing, cib_pareto_dominates_l1],
    cib_principled_framework,
    reason=(
        "@cib_resolves_paradox establishes the theoretical correctness of CIB for transformers. "
        "@cib_unifies_budget_forcing shows it subsumes prior methods. "
        "@cib_pareto_dominates_l1 demonstrates empirical superiority. Together, these three "
        "lines of evidence support the claim that CIB is a principled and effective framework."
    ),
    prior=0.88,
)

# --- Limitation claims ---

accuracy_degradation_at_scale = claim(
    "CIB accuracy degrades slightly (≤1.4 percentage points) when scaling the prior model "
    "from 1.5B to 7B parameters without re-tuning the $\\beta$ hyperparameter. This indicates "
    "that $\\beta$ values are not transferable across prior model sizes and must be re-calibrated "
    "when using a different prior.",
    title="Limitation: accuracy degradation without hyperparameter re-tuning across prior scales",
    metadata={"source_section": "Section 6, Limitations"},
)

strat_accuracy_degradation = support(
    [larger_prior_more_compression],
    accuracy_degradation_at_scale,
    reason=(
        "@larger_prior_more_compression shows that the 7B prior achieves 41% compression "
        "but with −0.7pp accuracy drop on DeepScaleR. The −1.3pp accuracy drop on DLER-7B "
        "with the 7B prior at $\\beta^+$ suggests the $\\beta$ value tuned for the smaller "
        "prior leads to over-compression with the larger prior, as the 7B model assigns "
        "higher surprisal to more tokens, amplifying the compression pressure beyond the "
        "tuned level."
    ),
    prior=0.85,
)

no_inference_overhead = claim(
    "CIB training requires a frozen base language model $Q_\\phi$ during training but does not "
    "add any overhead at inference time. The trained policy $\\pi_\\theta$ generates compressed "
    "reasoning traces autonomously without needing to query $Q_\\phi$.",
    title="CIB adds no inference-time overhead",
    metadata={"source_section": "Section 6"},
)

strat_no_overhead = support(
    [rl_objective_formulation],
    no_inference_overhead,
    reason=(
        "In the CIB RL training objective (@rl_objective_formulation), $Q_\\phi$ is frozen and "
        "used only to compute the reward $r_{\\text{min}}$ during training rollouts. Once training "
        "is complete, the policy $\\pi_\\theta$ has internalized the compression behavior and "
        "generates shorter traces directly without any reference to $Q_\\phi$ at inference time."
    ),
    prior=0.95,
)

framework_generality = claim(
    "The CIB framework is general and instantiable with different verifiers $Q_\\rho$ and "
    "priors $Q_\\phi$ for task-specific optimization. While demonstrated on mathematical "
    "reasoning with binary correctness verifiers, the objective $R(X,Y,Z) = r_{\\text{acc}} + "
    "\\beta r_{\\text{min}}$ can accommodate other domains with appropriate verifier designs.",
    title="CIB is general: adaptable to different verifiers and priors",
    metadata={"source_section": "Section 6"},
)

strat_framework_generality = support(
    [rl_objective_formulation],
    framework_generality,
    reason=(
        "The CIB RL objective (@rl_objective_formulation) is parameterized by: (1) the verifier "
        "$Q_\\rho$ used to compute $r_{\\text{acc}}$, and (2) the prior $Q_\\phi$ used to compute "
        "$r_{\\text{min}}$. Both components are modular — the verifier can be any function "
        "returning task reward signals, and the prior can be any language model. This modularity "
        "makes the framework applicable beyond mathematical reasoning to any domain with a "
        "verifiable reward signal."
    ),
    prior=0.90,
)
