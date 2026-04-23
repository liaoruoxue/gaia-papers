from .motivation import *
from .s2_approach import *
from .s3_experiments import *
from .s4_results import *
from .s5_discussion import *

__all__ = [
    # Core thesis claims
    "nlah_is_portable",
    "ihr_separates_concerns",
    "nlah_enables_module_ablation",
    # RQ1 conclusions
    "rq1_harness_controls_behavior",
    "rq1_ihr_is_not_prompt_wrapper",
    "rq1_process_moves_more_than_score",
    "rq1_most_instances_dont_flip",
    # RQ2 conclusions
    "rq2_frontier_concentration",
    "rq2_module_families",
    "rq2_self_evolution_mechanism",
    "rq2_verifier_negative",
    # RQ3 conclusions
    "rq3_migration_score_gain",
    "rq3_behavioral_relocation",
    # Discussion
    "nl_still_matters_for_control",
    "harness_search_space",
]
