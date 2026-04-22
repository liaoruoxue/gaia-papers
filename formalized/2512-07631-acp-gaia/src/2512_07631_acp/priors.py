"""Prior assignments for independent (leaf) claims in the ACP knowledge package.

Only independent premises that are not the conclusion of any strategy get priors here.
Derived claims get their belief from BP propagation.
"""

from . import (
    active_learning_connection,
    alt_heuristic_match,
    bayesian_opt_connection,
    diminishing_returns_rationale,
    graph_coloring_results_table,
    is_range,
    itotal_properties,
    lorden_overshoot,
    monte_carlo_error_bound,
    pred_lower_bound,
    problem_resource_allocation,
    ptas_fptas_connection,
    rkhs_surrogate_error,
    rl_intrinsic_connection,
)

PRIORS = {
    # --- Background claims from introduction ---
    problem_resource_allocation: (
        0.92,
        "Well-documented challenge: existing agent frameworks (ReAct, AutoGPT, etc.) have "
        "no principled pre-search solvability criterion. The claim is observable empirically.",
    ),
    active_learning_connection: (
        0.95,
        "MacKay (1992) and Houlsby et al. BALD (2011) are well-established results in the "
        "active learning literature; BALD's acquisition function is exactly mutual information. "
        "D-optimality is a classical criterion in experimental design. Very high confidence.",
    ),
    bayesian_opt_connection: (
        0.95,
        "Entropy Search (Hennig 2012) and PES (Hernández-Lobato 2014) are peer-reviewed papers "
        "explicitly framing BO as mutual information maximization. Srinivas et al. (2010) "
        "information-gain regret bounds are well-established. Very high confidence.",
    ),
    rl_intrinsic_connection: (
        0.90,
        "Schmidhuber curiosity (2010) and empowerment (Klyubin 2005) are peer-reviewed; "
        "the information-theoretic framing is correct though the connection to ACP is "
        "somewhat loose (curiosity uses prediction error, not mutual information directly).",
    ),
    # --- Mathematical/theoretical claims ---
    itotal_properties: (
        0.99,
        "Binary entropy formula $H(p) = -p\\log p - (1-p)\\log(1-p)$ is a mathematical fact. "
        "The behavior (maximized at p=1/2, decreasing toward endpoints) is an established "
        "property of binary entropy with no room for empirical uncertainty.",
    ),
    is_range: (
        0.99,
        "Mutual information is non-negative (by definition) and bounded above by the entropy "
        "of the variables (data processing inequality). This is a mathematical fact about "
        "information theory with certainty effectively 1.",
    ),
    diminishing_returns_rationale: (
        0.78,
        "The intuition that early actions eliminate large swaths and later actions refine is "
        "plausible and commonly observed in practice, but not universally true — some search "
        "problems have increasing information gains early on, or flat profiles. Moderate confidence.",
    ),
    lorden_overshoot: (
        0.96,
        "Lorden's inequality (1970) is a classical result in renewal theory for independent "
        "non-identically distributed variables. The paper cites it correctly. Very high confidence "
        "in the mathematical result; slight uncertainty about applicability to this exact setting.",
    ),
    monte_carlo_error_bound: (
        0.93,
        "Proposition 4.1 is a direct application of Hoeffding's inequality to bounded random "
        "variables — a standard result. The expression for L in Gaussian models follows from "
        "Lipschitz continuity of log(1+x). High confidence in the mathematical derivation.",
    ),
    rkhs_surrogate_error: (
        0.82,
        "Theorem 4.1 relies on GP concentration results from Srinivas et al. (2010) and "
        "the Lipschitz argument for mutual information. The sketch is plausible but the "
        "proof is only outlined; the RKHS assumption may be restrictive in practice. "
        "Moderate-high confidence in the result under the stated assumptions.",
    ),
    ptas_fptas_connection: (
        0.88,
        "PTAS for Euclidean TSP and FPTAS for Knapsack are well-known results in "
        "approximation algorithms. The translation to $I_{\\text{total}}(\\epsilon)$ complexity "
        "bounds is a natural interpretation but not rigorously proved in the paper. "
        "High confidence in the underlying algorithm results, moderate in the translation.",
    ),
    graph_coloring_results_table: (
        0.92,
        "Experimental results from 750 instances reported in Table 1. The numbers are "
        "internally consistent (ACP prediction always <= ACP actual, Greedy always < Random "
        "for larger graphs). No reason to doubt the reported values; standard empirical result.",
    ),
    # --- Abduction components ---
    pred_lower_bound: (
        0.90,
        "This claim is the theoretical prediction from Theorem 3.1. Given that the theorem's "
        "proof follows standard martingale + optional stopping arguments, the prediction that "
        "$C_{\\text{eff}} \\leq$ actual cost should hold with high probability.",
    ),
    alt_heuristic_match: (
        0.15,
        "The alternative — that ACP's bound holds only coincidentally without theoretical grounding — "
        "is implausible given the structured, monotonic gap pattern with noise level. "
        "Low prior reflects that coincidental consistent lower-bounding across all trials "
        "is unlikely, especially with the overshoot term predicting the gap direction.",
    ),
}
