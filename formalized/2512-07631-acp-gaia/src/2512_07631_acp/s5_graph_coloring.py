"""Section 4.6 and Section 5: Graph Coloring Experiments and Approximation Extensions"""

from gaia.lang import claim, setting, support, deduction, abduction, compare, induction

from .s2_framework import def_itotal, def_is, def_ceffective
from .s3_bounds import two_sided_bound, lower_bound_ceffective

# --- Experiment setup (settings = formal conditions) ---

graph_coloring_setup = setting(
    "Graph coloring experiment setup (Section 4.6): k-coloring of random Erdős–Rényi graphs "
    "$G(n, p)$ with $k = 3$ colors. Graph sizes $n \\in \\{8, 10, 12, 15\\}$ and edge probabilities "
    "$p \\in \\{0.25, 0.30, 0.35, 0.41\\}$; 50–250 random instances per configuration (750 total). "
    "Non-3-colorable instances (verified via ILP) are discarded. "
    "Three agents: (i) Random — selects variables and colors uniformly; "
    "(ii) Greedy — selects highest-degree vertex, minimizes local conflicts; "
    "(iii) ACP — uses entropy-based estimate $C_{\\text{eff}} = I_{\\text{total}}/I_s$ to bias ordering. "
    "All use backtracking with forward checking. Cost metric: node expansions until valid coloring.",
    title="Graph coloring experiment setup",
)

acp_bound_formulation = setting(
    "For each graph coloring instance, $I_{\\text{total}}$ is the entropy of the feasible coloring "
    "space and $I_s$ is the average information gain per assignment using partial constraint structure, "
    "giving $C_{\\text{eff}} = I_{\\text{total}}/I_s$ as the predicted lower bound (plus overshoot term). "
    "The ACP agent uses $C_{\\text{eff}}$ only to bias variable ordering; no ground-truth cost is provided.",
    title="ACP bound formulation for graph coloring",
)

# --- Results ---

graph_coloring_results_table = claim(
    "Graph coloring search cost results across 750 instances "
    "(node expansions, lower is better):\n\n"
    "| $(n, p)$ | Random | Greedy | ACP actual | ACP prediction |\n"
    "|----------|--------|--------|------------|----------------|\n"
    "| $(8, 0.25)$ | 9.16 | 8.00 | 8.00 | 8.00 |\n"
    "| $(10, 0.30)$ | 13.64 | 10.16 | 10.00 | 10.00 |\n"
    "| $(12, 0.35)$ | 27.34 | 13.10 | 13.04 | 12.00 |\n"
    "| $(15, 0.35)$ | 47.40 | 18.58 | 18.34 | 15.00 |\n"
    "| $(15, 0.41)$ | 39.46 | 18.08 | 16.46 | 15.00 |\n\n"
    "ACP prediction $C_{\\text{eff}}$ is at or below ACP actual cost in every row.",
    title="Graph coloring search cost results",
    metadata={"source_table": "artifacts/2512.07631-acp.pdf, Table 1"},
)

acp_lower_bound_graph = claim(
    "Across all 750 graph coloring instances, the predicted cost $C_{\\text{eff}}$ is "
    "at or below the observed ACP agent cost in every trial ($C_{\\text{eff}} \\leq C$ always), "
    "validating the theoretical lower bound of Theorem 3.1. The lower-bound condition is never violated.",
    title="ACP prediction is valid lower bound in all 750 graph coloring instances",
)

acp_vs_random_graph = claim(
    "The ACP agent consistently reduces node expansions relative to the Random agent in graph coloring, "
    "with larger gains for larger or denser graphs: "
    "at $(n=8, p=0.25)$, both use 8.00 expansions; "
    "at $(n=15, p=0.35)$, ACP uses 18.34 vs. Random's 47.40 (61% reduction); "
    "at $(n=15, p=0.41)$, ACP uses 16.46 vs. Random's 39.46 (58% reduction).",
    title="ACP outperforms Random agent in graph coloring",
)

acp_vs_greedy_graph = claim(
    "The ACP agent matches or outperforms the Greedy agent in graph coloring, with improvements "
    "becoming more pronounced with problem difficulty: "
    "at $(n=8, p=0.25)$, ACP and Greedy both use 8.00 expansions; "
    "at $(n=12, p=0.35)$, ACP uses 13.04 vs. Greedy's 13.10 (marginal); "
    "at $(n=15, p=0.41)$, ACP uses 16.46 vs. Greedy's 18.08 (9% reduction).",
    title="ACP matches or outperforms Greedy agent in graph coloring",
)

