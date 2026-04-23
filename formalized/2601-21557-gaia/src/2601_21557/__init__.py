from .motivation import *
from .s3_mce_framework import *
from .s4_experiments import *
from .s4_ablations import *
from .s5_discussion import *

__all__ = [
    # Core MCE claims (main contributions)
    "mce_decouples_what_how",
    "mce_opens_design_space",
    "mce_offline_gains",
    "mce_online_gains",
    "mce_top_rank",
    "mce_context_length_adaptability",
    "mce_context_efficiency",
    "mce_training_efficiency",
    "mce_transfer_superior",
    "model_confound_ruled_out",
    "mce_law",
    # Motivation claims
    "no_universal_harness",
    # Discussion
    "mce_reformulates_ce",
    "future_skill_evolution_generalizes",
]
