"""
Section 3: Optimizing Language Models with Set RL.

General scalable recipe: sample N generations, construct K subsets of size n,
compute marginal set advantage per generation, use as drop-in replacement for
standard advantage in any RL algorithm.
"""

from gaia.lang import claim, setting, support, deduction
from .s2_preliminaries import (
    set_rl_definition,
    set_rl_gradient,
    set_rl_practical_challenge,
    policy_gradient_identity,
)

# ──────────────────────────────────────────────────────────────────────
# Core algorithmic constructs
# ──────────────────────────────────────────────────────────────────────

combinatorial_set_construction = claim(
    "Scalable set construction: For a fixed prompt $x$, sample $N$ i.i.d. generations "
    "$y_1,\\ldots,y_N \\sim \\pi_\\theta(\\cdot|x)$ with $N > n$. Construct $K$ sets of size $n$ "
    "from these $N$ generations without replacement:\n\n"
    "$$G_j = \\{y_{(j_1)},\\ldots,y_{(j_n)}\\}, \\quad j_1 < \\cdots < j_n, "
    "\\{j_1,\\ldots,j_n\\} \\subseteq \\{1,\\ldots,N\\}$$\n\n"
    "Either enumerate all $\\binom{N}{n}$ sets (reduces gradient variance) or sample $K$ sets "
    "uniformly without replacement (when evaluating $f$ is expensive) [@OrneHamid2026].",
    title="Combinatorial set construction",
)

set_advantage_definition = claim(
    "Set advantage function: Given set-level baseline $\\hat{f}(x) = \\frac{1}{K}\\sum_{j=1}^K f(x,G_j)$ "
    "(average score over all constructed sets), the set advantage of set $G_j$ is:\n\n"
    "$$A^\\sharp(x, G_j; f) = f(x, G_j) - \\hat{f}(x)$$\n\n"
    "[@OrneHamid2026]",
    title="Set advantage",
)

marginal_set_advantage = claim(
    "Marginal set advantage of a single generation $y$: Let $\\mathcal{G}(y)$ be the collection of "
    "all constructed sets containing $y$. The marginal set advantage is:\n\n"
    "$$\\widehat{A^\\sharp_{\\text{marg}}}(x,y;f) = \\sum_{G \\in \\mathcal{G}(y)} A^\\sharp(x,G;f)$$\n\n"
    "Intuitively, this is the sum of advantages of all sets that contain generation $y$. "
    "It provides an advantage at the level of a single generation, enabling use of standard RL "
    "update rules [@OrneHamid2026].",
    title="Marginal set advantage",
)

gradient_estimator = claim(
    "Final set RL gradient estimator using marginal set advantage:\n\n"
    "$$\\widehat{\\nabla_\\theta} \\mathbb{E}_{y_{1:n} \\sim \\pi_\\theta}[f(x,y_{1:n})] = "
    "\\widehat{\\mathbb{E}}_{x \\sim \\mathcal{D},\\, y_1,\\ldots,y_N \\sim \\pi_\\theta(\\cdot|x)}"
    "\\!\\left[\\sum_{i=1}^N \\nabla_\\theta \\log \\pi_\\theta(y_i|x) "
    "\\cdot \\widehat{A^\\sharp_{\\text{marg}}}(x,y_i;f)\\right]$$\n\n"
    "This estimator is unbiased (up to a constant scaling factor $M > 0$) for both the "
    "enumerate-all-sets and uniform-sample-$K$-sets variants [@OrneHamid2026].",
    title="Set RL gradient estimator",
)

# ──────────────────────────────────────────────────────────────────────
# Key theoretical result
# ──────────────────────────────────────────────────────────────────────

proposition_unbiasedness = claim(
    "Proposition 3.1 (Unbiasedness): Fix a prompt $x$ and let $y_1,\\ldots,y_N "
    "\\stackrel{\\text{i.i.d.}}{\\sim} \\pi_\\theta(\\cdot|x)$. Then:\n\n"
    "$$\\mathbb{E}\\!\\left[\\sum_{i=1}^N \\nabla_\\theta \\log \\pi_\\theta(y_i|x) "
    "\\widehat{A^\\sharp_{\\text{marg}}}(x,y_i;f)\\right] = "
    "M \\nabla_\\theta \\mathbb{E}_{y_{1:n} \\sim \\pi_\\theta}[f(x,y_{1:n})]$$\n\n"
    "where $M \\in \\mathbb{R}_{>0}$ is a constant scaling factor depending on the number of sets. "
    "The proof uses the U-statistic structure of the estimator, with the scaling factor "
    "$M = \\binom{N}{n} - \\binom{N-1}{n-1} > 0$ for the enumerate-all-sets case (by Pascal's rule, "
    "since $N > n$) [@OrneHamid2026].",
    title="Unbiasedness of marginal set advantage estimator",
)

recipe_scalable = claim(
    "The scalable set RL recipe resolves the computational challenge of naive set RL: "
    "by computing the marginal set advantage, any standard RL algorithm (e.g., PPO [@SWD17], "
    "GRPO [@SWZ24]) can be adapted for set RL by simply replacing the standard per-generation "
    "advantage $A(x,y_i)$ with the marginal set advantage $\\widehat{A^\\sharp_{\\text{marg}}}(x,y_i;f)$. "
    "The sample complexity matches standard RL (same $N$ generations per prompt) "
    "[@OrneHamid2026].",
    title="Recipe scalability",
)

# ──────────────────────────────────────────────────────────────────────
# Reasoning connections
# ──────────────────────────────────────────────────────────────────────

strat_unbiasedness = support(
    [combinatorial_set_construction, set_advantage_definition, marginal_set_advantage,
     policy_gradient_identity],
    proposition_unbiasedness,
    reason=(
        "The estimator's unbiasedness follows from U-statistic theory. Constructing sets "
        "combinatorially from $N$ i.i.d. samples (@combinatorial_set_construction) causes the "
        "estimator to be a U-statistic estimator of the set RL gradient (@set_rl_gradient). "
        "The marginal set advantage (@marginal_set_advantage) sums set advantages over all sets "
        "containing a generation. After algebraic expansion using the score-function identity "
        "(@policy_gradient_identity) and the symmetry of the set objective, the expectation "
        "telescopes to $M \\nabla_\\theta \\mathbb{E}_{y_{1:n}}[f]$ where $M = \\binom{N}{n} - "
        "\\binom{N-1}{n-1} > 0$ by Pascal's rule. The same argument applies to the uniform "
        "sampling case with a different but still positive scaling factor $M$."
    ),
    prior=0.92,
)

strat_recipe_solves_challenge = support(
    [proposition_unbiasedness, combinatorial_set_construction, marginal_set_advantage],
    recipe_scalable,
    reason=(
        "The unbiasedness result (@proposition_unbiasedness) ensures correctness. The combinatorial "
        "construction (@combinatorial_set_construction) reuses the same $N$ i.i.d. samples "
        "already drawn for standard RL — no additional rollouts are needed. The marginal set "
        "advantage (@marginal_set_advantage) provides a per-generation scalar that plugs directly "
        "into existing RL algorithm infrastructure, satisfying the scalability desideratum. "
        "This directly resolves the practical challenge identified in @set_rl_practical_challenge."
    ),
    prior=0.9,
)

__all__ = [
    "combinatorial_set_construction",
    "set_advantage_definition",
    "marginal_set_advantage",
    "gradient_estimator",
    "proposition_unbiasedness",
    "recipe_scalable",
]
