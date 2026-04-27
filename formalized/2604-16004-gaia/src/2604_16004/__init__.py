"""AgentV-RL: Scaling Reward Modeling with Agentic Verifier (Zhang et al., 2026).

A Gaia knowledge package formalizing the central claims, evidence, and reasoning structure
of the paper introducing Agentic Verifier and the AgentV-RL training recipe.
"""

from .motivation import *
from .s2_related import *
from .s3_method import *
from .s4_experiments import *
from .s4_analysis import *
from .s5_conclusion import *

# Curated cross-package exports: top-level scientific claims of the paper.
__all__ = [
    # Motivation
    "verifier_role_claim",
    "genrm_unreliable_claim",
    "paradigm_shift_claim",
    # Related work
    "bidirectional_novelty_claim",
    # Method
    "forward_sufficiency_claim",
    "backward_necessity_claim",
    "bidirectional_design_claim",
    "tool_augmented_capability_claim",
    "multi_agent_distillable_claim",
    "grpo_stability_claim",
    # Experiments
    "bon_sota_claim",
    "bon_scales_with_n_claim",
    "iter_refine_helpful_claim",
    # Analysis
    "bidirectional_synergy_claim",
    "tool_contributes_claim",
    "training_recipe_claim",
    "scaling_law_claim",
    "generalization_claim",
    "cost_accuracy_tradeoff_claim",
    # Conclusion
    "agentic_verifier_promising_claim",
    "synthetic_data_limit_claim",
    "cost_limit_claim",
    "tool_dependency_limit_claim",
]
