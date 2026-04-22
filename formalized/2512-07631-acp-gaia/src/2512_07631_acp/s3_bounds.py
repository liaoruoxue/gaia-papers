"""Section 3: Theoretical Bounds"""

from gaia.lang import claim, setting, support, deduction

from .s2_framework import (
    def_itotal,
    def_is,
    def_ceffective,
    def_optimal_action,
    setup_hypothesis_space,
)

# --- Stochastic model assumptions (setting = formal setup) ---

stochastic_model = setting(
    "Stochastic model assumptions: Let $\\{X_i\\}_{i \\geq 1}$ represent information gains from "
    "successive actions under the optimal policy. Assumptions: "
    "(1) Independence — outcomes are conditionally independent given history; "
    "(2) Bounded moments — $\\sup_i \\mathbb{E}[X_i^2] < \\infty$; "
    "(3) Diminishing returns — expected gains satisfy $\\mu_1 \\geq \\mu_2 \\geq \\cdots \\geq \\mu_{\\inf} > 0$. "
    "Stopping time: $N := \\inf\\{n \\geq 1 : \\sum_{i=1}^n X_i \\geq I_{\\text{total}}\\}$; "
    "total cost: $C := C_s N$.",
    title="Stochastic model for information accumulation",
)

# --- Diminishing returns rationale (claim, can be questioned) ---

diminishing_returns_rationale = claim(
    "The diminishing returns assumption ($\\mu_1 \\geq \\mu_2 \\geq \\cdots \\geq \\mu_{\\inf} > 0$) "
    "is plausible: as search proceeds, remaining uncertainty becomes harder to resolve because "
    "early actions eliminate large swaths of hypothesis space while later actions only refine estimates. "
    "The initial expected gain $I_s := \\mu_1$ is the most optimistic per-step gain value.",
    title="Diminishing returns assumption rationale",
)

# --- Proof intermediate claims ---

martingale_optional_stopping = claim(
    "The partial sums minus their expectations, $M_n = S_n - \\sum_{i=1}^n \\mu_i$, form a martingale. "
    "Assuming finite expected stopping time, the optional stopping theorem gives $\\mathbb{E}[M_N] = 0$, "
    "hence $\\mathbb{E}[S_N] = \\mathbb{E}[\\sum_{i=1}^N \\mu_i]$.",
    title="Martingale optional stopping for information sums",
)

strat_diminishing_returns = support(
    [diminishing_returns_rationale],
    martingale_optional_stopping,
    reason=(
        "@diminishing_returns_rationale motivates the stochastic model assumption that "
        "$\\mu_1 \\geq \\mu_2 \\geq \\cdots$: early actions clear large chunks of hypothesis space. "
        "Under this assumption, partial sums minus their expectations form a martingale, enabling "
        "the optional stopping argument used in Theorem 3.1."
    ),
    prior=0.85,
    background=[stochastic_model],
)

lorden_overshoot = claim(
    "Lorden's inequality [@Lorden1970] for independent non-identically distributed variables bounds "
    "the expected overshoot $R := S_N - I_{\\text{total}}$ by $\\mathbb{E}[R] \\leq M_2/\\mu_{\\inf}$, "
    "where $M_2 = \\sup_i \\mathbb{E}[X_i^2]$ is the second moment of information gains.",
    title="Lorden's inequality bounds expected overshoot",
)

# --- Main theorems ---

lower_bound_ceffective = claim(
    "Under the stochastic model assumptions, $C_{\\text{effective}} \\leq \\mathbb{E}[C]$: "
    "the effective cost $C_{\\text{effective}} = (I_{\\text{total}} / I_s) \\times C_s$ "
    "(using the most optimistic initial gain $I_s = \\mu_1$) is a lower bound on expected total cost. "
    "No strategy can do better on average.",
    title="Ceffective lower-bounds expected cost",
)

upper_bound_ceffective = claim(
    "Under the stochastic model assumptions, the expected total cost satisfies "
    "$\\mathbb{E}[C] \\leq C_s \\left( I_{\\text{total}} / \\mu_{\\inf} + M_2 / \\mu_{\\inf}^2 \\right)$, "
    "where $M_2 = \\sup_i \\mathbb{E}[X_i^2]$ and $\\mu_{\\inf} = \\inf_i \\mu_i$. "
    "The gap between bounds depends on $M_2 / \\mu_{\\inf}^2$, a signal-to-noise ratio.",
    title="Upper bound on expected cost",
)

two_sided_bound = claim(
    "Theorem 3.1 (Two-Sided Cost Bound): Under the stochastic model assumptions, "
    "$C_{\\text{effective}} \\leq \\mathbb{E}[C] \\leq C_s \\left( I_{\\text{total}} / \\mu_{\\inf} + M_2 / \\mu_{\\inf}^2 \\right)$. "
    "The lower bound confirms $C_{\\text{effective}}$ is realistic; the upper bound warns that "
    "if information gains deteriorate severely ($\\mu_{\\inf} \\ll I_s$), costs can exceed "
    "initial estimates substantially.",
    title="Two-sided cost bound theorem",
)

