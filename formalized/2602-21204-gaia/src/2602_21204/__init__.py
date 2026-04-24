from .motivation import *
from .s2_background import *
from .s3_empirical_contradictions import *
from .s4_theory import *
from .s5_simplifications import *
from .s6_discussion import *
from . import priors  # noqa: F401 — loads PRIORS dict for gaia compile

__all__ = [
    # Core thesis
    "claim_ttt_is_linear_attention",
    # Theorems
    "thm_single_step",
    "thm_unrolled",
    "thm_momentum",
    # Concrete reductions
    "claim_lact_reduction",
    "claim_vitttt_glu_reduction",
    # Empirical contradictions
    "claim_memorization_contradicted",
    # Simplification findings
    "claim_ablation_summary",
    "claim_step6_standard_linear_attn",
    "claim_variant2_parallel_speedup",
    "claim_training_speedup",
    # Explanatory claims
    "claim_linear_view_explains_paradoxes",
    "claim_principled_simplifications",
    # Limitations
    "claim_linear_layer_limitation",
]
