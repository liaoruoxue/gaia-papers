"""Reasoning and Tool-use Compete in Agentic RL: From Quantifying Interference to Disentangled Tuning.

Formalization of Li, Yi, Li, Fan, Jiang, Chen, Li, Song, Zhang (2026)
[@Li2026]; arXiv:2602.00994.

Two contributions:
  - LEAS, a quantitative diagnostic for capability interference in ARL.
  - DART, a single-model gradient-isolated training scheme that resolves
    the interference and yields ~6.35% EM improvement averaged over seven
    QA benchmarks.
"""

from .motivation import *
from .s2_related_work import *
from .s3_preliminaries import *
from .s4_leas import *
from .s5_dart import *
from .s6_experiments import *

__all__ = [
    # core contributions (cross-package interface)
    "claim_contribution_leas",
    "claim_contribution_dart",
    "claim_contribution_empirical",
    # central findings
    "claim_interference_dominates",
    "claim_gradient_conflict_explains_interference",
    "claim_dart_beats_grpo_universally",
    "claim_dart_efficient_disentanglement",
    "claim_dart_solves_gradient_conflict",
    "claim_joint_degrades_reasoning",
    "claim_dart_improves_tool_use",
]
