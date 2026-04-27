"""ACON: Optimizing Context Compression for Long-Horizon LLM Agents.

Formalisation of arXiv:2510.00615 (Kang et al., 2025).
"""

from . import motivation, s3_method, s4_experiments, s5_analysis

# Headline exported conclusions of the paper -- the package's external API.
from .motivation import (
    acon_compresses_history_and_obs,
    acon_is_gradient_free,
    acon_distillable,
    claim_peak_token_reduction,
    claim_distillation_preserves_accuracy,
    claim_helps_small_agents,
)
from .s3_method import acon_solves_problem
from .s4_experiments import cost_limitation
from .s5_analysis import threshold_recommendation, strong_optimizer_matters

__all__ = [
    "motivation",
    "s3_method",
    "s4_experiments",
    "s5_analysis",
    # Headline conclusions
    "acon_compresses_history_and_obs",
    "acon_is_gradient_free",
    "acon_distillable",
    "claim_peak_token_reduction",
    "claim_distillation_preserves_accuracy",
    "claim_helps_small_agents",
    "acon_solves_problem",
    "cost_limitation",
    "threshold_recommendation",
    "strong_optimizer_matters",
]
