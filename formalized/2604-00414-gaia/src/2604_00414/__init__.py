"""Decision-Centric Design for LLM Systems (Wei Sun, arXiv:2604.00414)

This package formalizes the knowledge structure of the paper proposing a decision-centric
framework for LLM systems that separates decision-relevant signals from the policy that maps
them to actions, turning control into an explicit and inspectable layer.
"""

from .motivation import *
from .s3_framework import *
from .s5_exp1_calendar import *
from .s5_exp2_graph import *
from .s5_exp3_retrieval import *
from .s6_conclusion import *

# Exported conclusions (core contributions of the paper)
__all__ = [
    # Core framework claims
    "dc_framework_proposed",
    "separation_enables_attribution",
    "utility_maximization",
    "dc_unifies_settings",
    # Sequential framework
    "sufficiency_signal_def",
    "multi_signal_def",
    "joint_signal_value",
    "correlated_belief_update",
    "sequential_makes_failures_attributable",
    # Experiment 1: Calendar
    "dc_granite_100pct_success",
    "prompt_calendar_degrades",
    "retry_calendar_fails",
    "k1_failure_localized",
    "unresolvable_widens_gap",
    "dc_llama_transfer",
    # Experiment 2: Graph
    "dc_graph_100pct",
    "s5_correlated_update_result",
    "prompt_policy_insufficient_for_s5",
    # Experiment 3: Retrieval
    "medium_bucket_results",
    "prompt_correct_assessment_wrong_action",
    "modularity_signal_isolation",
    "failure_attribution_retrieval",
    "threshold_robustness",
    # Law
    "explicit_control_law",
    # Conclusion
    "framework_is_general",
    "prompt_fundamental_limit",
]
