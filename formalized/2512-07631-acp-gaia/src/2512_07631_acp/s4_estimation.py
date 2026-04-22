"""Section 4: Connections, Estimation, and Experimental Validation"""

from gaia.lang import claim, setting, support, deduction, abduction, compare

from .s2_framework import (
    def_itotal,
    def_is,
    def_ceffective,
    def_optimal_action,
    setup_hypothesis_space,
)
from .s3_bounds import two_sided_bound, lower_bound_ceffective

# --- Estimation algorithm (setting = formal procedure definition) ---

gp_surrogate_method = setting(
    "Algorithm 1 (A Priori Cost Estimation): "
    "(1) Model uncertainty with GP prior $f \\sim \\mathcal{GP}(0, k(\\cdot, \\cdot))$; "
    "(2) Approximate $I_{\\text{total}} = H[p(\\theta \\in \\Theta_{\\text{goal}})]$ as entropy "
    "of the GP-induced distribution over $\\Theta_{\\text{goal}}$; "
    "(3) Estimate per-step gain $\\hat{I}_s$ by simulating outcomes $y \\sim p(y|a)$, computing "
    "posterior entropies, and averaging $\\text{IG}(a) = H[p(\\theta)] - \\mathbb{E}_{y|a}[H[p(\\theta|a,y)]]$ "
    "over near-optimal actions; "
    "(4) Predict $\\widehat{C}_{\\text{effective}} = (I_{\\text{total}} / \\hat{I}_s) \\times \\bar{C}_s$. "
    "If $\\widehat{C}_{\\text{effective}} \\leq B$, predict solvability; otherwise reconsider.",
    title="GP-based cost estimation algorithm",
)

rkhs_regularity = setting(
    "Under standard RKHS regularity conditions [@Srinivas2010; @Rasmussen2006]: the true function "
    "$f \\in \\mathcal{H}_k$ with $\\|f\\|_{\\mathcal{H}_k} \\leq B$ (GP kernel properly specified), "
    "GP posteriors concentrate around the truth at rate controlled by $\\beta_t = O(\\log t)$ "
    "and maximum information gain $\\gamma_t$.",
    title="RKHS regularity conditions for GP surrogate",
)

# --- Monte Carlo error (claim, with proof) ---

monte_carlo_error_bound = claim(
    "Monte Carlo Error Bound (Proposition 4.1): If $0 \\leq I_{\\text{GP}}(\\theta) \\leq L$ "
    "for all candidates and $\\hat{I}_s$ averages over $S$ samples, then with probability "
    "at least $1 - \\delta$: "
    "$|\\hat{I}_s - \\mathbb{E}_\\theta[I_{\\text{GP}}(\\theta)]| \\leq L \\sqrt{\\log(2/\\delta) / (2S)}$. "
    "For Gaussian predictive models, $L = \\frac{1}{2} \\log(1 + \\sigma^2_{\\max}/\\sigma^2_n)$ "
    "where $\\sigma^2_{\\max}$ is the maximum GP predictive variance and $\\sigma^2_n$ is noise variance.",
    title="Monte Carlo estimation error bound",
)

# --- RKHS surrogate error ---

rkhs_surrogate_error = claim(
    "Surrogate Error Under RKHS (Theorem 4.1): Under RKHS regularity [@Srinivas2010; @Rasmussen2006], "
    "with probability $\\geq 1 - \\delta$: "
    "$|I_{\\text{true}}(\\theta) - I_{\\text{GP}}(\\theta)| \\leq \\frac{1}{2(\\sigma^2_n + \\underline{\\sigma}^2)} "
    "\\cdot \\Delta_\\sigma(\\theta)$, "
    "where $\\underline{\\sigma}^2 = \\inf_\\theta \\sigma^2_t(\\theta)$ (minimum GP posterior variance) and "
    "$\\Delta_\\sigma(\\theta) = O(\\sqrt{\\beta_t} \\sigma_t(\\theta))$ with $\\beta_t = O(\\log t)$. "
    "Mutual information $g(v) = \\frac{1}{2}\\log(1 + v/\\sigma^2_n)$ is Lipschitz in predictive variance "
    "with constant $1/(2(\\sigma^2_n + \\underline{\\sigma}^2))$, and GP concentration bounds variance errors "
    "by $\\sqrt{\\beta_t}\\sigma_t(\\theta)$.",
    title="Surrogate error bound under RKHS regularity",
)

# --- Error propagation ---

ceffective_error_propagation = claim(
    "Error propagation to $\\widehat{C}_{\\text{effective}}$: If surrogate estimates satisfy "
    "$|\\hat{I}_s - I_s| \\leq \\epsilon_s$ and $|\\hat{I}_{\\text{total}} - I_{\\text{total}}| \\leq \\epsilon_{\\text{tot}}$ "
    "with probability $1 - \\delta$, then with the same probability: "
    "$|\\widehat{C}_{\\text{effective}} - C_{\\text{effective}}| \\leq C_s \\left( \\epsilon_{\\text{tot}}/I_s + "
    "(I_{\\text{total}}/I_s^2) \\epsilon_s \\right) + O(\\epsilon^2)$. "
    "Practical solvability tests should include this margin.",
    title="Error propagation from surrogate to cost estimate",
)

