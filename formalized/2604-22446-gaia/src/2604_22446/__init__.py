"""Knowledge package for Yu et al. 2026, "From Skills to Talent:
Organising Heterogeneous Agents as a Real-World Company" (arXiv
2604.22446v1).

Section-by-section modules import-side-effect register their claims,
settings, questions, and strategies into the Gaia knowledge graph; the
top-level `s11_wiring` module connects claims across modules with
strategies, deductions, inductions, abductions, and contradictions.
"""

from . import (
    motivation,
    s2_related_work,
    s3_setup,
    s4_talent_abstraction,
    s5_e2r_tree_search,
    s6_dag_and_guarantees,
    s7_self_evolution,
    s8_evaluation_setup,
    s9_main_results,
    s10_discussion,
    s11_wiring,
)

__all__ = [
    "motivation",
    "s2_related_work",
    "s3_setup",
    "s4_talent_abstraction",
    "s5_e2r_tree_search",
    "s6_dag_and_guarantees",
    "s7_self_evolution",
    "s8_evaluation_setup",
    "s9_main_results",
    "s10_discussion",
    "s11_wiring",
]
