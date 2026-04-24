"""
Scaling Self-Play with Self-Guidance (SGS)
Bailey, Wen, Dong, Hashimoto, Ma -- arXiv:2604.20209 (2026)

Self-Guided Self-Play (SGS) is an asymmetric self-play algorithm for LLMs in which
a Guide component prevents Conjecturer collapse, enabling sustained learning over long
training runs. Applied to Lean4 formal theorem proving, SGS achieves a 7% higher
asymptotic solve rate than the strongest RL baseline, and enables a 7B model to surpass
the pass@4 of a 671B model after 6.3M generations.
"""

from .motivation import *
from .s3_algorithm import *
from .s4_experiments import *
from .s5_conclusion import *

__all__ = [
    # Core hypothesis
    "guide_hypothesis",
    # Main algorithmic result
    "sgs_two_mechanisms",
    "sgs_combined_reward",
    # Main empirical results
    "sgs_higher_asymptotic_rate",
    "sgs_surpasses_671b",
    "sgs_progress_on_never_solved",
    "sgs_outperforms_stp",
    # Mechanism findings
    "conjecturer_collapse_hypothesis",
    "entropy_conjecturer_coupling",
    "no_guide_conjecturer_collapse",
    # Conclusion
    "conclusion_sgs_sustains_learning",
]