overshoot_increases_with_difficulty = claim(
    "The overshoot (difference $C - C_{\\text{eff}}$ between actual ACP cost and prediction) "
    "increases with graph size and density: "
    "at $(n=8, p=0.25)$, overshoot is 0.00; "
    "at $(n=12, p=0.35)$, overshoot is $13.04 - 12.00 = 1.04$; "
    "at $(n=15, p=0.35)$, overshoot is $18.34 - 15.00 = 3.34$. "
    "This is consistent with the theoretical prediction that the overshoot term $M_2/\\mu_{\\inf}^2$ "
    "grows with problem difficulty.",
    title="Overshoot increases with problem difficulty as theoretically predicted",
)

strat_acp_lower_bound_graph = support(
    [graph_coloring_results_table],
    acp_lower_bound_graph,
    reason=(
        "From @graph_coloring_results_table: in every row, ACP Prediction $\\leq$ ACP actual. "
        "The bound is tight at $(n=8, p=0.25)$ (prediction = actual = 8.00) and holds with "
        "growing slack at larger graphs. No violation of $C_{\\text{eff}} \\leq C$ is observed "
        "across all 750 instances, confirming Theorem 3.1's lower bound claim."
    ),
    prior=0.95,
    background=[graph_coloring_setup, acp_bound_formulation],
)

strat_acp_vs_random = support(
    [graph_coloring_results_table],
    acp_vs_random_graph,
    reason=(
        "Directly reading from @graph_coloring_results_table: ACP actual cost is consistently "
        "below Random across all $(n, p)$ configurations, with the relative gap widening from 0% "
        "at $(n=8, p=0.25)$ to 61% at $(n=15, p=0.35)$, confirming ACP outperforms Random "
        "and that gains grow with problem difficulty."
    ),
    prior=0.93,
)

strat_acp_vs_greedy = support(
    [graph_coloring_results_table],
    acp_vs_greedy_graph,
    reason=(
        "Directly reading from @graph_coloring_results_table: ACP actual cost is at or below "
        "Greedy across all configurations, with the relative improvement growing from 0% "
        "at $(n=8)$ to 9% at $(n=15, p=0.41)$, confirming ACP matches or outperforms Greedy "
        "with benefits scaling with problem difficulty."
    ),
    prior=0.91,
)

strat_overshoot = support(
    [acp_lower_bound_graph, graph_coloring_results_table],
    overshoot_increases_with_difficulty,
    reason=(
        "From @graph_coloring_results_table, the absolute difference between ACP actual and "
        "ACP prediction grows from 0 at $(n=8)$ to 3.34 at $(n=15, p=0.35)$. "
        "Given that @acp_lower_bound_graph confirms the bound holds, the growing overshoot "
        "reflects increasing problem difficulty, consistent with the $M_2/\\mu_{\\inf}^2$ term "
        "from Theorem 3.1 (@two_sided_bound)."
    ),
    prior=0.87,
)

# --- Induction: general law that ACP is a valid lower bound ---

law_acp_lower_bound = claim(
    "For search problems framed as information acquisition, $C_{\\text{eff}} = I_{\\text{total}}/I_s$ "
    "is a valid lower bound on expected search cost, with overshoot increasing with problem difficulty. "
    "This generalizes across LLM-based continuous estimation tasks and combinatorial NP-hard search tasks.",
    title="General law: ACP is valid lower bound on search cost",
)

s1_graph = support(
    [law_acp_lower_bound], acp_lower_bound_graph,
    reason=(
        "@law_acp_lower_bound predicts $C_{\\text{eff}} \\leq C$ for all graph coloring instances. "
        "@acp_lower_bound_graph confirms this across all 750 instances (combinatorial domain)."
    ),
    prior=0.92,
)

s2_llm = support(
    [law_acp_lower_bound], lower_bound_ceffective,
    reason=(
        "@law_acp_lower_bound predicts $C_{\\text{effective}} \\leq \\mathbb{E}[C]$ in the LLM "
        "slope identification experiment. @lower_bound_ceffective is the theoretical statement "
        "confirmed empirically across all noise levels."
    ),
    prior=0.9,
)

ind_lower_bound_law = induction(
    s1_graph, s2_llm,
    law=law_acp_lower_bound,
    reason=(
        "Two independent empirical validations: graph coloring (combinatorial NP-hard, 750 instances) "
        "and LLM slope identification (continuous Bayesian estimation) confirm the lower bound law. "
        "The tasks differ in domain, agent type, and search structure, strengthening generalization."
    ),
)

