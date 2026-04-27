"""Section 4: Performance evaluation definitions (posterior consistency, regret, potential energy)."""

from gaia.lang import setting

# These are formal definitions, not assertions, so they are settings.

def_posterior_consistency = setting(
    "**Definition 4.1 (Posterior Consistency).** Let $q_t(s)$ denote the posterior "
    "belief over the latent parameter $s\\in\\mathcal{S}$ after observing dataset "
    "$D_t$. The learning process is **(strongly) consistent** if, with probability "
    "one,\n\n"
    "$$\\lim_{t\\to\\infty} q_t(s) = \\delta_{s^*},$$\n\n"
    "where $\\delta_{s^*}$ is the Dirac measure concentrated at the true parameter "
    "value $s^*$.",
    title="Definition 4.1: Posterior Consistency",
)

def_regret_function = setting(
    "**Definition 4.2 (Regret Function).** Let $\\mathcal{Y}$ denote the outcome "
    "space. A *regret function* is a mapping $r:\\mathcal{Y}\\to\\mathbb{R}_{\\geq 0}$ "
    "that quantifies the deviation of an outcome $y$ from its desired state $y^*$: "
    "smaller $r(y)$ means $y$ is closer to the desired outcome. Special cases:\n\n"
    "- When $y^*$ is the global optimum of an objective, $r(y)$ reduces to the "
    "conventional instantaneous regret in BO.\n"
    "- When all outcomes are equally desirable or informative (as in BED), "
    "$r(y) \\equiv 0$.\n"
    "- Intermediate cases correspond to hybrid objectives with both performance "
    "and safety constraints.",
    title="Definition 4.2: Regret Function",
)

def_potential_energy = setting(
    "**Definition 4.3 (Potential Energy Function).** Since the true regret "
    "function $r(y)$ is generally unknown or intractable, define a time-varying "
    "surrogate $h_t:\\mathcal{Y}\\to\\mathbb{R}_{\\geq 0}$ that encodes the "
    "current model's internal assessment of outcome desirability and is updated "
    "recursively as new data arrive: $h_t(y) := h(y|D_{t-1})$. This $h_t$ is "
    "non-negative ($h_t(y) \\geq 0$ for all $y\\in\\mathcal{Y}$) and serves as a "
    "heuristic estimator of regret conditioned on past observations.",
    title="Definition 4.3: Potential Energy Function (heuristic regret)",
)

def_cumulative_regret = setting(
    "**Cumulative regret.** For a query sequence $x_1,\\ldots,x_T$ producing "
    "true-function values $f(x_t)$, the cumulative regret over horizon $T$ is "
    "$R_T = \\sum_{t=1}^T r(f(x_t))$. \"No-regret\" optimization means "
    "$R_T$ grows sub-linearly in $T$ (so $R_T/T \\to 0$).",
    title="Cumulative regret definition",
)

