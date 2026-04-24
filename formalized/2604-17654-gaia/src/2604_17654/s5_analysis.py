"""
Section 5: Analysis — General Recipe and Exploration-Exploitation Synergy.

Section 5.1: Justifies why marginal set advantage enables standard RL to optimize set RL.
Section 5.2: Decomposes the polychromic marginal set advantage to show optimism and synergy.
"""

from gaia.lang import claim, setting, support, deduction
from .s2_preliminaries import standard_rl_objective, set_rl_definition
from .s3_set_rl_recipe import marginal_set_advantage, proposition_unbiasedness
from .s4_poly_epo import polychromic_objective_def, poly_epo_optimism, poly_epo_synergy
from .motivation import desideratum_optimism, desideratum_synergy

# ──────────────────────────────────────────────────────────────────────
# Logit shift analysis (Section 5.1)
# ──────────────────────────────────────────────────────────────────────

standard_rl_logit_shift = claim(
    "Logit shift in standard RL [@CZC25]: After one gradient update with learning rate $\\alpha$ "
    "on a softmax policy $\\pi_\\theta$, the shift in log-probability of generation $y$ is:\n\n"
    "$$\\log \\pi_\\theta^{k+1}(y|x) - \\log \\pi_\\theta^k(y|x) = "
    "\\alpha \\pi_\\theta^k(y|x) A(x,y;\\pi_\\theta^k)$$\n\n"
    "where $A(x,y;\\pi_\\theta^k)$ is the advantage under the current policy.",
    title="Standard RL logit shift",
)

set_rl_logit_shift = claim(
    "Lemma 5.1 — Logit shift in set RL: In set reinforcement learning, assuming $f$ is symmetric "
    "and learning rate $\\alpha$, the shift in log-probability of a fixed generation $y$ after "
    "one gradient update from $\\pi_\\theta^k$ to $\\pi_\\theta^{k+1}$ is:\n\n"
    "$$\\log \\pi_\\theta^{k+1}(y|x) - \\log \\pi_\\theta^k(y|x) = "
    "\\alpha \\pi_\\theta^k(y|x) \\left[\\mathbb{E}_{y_{2:n} \\sim \\pi_\\theta^k}[f(x,y,y_{2:n})] "
    "- \\mathbb{E}_{y_{1:n} \\sim \\pi_\\theta^k}[f(x,y_{1:n})]\\right]$$\n\n"
    "The proof follows from [@HOX26]: when a set is homogeneous, the scaffold value "
    "$\\Lambda_f(y^{\\oplus n};\\pi_\\theta^k,x)$ equals $\\pi_\\theta^k(y|x)$ times the marginal "
    "set advantage of $y$ [@OrneHamid2026].",
    title="Set RL logit shift (Lemma 5.1)",
)

marginal_advantage_interpretation = claim(
    "Comparing the standard RL logit shift (Eq. 12) with the set RL logit shift (Lemma 5.1, Eq. 13), "
    "the marginal set advantage of generation $y$ can be defined as:\n\n"
    "$$A^\\sharp_{\\text{marg}}(x,y;f,\\pi_\\theta^k) = "
    "\\mathbb{E}_{y_{2:n} \\sim \\pi_\\theta^k}[f(x,y,y_{2:n})] - "
    "\\mathbb{E}_{y_{1:n} \\sim \\pi_\\theta^k}[f(x,y_{1:n})]$$\n\n"
    "This shows that the logit shift under set RL is equivalent to that under standard RL "
    "when the standard advantage $A(x,y)$ is replaced by the marginal set advantage. "
    "Therefore, any standard RL algorithm can be used to optimize set RL objectives by "
    "this substitution [@OrneHamid2026].",
    title="Marginal set advantage enables standard RL for set RL",
)

pass_at_n_analysis = claim(
    "Example analysis using pass@$n$ objective $f_{\\text{pass@}n}(x,y_{1:n}) = \\max_{i} r(x,y_i)$: "
    "In set RL with pass@$n$, the marginal set advantage of an incorrect generation ($r(x,y)=0$) "
    "is $A^\\sharp_{\\text{marg}}(x,y_{\\text{incorrect}}) = (1-p)^n - (1-p)^{n-1} \\leq 0$, "
    "where $p$ is the probability of sampling a correct generation. "
    "The marginal set advantage of a correct generation is $(1-p)^n \\geq 0$. "
    "Thus under pass@$n$, incorrect generations always receive non-positive advantage — "
    "no optimistic exploration occurs [@OrneHamid2026].",
    title="Pass@n analysis: no optimistic exploration",
)

# ──────────────────────────────────────────────────────────────────────
# Polychromic advantage decomposition (Section 5.2)
# ──────────────────────────────────────────────────────────────────────

