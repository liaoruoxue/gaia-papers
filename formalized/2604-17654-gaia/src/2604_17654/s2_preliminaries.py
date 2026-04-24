"""
Section 2: Preliminaries — Standard RL and Set RL Frameworks.

Establishes the mathematical foundations for standard single-turn LM RL and the
set reinforcement learning (set RL) framework from Hamid et al. [@HOX26].
"""

from gaia.lang import claim, setting, support, deduction

# ──────────────────────────────────────────────────────────────────────
# Standard RL
# ──────────────────────────────────────────────────────────────────────

standard_rl_objective = claim(
    "Standard reinforcement learning (RL) for language models (RLVR setting): "
    "Let $x \\sim \\mathcal{D}$ be a prompt drawn from training distribution $\\mathcal{D}$, "
    "and let $y \\sim \\pi_\\theta(\\cdot | x)$ be a sampled generation from the parameterized policy. "
    "The standard RL objective is:\n\n"
    "$$\\max_\\theta \\mathbb{E}_{x \\sim \\mathcal{D}} \\mathbb{E}_{y \\sim \\pi_\\theta(\\cdot|x)}[r(x,y)]$$\n\n"
    "where $r(x,y)$ is the task reward. The policy gradient with advantage $A(x,y)$ is:\n\n"
    "$$\\nabla_\\theta \\mathbb{E}[r(x,y)] = \\mathbb{E}[\\nabla_\\theta \\log \\pi_\\theta(y|x) A(x,y)]$$\n\n"
    "[@SB18; @OrneHamid2026]",
    title="Standard RL objective (RLVR)",
)

policy_gradient_identity = claim(
    "Score-function (REINFORCE) policy gradient identity: For any differentiable objective "
    "$\\mathbb{E}_{y \\sim \\pi_\\theta}[f(y)]$, the gradient is "
    "$\\mathbb{E}_y[\\nabla_\\theta \\log \\pi_\\theta(y) \\cdot f(y)]$. "
    "This allows Monte Carlo estimation via sampled trajectories [@SB18].",
    title="Score-function identity",
)

# ──────────────────────────────────────────────────────────────────────
# Set RL Framework
# ──────────────────────────────────────────────────────────────────────

set_rl_definition = claim(
    "Set reinforcement learning (set RL) [@HOX26] is a framework that generalizes standard RL "
    "by assigning reward to **sets** of sampled generations rather than each independently. "
    "In the single-turn LM setting: draw $n$ i.i.d. generations $y_{1:n} = (y_1,\\ldots,y_n) "
    "\\stackrel{\\text{i.i.d.}}{\\sim} \\pi_\\theta(\\cdot|x)$, and let $f(x, y_{1:n})$ be a "
    "symmetric set-level objective. The set RL goal is:\n\n"
    "$$\\max_\\theta \\mathbb{E}_{x \\sim \\mathcal{D}} \\mathbb{E}_{y_{1:n} \\sim \\pi_\\theta(\\cdot|x)}"
    "[f(x,y_{1:n})]$$\n\n"
    "The key constraint is that $\\mathbb{E}_{y_{1:n}}[f(x,y_{1:n})]$ **cannot** be written as "
    "$\\mathbb{E}_y[g(x,y)]$ for any policy-independent $g$, distinguishing set RL from standard RL "
    "[@HOX26; @OrneHamid2026].",
    title="Set RL definition",
)

set_rl_irreducibility = claim(
    "The set RL objective is irreducible to standard RL: although one can always define "
    "$g_\\theta(x,y) = \\mathbb{E}_{y_{2:n}}[f(x,y,y_{2:n})]$, the resulting induced reward $g_\\theta$ "
    "depends on the policy $\\theta$ itself and is not an externally specified policy-independent "
    "reward function. This distinguishes set RL from multi-sample frameworks that use leave-one-out "
    "estimators to collapse the shared learning signal to an individualized one [@OrneHamid2026].",
    title="Set RL irreducibility",
)

set_rl_gradient = claim(
    "Set RL policy gradient (derived via score-function identity applied to the joint density "
    "$\\prod_{i=1}^n \\pi_\\theta(y_i|x)$):\n\n"
    "$$\\nabla_\\theta \\mathbb{E}_{y_{1:n}}[f(x,y_{1:n})] = "
    "\\mathbb{E}_{y_{1:n}}\\!\\left[(f(x,y_{1:n}) - \\hat{f}(x)) "
    "\\sum_{i=1}^n \\nabla_\\theta \\log \\pi_\\theta(y_i|x)\\right]$$\n\n"
    "where $\\hat{f}(x)$ is a **set-level baseline** that must be independent of $y_{1:n}$ or "
    "any strict subset thereof (leave-one-out estimators are inadmissible baselines). "
    "All generations in the set share the same scalar learning signal $f(x,y_{1:n}) - \\hat{f}(x)$ "
    "[@OrneHamid2026].",
    title="Set RL policy gradient",
)

set_rl_practical_challenge = claim(
    "The main practical challenge of the set RL gradient estimator is statistical and computational: "
    "a naive empirical estimator requires repeatedly sampling full sets of size $n$ for each prompt, "
    "which is expensive in sample complexity. A more efficient estimator is needed that retains the "
    "set-RL learning signal while being practical for large-scale LM training [@OrneHamid2026].",
    title="Set RL computational challenge",
)

# ──────────────────────────────────────────────────────────────────────
# Reasoning connections
# ──────────────────────────────────────────────────────────────────────

strat_irreducibility = deduction(
    [set_rl_definition],
    set_rl_irreducibility,
    reason=(
        "By @set_rl_definition, the defining constraint of set RL is that the expected set objective "
        "cannot be rewritten as an expectation over a policy-independent per-generation reward. "
        "While $g_\\theta(x,y) = \\mathbb{E}_{y_{2:n}}[f(x,y,y_{2:n})]$ satisfies "
        "$\\mathbb{E}_{y_{1:n}}[f] = \\mathbb{E}_y[g_\\theta(x,y)]$, the key point is that "
        "$g_\\theta$ depends on the policy — making it structurally different from standard RL "
        "where rewards are externally specified and policy-independent. This follows by definition."
    ),
    prior=0.99,
)

strat_practical_challenge = support(
    [set_rl_gradient],
    set_rl_practical_challenge,
    reason=(
        "The set RL gradient (@set_rl_gradient) requires evaluating the set objective $f$ on multiple "
        "complete sets of size $n$ per prompt to estimate both the set reward and the set-level "
        "baseline with low variance. The number of distinct sets of size $n$ from $N$ generations is "
        "$\\binom{N}{n}$, which grows combinatorially — making naive estimation computationally "
        "prohibitive at scale."
    ),
    prior=0.95,
)

__all__ = [
    "standard_rl_objective",
    "policy_gradient_identity",
    "set_rl_definition",
    "set_rl_irreducibility",
    "set_rl_gradient",
    "set_rl_practical_challenge",
]
