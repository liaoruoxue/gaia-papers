from .motivation import *
from .s2_background import *
from .s3_methodology import *
from .s4_theory import *
from .s5_experiments import *
from .s6_conclusions import *

__all__ = [
    # Core theoretical contributions
    "attention_paradox",
    "cib_resolves_paradox",
    "cib_unifies_budget_forcing",
    # Propositions
    "prop_length_penalty_equivalence",
    "prop_target_length_equivalence",
    # RL objective
    "rl_objective_formulation",
    # Experimental results
    "cib_pareto_dominates_l1",
    "deepscaler_cib_conservative",
    "deepscaler_cib_aggressive",
    "deepscaler_7b_prior",
    "dler_7b_cib_conservative",
    "dler_7b_cib_aggressive",
    # Framework summary
    "cib_principled_framework",
    # Limitations
    "accuracy_degradation_at_scale",
    "no_inference_overhead",
    "framework_generality",
]
