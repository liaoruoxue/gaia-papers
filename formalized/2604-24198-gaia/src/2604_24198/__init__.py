from .motivation import *
from .s2_architecture import *
from .s3_data import *
from .s4_training import *
from .s5_experiments import *
from .priors import PRIORS  # noqa: F401 – ensures priors are registered

__all__ = [
    # Core problem characterization
    "claim_silent_errors",
    "claim_grounding_errors",
    "claim_prm_fails_on_analysis",
    "claim_prm_scaling_failure",
    # Architecture contributions
    "claim_env_interaction_critical",
    "claim_ternary_reward_benefit",
    "claim_prm_mirrors_agent",
    # Data pipeline
    "claim_diversity_over_purity",
    "claim_7k_instances",
    # RL training
    "claim_process_beats_outcome",
    "claim_no_entropy_collapse",
    "claim_pass3_improvement",
    # Main results
    "claim_4b_beats_72b",
    "claim_effective_scaling",
    "claim_resists_reward_hacking",
    "claim_58x_efficiency",
]