strat_lower_bound = deduction(
    [martingale_optional_stopping],
    lower_bound_ceffective,
    reason=(
        "From @martingale_optional_stopping, $\\mathbb{E}[S_N] = \\mathbb{E}[\\sum_{i=1}^N \\mu_i]$. "
        "Since $S_N \\geq I_{\\text{total}}$ by definition of the stopping time, "
        "$\\mathbb{E}[S_N] \\geq I_{\\text{total}}$. Since $\\mu_i \\leq I_s$ for all $i$, "
        "$\\mathbb{E}[\\sum_{i=1}^N \\mu_i] \\leq I_s \\mathbb{E}[N]$. "
        "Combining: $I_{\\text{total}} \\leq I_s \\mathbb{E}[N]$, giving "
        "$\\mathbb{E}[N] \\geq I_{\\text{total}}/I_s$ and "
        "$\\mathbb{E}[C] = C_s \\mathbb{E}[N] \\geq (I_{\\text{total}}/I_s) C_s = C_{\\text{effective}}$."
    ),
    prior=0.97,
    background=[stochastic_model, def_ceffective],
)

strat_upper_bound = deduction(
    [martingale_optional_stopping, lorden_overshoot],
    upper_bound_ceffective,
    reason=(
        "From @martingale_optional_stopping, $\\mathbb{E}[S_N] = I_{\\text{total}} + \\mathbb{E}[R]$. "
        "Since $\\mu_i \\geq \\mu_{\\inf}$, $\\mathbb{E}[\\sum_{i=1}^N \\mu_i] \\geq \\mu_{\\inf} \\mathbb{E}[N]$. "
        "By @lorden_overshoot, $\\mathbb{E}[R] \\leq M_2/\\mu_{\\inf}$, so "
        "$\\mu_{\\inf} \\mathbb{E}[N] \\leq I_{\\text{total}} + M_2/\\mu_{\\inf}$, "
        "rearranging to $\\mathbb{E}[N] \\leq (I_{\\text{total}}/\\mu_{\\inf} + M_2/\\mu_{\\inf}^2)$ "
        "and multiplying by $C_s$ gives the stated bound."
    ),
    prior=0.95,
    background=[stochastic_model],
)

strat_two_sided_bound = deduction(
    [lower_bound_ceffective, upper_bound_ceffective],
    two_sided_bound,
    reason=(
        "The two-sided bound is the conjunction of @lower_bound_ceffective and "
        "@upper_bound_ceffective. Both hold simultaneously under the stochastic model, "
        "giving $C_{\\text{effective}} \\leq \\mathbb{E}[C] \\leq C_s(I_{\\text{total}}/\\mu_{\\inf} + M_2/\\mu_{\\inf}^2)$."
    ),
    prior=0.99,
)

# --- High-probability bound ---

high_prob_bound = claim(
    "High-probability cost bound (Section 3.3): When information increments are bounded, "
    "$0 \\leq X_i \\leq M$ almost surely, Hoeffding's inequality [@Hoeffding1963] gives: "
    "with probability $\\geq 1 - \\delta$, "
    "$C \\leq C_s \\left( I_{\\text{total}}/\\mu_{\\inf} + O\\left( (M^2/\\mu_{\\inf}^2) \\log(1/\\delta) \\right) \\right)$. "
    "The required step count is "
    "$n_\\delta \\geq I_{\\text{total}}/\\mu_{\\inf} + (M^2/(2\\mu_{\\inf}^2)) \\log(1/\\delta) + "
    "\\sqrt{(I_{\\text{total}} M^2 / (2\\mu_{\\inf}^3)) \\log(1/\\delta)}$. "
    "This allows setting budget reserves proportional to $\\log(1/\\delta)$ for mission-critical applications.",
    title="High-probability budget bound via Hoeffding",
)

strat_high_prob_bound = deduction(
    [lorden_overshoot],
    high_prob_bound,
    reason=(
        "When $X_i \\in [0, M]$, Hoeffding's inequality [@Hoeffding1963] applied to "
        "$\\Pr(S_n < I_{\\text{total}})$ gives $\\exp(-2(n\\mu_{\\inf} - I_{\\text{total}})^2/(nM^2))$ "
        "as an upper bound on the probability of not reaching $I_{\\text{total}}$ in $n$ steps. "
        "Setting this to $\\delta$ and solving for $n$ yields $n_\\delta$, which combined with "
        "the overshoot analysis in @lorden_overshoot gives the stated high-confidence budget."
    ),
    prior=0.95,
    background=[stochastic_model],
)

# --- Interpretation of bound gap ---

bound_gap_interpretation = claim(
    "The gap between the lower bound $C_{\\text{effective}}$ and the upper bound "
    "$C_s(I_{\\text{total}}/\\mu_{\\inf} + M_2/\\mu_{\\inf}^2)$ depends on $M_2/\\mu_{\\inf}^2$, "
    "which acts as a signal-to-noise ratio. When information gains deteriorate severely "
    "($\\mu_{\\inf} \\ll I_s$), actual costs can substantially exceed $C_{\\text{effective}}$.",
    title="Bound gap as signal-to-noise ratio",
)

strat_gap_interpretation = deduction(
    [two_sided_bound],
    bound_gap_interpretation,
    reason=(
        "From @two_sided_bound, the additive slack in the upper bound over the lower bound is "
        "$C_s M_2/\\mu_{\\inf}^2$. This term grows quadratically as $\\mu_{\\inf} \\to 0$ "
        "(severe deterioration), so the gap can be arbitrarily large when early gains "
        "substantially exceed late gains."
    ),
    prior=0.98,
)