strat_error_propagation = deduction(
    [monte_carlo_error_bound, rkhs_surrogate_error],
    ceffective_error_propagation,
    reason=(
        "Taylor expansion of $\\widehat{C}_{\\text{effective}} = I_{\\text{total}}/\\hat{I}_s \\times C_s$ "
        "around the true values $(I_{\\text{total}}, I_s)$: "
        "$\\partial C_{\\text{eff}}/\\partial I_{\\text{total}} = C_s/I_s$ and "
        "$\\partial C_{\\text{eff}}/\\partial I_s = -C_s I_{\\text{total}}/I_s^2$. "
        "Substituting the bounds from @monte_carlo_error_bound ($|\\hat{I}_s - I_s| \\leq \\epsilon_s$) "
        "and @rkhs_surrogate_error ($|I_{\\text{true}} - I_{\\text{GP}}| \\leq \\ldots$) "
        "gives the stated first-order error bound."
    ),
    prior=0.92,
)

# --- Experimental setup: LLM slope identification ---

exp_setup_slope = setting(
    "Experimental setup for LLM slope identification: An agent seeks the slope $a \\in [-2, 2]$ "
    "of a linear function $y(x) = ax + \\epsilon$ where $\\epsilon \\sim \\mathcal{N}(0, \\sigma^2)$ "
    "by querying points $x \\in [-3, 3]$. Algorithm 1 predicts required steps using a GP surrogate "
    "for noise levels $\\sigma \\in [0.1, 0.8]$. An LLM agent is then deployed, providing past "
    "observations and requesting the next query and current slope estimate at each step.",
    title="Experimental setup: LLM agent slope identification",
)

# --- Experimental results ---

acp_lower_bounds_llm = claim(
    "In the LLM slope identification experiment, the ACP estimate $C_{\\text{effective}}$ "
    "consistently lower-bounds actual LLM agent steps across all tested noise levels "
    "$\\sigma \\in [0.1, 0.8]$: at $\\sigma \\approx 0.1$, ACP predicts approximately 2 steps "
    "while LLM requires approximately 4 steps; at $\\sigma \\approx 0.8$, ACP predicts "
    "approximately 6 steps while LLM requires approximately 10 steps. "
    "The lower-bound condition is never violated.",
    title="ACP lower-bounds LLM agent steps in slope identification",
    metadata={"figure": "artifacts/2512.07631-acp.pdf", "caption": "Figure 1: ACP predictions versus actual LLM agent performance for noisy slope identification across noise levels."},
)

gap_increases_with_noise = claim(
    "The gap between ACP predictions and actual LLM agent performance increases with noise "
    "level $\\sigma$: at low noise ($\\sigma \\approx 0.1$), gap is approximately 2 steps; "
    "at high noise ($\\sigma \\approx 0.8$), gap grows to approximately 4 steps. "
    "This is consistent with the overshoot term $M_2/\\mu_{\\inf}^2$ in the upper bound, "
    "which grows with problem difficulty (higher noise).",
    title="Prediction gap grows with noise level",
    metadata={"figure": "artifacts/2512.07631-acp.pdf", "caption": "Figure 1: ACP predictions versus actual LLM agent performance."},
)

strat_gap_noise = support(
    [acp_lower_bounds_llm],
    gap_increases_with_noise,
    reason=(
        "From @acp_lower_bounds_llm, the gap between ACP predictions and LLM actual steps "
        "is approximately 2 steps at $\\sigma \\approx 0.1$ and grows to approximately 4 steps "
        "at $\\sigma \\approx 0.8$. This monotonic increase with noise level is directly "
        "observable from Figure 1 and consistent with the $M_2/\\mu_{\\inf}^2$ overshoot term "
        "growing with problem difficulty."
    ),
    prior=0.88,
)

# --- Abduction: is ACP a valid lower bound or coincidence? ---

pred_lower_bound = claim(
    "If $C_{\\text{effective}}$ is a valid theoretical lower bound (as claimed by Theorem 3.1), "
    "then predicted steps should be $\\leq$ actual LLM steps in all trials across all noise levels, "
    "and the gap should grow monotonically with noise (as predicted by the overshoot term $M_2/\\mu_{\\inf}^2$).",
    title="ACP prediction: valid lower bound implies prediction <= actual with growing gap",
)

alt_heuristic_match = claim(
    "If ACP predictions coincidentally track LLM performance without being a theoretically valid "
    "lower bound, predictions would sometimes exceed actual steps (random violations), and "
    "any noise-dependent gap pattern would be coincidental.",
    title="Alternative: coincidental match without guaranteed lower bound validity",
)

s_h_llm = support(
    [pred_lower_bound],
    acp_lower_bounds_llm,
    reason=(
        "@pred_lower_bound follows from Theorem 3.1 (@two_sided_bound): "
        "$C_{\\text{effective}} \\leq \\mathbb{E}[C]$ means the predicted lower bound must be "
        "$\\leq$ actual steps in expectation, and the overshoot term predicts the observed "
        "noise-dependent gap pattern."
    ),
    prior=0.9,
)

s_alt_llm = support(
    [alt_heuristic_match],
    acp_lower_bounds_llm,
    reason=(
        "@alt_heuristic_match: a coincidental match would only approximately bound actual steps "
        "and would fail in some trials; the observed structured gap pattern would be unlikely."
    ),
    prior=0.2,
)

comp_llm = compare(
    pred_lower_bound, alt_heuristic_match, acp_lower_bounds_llm,
    reason=(
        "The ACP prediction is a consistent lower bound across all noise levels (never violated), "
        "and the gap monotonically increases with $\\sigma$ as predicted by the overshoot "
        "term $M_2/\\mu_{\\inf}^2$. This structured behavior strongly favors the valid "
        "lower bound interpretation over a coincidental match."
    ),
    prior=0.88,
)

abduction_llm_validation = abduction(
    s_h_llm, s_alt_llm, comp_llm,
    reason="LLM slope experiment provides empirical test of Theorem 3.1's lower bound claim",
)
