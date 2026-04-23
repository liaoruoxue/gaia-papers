from .motivation import *
from .s3_methodology import *
from .s4_results import *
from .s5_discussion import *

__all__ = [
    # Core empirical findings
    "sas_best_overall_tradeoff",
    "mas_limited_gains",
    "no_universal_winner",
    # Key observations
    "obs_sas_nrq",
    "obs_completion_rates",
    "obs_base_uturn",
    # Practical guidelines
    "guideline_sas_for_complex",
    "guideline_mas_for_high_entropy",
    "guideline_base_for_extraction",
    "guideline_fallback",
    # Theoretical insights
    "coordination_tax",
    "context_management_bottleneck",
    "architectural_fragility",
]
