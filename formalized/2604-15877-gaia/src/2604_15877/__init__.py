"""Experience Compression Spectrum: Unifying Memory, Skills, and Rules in LLM Agents."""

from .motivation import *
from .s2_spectrum import *
from .s2_mapping import *
from .s3_insights import *
from .s4_design import *

__all__ = [
    # Core empirical motivation
    "community_disconnect",
    "shared_problem",
    "practitioner_compression",
    # Spectrum framework -- exported conceptual contributions
    "generalizability_tradeoff",
    "acquisition_maintenance_tradeoff",
    "spectrum_not_pipeline",
    # Mapping conclusions
    "missing_diagonal",
    "framing_limitation",
    "scalability_bottleneck",
    "l3_barriers",
    "higher_compression_better",
    "fidelity_matters",
    # Four structural insights
    "specialization_insufficient",
    "evaluation_should_unify",
    "transferability_monotonic",
    "transferability_concavity",
    "lifecycle_neglected",
    "lifecycle_borrow_se",
    # Testable predictions
    "prediction_l2_beats_l1_transfer",
    "prediction_multilevel_better",
    "prediction_concave_curve",
    "prediction_l3_constraints",
    "predictions_distinguish_taxonomy",
    # Open problems
    "problem_adaptive_selection",
    "problem_cross_level_consistency",
    "problem_lifecycle_management",
    # Design principles and architecture
    "principle_level_agnostic_core",
    "principle_bidirectional",
    "principle_lifecycle_governance",
    "idle_time_consolidation",
    "diagonal_architecture",
    "diagonal_is_core_proposal",
    "unification_is_timely",
]