# --- Approximation algorithms extension (Section 5) ---

epsilon_approximate_goal = setting(
    "Epsilon-Approximate Goal (Definition 5.1): The goal set is "
    "$\\Theta_{\\text{goal}}(\\epsilon) = \\{\\theta \\in \\Theta : f(\\theta) \\leq (1+\\epsilon) f(\\theta^*)\\}$, "
    "where $\\theta^*$ minimizes $f$ and $\\epsilon \\geq 0$ controls approximation quality. "
    "As $\\epsilon$ increases, $|\\Theta_{\\text{goal}}(\\epsilon)|$ grows and $I_{\\text{total}}(\\epsilon)$ decreases.",
    title="Epsilon-approximate goal set definition",
)

ptas_fptas_connection = claim(
    "For problems admitting a Polynomial-Time Approximation Scheme (PTAS, e.g., Euclidean TSP), "
    "$I_{\\text{total}}(\\epsilon)$ is achievable in time $n^{O(1)} \\cdot 2^{O(1/\\epsilon)}$. "
    "For Fully Polynomial-Time Approximation Schemes (FPTAS, e.g., Knapsack), "
    "$I_{\\text{total}}(\\epsilon)$ is achievable in time polynomial in both $n$ and $1/\\epsilon$. "
    "These complexity bounds translate directly to $C_{\\text{effective}}(\\epsilon)$ bounds.",
    title="PTAS/FPTAS complexity through information-theoretic lens",
)

approximation_reduces_info = claim(
    "Relaxing the approximation quality (increasing $\\epsilon$) strictly reduces "
    "$I_{\\text{total}}(\\epsilon)$ and hence $C_{\\text{effective}}(\\epsilon)$: "
    "a larger goal set $\\Theta_{\\text{goal}}(\\epsilon)$ means a larger fraction $p$ of "
    "candidates satisfy the goal, and binary entropy $-p \\log p - (1-p) \\log(1-p)$ "
    "decreases as $p$ increases beyond $1/2$ toward 1, reducing information requirements.",
    title="Relaxed approximation reduces information requirements",
)

strat_approx_reduces_info = support(
    [ptas_fptas_connection],
    approximation_reduces_info,
    reason=(
        "From the epsilon-approximate goal definition, larger $\\epsilon$ implies larger "
        "$\\Theta_{\\text{goal}}(\\epsilon)$ (more candidates qualify). The fraction $p$ of qualifying "
        "candidates increases. Since $I_{\\text{total}} = H(\\mathbf{1}(\\theta \\in \\Theta_{\\text{goal}}))$ "
        "is binary entropy and entropy decreases as $p$ moves from $1/2$ toward 1 (for hard problems "
        "where $p < 1/2$ initially), $I_{\\text{total}}(\\epsilon)$ monotonically decreases with $\\epsilon$. "
        "@ptas_fptas_connection shows this holds across PTAS and FPTAS complexity classes."
    ),
    prior=0.95,
    background=[epsilon_approximate_goal, def_itotal],
)

inapproximability_as_infinite_cost = claim(
    "Inapproximability results from the PCP theorem translate to ACP: if a problem is NP-hard "
    "to approximate within ratio $\\rho$, then $I_{\\text{total}}(\\epsilon) = \\infty$ for "
    "$\\epsilon < \\rho - 1$, making the problem unsolvable regardless of budget. "
    "This provides a principled unified framework for reasoning about both exact and "
    "approximate solvability through information requirements.",
    title="Inapproximability as infinite ACP cost",
)

strat_inapprox = support(
    [approximation_reduces_info],
    inapproximability_as_infinite_cost,
    reason=(
        "If no polynomial-time algorithm can approximate within ratio $\\rho$ (by PCP theorem), "
        "no agent can identify a solution in $\\Theta_{\\text{goal}}(\\epsilon < \\rho - 1)$ efficiently. "
        "Since @approximation_reduces_info shows $I_{\\text{total}}$ depends on the size of the goal set, "
        "and the PCP theorem implies the goal set is effectively empty for $\\epsilon < \\rho - 1$ "
        "under any polynomial-time constraint, $I_{\\text{total}}(\\epsilon) \\to \\infty$ for such $\\epsilon$."
    ),
    prior=0.82,
    background=[epsilon_approximate_goal],
)
