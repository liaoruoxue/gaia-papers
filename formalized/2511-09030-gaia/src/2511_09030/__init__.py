from .motivation import *
from .s3_framework import *
from .s4_experiments import *
from .s5_discussion import *

__all__ = [
    # Core exported conclusions
    "maker_zero_errors",
    "voting_pfull_high_mad",
    "cost_scales_log_linearly",
    "mad_enables_error_correction",
    "cost_exponential_with_m",
    # Key empirical results
    "error_rate_mini_low",
    "errors_decorrelated",
    "red_flag_reduces_collisions",
    "error_rate_stable",
    # Scalability claims
    "maker_scalable_beyond",
    "mdap_orthogonal_direction",
]
