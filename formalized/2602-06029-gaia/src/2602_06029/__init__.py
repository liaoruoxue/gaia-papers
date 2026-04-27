"""Curiosity is Knowledge: Self-Consistent Learning and No-Regret Optimization with Active Inference.

Formalization of the paper by Yingke Li, Anjali Parashar, Enlu Zhou, Chuchu Fan
(arXiv:2602.06029v1, Feb 2026).
"""

from .motivation import *
from .s2_preliminaries import *
from .s4_definitions import *
from .s5_consistency import *
from .s6_regret import *
from .s7_synthetic_experiments import *
from .s8_real_world import *
from .s9_conclusion import *

# Cross-package exports: the paper's headline contributions.
__all__ = [
    "claim_curiosity_is_knowledge",
    "claim_contribution_consistency",
    "claim_contribution_regret",
    "claim_contribution_design",
    "claim_theorem_5_1",
    "claim_theorem_6_1",
    "claim_classical_bo_special_case",
    "claim_th5_1_corroborated",
    "claim_th6_1_corroborated",
    "claim_real_world_corroborated",
    "claim_design_guideline_csi",
]
