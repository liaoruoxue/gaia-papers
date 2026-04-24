"""
Section 4: Polychromic Exploratory Policy Optimization (Poly-EPO).

Instantiates the general set RL recipe with the polychromic objective
(product of average reward and diversity), using an LM-judge for clustering.
"""

from gaia.lang import claim, setting, support, deduction
from .s3_set_rl_recipe import (
    recipe_scalable,
    marginal_set_advantage,
    combinatorial_set_construction,
)
from .motivation import desideratum_optimism, desideratum_synergy, desideratum_scalability

# ──────────────────────────────────────────────────────────────────────
# Polychromic objective
# ──────────────────────────────────────────────────────────────────────

polychromic_objective_def = claim(
    "Polychromic objective (adapted from [@HOX26] to the LM reasoning setting): "
    "Given a prompt $x$ and a set of $n$ generations $y_1,\\ldots,y_n$, the polychromic "
    "objective is:\n\n"
    "$$f_{\\text{poly}}(x, y_1,\\ldots,y_n) = \\frac{1}{n}\\sum_{i=1}^n r(x,y_i) \\cdot "
    "d(x, y_1,\\ldots,y_n)$$\n\n"
    "where $r(x,y_i)$ is the task reward for generation $y_i$, and $d(x,y_{1:n})$ is a "
    "diversity function. The objective is the product of average reward (exploitation) and "
    "diversity (exploration), so the set must optimize both simultaneously and cannot ignore "
    "one for the other [@OrneHamid2026].",
    title="Polychromic objective",
)

diversity_function_def = claim(
    "Diversity function: An LM-judge (language model judge) clusters all $N$ generations "
    "$y_1,\\ldots,y_N$ for prompt $x$ according to semantic similarity of reasoning strategies. "
    "Let $\\mathcal{C}(y_i) \\in \\{1,\\ldots,N\\}$ be the cluster assignment of generation $y_i$. "
    "The diversity of a set $(y_1,\\ldots,y_n)$ is the fraction of distinct clusters:\n\n"
    "$$d(x, y_{1:n}) = \\frac{|\\{\\mathcal{C}(y_1),\\ldots,\\mathcal{C}(y_n)\\}|}{n} \\in [0,1]$$\n\n"
    "A special cluster index 100 (out-of-bounds) is reserved for degenerate generations "
    "(gibberish, random guesses, code without mathematical reasoning). "
    "Cluster-100 assignments are excluded from diversity numerator. "
    "A set receives diversity score 0 if all generations fall in the same cluster "
    "[@OrneHamid2026].",
    title="LM-judge diversity function",
)

lm_judge_design = claim(
    "The LM-judge-based diversity measurement is: (1) computationally efficient — clustering "
    "is substantially easier than solving the original task, exploiting the generator-verifier gap; "
    "(2) broadly applicable — LM-judges are already integrated into modern post-training pipelines "
    "including proof generation and non-verifiable tasks; (3) strategy-centric — the judge is "
    "steered via in-context learning to cluster on macro-strategy (overall conceptual framework) "
    "and micro-strategy (specific techniques at key intermediate steps), not on superficial "
    "features like tone or phrasing [@OrneHamid2026].",
    title="LM-judge design rationale",
)

poly_epo_algorithm = claim(
    "Poly-EPO algorithm: Instantiate the general set RL recipe (Algorithm 1) with the "
    "polychromic objective. For each prompt $x$, sample $N = 8$ generations; construct "
    "$K = 70$ sets of size $n = 4$ using uniform sampling without replacement; cluster "
    "all $N$ generations using the LM-judge (Qwen-3-4B-Instruct); compute polychromic "
    "score for each set as: $f_{\\text{poly}}(x, G_l) = \\bar{r}_l \\cdot \\frac{|U_l|}{n} "
    "\\cdot \\mathbb{I}(|U_l| > 1)$ where $\\bar{r}_l$ is mean reward and $U_l$ is the set "
    "of distinct clusters. The marginal set advantage replaces the standard advantage in "
    "the GRPO update. Each generation within a response receives the same advantage "
    "(token-level), and response lengths are normalized using $T_i = T_{\\max}$ (max response "
    "length), following Dr.GRPO [@LCL25] [@OrneHamid2026].",
    title="Poly-EPO algorithm",
)

poly_epo_optimism = claim(
    "Under the polychromic objective in set RL, an unsuccessful generation ($r(x,y) = 0$) "
    "can still receive a positive marginal set advantage if it is highly exploratory: because "
    "the set objective shares credit among all generations in a set, an incorrect but diverse "
    "generation benefits from the presence of correct generations in the same set. "
    "This implements optimistic exploration: novel strategies receive positive learning signal "
    "even before they become individually successful [@OrneHamid2026].",
    title="Poly-EPO optimistic exploration",
)

