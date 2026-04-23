from .motivation import *
from .s3_optimal_distributions import *
from .s4_mode_coverage_analysis import *
from .s5_mara import *
from .s6_experiments import *
from .priors import *

__all__ = [
    # Core theoretical results — exported conclusions
    "reverse_kl_optimal_dist",
    "forward_kl_optimal_dist",
    "forward_kl_gradient_not_forward_kl",
    "log_prob_ratio_formula",
    "equal_support_exponential_gap",
    "equal_reward_preserves_ratio",
    "beta_as_mode_knob",
    "typical_settings_unimodal",
    "kl_type_not_primary_driver",
    # Algorithm
    "mara_augmented_reward",
    "mara_solution_is_uniform",
    "mara_exists",
    # Empirical
    "exp_12_mara_diverse",
    "exp_creative_qa_table",
    "exp_drug_synth_yield",
    "exp_drug_amide_yield",
]
