from .motivation import *
from .s3_method import *
from .s4_experiments import *
from .s6_conclusion import *
from .priors import PRIORS  # noqa: F401 — ensures priors are registered

__all__ = [
    # Motivation: framing claims
    "claim_distribution_sharpening",
    "claim_agency_internalization",
    "claim_test_time_cost",
    # Method: design claims
    "claim_branching_targets_failures",
    "claim_cf_internalizes_recovery",
    "claim_lreh_stabilizes",
    # Empirical headline conclusions
    "claim_leafe_beats_grpo_passk",
    "claim_leafe_beats_alternatives",
    "claim_internalization_supported",
    "claim_grpo_sharpens_evidence",
    "claim_stage1_branching_better",
    "claim_aux_pass1_pass128_tradeoff",
    # Limitations
    "claim_lim_feedback_quality",
    "claim_lim_resettable_env",
    # Synthesis
    "claim_leafe_practical",
    "claim_pass_burden_shift",
]
