"""Knowledge package for Rodriguez 2026, "Emergent Coordination in
Multi-Agent Systems via Pressure Fields and Temporal Decay" (arXiv
2601.08129v3).

Section-by-section modules import-side-effect register their claims,
settings, questions, and strategies into the Gaia knowledge graph; the
top-level `s11_wiring` module connects claims across modules with
strategies, abductions, inductions, and contradictions.
"""

from . import (
    motivation,
    s2_related_work,
    s3_problem_formulation,
    s4_method,
    s5_theoretical_analysis,
    s6_experiments_setup,
    s6b_main_results,
    s6c_ablations,
    s6d_difficulty_breakdown,
    s7_discussion,
    s11_wiring,
)

__all__ = [
    "motivation",
    "s2_related_work",
    "s3_problem_formulation",
    "s4_method",
    "s5_theoretical_analysis",
    "s6_experiments_setup",
    "s6b_main_results",
    "s6c_ablations",
    "s6d_difficulty_breakdown",
    "s7_discussion",
    "s11_wiring",
]
