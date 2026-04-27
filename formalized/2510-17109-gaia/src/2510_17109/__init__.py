"""VeriMAP — Verification-Aware Planning for Multi-Agent Systems.

Formalization of Xu, Zhang, Mitra, Hruschka (arXiv:2510.17109, Oct 2025).
"""

# Expose exported conclusions and key claims for cross-package consumption.
from .motivation import (
    multi_agent_planning_central,
    failures_context_dependent,
    existing_verification_misses_context,
    contribution_verimap,
)
from .s2_system import (
    verimap_modules,
    structured_io_named_vars,
    planner_generated_vfs,
    python_vf_definition,
    nl_vf_definition,
    coordinator_replanning,
)
from .s3_evaluation import (
    verimap_best_overall,
    verimap_beats_react_olympiads,
    verimap_beats_react_bigcode,
    verimap_beats_mapv,
    replanning_helps_verimap,
    replanning_limited_for_mapv,
    vf_count_adapts_to_domain,
    verimap_lower_fp_than_mapv,
    verimap_higher_fn_in_code,
    case_study_resolves_error,
    other_planners_consistent,
)
from .s4_critical import (
    centralized_planner_dependence,
    cost_overhead_modest,
    fn_overconservative_tradeoff,
)

__all__ = [
    # Motivation
    "multi_agent_planning_central",
    "failures_context_dependent",
    "existing_verification_misses_context",
    "contribution_verimap",
    # System
    "verimap_modules",
    "structured_io_named_vars",
    "planner_generated_vfs",
    "python_vf_definition",
    "nl_vf_definition",
    "coordinator_replanning",
    # Evaluation
    "verimap_best_overall",
    "verimap_beats_react_olympiads",
    "verimap_beats_react_bigcode",
    "verimap_beats_mapv",
    "replanning_helps_verimap",
    "replanning_limited_for_mapv",
    "vf_count_adapts_to_domain",
    "verimap_lower_fp_than_mapv",
    "verimap_higher_fn_in_code",
    "case_study_resolves_error",
    "other_planners_consistent",
    # Critical
    "centralized_planner_dependence",
    "cost_overhead_modest",
    "fn_overconservative_tradeoff",
]
