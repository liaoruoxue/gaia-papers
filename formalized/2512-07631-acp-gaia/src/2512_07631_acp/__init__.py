"""Agent Capability Problem (ACP): Predicting Solvability Through Information-Theoretic Bounds

Lutati (2025). Formalizes the ACP framework, two-sided cost bounds, GP-based estimation,
and empirical validation on LLM and graph coloring tasks.
"""

from .motivation import *
from .s2_framework import *
from .s3_bounds import *
from .s4_estimation import *
from .s5_graph_coloring import *

__all__ = [
    # Core framework claims (exported conclusions)
    "acp_ceffective_formula",
    "two_sided_bound",
    "lower_bound_ceffective",
    "upper_bound_ceffective",
    "high_prob_bound",
    # Key experimental results
    "acp_lower_bounds_llm",
    "acp_lower_bound_graph",
    "graph_coloring_results_table",
    "acp_vs_random_graph",
    "acp_vs_greedy_graph",
    # Theoretical extensions
    "inapproximability_as_infinite_cost",
    "unified_principle",
    "law_acp_lower_bound",
]