polychromic_advantage_decomposition = claim(
    "Decomposition of the polychromic marginal set advantage (Eq. 15): For fixed generation $y$ "
    "with $\\pi_\\theta(y|x) > 0$:\n\n"
    "$$A^\\sharp_{\\text{marg}}(x,y;f_{\\text{poly}},\\theta)$$\n\n"
    "$$= \\underbrace{\\left(\\frac{1}{n}r(x,y) + \\frac{n-1}{n}\\mathbb{E}_Y[r(x,Y)]\\right) "
    "\\mathbb{E}_{Y_{2:n}}[d(x,y,Y_{2:n})] - \\mathbb{E}_Y[r(x,Y)]\\mathbb{E}_{Y_{1:n}}"
    "[d(x,Y_{1:n})]}_{"
    "\\text{Term 1: Mean reward} \\times \\text{Mean diversity of sets containing }y}$$\n\n"
    "$$+ \\underbrace{\\text{Cov}_{Y_{2:n}}\\!\\left(\\frac{1}{n}r(x,y) + "
    "\\frac{1}{n}\\sum_{i=2}^n r(x,Y_i),\\; d(x,y,Y_{2:n})\\right) - "
    "\\text{Cov}_{Y_{1:n}}(r(x,Y_1), d(x,Y_{1:n}))}_{"
    "\\text{Term 2: Exploration-exploitation synergy in sets containing }y}$$\n\n"
    "Term 1: A generation $y$ with low reward but high diversity can still receive positive "
    "signal if other generators provide both reward and diversity. "
    "Term 2: Favors generations that help sets simultaneously achieve high reward and high "
    "diversity (covariance between reward and diversity is higher in sets containing $y$) "
    "[@OrneHamid2026].",
    title="Polychromic marginal advantage decomposition",
)

# ──────────────────────────────────────────────────────────────────────
# Reasoning connections
# ──────────────────────────────────────────────────────────────────────

strat_set_rl_logit_shift = support(
    [set_rl_definition, proposition_unbiasedness],
    set_rl_logit_shift,
    reason=(
        "The set RL logit shift follows from [@HOX26]'s analysis of scaffold values in set RL. "
        "The scaffold value $\\Lambda_f(y^{\\oplus n};\\pi_\\theta^k,x)$ for a homogeneous set "
        "(all copies of $y$) equals $\\pi_\\theta^k(y|x) \\cdot A^\\sharp_{\\text{marg}}(x,y)$ "
        "under the symmetry of $f$ (@set_rl_definition) and the unbiasedness structure "
        "(@proposition_unbiasedness). Applying the score-function gradient yields Eq. 13."
    ),
    prior=0.88,
)

strat_marginal_enables_standard = deduction(
    [standard_rl_logit_shift, set_rl_logit_shift],
    marginal_advantage_interpretation,
    reason=(
        "By comparing Eq. 12 (standard RL logit shift, @standard_rl_logit_shift) with "
        "Eq. 13 (set RL logit shift, @set_rl_logit_shift), the two expressions have identical "
        "structure: $\\alpha \\pi_\\theta^k(y|x) \\cdot [\\text{advantage term}]$. "
        "Setting $A(x,y) = A^\\sharp_{\\text{marg}}(x,y;f,\\pi_\\theta^k)$ makes the logit "
        "shifts equivalent. This is a deductive consequence of the two equations sharing "
        "the same functional form."
    ),
    prior=0.99,
)

strat_decomposition = support(
    [polychromic_objective_def, marginal_advantage_interpretation],
    polychromic_advantage_decomposition,
    reason=(
        "Substituting the polychromic objective $f_{\\text{poly}} = \\bar{r} \\cdot d$ "
        "(@polychromic_objective_def) into the marginal set advantage formula "
        "(@marginal_advantage_interpretation) and expanding the expectation algebraically "
        "yields the two-term decomposition via the covariance decomposition identity: "
        "$\\mathbb{E}[XY] = \\mathbb{E}[X]\\mathbb{E}[Y] + \\text{Cov}(X,Y)$. "
        "The derivation is a direct algebraic manipulation."
    ),
    prior=0.92,
)

strat_optimism_from_decomp = deduction(
    [polychromic_advantage_decomposition],
    poly_epo_optimism,
    reason=(
        "Term 1 of the polychromic advantage decomposition (@polychromic_advantage_decomposition) "
        "shows that generation $y$'s advantage depends on $\\frac{1}{n}r(x,y)$ (own reward, "
        "weight $1/n$) plus $\\frac{n-1}{n}\\mathbb{E}_Y[r]$ (other generators' reward) times "
        "expected diversity. For $r(x,y) = 0$ but high $\\mathbb{E}_Y[r]$ and high diversity, "
        "Term 1 can be positive. This directly implies @poly_epo_optimism by construction."
    ),
    prior=0.97,
)

strat_synergy_from_decomp = deduction(
    [polychromic_advantage_decomposition],
    poly_epo_synergy,
    reason=(
        "Term 2 of @polychromic_advantage_decomposition is the covariance between reward and "
        "diversity in sets containing $y$ minus the global covariance. This term is positive "
        "when presence of $y$ increases reward-diversity correlation — precisely when $y$ "
        "helps coordinate exploration and exploitation. This term is structurally absent from "
        "pointwise objectives like $r(x,y) \\cdot d(x,y)$ or $r + \\lambda d$, confirming "
        "@poly_epo_synergy."
    ),
    prior=0.97,
)

__all__ = [
    "standard_rl_logit_shift",
    "set_rl_logit_shift",
    "marginal_advantage_interpretation",
    "pass_at_n_analysis",
    "polychromic_advantage_decomposition",
]