poly_epo_synergy = claim(
    "Under reward-shaped standard RL (objective $\\mathbb{E}_y[r(x,y) + \\lambda d(x,y)]$), "
    "an incorrect generation ($r(x,y)=0$) with high diversity receives positive advantage only "
    "if $d(x,y) \\geq \\frac{p}{\\lambda} + \\mathbb{E}_Y[d(x,Y)]$, where $p$ is the model's "
    "accuracy. As accuracy improves ($p$ increases), this threshold becomes harder to satisfy — "
    "e.g., with $\\lambda=0.5$ and $p > 0.5$, the bound is impossible to satisfy. "
    "In contrast, Poly-EPO's incentive for exploration does not vanish as accuracy improves, "
    "since set credit sharing persists regardless of $p$ [@OrneHamid2026].",
    title="Poly-EPO vs reward shaping",
)

# ──────────────────────────────────────────────────────────────────────
# Reasoning connections
# ──────────────────────────────────────────────────────────────────────

strat_lm_judge_rationale = support(
    [diversity_function_def],
    lm_judge_design,
    reason=(
        "The cluster-based diversity measure (@diversity_function_def) inherits all three "
        "properties: computational efficiency comes from the generator-verifier gap (clustering "
        "is easier than solving); breadth across domains from LM-judges' instruction-following "
        "capability; strategy-centricity from the rubric that distinguishes macro- and "
        "micro-strategy while ignoring surface features. The few-shot examples in the judge "
        "prompt explicitly demonstrate invariance to arithmetic errors and tone."
    ),
    prior=0.85,
)

strat_poly_epo_instantiation = deduction(
    [recipe_scalable, polychromic_objective_def, diversity_function_def],
    poly_epo_algorithm,
    reason=(
        "Poly-EPO is a direct instantiation of the general set RL recipe (@recipe_scalable) "
        "with the polychromic objective (@polychromic_objective_def). The diversity function "
        "(@diversity_function_def) is evaluated via LM-judge clustering. The algorithm "
        "inherits the recipe's scalability: same $N$ generations as standard RL, marginal "
        "set advantage computed via Algorithm 2 and plugged into the GRPO update rule "
        "(@marginal_set_advantage). All design choices (cluster-100, $T_i = T_{\\max}$) "
        "follow directly from the definitions."
    ),
    prior=0.98,
)

strat_optimism = support(
    [polychromic_objective_def, marginal_set_advantage],
    poly_epo_optimism,
    reason=(
        "In the polychromic objective (@polychromic_objective_def), the set score is a "
        "product of average reward and diversity. The marginal set advantage "
        "(@marginal_set_advantage) sums set advantages over sets containing a given generation. "
        "Even if a generation has $r(x,y) = 0$, the sets it belongs to can still have high "
        "polychromic scores (via other high-reward, diverse generators in those sets), giving "
        "the generation a positive marginal set advantage. This is the formal mechanism for "
        "optimistic exploration — encoded in Term 1 of the marginal advantage decomposition "
        "(Eq. 15 of the paper)."
    ),
    prior=0.9,
)

strat_vs_reward_shaping = support(
    [polychromic_objective_def, poly_epo_optimism],
    poly_epo_synergy,
    reason=(
        "Under reward-shaped RL (separate $r + \\lambda d$ objective), the advantage for a "
        "generation is $r(x,y) - \\mathbb{E}_Y[r] + \\lambda(d(x,y) - \\mathbb{E}_Y[d])$. "
        "For $r(x,y)=0$, positivity requires $d(x,y) \\geq p/\\lambda + \\mathbb{E}_Y[d]$. "
        "As $p \\to 1$ (model improves), this bound grows unboundedly for fixed $\\lambda$. "
        "In contrast, Poly-EPO (@poly_epo_optimism) maintains positive learning signal for "
        "exploratory incorrect generations regardless of $p$ via set credit sharing. "
        "Furthermore, the covariance term (Term 2 of Eq. 15) in Poly-EPO — absent in "
        "$r(x,y) \\cdot d(x,y)$ pointwise objectives — explicitly rewards synergistic "
        "exploration-exploitation."
    ),
    prior=0.88,
)

__all__ = [
    "polychromic_objective_def",
    "diversity_function_def",
    "lm_judge_design",
    "poly_epo_algorithm",
    "poly_epo_optimism",
    "poly_epo_synergy",
]
