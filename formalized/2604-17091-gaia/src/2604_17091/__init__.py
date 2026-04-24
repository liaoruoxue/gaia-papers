from .motivation import *
from .s2_design import *
from .s3_architecture import *
from .s4_experiments import *
from .s5_discussion import *

__all__ = [
    # Core thesis claims (primary contributions)
    "thesis_density",
    "thesis_minimal_capability",
    "thesis_token_efficiency",
    "thesis_minimal_architecture",
    # Architecture claims
    "claim_tool_minimality",
    "claim_hierarchical_memory",
    "claim_self_evolution",
    "claim_context_compression",
    "claim_cli_minimality",
    "claim_autonomous_exploration",
    # Experimental results
    "result_lifelong_ga_claude",
    "result_sop_bench_ga_claude",
    "result_realfin_ga",
    "result_long_horizon_tool",
    "result_condensed_memory_ablation",
    "result_factual_memory",
    "result_context_explosion",
    "result_evolution_trajectory",
    "result_cross_task_evolution",
    "result_web_browsing",
    # Discussion claims
    "claim_permissions_ceiling",
    "claim_architecture_evolution_path",
    # Law
    "law_hierarchical_memory_factual",
]
