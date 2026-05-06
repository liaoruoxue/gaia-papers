"""Section 4: Method -- pressure alignment, potential-game connection,
the coordination algorithm, stability and termination semantics.

Source: Rodriguez 2026 [@Rodriguez2026PressureField], Section 4.
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# 4.1 Pressure alignment definitions
# ---------------------------------------------------------------------------

setup_pressure_alignment = setting(
    "**Definition 4.1 (Pressure Alignment).** A pressure system is "
    "*aligned* if, for any region $i$, state $s$, and action $a_i$ "
    "that reduces local pressure, the global pressure also "
    "decreases: $P_i(s') < P_i(s) \\Rightarrow P(s') < P(s)$, where "
    "$s' = s[c_i \\mapsto a_i(c_i)]$ is the state after applying "
    "$a_i$. Alignment holds *automatically* when pressure functions "
    "are *separable* -- each $P_i$ depends only on $c_i$, so "
    "$P(s) = \\sum_i P_i(s)$ and local improvement directly implies "
    "global improvement.",
    title="Setup: Definition 4.1 pressure alignment (local reduction => global reduction); separable pressure is automatically aligned",
)

setup_bounded_coupling = setting(
    "**Definition 4.2 ($\\epsilon$-bounded coupling).** A pressure "
    "system has $\\epsilon$-bounded coupling if, for any action "
    "$a_i$ on region $i$ and any other region $j \\ne i$: "
    "$|P_j(s') - P_j(s)| \\le \\epsilon$. That is, modifying region "
    "$i$ changes any other region's pressure by at most $\\epsilon$. "
    "Under $\\epsilon$-bounded coupling with $n$ regions, if a "
    "local action reduces $P_i$ by $\\delta > (n-1)\\epsilon$, then "
    "global pressure decreases by at least $\\delta - (n-1)\\epsilon "
    "> 0$.",
    title="Setup: Definition 4.2 epsilon-bounded coupling (|P_j(s') - P_j(s)| <= eps); enables alignment when delta > (n-1)*eps",
)

# ---------------------------------------------------------------------------
# 4.2 Connection to potential games
# ---------------------------------------------------------------------------

claim_potential_game_connection = claim(
    "**The aligned pressure system forms a potential game with "
    "$\\Phi(s) = P(s)$.** Players are regions (or agents acting on "
    "regions); strategies are content choices $c_i \\in "
    "\\mathcal{C}$; the potential function is $\\Phi(s) = P(s)$. By "
    "the Monderer-Shapley result on potential games "
    "[@PotentialGames], any sequence of improving moves converges "
    "to a Nash equilibrium. In this setting, Nash equilibria "
    "correspond to stable basins (states where no local action "
    "reduces pressure below the activation threshold). This is the "
    "convergence guarantee without requiring explicit coordination.",
    title="Result: aligned pressure system is a potential game with Phi(s) = P(s); Nash equilibria = stable basins",
)

setup_finite_action_assumption = setting(
    "**Finite-action assumption (operative for the convergence "
    "result).** The convergence result (Theorem 5.1) assumes finite "
    "action spaces. In practice, patches are drawn from a finite "
    "set of LLM-generated proposals per region, satisfying this "
    "requirement. The validation phase implicitly discretizes the "
    "action space: only patches that reduce pressure are accepted, "
    "so the effective action set at any state is the finite set of "
    "pressure-reducing proposals generated that tick. For infinite "
    "content spaces, convergence to *approximate* equilibria can be "
    "established under Lipschitz continuity conditions on pressure "
    "functions.",
    title="Setup: finite-action assumption (validation discretizes the action space to pressure-reducing proposals)",
)

# ---------------------------------------------------------------------------
# 4.3 Algorithm 1 properties
# ---------------------------------------------------------------------------

setup_algorithm_1 = setting(
    "**Algorithm 1 (Pressure-Field Tick).** Inputs: state $s_t$, "
    "signal functions $\\{\\sigma_j\\}$, pressure functions "
    "$\\{\\phi_j\\}$, actors $\\{a_k\\}$, and parameters "
    "$(\\tau_{act}, \\lambda_f, \\lambda_\\gamma, \\Delta_f, "
    "\\Delta_\\gamma, \\kappa)$. The tick proceeds in four phases:\n\n"
    "1. **Decay** -- $f_i \\leftarrow f_i \\cdot e^{-\\lambda_f}$, "
    "$\\gamma_i \\leftarrow \\gamma_i \\cdot e^{-\\lambda_\\gamma}$ "
    "for each region $i$.\n"
    "2. **Activation and Proposal** -- candidate set "
    "$\\mathcal{P} \\gets \\emptyset$; for each region $i$ where "
    "$P_i(s) \\ge \\tau_{act}$ and $i$ is not inhibited, each actor "
    "$a_k$ proposes $\\delta = a_k(c_i, h_i, \\sigma_i)$ and "
    "$\\mathcal{P} \\gets \\mathcal{P} \\cup \\{(i, \\delta, "
    "\\hat{\\Delta}(\\delta))\\}$.\n"
    "3. **Parallel Validation and Selection** -- fork artifact, "
    "apply each candidate $\\delta$ to its fork, run validation "
    "(tests, compilation), collect $\\{(i, \\delta, "
    "\\Delta_{actual}, \\text{valid})\\}$; sort validated patches "
    "by $\\Delta_{actual}$; greedily select top-$\\kappa$ non-"
    "conflicting patches.\n"
    "4. **Application and Reinforcement** -- apply selected "
    "$\\delta$ to $c_i$; boost $f_i, \\gamma_i$ (clamped at 1); "
    "mark region $i$ inhibited for $\\tau_{inh}$ ticks.",
    title="Setup: Algorithm 1 (Pressure-Field Tick) -- decay / proposal / validation / reinforcement",
    metadata={
        "figure": "artifacts/2601.08129.pdf, Algorithm 1 (page 18)",
        "caption": "Algorithm 1: Pressure-Field Tick -- four phases (decay, proposal, validation, reinforcement).",
    },
)

claim_algorithm_three_properties = claim(
    "**Algorithm 1 has three key properties.** "
    "(P1) **Locality** -- each actor observes only "
    "$(c_i, h_i, \\sigma(c_i))$; no global state is accessed. "
    "(P2) **Bounded parallelism** -- at most $\\kappa$ patches per "
    "tick prevents thrashing; inhibition prevents repeated "
    "modification of the same region. "
    "(P3) **Decay-driven exploration** -- even stable regions "
    "eventually decay below confidence thresholds, attracting re-"
    "evaluation; this prevents premature convergence to local minima.",
    title="Result: Algorithm 1 has locality / bounded parallelism / decay-driven exploration",
)

# ---------------------------------------------------------------------------
# 4.4 Stability and termination semantics
# ---------------------------------------------------------------------------

claim_economic_termination = claim(
    "**Termination is economic, not logical.** The system stops "
    "acting when the cost of action (measured in pressure reduction "
    "per patch) falls below the benefit. This matches natural "
    "systems: activity ceases when gradients flatten, not when an "
    "external goal is declared achieved. In practice, budget "
    "constraints (maximum ticks or patches) bound computation.",
    title="Result: pressure-field termination is economic (gradient-flattening), not goal-achievement-based",
)

__all__ = [
    "setup_pressure_alignment",
    "setup_bounded_coupling",
    "claim_potential_game_connection",
    "setup_finite_action_assumption",
    "setup_algorithm_1",
    "claim_algorithm_three_properties",
    "claim_economic_termination",
]
