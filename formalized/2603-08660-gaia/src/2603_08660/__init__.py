from .motivation import *
from .s2_taxonomy import *
from .s3_sharpening import *
from .s4_rise_and_fall import *
from .s5_safe_application import *
from .s6_model_collapse_step import *
from .s7_external_rewards import *

__all__ = [
    # Core theoretical results
    "theorem1_sharpening",
    "unified_sharpening_framework",
    "sharpening_dual_nature",
    # Core empirical findings
    "rise_then_fall_universal",
    "hyperparameter_robustness_collapse",
    "three_failure_modes",
    # Safe application
    "small_dataset_stability",
    "ttt_safe_conclusion",
    # Model prior measurement
    "mcs_predicts_rl_gains",
    "mcs_computation_efficiency",
    "collapse_step_values",
    # External rewards
    "self_verify_no_collapse",
    "external_rewards_path_forward",
    "instruction_alignment_key",
]
